# Laboratory 12: Data Center Cooling Digital Twin with BACnet/IP, PID & MPC

## Overview

This laboratory extends the data center thermal management digital twin from **Modbus TCP** (Laboratory 11) to **BACnet/IP (ASHRAE Standard 135)**—the dominant open communication protocol in commercial Building Management Systems (BMS) and data center facility infrastructure.

Rather than polling raw 16-bit integer registers and manually scaling fixed-point numbers, the Python physics simulator (`bacnet_twin.py`) acts as a virtual **CRAC (Computer Room Air Conditioning) Field Controller** exposing self-describing BACnet objects with native floating-point values and engineering units over UDP. A supervisory BMS controller (`bacnet_pid.py` or `bacnet_mpc.py`) communicates with the field controller using standard BACnet **`ReadProperty`** and **`WriteProperty`** services, including **16-level command priority arbitration** and automatic **`Relinquish_Default`** fail-safe fallback.

### Repository Structure

```text
me137-237a/
├── environment.yml
└── laboratories/
    └── 12/
        ├── README.md
        ├── thermal_load.py      # IT server heat load generator (baseline + diurnal + spikes)
        ├── bacnet_twin.py       # BACnet/IP CRAC Field Controller & thermal physics simulator
        ├── bacnet_pid.py        # Supervisory BMS PID controller (Priority 8 override)
        └── bacnet_mpc.py        # Supervisory BMS Nonlinear MPC controller (Priority 8 override)
```

---

## Industrial Protocol Comparison: Modbus TCP vs. BACnet/IP

| Feature | Laboratory 11 (Modbus TCP) | Laboratory 12 (BACnet/IP) |
| :--- | :--- | :--- |
| **Transport & Port** | TCP port `5020` (standard `502`) | UDP port `47808` (`0xBAC0`) & `47809` |
| **Data Model** | Flat memory tables (Coils, Holding Registers) | Object-oriented (`AnalogInput`, `AnalogValue`, `BinaryValue`, `Device`) |
| **Data Types & Scaling** | 16-bit integers (`sensor_temp` scaled $\times 100$) | Native IEEE-754 `REAL` floats with engineering units (`degreesCelsius`, `kilowatts`, `percent`) |
| **Self-Description** | External CSV/documentation required | Object names, descriptions, and units are embedded in each BACnet object |
| **Actuator Arbitration** | Last write wins (`%QW0` overwritten directly) | **16-Level Priority Array** (`1` = Life Safety, `8` = Operator/BMS Override, `16` = Lowest) |
| **Controller Disconnect** | Fan remains frozen at last written register value | Relinquishing (`Null`) reverts fan to **`Relinquish_Default` ($50.0\%$)** automatically |

---

## BACnet/IP Network & Object Architecture

Because BACnet/IP binds a UDP socket per device node, running both scripts locally on the same machine assigns each node its own loopback UDP port:

* **Node 1 — CRAC Field Controller (`Device 1001` at `127.0.0.1:47808`):** Runs `bacnet_twin.py`, integrates the air-side sensible heat balance at $1\text{ Hz}$, enforces the local high-temperature interlock (`OverheatAlarm` active when `OutletAirTemp` $> 35.0^\circ\text{C}$), and serves four BACnet objects:

| Object Identifier | Object Name | Engineering Units | Access | Description |
| :--- | :--- | :--- | :--- | :--- |
| `analogInput,1` | `OutletAirTemp` | `degreesCelsius` | Read-Only | CRAC hot-aisle return/outlet air temperature ($^\circ\text{C}$) |
| `analogInput,2` | `ITServerLoad` | `kilowatts` | Read-Only | Instantaneous IT server hall thermal dissipation ($\text{kW}$) |
| `analogValue,1` | `CRACFanSpeedCmd` | `percent` | **Commandable** | CRAC VFD fan speed command ($0\text{--}100\%$; `Relinquish_Default = 50.0%`) |
| `binaryValue,1` | `OverheatAlarm` | `active` / `inactive` | Read-Only | Field controller high-temperature interlock ($> 35.0^\circ\text{C}$) |

* **Node 2 — Supervisory BMS Controller (`Device 2001` at `127.0.0.1:47809`):** Runs either `bacnet_pid.py` or `bacnet_mpc.py`. On every $1\text{ s}$ control step, it reads `OutletAirTemp`, `ITServerLoad`, and `OverheatAlarm` via `ReadProperty` and commands `CRACFanSpeedCmd` at **Priority 8** (`Manual Operator / Supervisory Override`) via `WriteProperty`.

---

## Prerequisites & Environment Setup

1. **Conda / Miniforge / Anaconda** with the repository environment (`me137-237a-env`).
2. From the repository root (`me137-237a/`), update your Conda environment so `bacpypes3`, `numpy`, and `scipy` are installed:

```bash
conda env update -f environment.yml --prune
conda activate me137-237a-env
```

*(No Docker container is required for Laboratory 12—the BACnet/IP field device and supervisory controller run natively in Python via `bacpypes3`.)*

---

## Running the Simulation

Open **two terminals** inside `me137-237a/laboratories/12/` with `me137-237a-env` activated:

1. **Terminal 1 — Start the BACnet/IP CRAC Field Controller (Digital Twin):**
   ```bash
   python3 bacnet_twin.py
   ```
   The field controller starts on `127.0.0.1:47808` (`Device 1001`) with `CRACFanSpeedCmd` initialized to its `Relinquish_Default` of **$50.0\%$**.

2. **Terminal 2 — Start Either the BACnet PID or Nonlinear MPC Controller:**
   ```bash
   # Option A: Classical PID supervisory controller
   python3 bacnet_pid.py

   # Option B: Nonlinear Model Predictive supervisory controller
   python3 bacnet_mpc.py
   ```

---

## Exploring BACnet Priority Arbitration & Fail-Safe Fallback

1. **Before Starting Terminal 2:** Observe Terminal 1 (`bacnet_twin.py`). With no supervisory controller writing to `CRACFanSpeedCmd`, the fan runs at its `Relinquish_Default` ($50.0\%$), causing the outlet temperature under $\approx 500\text{ kW}$ load to climb past $35.0^\circ\text{C}$ and trigger `OverheatAlarm = active`.
2. **Start `bacnet_pid.py` or `bacnet_mpc.py`:** The supervisory controller writes fan commands into **Priority 8** of `analogValue,1`'s priority array, driving `OutletAirTemp` back to the $29.5^\circ\text{C}$ setpoint and clearing `OverheatAlarm`.
3. **Stop Terminal 2 with `Ctrl+C`:** Before exiting, the supervisory controller sends a BACnet `WriteProperty` containing `Null()` at **Priority 8** to relinquish its override. Watch Terminal 1 immediately fall back to `Relinquish_Default = 50.0%` without needing a manual reset.

---

## Troubleshooting

| Symptom / Error Message | Cause | Fix |
| :--- | :--- | :--- |
| `OSError: [Errno 48] Address already in use` on `47808` or `47809` | Another BACnet process is already bound to that UDP port. | Close any existing `bacnet_*.py` processes (`lsof -nP -iUDP:47808`) and restart. |
| `Timeout` / `AbortPDU` in `bacnet_pid.py` or `bacnet_mpc.py` | `bacnet_twin.py` is not running yet on `127.0.0.1:47808`. | Start `python3 bacnet_twin.py` in Terminal 1 before launching the controller in Terminal 2. |
| `ModuleNotFoundError: No module named 'bacpypes3'` | Conda environment has not been updated with the new dependency. | Run `conda env update -f environment.yml --prune` and `conda activate me137-237a-env`. |