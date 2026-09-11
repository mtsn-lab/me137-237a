# Psychrometric principles

```
+----------+   +----------+                +----------+
|          |   | water    |                | probably |
| dry air  | + | vapor    | <=transition=> | water    |
|          |   |          |                |          |
+----------+   +----------+                +----------+
```

dry air + water vapor = gas mixture

probably water = liquid (condensate)

dry air: mass, $m_\text{a}$, $n_\text{a}$

water vapor: $m_\text{v}$, $n_\text{v}$

$$ m = m_\text{a} + m_\text{v}$$

$$ n = n_\text{a} + n_\text{v}$$

$$y_\text{a} = \frac{n_\text{a}}{n} $$

$$y_\text{v} = \frac{n_\text{v}}{n} $$

```
+--------------+
|              |
|              |
|   T, p, V    |
|              |
|              |
+--------------+
```

## Characteristics of humidity
$$p = \frac{n R T}{V} $$

$$p_\text{a} = \frac{n_\text{a} R T}{V}  $$

$$p_\text{v} = \frac{n_\text{v} R T}{V}  $$

### Saturated vapor: molecules entering = molecules leaving
The vapor pressure depends on temperature:

$$p_\text{v}(T)$$



saturated vapor:
```
o       vapor
  \          _
   _|        /|
---------------------
           o
      liquid
```

unsaturated vapor:
```
        vapor
    _        _
   |\        /|
---------------------
      o    o
      liquid
```


supersaturated vapor: show molecules hitting the liquid interface and the liquid level rising.


### Humidity ratio

$$\omega = \frac{m_\text{v}}{m_\text{a}} $$

$$n = \frac{m}{M} $$

where $M$ is the molar mass. 

$$n_\text{a} = \frac{m_\text{a}}{M_\text{a}} $$

$$n_\text{v} = \frac{m_\text{v}}{M_\text{v}} $$

$$p_\text{a} = \frac{m_\text{a}}{M_\text{a}} \frac{R T}{V} $$

$$\implies m_\text{a} = \frac{p_\text{a} M_\text{a} V}{R T} $$

$$p_\text{v} = \frac{m_\text{v}}{M_\text{v}} \frac{R T}{V} $$

$$\implies m_\text{v} = \frac{p_\text{v} M_\text{v} V}{R T} $$

Combining:

$$\omega = \frac{\frac{p_\text{v} M_\text{v} V}{R T}}{\frac{p_\text{a} M_\text{a} V}{R T}} $$

$$\implies \omega = \frac{p_\text{v} M_\text{v}}{p_\text{a} M_\text{a}} $$

### The Dalton law
$$p = p_\text{a} + p_\text{v} $$

$$\implies p_\text{a} = p - p_\text{v}$$

$$\omega = \frac{p_\text{v} M_\text{v}}{(p - p_\text{v}) M_\text{a}} $$

The molecular weights of water and air are $M_\text{v} = 18 \text{ Da}$ and $M_\text{a} = 28 \text{ Da}$, respectively. Therefore:

$$\omega = 0.622 \frac{p_\text{v}}{p - p_\text{v}} $$

### Relative humidity

$$\phi = \frac{y_\text{v}}{y_\text{v,sat}} \le  1$$

$$p_\text{v} = p y_\text{v} $$

$$\implies y_\text{v} = \frac{p_\text{v}}{p} $$

$$p_\text{v,sat} = p y_\text{v,sat} $$

$$\implies y_\text{v,sat} = \frac{p_\text{v,sat}}{p} $$

Substituting:

$$\phi = \frac{\frac{p_\text{v}}{p}}{\frac{p_\text{v,sat}}{p}}$$

$$\phi = \frac{p_\text{v}}{p_\text{v,sat}} \le  1$$

This is what you see in the weather forecast. 


```python
!pip install pyCalor
from pyCalor import thermo as th
```

    Requirement already satisfied: pyCalor in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (1.0.21)
    Requirement already satisfied: CoolProp in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (from pyCalor) (8.0.0)
    Requirement already satisfied: igraph in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (from pyCalor) (1.0.0)
    Requirement already satisfied: numpy>=1.20 in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (from CoolProp->pyCalor) (2.4.6)
    Requirement already satisfied: texttable>=1.6.2 in /Users/thomschu/anaconda3/envs/me137-237a-env/lib/python3.11/site-packages (from igraph->pyCalor) (1.7.0)



```python
T_C = 20
p_kPa = 101.325
phi = 0.39

st1_sat = th.state('water',T=(T_C,'C'),x=1)
psat_kPa = st1_sat.p
#print('psat_kPa=',psat_kPa,'kPa')
print('psat_kPa=',f"{psat_kPa:.3f}") 

y_v_sat = psat_kPa/p_kPa
#print('y_v_sat=',y_v_sat)
print('y_v_sat=',f"{y_v_sat:.3f}") 

# phi = y_v / y_v_sat => y_v = phi * y_v_sat
y_v = phi*y_v_sat
# print('y_v=',y_v)
print('y_v=',f"{y_v:.4f}") 

p_v_kPa = p_kPa*y_v
# print('p_v_kPa=',p_v_kPa)
print('p_v_kPa=',f"{p_v_kPa:.2f}") 

omega = 0.622*(p_v_kPa)/(p_kPa - p_v_kPa)
print('omega=',f"{omega:.4f}") 
```

    psat_kPa= 2.341
    y_v_sat= 0.023
    y_v= 0.0090
    p_v_kPa= 0.91
    omega= 0.0057


### Thermodynamic properties

$U$, $H$, $S$

$$H = H_\text{a} + H_\text{v} = m_\text{a} h_\text{a} + m_\text{v} h_\text{v} $$

$$\frac{H}{m_\text{a} + m_\text{v}} = \frac{m_\text{a} h_\text{a} + m_\text{v} h_\text{v}}{m_\text{a} + m_\text{v}} $$

Since $m_\text{a} >> m_\text{v}$, we can write:

$$\frac{H}{m_\text{a}} = h = \frac{m_\text{a} h_\text{a} + m_\text{v} h_\text{v}}{m_\text{a} } $$

The specific enthalpy then has units of kJ per kg dry air.

$$h = h_\text{a} + \frac{m_\text{v}}{m_\text{a}} h_\text{v}$$

$$h = h_\text{a} + \omega h_\text{v}$$

We assume that the specific enthalpy of water vapor is:

$$h_\text{v} \approx h_\text{g}(T) $$

Typically don't know $\omega$. We can convert the specific enthalpy from units of kJ per kg dry air, $h$, to kJ per kg humid air via, $h_\text{ha}$:

$$h = h_\text{ha} \left( 1 + \omega \right) $$

### Equilibrium of moist air and water

Moist air behaves as dry air plus water vapor. At equilibrium, the amount of water that is evaporating is equal to the amount of water that is condensing. 

We **assume**:
1. Dry air and water vapor behave as independent ideal gases.
2. The equilibrium between liquid water and water vapor isn't affected by air pressure.
3. Partial pressure of water vapor equals to that of the saturation pressure at the mixture temperature:

$$p_\text{v} = p_\text{g}(T) $$

```
|       p       |
|       |       |
|       v       |
+---------------+
+---------------+
|               |
| y_v1+y_a1 = 1 |
| vapor+dry air |
|               |
|               |
|               |
+---------------+
initial state, v1
```


```
|               |
|               |
|               |
|               |
|       p       |
|       |       |
|       v       |
+---------------+
+---------------+
|  vapor        |
|---------------|
| condensate    |
+---------------+
final state
less vapor
v2; v3
```

Examples: Steam from a steam pot. Vapor condenses on your hand. As it condenses, latent heat is released. 

## How do we measure the humidity ratio? 

Adiabatic saturator. Determining the adiabatic saturating temperature, $T_\text{as}$, which is less than $T$.

$$ \omega = \frac{\dot{m}_\text{v}}{\dot{m}_\text{a}} = ?$$

```
----------------------------------------------------

undersaturated air entering                       saturated air exiting
T                                                  T_as


|                                                  |
|                                                  |
+-----------------------    -----------------------+
                      liquid water 
                     entering
```

$$\omega = F(T_\text{as}) $$

We measure $T_\text{as}$ and evaluate $\omega$. 

Saturated vapor is at the outlet if the device is long enough. 

Steady flow analysis:

$$\dot{m}_\text{a,in} + \dot{m}_\text{v,in} + \dot{m}_\text{l,in} = \dot{m}_\text{a,out} + \dot{m}_\text{v,out} $$

The mass of the air entering equals the mass of the air exiting:

$$\dot{m}_\text{v,in} + \dot{m}_\text{l,in} = \dot{m}_\text{v,out} $$

$$\implies \dot{m}_\text{l,in} = \dot{m}_\text{v,out} - \dot{m}_\text{v,in}$$

$$\dot{m}_\text{a,in} h_\text{a,in} + \dot{m}_\text{v,in} h_\text{v,in} + \dot{m}_\text{l,in} h_\text{l,in} = \dot{m}_\text{a,out} h_\text{a,out} + \dot{m}_\text{v,out} h_\text{v,out} $$

Some notation:
$$ \dot{m}_\text{a} = \dot{m}_\text{a,in} = \dot{m}_\text{a,out}$$

$$ \dot{m}_\text{v}' =  \dot{m}_\text{v,out}$$

$$ \dot{m}_\text{v} = \dot{m}_\text{v,in}$$

From the above we can write:
$$\dot{m}_\text{l,in} =  \dot{m}_\text{v}' - \dot{m}_\text{v}$$

We can then re-write our energy equation as:

$$\dot{m}_\text{a} h_\text{a,in} + \dot{m}_\text{v} h_\text{v,in} + (\dot{m}_\text{v}' - \dot{m}_\text{v}) h_\text{l,in} = \dot{m}_\text{a} h_\text{a,out} + \dot{m}_\text{v}' h_\text{v,out}  $$

We know that at the exit of the device, the air is saturated ($x = 1$) and at the adiabatic saturation temperature, $T_\text{as}$:

$$h_\text{v,out} = h(T=T_\text{as},x=1)$$

We also know that the liquid entering the device is a saturated liquid also at the adiabatic saturation temperature:

$$h_\text{l,in} = h(T=T_\text{as},x=0) $$

$$\dot{m}_\text{a} h_\text{a,in} + \dot{m}_\text{v} h_\text{v,in} + (\dot{m}_\text{v}' - \dot{m}_\text{v}) h(T=T_\text{as},x=0) = \dot{m}_\text{a} h_\text{a,out} + \dot{m}_\text{v}' h(T=T_\text{as},x=1)  $$

We can define the absolute humidities as:

$$\omega = \frac{m_\text{v}}{m_\text{a}} = \frac{\dot{m}_\text{v}}{\dot{m}_\text{a}} $$

$$\omega' = \frac{\dot{m}_\text{v}'}{\dot{m}_\text{a}} $$

We can re-write our steady flow energy equation as:

$$ h_\text{a,in} + \omega h_\text{v,in} + (\omega' - \omega) h(T=T_\text{as},x=0) = h_\text{a,out} + \omega' h(T=T_\text{as},x=1)  $$

$$ h_\text{a,in} + \omega (h_\text{v,in} - h(T=T_\text{as},x=0))  + h(T=T_\text{as},x=0) \omega' = h_\text{a,out} + \omega' h(T=T_\text{as},x=1)  $$

$$ \omega (h_\text{v,in} - h(T=T_\text{as},x=0))  = h_\text{a,out} - h_\text{a,in} + \omega' h(T=T_\text{as},x=1) - h(T=T_\text{as},x=0) \omega' $$

$$ \omega   = \frac{h_\text{a,out} - h_\text{a,in} + \omega' \left[ h(T=T_\text{as},x=1) - h(T=T_\text{as},x=0)\right]}{(h_\text{v,in} - h(T=T_\text{as},x=0))} $$

Substitute in the measured value of $T_\text{as}$ to get $\omega$. We know $\omega'$ because $\phi' = 100\%$, $p'=p$, and $T'=T_\text{as}$. 


```python

```
