import time
import numpy as np
from pymodbus.client import ModbusTcpClient

# --- Configuration ---
PLC_IP = '127.0.0.1'
PLC_PORT = 5020
SLAVE_ID = 1

# Address Mapping
ADDR_WRITE_TEMP = 1024  # %MW0 (The PLC reads this as the current sensor value)
ADDR_READ_FAN   = 0     # %QW0 (The PLC/Controller writes the fan speed here)

# Physical Constants
AIR_DENSITY = 1.225
SPECIFIC_HEAT_AIR = 1.006
MAX_AIRFLOW = 50.0
AMBIENT_TEMP = 20.0

class DataCenterTwin:
    def __init__(self):
        self.client = ModbusTcpClient(PLC_IP, port=PLC_PORT, framer='socket')
        self.current_temp = 22.0
        self.time_step = 0

    def get_it_load(self):
        # Synthetic Load Generation
        diurnal = 100 * np.sin(2 * np.pi * self.time_step / 100)
        noise = np.random.uniform(-20, 20)
        self.time_step += 1
        return 500 + diurnal + noise

    def run(self):
        print("🌐 Digital Twin Running. Simulating Physics...")
        try:
            while True:
                if not self.client.connect():
                    time.sleep(2); continue

                # 1. Read Fan Speed from %QW0
                res = self.client.read_holding_registers(ADDR_READ_FAN, count=1, slave=SLAVE_ID)
                fan_speed = res.registers[0] if not res.isError() else 0

                # 2. Physics Calculation
                load = self.get_it_load()
                m_dot = (MAX_AIRFLOW * (fan_speed / 100.0) + 0.5) * AIR_DENSITY
                delta_t = load / (m_dot * SPECIFIC_HEAT_AIR)
                target_outlet = AMBIENT_TEMP + delta_t
                
                # Thermal inertia (smoothing)
                self.current_temp += (target_outlet - self.current_temp) * 0.2

                # 3. Write Temp to %MW0 (scaled by 100)
                self.client.write_register(ADDR_WRITE_TEMP, int(self.current_temp * 100), slave=SLAVE_ID)

                print(f"🔥 Load: {load:.1f}kW | ❄️ Fan: {fan_speed}% | 🌡️ Outlet: {self.current_temp:.2f}°C")
                time.sleep(1)
        except KeyboardInterrupt:
            self.client.close()

if __name__ == "__main__":
    DataCenterTwin().run()