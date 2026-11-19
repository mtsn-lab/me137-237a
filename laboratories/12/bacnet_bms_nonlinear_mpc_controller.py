import asyncio
import signal
import time
import numpy as np
from scipy.optimize import minimize
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.pdu import Address
from bacpypes3.primitivedata import Null, ObjectIdentifier, Real

# --- Network Configuration ---
BMS_DEVICE_NAME = "BMS-MPC-Controller"
BMS_DEVICE_INSTANCE = 2001
BMS_ADDRESS = "127.0.0.1:47809"

CRAC_ADDRESS = Address("127.0.0.1:47808")
WRITE_PRIORITY = 8  # BACnet Priority 8 = Manual Operator / Supervisory Override

# --- Internal Prediction Model Parameters ---
AIR_DENSITY = 1.225
SPECIFIC_HEAT_AIR = 1.006
MAX_AIRFLOW = 50.0
AMBIENT_TEMP = 20.0
THERMAL_ALPHA = 0.2

# --- MPC Horizon & Tuning Parameters ---
HORIZON = 10            # Prediction steps (10 seconds at 1 Hz)
SETPOINT = 29.5         # Target outlet air temperature (°C)
ALARM_LIMIT = 35.0      # Field controller overheat threshold (°C)
U_MIN, U_MAX = 20.0, 100.0

W_TRACK = 25.0          # Temperature tracking error weight
W_EFFORT = 0.002        # Fan effort deviation weight around steady state
W_SLEW = 0.05           # Control move suppression weight (du)
W_SAFETY = 500.0        # Soft safety penalty approaching 35.0°C alarm


class BACnetMpcOptimizer:
    def __init__(self):
        self.u_prev = 80.0

    @staticmethod
    def predict_next_temp(temp: float, fan_pct: float, load_kw: float) -> float:
        """One-step discrete-time air-side sensible energy balance."""
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

    def solve(self, temp_curr: float, load_kw: float) -> float:
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
            method="SLSQP",
            bounds=bounds,
            options={"maxiter": 50, "ftol": 1e-5},
        )
        u_opt = float(np.clip(res.x[0], U_MIN, U_MAX))
        self.u_prev = u_opt
        return u_opt


async def main() -> None:
    parser = SimpleArgumentParser()
    args = parser.parse_args([
        "--name", BMS_DEVICE_NAME,
        "--instance", str(BMS_DEVICE_INSTANCE),
        "--address", BMS_ADDRESS,
    ])
    app = Application.from_args(args)

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except NotImplementedError:
            pass

    mpc = BACnetMpcOptimizer()

    print(f"🧠 BACnet BMS Nonlinear MPC Started on {BMS_ADDRESS} (Device {BMS_DEVICE_INSTANCE})")
    print(
        f"🎯 Target Setpoint: {SETPOINT:.1f}°C | 🔭 Horizon: {HORIZON}s | "
        f"🚨 Safety Limit: {ALARM_LIMIT:.1f}°C | 🎚️ Priority: {WRITE_PRIORITY}"
    )

    try:
        while not stop_event.is_set():
            try:
                # 1. Read BACnet sensor & alarm objects from CRAC Field Controller
                temp_val = await app.read_property(
                    CRAC_ADDRESS, ObjectIdentifier("analogInput,1"), "presentValue"
                )
                power_val = await app.read_property(
                    CRAC_ADDRESS, ObjectIdentifier("analogInput,2"), "presentValue"
                )
                alarm_val = await app.read_property(
                    CRAC_ADDRESS, ObjectIdentifier("binaryValue,1"), "presentValue"
                )

                current_temp = float(temp_val)
                current_power = float(power_val)
                alarm_active = str(alarm_val).lower() in ("active", "1")

                # 2. Solve receding-horizon nonlinear optimal control problem
                t_start = time.perf_counter()
                fan_cmd = round(mpc.solve(current_temp, current_power), 1)
                solve_ms = (time.perf_counter() - t_start) * 1000.0

                # 3. Write optimal control move at Priority 8 via BACnet WriteProperty
                await app.write_property(
                    CRAC_ADDRESS,
                    ObjectIdentifier("analogValue,1"),
                    "presentValue",
                    Real(fan_cmd),
                    priority=WRITE_PRIORITY,
                )

                alarm_str = "🚨 ALARM" if alarm_active else "✅ OK"
                print(
                    f"🌡️ Temp: {current_temp:5.2f}°C | 🔥 Load: {current_power:5.1f}kW | "
                    f"⚙️ Fan (Prio {WRITE_PRIORITY}): {fan_cmd:5.1f}% | ⏱️ {solve_ms:4.1f}ms | CRAC: {alarm_str}"
                )

            except Exception as exc:
                print(f"⚠️ BACnet communication error (is bacnet_twin.py running?): {exc}")

            try:
                await asyncio.wait_for(stop_event.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                pass
    finally:
        # Relinquish Priority 8 override so CRAC fan returns to Relinquish_Default (50.0%)
        try:
            await app.write_property(
                CRAC_ADDRESS,
                ObjectIdentifier("analogValue,1"),
                "presentValue",
                Null(()),
                priority=WRITE_PRIORITY,
            )
            print(f"\n🔓 Relinquished Priority {WRITE_PRIORITY} override (fan returned to Relinquish_Default).")
        except Exception:
            pass
        app.close()


if __name__ == "__main__":
    asyncio.run(main())