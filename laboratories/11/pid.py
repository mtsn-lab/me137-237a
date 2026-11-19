import time
from pymodbus.client import ModbusTcpClient

# --- Configuration ---
PLC_IP = '127.0.0.1'
PLC_PORT = 5020
SLAVE_ID = 1

# Address Mapping
ADDR_READ_TEMP = 1024  # %MW0 (Inlet/Outlet Temp from Twin)
ADDR_WRITE_FAN = 0     # %QW0 (Command to the fans)

# --- PID Parameters ---
# Proportional Gain: Immediate response to error
KP = 12.0  
# Integral Gain: Corrects steady-state error over time
KI = 0.5   
# Derivative Gain: Prevents overshoot by sensing rate of change
KD = 0.1   

SETPOINT = 22.0        # Target Temperature in Celsius

class BMSPidController:
    def __init__(self):
        self.client = ModbusTcpClient(PLC_IP, port=PLC_PORT, framer='socket')
        self.integral = 0
        self.last_error = 0
        self.last_time = time.time()

    def run(self):
        print(f"🚀 ALC-Style Optimizer Started.")
        print(f"🎯 Target Setpoint: {SETPOINT}°C")
        
        try:
            while True:
                if not self.client.connect():
                    print("❌ Connection to OpenPLC failed. Retrying...")
                    time.sleep(2)
                    continue

                # 1. Read Current Temp from PLC (%MW0)
                result = self.client.read_holding_registers(ADDR_READ_TEMP, count=1, slave=SLAVE_ID)
                
                if not result.isError():
                    # Convert from fixed-point (e.g., 2550 -> 25.5)
                    current_temp = result.registers[0] / 100.0
                    
                    # 2. PID Math
                    now = time.time()
                    dt = now - self.last_time
                    
                    error = current_temp - SETPOINT
                    
                    # Proportional term
                    P = KP * error
                    
                    # Integral term with Anti-Windup (preventing infinite growth)
                    self.integral += error * dt
                    self.integral = max(min(self.integral, 50), -50) 
                    I = KI * self.integral
                    
                    # Derivative term
                    D = KD * (error - self.last_error) / dt
                    
                    # Calculate total output (0-100% fan speed)
                    output = P + I + D
                    fan_speed = int(max(min(output, 100), 20)) # Clamp between 20% and 100%
                    
                    # 3. Write Output back to PLC (%QW0)
                    self.client.write_register(ADDR_WRITE_FAN, fan_speed, slave=SLAVE_ID)
                    
                    print(f"🌡️ Temp: {current_temp:.2f}°C | 📉 Error: {error:.2f} | ⚙️ Fan: {fan_speed}%")
                    
                    # Save state for next tick
                    self.last_error = error
                    self.last_time = now
                else:
                    print("⚠️ Modbus Read Error")

                time.sleep(1) # 1Hz control loop (standard for ALC HVAC)

        except KeyboardInterrupt:
            print("\nShutting down controller...")
        finally:
            self.client.close()

if __name__ == "__main__":
    controller = BMSPidController()
    controller.run()