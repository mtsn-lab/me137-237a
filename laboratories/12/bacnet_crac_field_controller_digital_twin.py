import asyncio
import signal
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.local.analog import AnalogInputObject, AnalogValueObject
from bacpypes3.local.binary import BinaryValueObject
from bacpypes3.local.cmd import Commandable
from bacpypes3.primitivedata import Real
from thermal_load import ITLoadSimulator

# --- Network Configuration (CRAC Field Controller) ---
DEVICE_NAME = "CRAC-Field-Controller"
DEVICE_INSTANCE = 1001
DEVICE_ADDRESS = "127.0.0.1:47808"

# --- Physical Constants ---
AIR_DENSITY = 1.225
SPECIFIC_HEAT_AIR = 1.006
MAX_AIRFLOW = 50.0
AMBIENT_TEMP = 20.0
THERMAL_ALPHA = 0.2
ALARM_THRESHOLD = 35.0
DEFAULT_FAN_PCT = 50.0


class CommandableAnalogValueObject(Commandable, AnalogValueObject):
    """Commandable BACnet Analog Value supporting the 16-level priority array."""
    pass


async def main() -> None:
    parser = SimpleArgumentParser()
    args = parser.parse_args([
        "--name", DEVICE_NAME,
        "--instance", str(DEVICE_INSTANCE),
        "--address", DEVICE_ADDRESS,
    ])
    app = Application.from_args(args)

    # Register self-describing BACnet objects with engineering units
    ai_temp = AnalogInputObject(
        objectIdentifier=("analogInput", 1),
        objectName="OutletAirTemp",
        presentValue=Real(22.0),
        units="degreesCelsius",
        description="CRAC Hot-Aisle Return Air Temperature",
    )
    ai_power = AnalogInputObject(
        objectIdentifier=("analogInput", 2),
        objectName="ITServerLoad",
        presentValue=Real(500.0),
        units="kilowatts",
        description="Total IT Hall Power Dissipation",
    )
    av_fan = CommandableAnalogValueObject(
        objectIdentifier=("analogValue", 1),
        objectName="CRACFanSpeedCmd",
        presentValue=Real(DEFAULT_FAN_PCT),
        relinquishDefault=Real(DEFAULT_FAN_PCT),
        units="percent",
        description="Commanded CRAC VFD Fan Speed (16-Level Priority Array)",
    )
    bv_alarm = BinaryValueObject(
        objectIdentifier=("binaryValue", 1),
        objectName="OverheatAlarm",
        presentValue="inactive",
        description="Field Controller High-Temperature Interlock (> 35.0 C)",
    )

    for obj in (ai_temp, ai_power, av_fan, bv_alarm):
        app.add_object(obj)

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except NotImplementedError:
            pass

    load_sim = ITLoadSimulator(base_load_kw=500, variability=50)
    current_temp = 22.0

    print(f"🏢 BACnet/IP CRAC Field Controller Running on {DEVICE_ADDRESS} (Device {DEVICE_INSTANCE})")
    print(f"🛡️  Relinquish_Default Fan Speed: {DEFAULT_FAN_PCT:.1f}% | Overheat Interlock: > {ALARM_THRESHOLD:.1f}°C")

    try:
        while not stop_event.is_set():
            # 1. Read active fan command resolved by the BACnet 16-level priority array
            fan_speed = float(av_fan.presentValue)

            # 2. Sample IT thermal load & integrate air-side energy balance
            load = load_sim.get_current_load()
            m_dot = (MAX_AIRFLOW * (fan_speed / 100.0) + 0.5) * AIR_DENSITY
            delta_t = load / (m_dot * SPECIFIC_HEAT_AIR)
            target_outlet = AMBIENT_TEMP + delta_t
            current_temp += THERMAL_ALPHA * (target_outlet - current_temp)

            # 3. Publish updated sensor values & evaluate local safety interlock
            ai_temp.presentValue = Real(round(current_temp, 2))
            ai_power.presentValue = Real(round(load, 2))
            alarm_on = current_temp > ALARM_THRESHOLD
            bv_alarm.presentValue = "active" if alarm_on else "inactive"

            alarm_str = "🚨 ACTIVE" if alarm_on else "✅ OK"
            print(
                f"🔥 Load: {load:6.1f}kW | ❄️ Fan: {fan_speed:5.1f}% | "
                f"🌡️ Outlet: {current_temp:5.2f}°C | Alarm: {alarm_str}"
            )

            try:
                await asyncio.wait_for(stop_event.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                pass
    finally:
        print("\nShutting down BACnet CRAC Field Controller...")
        app.close()


if __name__ == "__main__":
    asyncio.run(main())