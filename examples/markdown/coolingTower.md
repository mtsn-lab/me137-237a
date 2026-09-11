## 1. Problem Statement

Cooling water leaves a data center and enters a wet cooling tower at 35°C at a rate of 100 kg/s. Water is cooled to 22°C in the cooling tower by air that enters the tower at 1 atm, 20°C, and 60 percent relative humidity and leaves saturated at 30°C. 

**Goal:** Neglecting the power input to the fan, determine: 
- (a) the mass flow rate of air into the cooling tower and
- (b) the mass flow rate of the required makeup water.
- (c) the cooling provided to the data center.

## 2. Schematic 
```
              ^
              |
              2
              |
     +------------------+
     |                  |
-3-->|                  |
     |                  |
     |                  |<---1 (air)
     |                  |
     |                  |
     |                  |
     |                  |
<-+4-|                  |
 ^   |                  |
 |   +------------------+
makeup
water
```
State 1: Air
State 2: Saturated air
State 3: Warm water
State 4: Cool water

## 3. Assumptions and Approximations
* **Ideal gas mixture**: Water vapor and air behave as an ideal gas mixture

**Property Model and Analysis Method:**
* **Property tables: `pyCalor` (Accurate):**
        * **Purpose:** Must be used for determining water vapor and air properties. 
        * **Tools:** Properties ($h$, $s$, $T$, and $p$) are retrieved directly from a **thermodynamic property library** (e.g., **`pyCalor`**). Since it is a pure substance we only need to know two independent properties.

## 4. Physical Laws
**Mass balance:**
$$\dot{m}_\text{a1} = \dot{m}_\text{a2} = \dot{m}_\text{a} $$

$$\dot{m}_3 + \dot{m}_\text{a1}\omega_1 = \dot{m}_4 + \dot{m}_\text{a2}\omega_2$$

**Energy balance:**

$$\dot{m}_\text{a1}h_1 + \dot{m}_\text{3}h_3 = \dot{m}_\text{a2}h_2 + \dot{m}_\text{4}h_4 $$

$$\dot{m}_\text{a}(h_1 - h_2) = \dot{m}_\text{4}h_4 - \dot{m}_\text{3}h_3 $$

The losses due to evaporation that must be "made up" are: 

$$\dot{m}_\text{makeup} = \dot{m}_3 - \dot{m}_4 = \dot{m}_\text{a} (\omega_2 - \omega_1)  $$

$$\implies \dot{m}_4 = \dot{m}_3 - \dot{m}_\text{makeup} $$

Re-writing our energy balance yields:

$$\dot{m}_\text{a}(h_1 - h_2) = (\dot{m}_\text{3} - \dot{m}_\text{makeup})h_4 - \dot{m}_\text{3}h_3 $$

$$\dot{m}_\text{a}(h_1 - h_2) = \dot{m}_\text{3}h_4 - \dot{m}_\text{makeup}h_4 - \dot{m}_\text{3}h_3 $$

Substituting the definition for the makeup mass flow rate:

$$\dot{m}_\text{a}(h_1 - h_2) = h_4\dot{m}_\text{3} - h_4(\dot{m}_\text{a} (\omega_2 - \omega_1) ) - \dot{m}_\text{3}h_3 $$

$$\dot{m}_\text{a}[(h_1 - h_2) + h_4(\omega_2 - \omega_1)] = h_4\dot{m}_\text{3} - \dot{m}_\text{3}h_3 $$

$$\dot{m}_\text{a} = \frac{h_4\dot{m}_\text{3} - \dot{m}_\text{3}h_3}{[(h_1 - h_2) + h_4(\omega_2 - \omega_1)]} $$

Rearranging:
$$\dot{m}_\text{a} = \frac{\dot{m}_\text{3}(h_3 - h_4)}{[(h_2 - h_1) - h_4(\omega_2 - \omega_1)]} $$


```python
# 5. Properties (Code Cell)
!pip install pyCalor
from pyCalor import thermo as th

Tw3_C = 35
mdot_w_kgPerS = 100

Tw4_C = 22

pAir_Pa = 101325
pAir_kPa = pAir_Pa/1000
Tair1_C = 20
RH1 = 60

Tair2_C = 30
RH2 = 100

# state 3
st3 = th.state('water',T=(Tw3_C,'C'), x=0, name='3')
h3_kJperKg = st3.h; print("h3_kJperKg=",h3_kJperKg,"kJ/kg")

# state 4
st4 = th.state('water',T=(Tw4_C,'C'), x=0, name='4')
h4_kJperKg = st4.h; print("h4_kJperKg=",h4_kJperKg,"kJ/kg")

# state 1 humid air
st1_air = th.state('air',T=(Tair1_C,'C'),p=(pAir_Pa,'Pa'),name='1 air')
st1_v = th.state('water',T=(Tair1_C,'C'),x=1,name='1 vapor')

p1_v_sat_kPa = st1_v.p; print("p1_v_sat_kPa=",p1_v_sat_kPa,"kPa")
p1_v_kPa = (RH1/100)*p1_v_sat_kPa; print("p1_v_kPa=",p1_v_kPa,"kPa")

omega_1 = 0.622*p1_v_kPa/(pAir_kPa - p1_v_kPa); print("omega_1=",omega_1)

# state 2 saturated air
st2_air = th.state('air',T=(Tair2_C,'C'),p=(pAir_Pa,'Pa'),name='2 air')
st2_v = th.state('water',T=(Tair2_C,'C'),x=1,name='2 vapor')

p2_v_sat_kPa = st2_v.p; print("p2_v_sat_kPa=",p2_v_sat_kPa,"kPa")
p2_v_kPa = (RH2/100)*p2_v_sat_kPa; print("p2_v_kPa=",p2_v_kPa,"kPa")

omega_2 = 0.622*p2_v_kPa/(pAir_kPa - p2_v_kPa); print("omega_2=",omega_2)
```
    h3_kJperKg= 146.6756538334547 kJ/kg
    h4_kJperKg= 92.32366528444535 kJ/kg
    p1_v_sat_kPa= 2.3407676975240133 kPa
    p1_v_kPa= 1.404460618514408 kPa
    omega_1= 0.008742692044332855
    p2_v_sat_kPa= 4.249409363174745 kPa
    p2_v_kPa= 4.249409363174745 kPa
    omega_2= 0.02722757190098444

```python
# 6 Calculations (Code Cell)
# h = h_a + omega*h_v
h1_kJperKg = st1_air.h + omega_1*st1_v.h; print("h1_kJperKg=",h1_kJperKg,"kJ/kg")

h2_kJperKg = st2_air.h + omega_2*st2_v.h; print("h2_kJperKg=",h2_kJperKg,"kJ/kg")

mdot_a_kgPerS = mdot_w_kgPerS*(st3.h-st4.h)/((h2_kJperKg-h1_kJperKg)-st4.h*(omega_2-omega_1))

print(f"(a) Mass flow rate of air into the cooling tower: {mdot_a_kgPerS:.2f} kg/s")

mdot_makeup_kgPerS = mdot_a_kgPerS * (omega_2 - omega_1)

print(f"(b) Mass flow rate of the makeup water: {mdot_makeup_kgPerS:.2f} kg/s")

Qdot_dataCenter_kW = mdot_w_kgPerS*(h3_kJperKg - h4_kJperKg)

print(f"(c) Cooling power provided to data center: {Qdot_dataCenter_kW:.2f} kW")
```

    h1_kJperKg= 441.5991409196139 kJ/kg
    h2_kJperKg= 499.0598834019021 kJ/kg
    (a) Mass flow rate of air into the cooling tower: 97.49 kg/s
    (b) Mass flow rate of the makeup water: 1.80 kg/s
    (c) Cooling power provided to data center: 5435.20 kW


## 7. Summary and Reasoning

* **Key Insight:** The mass of water that is lost due to evaporation must be made up by adding water back into the system.  
