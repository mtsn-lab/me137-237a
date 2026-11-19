# Laboratory 11: Data Center Cooling Digital Twin with OpenPLC & PID Control

## Overview

This laboratory implements a closed-loop **Hardware/Software-in-the-Loop (HIL/SIL)** simulation of a data center thermal management system. A Python physics simulator (digital twin) models the air-side energy balance of a server hall, exchanges sensor and actuator signals over **Modbus TCP** with an industrial **OpenPLC Runtime v4** container, and is regulated by a supervisory **PID controller**.

### Repository Structure

```text
me137-237a/
├── environment.yml
└── laboratories/
    └── 11/
        ├── README.md
        ├── dataCenterCooling/   # Pre-configured OpenPLC Editor 4.3.5 project
        │   ├── devices/
        │   ├── pous/
        │   ├── servers/
        │   └── project.json
        ├── digital_twin.py      # Air-side thermal physics simulator
        ├── pid.py               # Supervisory BMS PID fan controller
        └── thermal_load.py      # Synthetic IT server load generator
```

### System Architecture

1. **`thermal_load.py` (IT Heat Load Generator):** Synthesizes server power demand ($\text{kW}$) combining a baseline load, a sinusoidal diurnal traffic cycle, random noise, and stochastic $+200\text{ kW}$ batch-processing spikes.
2. **`digital_twin.py` (Thermal Physics Simulator):** Reads the commanded CRAC fan speed ($0\text{--}100\%$) from the PLC, computes air mass flow rate $\dot{m}$ and outlet air temperature using first-principles sensible heat transfer ($\Delta T = \dot{Q}_{\text{IT}} / (\dot{m} c_p)$) with first-order thermal inertia, and writes scaled sensor readings back to the PLC over Modbus TCP.
3. **`dataCenterCooling/` on OpenPLC Runtime v4 (PLC Safety & I/O Layer):** Runs compiled IEC 61131-3 Ladder Logic inside Docker, exposing memory registers and coils on port `5020` and evaluating high-temperature interlock logic (`overheat_alarm` when `sensor_temp` $> 3500$, corresponding to $35.00^\circ\text{C}$).
4. **`pid.py` (Supervisory BMS PID Controller):** Polls the outlet temperature from the PLC at $1\text{ Hz}$, computes a PID control law with integral anti-windup against a target setpoint, and writes the updated fan speed command to the PLC.

---

## Prerequisites

* **Docker Desktop** installed and running.
* **OpenPLC Editor v4.3.5** (or newer v4.1+ compatible release).
* **Conda / Miniforge / Anaconda** with the repository environment (`me137-237a-env`).

### Update the Conda Environment

From the repository root (`me137-237a/`), update your Conda environment so that `pymodbus` and `numpy` are installed:

```bash
conda env update -f environment.yml --prune
conda activate me137-237a-env
```

---

## Step 1: Launch OpenPLC Runtime v4 in Docker

Start an **OpenPLC Runtime v4.1.0+** container exposing port `8443` (REST/WebSocket control & debugging) and port `5020` (Modbus TCP server):

```bash
docker pull ghcr.io/autonomy-logic/openplc-runtime:latest

docker run -d \
  --name openplc-runtime \
  -p 8443:8443 \
  -p 5020:5020 \
  --cap-add=SYS_NICE \
  --cap-add=SYS_RESOURCE \
  -v openplc-runtime-data:/var/run/runtime \
  ghcr.io/autonomy-logic/openplc-runtime:latest
```

Verify the container is running:

```bash
docker ps
```

> **Note:** If you have an older pre-v4.1.0 `openplc-runtime` container from an earlier session, remove it with `docker stop openplc-runtime && docker rm openplc-runtime` before running the commands above.

---

## Step 2: Open & Deploy the OpenPLC Project

1. Launch **OpenPLC Editor 4.3.5**.
2. Choose **File $\rightarrow$ Open Project** and select the directory **`me137-237a/laboratories/11/dataCenterCooling/`**.
3. Open **Device $\rightarrow$ Configuration**, confirm the target is set to **OpenPLC Runtime v4** with **IP Address** `localhost`, and click **Connect**. *(On a fresh container, create a new username and password when prompted.)*
4. Click **Transfer to PLC (Upload)** in the top toolbar to compile and upload the program bundle. *(This generates a local `build/` folder inside `dataCenterCooling/`, which is excluded from Git.)*
5. Click **Start PLC (Play)** so the runtime transitions to **Running** and opens port `5020`.
6. *(Optional)* Click **Debug** to monitor live tag values inside the Editor.

---

## Reference: Pre-Configured PLC Architecture

The `laboratories/11/dataCenterCooling/` project already includes the variable bindings, ladder logic, and Modbus TCP buffer mappings documented below.

### A. Variable Table & IEC 61131-3 Addressing

| # | Name | Class | Type | Location | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | `CRAC_Fan_Status` | Local | `BOOL` | *(blank)* | Internal fan running status |
| 1 | `Temp_High_Alarm` | Local | `BOOL` | *(blank)* | Internal high-temperature alarm flag |
| 2 | `sensor_temp` | Local | `INT` | `%MW0` | Outlet air temperature ($^\circ\text{C} \times 100$) |
| 3 | `fan_speed` | Local | `INT` | `%QW0` | Commanded CRAC fan speed ($0\text{--}100\%$) |
| 4 | `sensor_power` | Local | `INT` | `%MW1` | Current IT server power load ($\text{kW}$) |
| 5 | `overheat_alarm` | Local | `BOOL` | `%QX0.0` | High-temperature interlock coil ($> 35.00^\circ\text{C}$) |

### B. Ladder Logic

1. **Overheat Interlock Rung:** Connects `sensor_temp` (`IN1`) and constant `3500` (`IN2`) to a **`GT`** (Greater Than) block whose `OUT` drives the coil **`overheat_alarm`**.
2. **Fan Status Rung:** Connects a contact for **`CRAC_Fan_Status`** to the coil **`Temp_High_Alarm`**.

### C. Modbus TCP Server & Buffer Mapping

Under **Servers**, the Modbus TCP server is configured with **Network Interface** set to `All Interfaces (0.0.0.0)` on **Port** `5020`, with **Buffer Mapping** sized to `%QW = 1024`, `%MW = 1024`, and `%QX = 8`:

| PLC Tag | IEC Location | Modbus Area | 0-Based Offset | Modicon Address | Script Constant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `fan_speed` | `%QW0` | Holding Registers | `0` | `400001` | `ADDR_READ_FAN = 0` / `ADDR_WRITE_FAN = 0` |
| `sensor_temp` | `%MW0` | Holding Registers | `1024` | `401025` | `ADDR_WRITE_TEMP = 1024` / `ADDR_READ_TEMP = 1024` |
| `sensor_power` | `%MW1` | Holding Registers | `1025` | `401026` | Holding Register `1025` |
| `overheat_alarm` | `%QX0.0` | Coils | `0` | `1` | Coil `0` |

---

## Step 3: Run the Simulation Scripts

Navigate to `me137-237a/laboratories/11/` with `me137-237a-env` activated.

1. **(Optional) Standalone Load Generator Test:**
   ```bash
   python3 thermal_load.py
   ```
2. **Terminal 1 — Start the Digital Twin:**
   ```bash
   python3 digital_twin.py
   ```
3. **Terminal 2 — Start the PID Controller:**
   ```bash
   python3 pid.py
   ```

### Expected Closed-Loop Behavior

* On the first tick before `pid.py` writes a fan command, `fan_speed` defaults to $0\%$, causing the simulated outlet temperature to spike above $35.00^\circ\text{C}$ and trip `overheat_alarm` (`%QX0.0 = TRUE`).
* Once `pid.py` reads the elevated temperature from `%MW0` (`1024`), it commands `fan_speed` to $100\%$ via `%QW0` (`0`), driving the outlet temperature exponentially down toward steady state ($\approx 28.0\text{--}28.5^\circ\text{C}$ at $500\text{ kW}$ load) and clearing `overheat_alarm` as soon as `sensor_temp` drops below `3500`.

---

## Troubleshooting

| Symptom / Error Message | Cause | Fix |
| :--- | :--- | :--- |
| `[Errno 61] Connection refused` on `127.0.0.1:5020` | PLC is stopped or Modbus server is bound only to container loopback (`127.0.0.1`). | Verify Modbus **Network Interface** is `0.0.0.0`, upload the project, and ensure the PLC state is **Running**. |
| `Compilation aborted: 4 located variables have no producer` | Modbus server buffer sizes are unconfigured (`0`). | Set `%QW = 1024`, `%MW = 1024`, and `%QX = 8` under **Servers $\rightarrow$ Buffer Mapping**. |
| `Runtime version unknown is not compatible with this editor` | Running a pre-v4.1.0 Docker image without STruC++ support. | Pull `ghcr.io/autonomy-logic/openplc-runtime:latest` and recreate the container. |
| `Could not verify MD5: Unknown error code: 0x83` | Clicking **Debug** on a fresh container that has no program uploaded yet. | Click **Transfer to PLC (Upload)** first, start the PLC, and then attach the debugger. |