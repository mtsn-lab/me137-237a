## 1 Problem statement and goal

A data center server rack consumes $15\text{ kW}$ of IT electrical power, with an additional fan power dissipation (assumed to be $0.75\text{ kW}$, i.e., $5\%$ of IT load). Air enters the rack cabinet at $1\text{ atm}$, $20^\circ\text{C}$, and $45\%$ relative humidity. Heat from the IT equipment and fans is transferred entirely to the air stream as sensible heat, keeping absolute humidity constant ($\omega_1 = \omega_2$). Assuming a standard rack exhaust temperature limit of $T_2 = 35^\circ\text{C}$:

**Goal:** Determine:

* (a) The required mass flow rate of dry air ($\dot{m}_a$) through the rack.
* (b) The inlet volumetric flow rate ($\dot{V}_1$) in $\text{m}^3/\text{s}$ and CFM.
* (c) The relative humidity ($\phi_2$) of the exhaust air.

---

## 2 Schematic


I will draw this.

---

## 3 Assumptions

* **Steady-State Operation:** Mass flow rate and heat dissipation rates are constant over time.
* **Conservation of Moisture:** No water is added or removed inside the cabinet ($\omega_1 = \omega_2$).
* **Negligible Heat Loss:** The rack casing is insulated/adiabatic relative to surrounding ambient room air; all electrical energy dissipates into the cooling air stream.
* **Fan Dissipation:** $100\%$ of fan electrical input power converts into thermal energy added to the air stream.
* **Constant Pressure:** Pressure drop across the cabinet is neglected ($P_1 = P_2 = 1\text{ atm} = 101.325\text{ kPa}$).

---

## 4 Physical Laws

**Mass Balance for Dry Air and Moisture:**


$$\dot{m}_{a,1} = \dot{m}_{a,2} = \dot{m}_a$$

$$\omega_1 = \omega_2 = \omega$$

**Energy Balance (Control Volume around Rack Envelope):**


$$\dot{Q}_{\text{total}} = \dot{W}_{\text{IT}} + \dot{W}_{\text{fan}}$$

$$\dot{Q}_{\text{total}} = \dot{m}_a (h_2 - h_1)$$

Rearranging to solve for dry air mass flow rate:


$$\dot{m}_a = \frac{\dot{Q}_{\text{total}}}{h_2 - h_1}$$

**Volumetric Flow Rate at Inlet:**


$$\dot{V}_1 = \dot{m}_a \cdot v_{v,1}$$



```python
#5 Properties
!pip install pyfluids

from pyfluids import HumidAir, InputHumidAir

# Constants and Parameters
P_atm_Pa = 101325  # Atmospheric pressure in Pa
T1_C = 20.0        # Inlet temperature in °C
RH1 = 45.0         # Inlet relative humidity in %
T2_C = 35.0        # Target outlet temperature in °C

W_IT_kW = 15.0     # IT power consumption in kW
W_fan_kW = 0.75    # Fan power consumption in kW (5% of IT power)
Q_total_kW = W_IT_kW + W_fan_kW  # Total thermal load in kW

# State 1: Inlet Air
st1 = HumidAir().with_state(
    InputHumidAir.temperature(T1_C),
    InputHumidAir.relative_humidity(RH1),
    InputHumidAir.pressure(P_atm_Pa)
)

omega1 = st1.humidity
h1_kJperKg = st1.enthalpy / 1000.0  # Convert J/kg to kJ/kg
v1_m3perKg = st1.specific_volume

print(f"State 1 Enthalpy (h1): {h1_kJperKg:.3f} kJ/kg")
print(f"State 1 Humidity Ratio (omega1): {omega1:.5f} kg w/kg da")
print(f"State 1 Specific Volume (v1): {v1_m3perKg:.4f} m^3/kg")

# State 2: Exhaust Air (Constant Humidity Ratio)
st2 = HumidAir().with_state(
    InputHumidAir.temperature(T2_C),
    InputHumidAir.humidity(omega1),
    InputHumidAir.pressure(P_atm_Pa)
)

h2_kJperKg = st2.enthalpy / 1000.0  # Convert J/kg to kJ/kg
RH2 = st2.relative_humidity

print(f"State 2 Enthalpy (h2): {h2_kJperKg:.3f} kJ/kg")
print(f"State 2 Relative Humidity (RH2): {RH2:.2f} %")
```

    Requirement already satisfied: pyfluids in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (4.0.0)
    Requirement already satisfied: coolprop==8.0.0 in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (from pyfluids) (8.0.0)
    Requirement already satisfied: numpy>=1.20 in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (from coolprop==8.0.0->pyfluids) (2.4.6)
    State 1 Enthalpy (h1): 36.514 kJ/kg
    State 1 Humidity Ratio (omega1): 0.00656 kg w/kg da
    State 1 Specific Volume (v1): 0.8334 m^3/kg
    State 2 Enthalpy (h2): 51.695 kJ/kg
    State 2 Relative Humidity (RH2): 18.69 %



```python
#6 Calculations
# Mass flow rate calculation
# mdot_a = Q_total / (h2 - h1)
mdot_a_kgPerS = Q_total_kW / (h2_kJperKg - h1_kJperKg)

# Volumetric flow rate calculations
Vdot_1_m3perS = mdot_a_kgPerS * v1_m3perKg
Vdot_1_CFM = Vdot_1_m3perS * 2118.88  # Convert m^3/s to CFM

print(f"(a) Required mass flow rate of dry air: {mdot_a_kgPerS:.4f} kg/s")
print(f"(b) Volumetric flow rate at inlet: {Vdot_1_m3perS:.4f} m^3/s ({Vdot_1_CFM:.1f} CFM)")
print(f"(c) Relative humidity at rack exit: {RH2:.1f}%")
```

    (a) Required mass flow rate of dry air: 1.0375 kg/s
    (b) Volumetric flow rate at inlet: 0.8646 m^3/s (1832.1 CFM)
    (c) Relative humidity at rack exit: 18.7%


## 7 Conclusions
* Since heat is added without adding moisture, the absolute humidity ($\omega$) remains constant while the relative humidity drops significantly from $45\%$ at the inlet to roughly $18\%$ at the outlet.
* To remove $15.75\text{ kW}$ of total thermal load within a $15^\circ\text{C}$ temperature rise ($\Delta T = 15^\circ\text{C}$), the rack cooling system must deliver approximately $1.04\text{ kg/s}$ ($\approx 1880\text{ CFM}$) of air flow.


```python

```
