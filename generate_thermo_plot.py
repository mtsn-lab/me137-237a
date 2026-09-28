import matplotlib.pyplot as plt
import numpy as np

# Constants
kB = 1.38e-23  # J/K
T = 300        # K
landauer_limit_joules_per_bit = kB * T * np.log(2)

# Assume 1 FLOP involves roughly 10^3 to 10^4 bit flips for simplicity, 
# or just compare J/bit and J/FLOP separately.
# Let's compare energy per bit flip vs energy per FLOP.
# Landauer limit per bit flip:
e_landauer_bit = landauer_limit_joules_per_bit

# Modern computing estimates (very rough)
# A modern GPU might use ~10^-12 to 10^-15 Joules per operation/bit flip.
# Let's use a range.
modern_values = np.logspace(-15, -10, 50)

plt.figure(figsize=(8, 6))
plt.semilogy(modern_values, [e_landauer_bit]*len(modern_values), 'r--', label='Landauer Limit (Theoretical)')
plt.semilogy(modern_values, modern_values, 'b-', label='Modern Computing (Approximate)')

plt.xlabel('Energy per bit flip [J]')
plt.ylabel('Energy [J]')
plt.title('Thermodynamic Limit vs Modern Computing')
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend()
plt.savefig('lectures/figures/thermodynamics_limit.pdf')
print("Saved thermodynamics_limit.pdf")
