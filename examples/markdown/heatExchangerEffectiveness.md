# Heat Exchanger Analysis: The Effectiveness–NTU ($\varepsilon$-$\text{NTU}$) Method

When modeling thermofluid flow networks in data center energy systems (e.g., facility heat exchangers, liquid cooling distribution units, air handling units), the Effectiveness–NTU Method enables calculation of heat transfer rates without requiring prior knowledge of outlet temperatures.

### Heat Capacity Rates

The heat capacity rate $C$ measures the thermal energy transport rate per unit temperature change for a fluid stream. The hot fluid heat capacity rate is defined as:

$$C_h = \dot{m}_h c_{p,h}$$

while the cold fluid heat capacity rate is:

$$C_c = \dot{m}_c c_{p,c}$$

where $\dot{m}$ is the mass flow rate ($\text{kg/s}$) and $c_p$ is Specific heat capacity at constant pressure ($\text{J}/(\text{kg}\cdot\text{K})$). From these rates, we define the critical sizing parameters:

$$C_{\min} = \min(C_h, C_c)$$
$$C_{\max} = \max(C_h, C_c)$$

The capacity ratio is then defined as:

$$C_r = \frac{C_{\min}}{C_{\max}} \quad (0 \le C_r \le 1)$$

### Maximum Heat Transfer and Effectiveness

The maximum possible heat transfer rate occurs in a counter-flow heat exchanger of infinite surface area:

$$q_{\max} = C_{\min} (T_{h,\text{in}} - T_{c,\text{in}})$$

The heat exchanger effectiveness, $\varepsilon$, is the ratio of actual heat transfer rate ($q$) to the maximum possible rate ($q_{\max}$):

$$\varepsilon = \frac{q}{q_{\max}} = \frac{C_h (T_{h,\text{in}} - T_{h,\text{out}})}{C_{\min} (T_{h,\text{in}} - T_{c,\text{in}})} = \frac{C_c (T_{c,\text{out}} - T_{c,\text{in}})}{C_{\min} (T_{h,\text{in}} - T_{c,\text{in}})}$$

The actual heat transfer rate realized within the thermofluid network is:

$$q = \varepsilon \, C_{\min} (T_{h,\text{in}} - T_{c,\text{in}})$$


### Number of Transfer Units ($\text{NTU}$)

The **Number of Transfer Units ($\text{NTU}$)** is a dimensionless parameter characterizing the thermal size and overall thermal conductance of the heat exchanger:

$$\text{NTU} = \frac{U A}{C_{\min}}$$

Where:

* $U$ = Overall heat transfer coefficient ($\text{W}/(\text{m}^2\cdot\text{K})$)
* $A$ = Heat transfer surface area ($\text{m}^2$)

### Effectiveness-NTU Relations

See my notes for the derivation of the parallel plate heat exchanger.


```python

```
