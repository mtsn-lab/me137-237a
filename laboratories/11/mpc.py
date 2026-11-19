import time
import numpy as np
from scipy.optimize import minimize
from pymodbus.client import ModbusTcpClient

# --- Modbus Configuration (Matches OpenPLC & digital_twin.py) ---
PLC_IP = '127.0.0.1'
PLC_PORT = 5020
SLAVE_ID = 1

ADDR_READ_TEMP  = 1024  # %MW0 (Outlet Temp in °C * 100)
ADDR_READ_POWER = 1025  # %MW1 (Optional IT Load in kW)
ADDR_WRITE_FAN  = 0     # %QW0 (Fan speed command 20-100%)
COIL_OVERHEAT   = 0     # %QX0.0 (PLC overheat_alarm status)

# --- Internal Prediction Model Parameters ---
AIR_DENSITY = 1.225
SPECIFIC_HEAT_AIR = 1.006
MAX_AIRFLOW = 50.0
AMBIENT_TEMP = 20.0
THERMAL_ALPHA = 0.2     # First-order thermal inertia factor

# --- MPC Horizon & Tuning Parameters ---
HORIZON = 10            # Prediction steps (10 seconds at 1 Hz)
SETPOINT = 29.5         # Target outlet temperature (°C)
ALARM_LIMIT = 35.0      # PLC overheat_alarm threshold (°C)
U_MIN, U_MAX = 20.0, 100.0

W_TRACK = 25.0          # State tracking error weight
W_EFFORT = 0.002        # Fan effort deviation weight
W_SLEW = 0.05           # Control move suppression weight (du)
W_SAFETY = 500.0        # Soft penalty approaching 35.0°C PLC alarm


class BMSMpcController:
    def __init__(self):
        self.client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
        self.u_prev = 80.0
        self.temp_prev = None
        self.q_est = 500.0  # Initial IT load estimate (kW)

    @staticmethod
    def predict_next_temp(temp: float, fan_pct: float, load_kw: float) -> float:
        """One-step discrete-time air-side energy balance."""
        m_dot = (MAX_AIRFLOW * (fan_pct / 100.0) + 0.5) * AIR_DENSITY
        delta_t = load_kw / (m_dot * SPECIFIC_HEAT_AIR)
        target_outlet = AMBIENT_TEMP + delta_t
        return temp + THERMAL_ALPHA * (target_outlet - temp)

    @staticmethod
    def steady_state_fan(load_kw: float, setpoint: float) -> float:
        """Fan speed (%) required to hold setpoint at steady state."""
        if setpoint <= AMBIENT_TEMP:
            return U_MAX
        m_dot_req = load_kw / ((setpoint - AMBIENT_TEMP) * SPECIFIC_HEAT_AIR)
        u_req = ((m_dot_req / AIR_DENSITY) - 0.5) / MAX_AIRFLOW * 100.0
        return float(np.clip(u_req, U_MIN, U_MAX))

    def update_load_estimate(self, temp_curr: float, power_reg: int) -> float:
        """Uses measured %MW1 power if available; otherwise estimates Q_IT from dT."""
        if power_reg > 0:
            self.q_est = float(power_reg)
        elif self.temp_prev is not None:
            m_dot_prev = (MAX_AIRFLOW * (self.u_prev / 100.0) + 0.5) * AIR_DENSITY
            q_inferred = (
                ((temp_curr - self.temp_prev) / THERMAL_ALPHA) + self.temp_prev - AMBIENT_TEMP
            ) * m_dot_prev * SPECIFIC_HEAT_AIR
            # Low-pass filter on inferred heat load (clamped to physical range)
            q_inferred = float(np.clip(q_inferred, 50.0, 1500.0))
            self.q_est = 0.7 * q_inferred + 0.3 * self.q_est
        return self.q_est

    def solve_mpc(self, temp_curr: float, load_kw: float) -> float:
        """Solves the finite-horizon nonlinear MPC problem via SLSQP."""
        u_ss = self.steady_state_fan(load_kw, SETPOINT)
        u0_guess = np.full(HORIZON, u_ss)
        bounds = [(U_MIN, U_MAX)] * HORIZON

        def objective(u_seq: np.ndarray) -> float:
            t_pred = temp_curr
            cost = 0.0
            u_last = self.u_prev
            for k in range(HORIZON):
                t_pred = self.predict_next_temp(t_pred, u_seq[k], load_kw)
                err = t_pred - SETPOINT
                du = u_seq[k] - u_last
                safety_margin = max(0.0, t_pred - (ALARM_LIMIT - 0.5))
                cost += (
                    W_TRACK * (err ** 2)
                    + W_EFFORT * ((u_seq[k] - u_ss) ** 2)
                    + W_SLEW * (du ** 2)
                    + W_SAFETY * (safety_margin ** 2)
                )
                u_last = u_seq[k]
            return float(cost)

        res = minimize(
            objective,
            u0_guess,
            method='SLSQP',
            bounds=bounds,
            options={'maxiter': 50, 'ftol': 1e-5},
        )
        return float(np.clip(res.x[0], U_MIN, U_MAX))

    def run(self):
        print("🧠 Nonlinear MPC Controller Started.")
        print(f"🎯 Target Setpoint: {SETPOINT}°C | 🔭 Horizon: {HORIZON}s | 🚨 Safety Limit: {ALARM_LIMIT}°C")

        try:
            while True:
                if not self.client.connect():
                    print("❌ Connection to OpenPLC failed. Retrying...")
                    time.sleep(2)
                    continue

                # 1. Read Temperature (%MW0) and optional IT Power (%MW1)
                res = self.client.read_holding_registers(ADDR_READ_TEMP, count=2, slave=SLAVE_ID)
                alarm_res = self.client.read_coils(COIL_OVERHEAT, count=1, slave=SLAVE_ID)

                if not res.isError():
                    current_temp = res.registers[0] / 100.0
                    power_kw = res.registers[1]
                    alarm_active = alarm_res.bits[0] if not alarm_res.isError() else False

                    # 2. Estimate IT thermal load disturbance & solve receding-horizon OCP
                    t_start = time.perf_counter()
                    q_hat = self.update_load_estimate(current_temp, power_kw)
                    u_opt = self.solve_mpc(current_temp, q_hat)
                    solve_ms = (time.perf_counter() - t_start) * 1000.0

                    fan_cmd = int(round(u_opt))

                    # 3. Write optimal first move to PLC (%QW0)
                    self.client.write_register(ADDR_WRITE_FAN, fan_cmd, slave=SLAVE_ID)

                    alarm_tag = "🚨 ALARM" if alarm_active else "✅ OK"
                    print(
                        f"🌡️ Temp: {current_temp:5.2f}°C | 🔥 Q_est: {q_hat:5.1f}kW | "
                        f"⚙️ Fan: {fan_cmd:3d}% | ⏱️ {solve_ms:4.1f}ms | PLC: {alarm_tag}"
                    )

                    self.temp_prev = current_temp
                    self.u_prev = float(fan_cmd)
                else:
                    print("⚠️ Modbus Read Error")

                time.sleep(1)

        except KeyboardInterrupt:
            print("\nShutting down MPC controller...")
        finally:
            self.client.close()


if __name__ == "__main__":
    BMSMpcController().run()