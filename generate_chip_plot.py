import matplotlib.pyplot as plt
import numpy as np

# Layer properties (thickness in m, conductivity in W/mK)
layers = [
    {'name': 'Silicon', 'L': 0.0007, 'k': 140, 'q_gen': 1e8}, # W/m^3 (100 W/cm^2 / 0.7mm ~ 1.4e8)
    {'name': 'TIM', 'L': 0.00005, 'k': 5, 'q_gen': 0},
    {'name': 'Spreader', 'L': 0.003, 'k': 390, 'q_gen': 0},
    {'name': 'Vapor Chamber', 'L': 0.003, 'k': 5000, 'q_gen': 0},
    {'name': 'Heat Sink', 'L': 0.025, 'k': 200, 'q_gen': 0},
]

# Total thickness
total_L = sum(l['L'] for l in layers)

# x coordinates of interfaces
x_interfaces = [0.0]
current_x = 0.0
for l in layers:
    current_x += l['L']
    x_interfaces.append(current_x)

x_interfaces = np.array(x_interfaces)

# Let's solve from the bottom up (ambient temperature at the end)
# T_ambient = 300K at x = total_L
T_ambient = 300.0

# We need to find the heat flux Q. 
# In steady state, the heat flux through every layer (except silicon) is constant.
# Q = -k * dT/dx
# For layers with q_gen=0: dT/dx = -Q/k
# For silicon: dT/dx = -(q_gen * x)/k + C. At x=0, dT/dx=0 (if we assume symmetry or top boundary).
# So dT/dx = -q_gen * x / k.
# Total heat flux at the bottom of silicon: Q = q_gen * L_si

# Let's calculate Q from the silicon properties.
q_gen_si = layers[0]['q_gen']
L_si = layers[0]['L']
Q = q_gen_si * L_si

# Now calculate temperatures from bottom to top.
# Layers: 4, 3, 2, 1, 0
T = np.zeros(len(layers))
T_at_interfaces = np.zeros(len(layers) + 1)

# T at last interface (x = total_L) is T_ambient
T_at_interfaces[-1] = T_ambient

# Work backwards from the last interface
for i in range(len(layers)-1, -1, -1):
    # Interface i is the boundary between layer i-1 and layer i.
    # We are going from interface i+1 to interface i.
    # Layer i is between x_interfaces[i] and x_interfaces[i+1]
    
    L_i = layers[i]['L']
    k_i = layers[i]['k']
    q_gen_i = layers[i]['q_gen']
    
    # If q_gen_i == 0:
    # T(x) = T_interface_next - (Q/k_i) * (x_interface_next - x)
    # T(x_i) = T_interface_next - (Q/k_i) * L_i
    
    if q_gen_i == 0:
        T_at_interfaces[i] = T_at_interfaces[i+1] + Q * L_i / k_i
    else:
        # Silicon layer (i=0)
        # T(x) = - (q_gen * x^2) / (2k) + C
        # But we are working backwards.
        # Let's integrate from the boundary x_i to x_{i+1}.
        # For Silicon (i=0), x_i = 0.
        # T(x) = - (q_gen * x^2) / (2k) + T(0)
        # Q = q_gen * L_si
        # T(L_si) = T(0) - (q_gen * L_si^2) / (2k)
        # T(0) = T(L_si) + (q_gen * L_si^2) / (2k)
        T_at_interfaces[i] = T_at_interfaces[i+1] + (q_gen_i * L_i**2) / (2 * k_i)

# Now build the full temperature profile
x_fine = np.linspace(0, total_L, 1000)
T_fine = np.zeros_like(x_fine)

for i in range(len(layers)):
    # layer i is between x_interfaces[i] and x_interfaces[i+1]
    idx_start = np.searchsorted(x_fine, x_interfaces[i])
    idx_end = np.searchsorted(x_fine, x_interfaces[i+1])
    
    x_layer = x_fine[idx_start:idx_end]
    if len(x_layer) == 0: continue
    
    L_i = layers[i]['L']
    k_i = layers[i]['k']
    q_gen_i = layers[i]['q_gen']
    T_start = T_at_interfaces[i]
    
    if q_gen_i == 0:
        # Linear: T(x) = T_start - (Q/k_i) * (x - x_start)
        # Wait, my backwards calculation was: T_at_interfaces[i] = T_at_interfaces[i+1] + Q*L/k
        # So T_at_interfaces[i] is the higher temperature.
        # T(x) = T_at_interfaces[i] - (Q/k_i) * (x - x_interfaces[i])
        T_fine[idx_start:idx_end] = T_at_interfaces[i] - (Q/k_i) * (x_layer - x_interfaces[i])
    else:
        # Silicon: T(x) = T_at_interfaces[0] - (q_gen * x^2) / (2k)
        # Since x_interfaces[0] = 0
        T_fine[idx_start:idx_end] = T_at_interfaces[0] - (q_gen_i * x_layer**2) / (2 * k_i)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x_fine * 1000, T_fine, 'b-', linewidth=2)
plt.axvline(x=x_interfaces[0]*1000, color='k', linestyle='--')
for x_int in x_interfaces:
    plt.axvline(x=x_int*1000, color='gray', linestyle=':', alpha=0.5)

plt.xlabel('Distance [mm]')
plt.ylabel('Temperature [K]')
plt.title('1D Chip Cooling Temperature Profile')
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.savefig('lectures/figures/chip_temperature_profile.pdf')
print("Saved chip_temperature_profile.pdf")
