# Thermofluids Flow Network

In order to model our data center, we can build a simplified flow network by treating the fluid system as an electrical circuit analog. This will help us in understanding the acausal equation-solving mechanics that Modelica does. 

We can represent the data center cooling loops (pumps, chillers, server racks) as a graph of nodes and branches. We can then write a simple system of non-linear equations to solve for unknown pressures and mass flow. 

## Node $i$ Control Volume Equations

Nodes represent lumped control volumes with mass $m_i$, volume $V_i$, and total energy $E_i = U_i + \frac{1}{2} m_i v_i^2 + m_i g z_i$. Flow enters node $i$ from neighbor nodes $k \in \text{in}(i)$ and leaves node $i$ toward neighbor nodes $l \in \text{out}(i)$.

### Conservation of Mass:

$$\frac{d m_i}{dt} = \sum_{k \in \text{in}(i)} \dot{m}_{ki} - \sum_{l \in \text{out}(i)} \dot{m}_{il}$$


### Conservation of Energy:

$$\frac{d E_i}{dt} = \dot{Q}_i - \dot{W}_i + \sum_{k \in \text{in}(i)} \dot{m}_{ki} \left( h_k + \frac{v_k^2}{2} + g z_k \right) - \sum_{l \in \text{out}(i)} \dot{m}_{il} \left( h_i + \frac{v_i^2}{2} + g z_i \right)$$


* $\dot{Q}_i$: External heat addition rate across node $i$ boundary (e.g., direct thermal dissipation)
* $\dot{W}_i$: Boundary or shaft work rate done by control volume node $i$

## Branch $ij$ Control Volume Equations

Branch $ij$ connects upstream node $i$ to downstream node $j$ with length $L_{ij}$ and cross-sectional area $A_{ij}$.

### Conservation of Mass:

$$\frac{d m_{ij}}{dt} = \dot{m}_{ij, \text{in}} - \dot{m}_{ij, \text{out}}$$


### Conservation of Momentum (1D Integrated Navier-Stokes):

Integrating the 3D Cauchy momentum equation along a 1D stream-oriented coordinate $s$ directly yields the dynamic branch pressure drop.

#### 1. Generalized 3D Momentum Equation

The differential conservation of linear momentum for an incompressible, viscous fluid in a gravitational field is given by:

$$\rho \left( \frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v} \right) = -\nabla P + \nabla \cdot \boldsymbol{\tau} + \rho \mathbf{g} + \mathbf{f}_{\text{ext}}$$

where $\mathbf{v}$ is the 3D velocity vector, $p$ is static pressure, $\boldsymbol{\tau}$ is the viscous stress tensor, $\mathbf{g}$ is gravitational acceleration, and $\mathbf{f}_{\text{ext}}$ represents external body forces per unit volume (e.g., pump momentum insertion).

#### 2. 1D Reduction

Assume the flow is predominantly 1-dimensional along path $s \in [0, L_{ij}]$ with unit tangent vector $\hat{e}_s$, reducing velocity to scalar $v(s, t) = \mathbf{v} \cdot \hat{e}_s$. Projecting the 3D momentum equation along $s$:

$$\rho \left( \frac{\partial v}{\partial t} + v \frac{\partial v}{\partial s} \right) = -\frac{\partial P}{\partial s} - \rho g \frac{dz}{ds} - f_{\text{viscous}} + f_{\text{source}}$$

where $z(s)$ is the vertical elevation coordinate along the branch length, $f_{\text{viscous}} = -(\nabla \cdot \boldsymbol{\tau}) \cdot \hat{e}_s$ is the internal viscous resistance force per unit volume, and $f_{\text{source}} = \mathbf{f}_{\text{ext}} \cdot \hat{e}_s$ is the active pump pressure gradient per unit volume.

#### 3. Spatial Integration across Branch $ij$

Integrate the differential equation along the path length from node $i$ ($s=0$) to node $j$ ($s=L_{ij}$):

$$\int_{0}^{L_{ij}} \rho \frac{\partial v}{\partial t} \, ds + \int_{0}^{L_{ij}} \rho v \frac{\partial v}{\partial s} \, ds = -\int_{p_i}^{p_j} dp - \int_{z_i}^{z_j} \rho g \, dz - \int_{0}^{L_{ij}} f_{\text{viscous}} \, ds + \int_{0}^{L_{ij}} f_{\text{source}} \, ds$$

We can evaluate each integral individually. For the transient inertia, we can express the local velocity via mass flow rate $v(s, t) = \frac{\dot{m}_{ij}(t)}{\rho A(s)}$. Therefore:

$$\int_{0}^{L_{ij}} \rho \frac{\partial}{\partial t} \left( \frac{\dot{m}_{ij}}{\rho A(s)} \right) ds = \left( \int_{0}^{L_{ij}} \frac{ds}{A(s)} \right) \frac{d\dot{m}_{ij}}{dt}$$

For a uniform cross-sectional area $A_{ij}$, this simplifies to $\frac{L_{ij}}{A_{ij}} \frac{d\dot{m}_{ij}}{dt}$.

For the advective kinetic energy change, we can write:

$$\int_{0}^{L_{ij}} \rho v \frac{\partial v}{\partial s} \, ds = \int_{v_i}^{v_j} \rho v \, dv = \frac{1}{2}\rho \left( v_j^2 - v_i^2 \right)$$

For the static pressure drop, we can write:

$$-\int_{p_i}^{p_j} dp = p_i - p_j$$

For the gravitational potential energy change, we can write: 

$$-\int_{z_i}^{z_j} \rho g \, dz = -\rho g (z_j - z_i) = \rho g (z_i - z_j)$$

For viscous friction losses, we can write:

$$\int_{0}^{L_{ij}} f_{\text{viscous}} \, ds = \Delta p_{\text{loss}, ij} = \frac{1}{2}\rho v^2 \left( \frac{f_D L_{ij}}{D_{h, ij}} \right)$$

where $D_{h, ij}$ is the hydraulic diameter. The hydraulic diameter generalizes non-circular conduit cross-sections so standard pipe friction correlations can be applied. It is defined as $D_{h, ij} = \frac{4 A_{ij}}{P_{w, ij}}$, where $A_{ij}$ is the cross-sectional flow area of the conduit and $P_{w, ij}$ is the wetted perimeter, which is the perimeter of the cross-section in physical contact with the flowing fluid.

For the active mechanical work source, we can write:

$$\int_{0}^{L_{ij}} f_{\text{source}} \, ds = \Delta p_{\text{source}, ij}$$

Combining terms and isolating the node potential difference $(p_i - p_j)$:

$$p_i - p_j = \left( \int_{0}^{L_{ij}} \frac{ds}{A(s)} \right) \frac{d\dot{m}_{ij}}{dt} + \frac{1}{2}\rho \left( v_j^2 - v_i^2 \right) + \rho g (z_j - z_i) + \Delta p_{\text{loss}, ij} - \Delta p_{\text{source}, ij}$$

### Conservation of Energy:

$$\frac{d E_{ij}}{dt} = \dot{Q}_{ij} - \dot{W}_{ij} + \dot{m}_{ij, \text{in}} \left( h_i + \frac{v_i^2}{2} + g z_i \right) - \dot{m}_{ij, \text{out}} \left( h_j + \frac{v_j^2}{2} + g z_j \right)$$


