# Laboratory 11: Data Center Cooling Digital Twin with OpenPLC, PID & MPC

## Overview

This laboratory implements a closed-loop **Hardware/Software-in-the-Loop (HIL/SIL)** simulation of a data center thermal management system. A Python physics simulator (`digital_twin.py`) models the air-side energy balance of a server hall, exchanges sensor and actuator signals over **Modbus TCP** with an industrial **OpenPLC Runtime v4** container, and is regulated by either a classical **PID controller** (`pid.py`) or a **Nonlinear Model Predictive Controller** (`mpc.py`).

### Repository Structure

```
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
        ├── digital_twin.py      # Air-side thermal physics & sensor simulator
        ├── thermal_load.py      # IT load profile helper imported by digital_twin.py
        ├── pid.py               # Supervisory BMS PID fan controller
        └── mpc.py               # Nonlinear Model Predictive Controller

```

### System Architecture

1. **`digital_twin.py` (Thermal Physics & Sensor Simulator):** Acts as the virtual data center plant at $1\text{ Hz}$. On each time step, it performs five operations over Modbus TCP:

   * **Reads Actuator Command (`%QW0`):** Polls Holding Register `0` for the commanded CRAC fan speed $u_k \in [0, 100]\%$.

   * **Generates IT Thermal Load:** Calls `ITLoadSimulator` (from `thermal_load.py`) to compute instantaneous server heat dissipation $\dot{Q}_{\text{IT},k}$ ($\text{kW}$), combining a $500\text{ kW}$ baseline, a sinusoidal diurnal traffic cycle, random noise, and stochastic $+200\text{ kW}$ batch-job spikes.

   * **Integrates Air-Side Energy Balance:** Computes cooling air mass flow rate $\dot{m}_k = \left(V_{\max}\frac{u_k}{100} + 0.5\right)\rho_{\text{air}}$ (including a $0.5\text{ m}^3/\text{s}$ leakage term at zero fan speed), steady-state outlet temperature $T_{\text{eq},k} = T_{\text{amb}} + \frac{\dot{Q}_{\text{IT},k}}{\dot{m}_k c_p}$, and updates the outlet temperature using first-order thermal inertia ($\alpha = 0.2$):
     

     $$
     T_{k+1} = T_k + \alpha \left(T_{\text{eq},k} - T_k\right)
     $$

   * **Publishes Virtual Sensors (`%MW0`, `%MW1`):** Writes fixed-point outlet temperature $\lfloor 100 \, T_{k+1} \rfloor$ to Holding Register `1024` (`sensor_temp`) and IT power demand $\text{round}(\dot{Q}_{\text{IT},k})$ to Holding Register `1025` (`sensor_power`).

   * **Monitors PLC Alarm State (`%QX0.0`):** Reads Coil `0` (`overheat_alarm`) to log when the PLC safety interlock trips.

2. **`dataCenterCooling/` on OpenPLC Runtime v4 (PLC Safety & I/O Layer):** Runs compiled IEC 61131-3 Ladder Logic inside Docker, exposing memory registers and coils on port `5020` and evaluating high-temperature interlock logic (`overheat_alarm` energizes when `sensor_temp` $> 3500$, corresponding to $35.00^\circ\text{C}$).

3. **`pid.py` (Supervisory BMS PID Controller):** Polls `sensor_temp` from `%MW0` (`1024`) at $1\text{ Hz}$, evaluates a PID control law with integral anti-windup, and writes the clamped fan speed command ($20\text{--}100\%$) to `%QW0` (`0`).

4. **`mpc.py` (Nonlinear Model Predictive Controller):** Drop-in replacement for `pid.py` that uses the nonlinear air-side energy balance over a $10\text{ s}$ prediction horizon to optimize fan speed trajectories subject to actuator bounds ($20\text{--}100\%$) and a soft safety penalty below the $35.0^\circ\text{C}$ PLC alarm limit.

## Prerequisites

* **Docker Desktop** installed and running.

* **OpenPLC Editor v4.3.5** (or newer v4.1+ compatible release).

* **Conda / Miniforge / Anaconda** with the repository environment (`me137-237a-env`).

### Update the Conda Environment

From the repository root (`me137-237a/`), update your Conda environment so that `pymodbus`, `numpy`, and `scipy` are installed:

```
conda env update -f environment.yml --prune
conda activate me137-237a-env

```

## Step 1: Launch OpenPLC Runtime v4 in Docker

Start an **OpenPLC Runtime v4.1.0+** container exposing port `8443` (REST/WebSocket control & debugging) and port `5020` (Modbus TCP server):

```
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

```
docker ps

```

> **Note:** If you have an older pre-v4.1.0 `openplc-runtime` container from an earlier session, remove it with `docker stop openplc-runtime && docker rm openplc-runtime` before running the commands above.

## Step 2: Open & Deploy the OpenPLC Project

1. Launch **OpenPLC Editor 4.3.5**.

2. Choose **File** $\rightarrow$ **Open Project** and select **`me137-237a/laboratories/11/dataCenterCooling/`**.

3. Open **Device** $\rightarrow$ **Configuration**, confirm the target is set to **OpenPLC Runtime v4** with **IP Address** `localhost`, and click **Connect**. *(On a fresh container, create a new username and password when prompted.)*

4. Click **Transfer to PLC (Upload)** in the top toolbar to compile and upload the program bundle. *(This generates a local `build/` folder inside `dataCenterCooling/`, which is excluded from Git.)*

5. Click **Start PLC (Play)** so the runtime transitions to **Running** and opens port `5020`.

6. *(Optional)* Click **Debug** to monitor live tag values inside the Editor.

## Reference: Pre-Configured PLC Architecture

The `laboratories/11/dataCenterCooling/` project already includes the variable bindings, ladder logic, and Modbus TCP buffer mappings documented below.

### A. Variable Table & IEC 61131-3 Addressing

| \# | Name | Class | Type | Location | Description | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
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
| ----- | ----- | ----- | ----- | ----- | ----- | 
| `fan_speed` | `%QW0` | Holding Registers | `0` | `400001` | `ADDR_READ_FAN = 0` / `ADDR_WRITE_FAN = 0` | 
| `sensor_temp` | `%MW0` | Holding Registers | `1024` | `401025` | `ADDR_WRITE_TEMP = 1024` / `ADDR_READ_TEMP = 1024` | 
| `sensor_power` | `%MW1` | Holding Registers | `1025` | `401026` | `ADDR_WRITE_POWER = 1025` / `ADDR_READ_POWER = 1025` | 
| `overheat_alarm` | `%QX0.0` | Coils | `0` | `1` | `COIL_OVERHEAT = 0` | 

## Step 3: Run the Closed-Loop Simulation

Open **two terminals** in `me137-237a/laboratories/11/` with `me137-237a-env` activated:

1. **Terminal 1 — Start the Digital Twin:**

   ```
   python3 digital_twin.py
   
   ```

2. **Terminal 2 — Start Either the PID Controller or the MPC Controller:**

   ```
   # Option A: Classical PID controller
   python3 pid.py
   
   # Option B: Nonlinear Model Predictive Controller
   python3 mpc.py
   
   ```

### Expected Closed-Loop Behavior

* **Startup Transient:** If `digital_twin.py` starts before a controller writes a fan speed command, `fan_speed` defaults to $0\%$, causing the outlet temperature to spike above $35.00^\circ\text{C}$ and trip `overheat_alarm` (`%QX0.0 = TRUE`). Once the controller responds, the fan ramps up and clears `overheat_alarm` as soon as `sensor_temp` drops below `3500`.

* **Steady-State & Spike Response:** At $500\text{ kW}$ load and $100\%$ fan speed, the minimum physically achievable outlet temperature is $28.03^\circ\text{C}$. With `SETPOINT = 29.5` ($^\circ\text{C}$), the controller modulates `fan_speed` around $\approx 84\%$ during nominal load and ramps to $100\%$ during $+200\text{ kW}$ batch spikes.

## Troubleshooting

| Symptom / Error Message | Cause | Fix | 
| ----- | ----- | ----- | 
| `[Errno 61] Connection refused` on `127.0.0.1:5020` | PLC is stopped or Modbus server is bound only to container loopback (`127.0.0.1`). | Verify Modbus **Network Interface** is `0.0.0.0`, upload the project, and ensure the PLC state is **Running**. | 
| `Compilation aborted: 4 located variables have no producer` | Modbus server buffer sizes are unconfigured (`0`). | Set `%QW = 1024`, `%MW = 1024`, and `%QX = 8` under **Servers** $\rightarrow$ **Buffer Mapping**. | 
| `Runtime version unknown is not compatible with this editor` | Running a pre-v4.1.0 Docker image without STruC++ support. | Pull `ghcr.io/autonomy-logic/openplc-runtime:latest` and recreate the container. | 
| `Could not verify MD5: Unknown error code: 0x83` | Clicking **Debug** on a fresh container that has no program uploaded yet. | Click **Transfer to PLC (Upload)** first, start the PLC, and then attach the debugger. | 
