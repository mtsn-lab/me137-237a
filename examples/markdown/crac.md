## 1. Problem Statement
A computer-room air-conditioning (CRAC) system in a data center is cooled using a chiller. The chiller consists of a vapor-compression refrigeration system that operates using R-744 (carbon dioxide). It is used to cool water, which is circulated with a pump between the CRAH and the evaporator. Air enters the CRAH with a flow rate of 10,000 CFM with a drybulb temperature of $T_1 = $29 C and a relative humidity of $\phi_1 = $25 % and exits with a drybulb temperature of $T_2$ and a relative humidity of $\phi_2$. The fan efficiency is 80 % and the pressure drop across the fan is 250 Pa. 

**Goal:** Assuming that the chiller operates with a coefficient of performance of 3.0, determine:
* (a) The input power to the fan in the CRAC.
* (b) The input power required for the compressor in order to achieve $T_2$ = 10 C and 5 C.

## 2. Schematic 
```
     +------------------+
     |                  |
     |                  |
<-5--|                  |<---4 (refrigerant)
     |                  |
     |                  |
     +------------------+
     |                  |
     |                  |
--1->|                  |--2-> (air)
     |                  |
     |                  |
     +------------------+
               |
               v
              (3) (water)
```
State 1: air entering the CRAC
State 2: air exiting the CRAC
State 3: potentially liquid water exiting the CRAC
State 4: refrigerant entering the CRAC
State 5: refrigerant exiting the CRAC


## 3. Assumptions and Approximations
* **Ideal gas mixture**: Water vapor and air behave as an ideal gas mixture

**Property Model and Analysis Method:**
* **Property tables: `pyCalor` (Accurate):**
        * **Purpose:** Must be used for determining water vapor and air properties. 
        * **Tools:** Properties ($h$, $s$, $T$, and $p$) are retrieved directly from a **thermodynamic property library** (e.g., **`pyCalor`**). Since it is a pure substance we only need to know two independent properties.

## 4. Physical Laws
**Mass balance:**
$$\dot{m}_\text{a1} = \dot{m}_\text{a2} = \dot{m}_\text{a} $$

$$\dot{m}_\text{a1}\omega_1 = \dot{m}_3 + \dot{m}_\text{a2}\omega_2$$

We can then write the amount of water leaving the CRAH as:

$$\dot{m}_3 = \dot{m}_\text{a} \left( \omega_1 - \omega_2 \right)$$

**Energy balance:**

$$\dot{m}_\text{a1}h_1 + \dot{W}_\text{fan} = \dot{m}_\text{a2}h_2 + \dot{m}_\text{3}h_3 + \dot{Q}_\text{out}$$

$$\dot{Q}_\text{out} = \dot{m}_\text{a1}h_1 + \dot{W}_\text{fan} - (\dot{m}_\text{a2}h_2 + \dot{m}_\text{3}h_3) $$

$$ \dot{W}_\text{fan} = \Delta p \dot{V} / \eta$$

**Coefficient of Performance:**

$$\text{COP}_\text{R} = \frac{\dot{Q}_\text{L}}{\dot{W}_\text{in,compressor}} $$

Here we have: $\dot{Q}_\text{L} = \dot{Q}_\text{out}$. Therefore:

$$\dot{W}_\text{in,compressor} = \frac{\dot{Q}_\text{out}}{\text{COP}_\text{R}} $$

Substituting:

$$\dot{W}_\text{in,compressor} = \frac{\dot{m}_\text{a}\left[h_1 - h_2 - \left( \omega_1 - \omega_2 \right)h_3 \right] + \dot{W}_\text{fan}}{\text{COP}_\text{R}} $$



```python
# 5. Properties (Code Cell)
try:
    from pyfluids import HumidAir, InputHumidAir
except ImportError:
    !pip install pyfluids
    from pyfluids import HumidAir, InputHumidAir

try:
    from CoolProp.CoolProp import PropsSI
except ImportError:
    !pip install CoolProp
    from CoolProp.CoolProp import PropsSI



# air flow rate
Vdot_CFM = 10000
Vdot_m3PerMin = Vdot_CFM/35.3147
Vdot_m3PerS = Vdot_m3PerMin/60

# COP
COP = 3

# fan efficiency, pressure drop
eta = 0.8
dp_Pa = 250

# state 1
T1_C = 29
RH1 = 25
p1_Pa = 101325

st1 = HumidAir().with_state(
InputHumidAir.pressure(p1_Pa),
InputHumidAir.temperature(T1_C),
InputHumidAir.relative_humidity(RH1),
#InputHumidAir.wet_bulb_temperature(Twb_C),
# InputHumidAir.dew_temperature(Tdp_C),
)

T1_dp_C = st1.dew_temperature; print("T1_dp_C=",T1_dp_C)
h1_JperKgHumidAir = st1.enthalpy; print("h1_JperKgHumidAir=",h1_JperKgHumidAir)
rho1_kgHumidAirPerM3 = st1.density; print("rho1_kgHumidAirPerM3=",rho1_kgHumidAirPerM3)
omega_1 = st1.humidity; print("omega_1=",omega_1)
h1_JperKgDryAir = h1_JperKgHumidAir*(1+omega_1); print("h1_JperKgDryAir=",h1_JperKgDryAir)
rho1_kgDryAirPerM3 = rho1_kgHumidAirPerM3/(1+omega_1); print("rho1_kgDryAirPerM3=",rho1_kgDryAirPerM3)

mdotAir_kgDryAirPerS = Vdot_m3PerS*rho1_kgDryAirPerM3; print("mdotAir_kgDryAirPerS=",mdotAir_kgDryAirPerS)

# state 2, T2 = 10 C
T2_C = 10
p2_Pa = p1_Pa
# since the dew point is at state 1 is less than T2, the absolute humidity hasn't changed
omega_2 = omega_1; print("omega_2 =",omega_2)

st2 = HumidAir().with_state(
InputHumidAir.pressure(p2_Pa),
InputHumidAir.temperature(T2_C),
InputHumidAir.humidity(omega_2)
#InputHumidAir.relative_humidity(RH1),
#InputHumidAir.wet_bulb_temperature(Twb_C),
# InputHumidAir.dew_temperature(Tdp_C),
)

h2_JperKgHumidAir = st2.enthalpy; print("h2_JperKgHumidAir=",h2_JperKgHumidAir)
h2_JperKgDryAir = h2_JperKgHumidAir*(1+omega_2); print("h2_JperKgDryAir=",h2_JperKgDryAir)

# state 3, for T2 = 10 c there is no water exiting

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# state 2', T2 = 5 C
T2_C_ = 5
phi_2_ = 100
p2_Pa_ = p1_Pa

st2_ = HumidAir().with_state(
InputHumidAir.pressure(p2_Pa_),
InputHumidAir.temperature(T2_C_),
InputHumidAir.relative_humidity(phi_2_),
#InputHumidAir.wet_bulb_temperature(Twb_C),
# InputHumidAir.dew_temperature(Tdp_C),
)
omega_2_ = st2_.humidity; print("omega_2_ =",omega_2_)

h2_JperKgHumidAir_ = st2_.enthalpy; print("h2_JperKgHumidAir_=",h2_JperKgHumidAir_)
h2_JperKgDryAir_ = h2_JperKgHumidAir_*(1+omega_2_); print("h2_JperKgDryAir_=",h2_JperKgDryAir_)

# state 3, saturated liquid
x3 = 0
T3_C = T2_C_
h3_JperKgWater = PropsSI('H','T',T3_C+273.15,'Q',x3,'water'); print("h3_JperKgWater=",h3_JperKgWater)
```

    T1_dp_C= 7.00697358351033
    h1_JperKgHumidAir= 44834.37451741706
    rho1_kgHumidAirPerM3= 1.1642618189807894
    omega_1= 0.006240871974970756
    h1_JperKgDryAir= 45114.18010885815
    rho1_kgDryAirPerM3= 1.1570408750100436
    mdotAir_kgDryAirPerS= 5.460619680614793
    omega_2 = 0.006240871974970756
    h2_JperKgHumidAir= 25615.017587096074
    h2_JperKgDryAir= 25774.877632493764
    omega_2_ = 0.005424654108935187
    h2_JperKgHumidAir_= 18539.091975689273
    h2_JperKgDryAir_= 18639.66013715112
    h3_JperKgWater= 21019.950998530858



```python
# 6 Calculations (Code Cell)
# h = h_a + omega*h_v
WdotFan_kW = (dp_Pa * Vdot_m3PerS)/eta/1000

print(f"(a) The power input to the fan is: {WdotFan_kW:.2f} kW")

QdotOut_kW = (mdotAir_kgDryAirPerS*(h1_JperKgDryAir - h2_JperKgDryAir) + WdotFan_kW)/1000
WdotInComp_kW = ((mdotAir_kgDryAirPerS*(h1_JperKgDryAir - h2_JperKgDryAir) + WdotFan_kW)/COP)/1000

print(f"(b) The heat transferred out of the CRAH for T2 = 10 C is: {QdotOut_kW:.2f} kW")

print(f"(b) The power input to the compressor for T2 = 10 C is: {WdotInComp_kW:.2f} kW")

QdotOut_kW_ = (mdotAir_kgDryAirPerS*(h1_JperKgDryAir - h2_JperKgDryAir_ - (omega_1 - omega_2_)*h3_JperKgWater) + WdotFan_kW)/1000
WdotInComp_kW_ = ((mdotAir_kgDryAirPerS*(h1_JperKgDryAir - h2_JperKgDryAir_ - (omega_1 - omega_2_)*h3_JperKgWater) + WdotFan_kW)/COP)/1000

print(f"(b) The heat transferred out of the CRAH for T2 = 5 C is: {QdotOut_kW_:.2f} kW")

print(f"(b) The power input to the compressor for T2 = 5 C is: {WdotInComp_kW_:.2f} kW")
```

    (a) The power input to the fan is: 1.47 kW
    (b) The heat transferred out of the CRAH for T2 = 10 C is: 105.61 kW
    (b) The power input to the compressor for T2 = 10 C is: 35.20 kW
    (b) The heat transferred out of the CRAH for T2 = 5 C is: 144.48 kW
    (b) The power input to the compressor for T2 = 5 C is: 48.16 kW


## 7. Summary and Reasoning

* **Key Insight:** Lowering the supply air temperatures causes condensation of the moisture in the air, which results in an increase in the required CRAH cooling capacity. 
