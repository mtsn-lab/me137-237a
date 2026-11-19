import asyncio
import signal
import time
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.pdu import Address
from bacpypes3.primitivedata import Null, ObjectIdentifier, Real

# --- Network Configuration ---
BMS_DEVICE_NAME = "BMS-PID-Controller"
BMS_DEVICE_INSTANCE = 2001
BMS_ADDRESS = "127.0.0.1:47809"

CRAC_ADDRESS = Address("127.0.0.1:47808")
WRITE_PRIORITY = 8  # BACnet Priority 8 = Manual Operator / Supervisory Override

# --- PID Parameters ---
KP = 12.0
KI = 0.5
KD = 0.1
SETPOINT = 29.5
U_MIN, U_MAX = 20.0, 100.0


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

    integral = 0.0
    last_error = 0.0
    last_time = time.time()

    print(f"🚀 BACnet BMS PID Controller Started on {BMS_ADDRESS} (Device {BMS_DEVICE_INSTANCE})")
    print(f"🎯 Target Setpoint: {SETPOINT:.1f}°C | 🎚️ Command Priority: {WRITE_PRIORITY}")

    try:
        while not stop_event.is_set():
            try:
                # 1. Read BACnet properties from CRAC Field Controller
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

                # 2. PID Control Law with Anti-Windup
                now = time.time()
                dt = max(now - last_time, 1e-3)
                error = current_temp - SETPOINT

                P = KP * error
                integral = max(min(integral + error * dt, 50.0), -50.0)
                I = KI * integral
                D = KD * (error - last_error) / dt

                fan_cmd = float(max(min(P + I + D, U_MAX), U_MIN))

                # 3. Write fan command at Priority 8 via BACnet WriteProperty
                await app.write_property(
                    CRAC_ADDRESS,
                    ObjectIdentifier("analogValue,1"),
                    "presentValue",
                    Real(round(fan_cmd, 1)),
                    priority=WRITE_PRIORITY,
                )

                alarm_str = "🚨 ALARM" if alarm_active else "✅ OK"
                print(
                    f"🌡️ Temp: {current_temp:5.2f}°C | 🔥 Load: {current_power:5.1f}kW | "
                    f"⚙️ Fan (Prio {WRITE_PRIORITY}): {fan_cmd:5.1f}% | CRAC: {alarm_str}"
                )

                last_error = error
                last_time = now

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