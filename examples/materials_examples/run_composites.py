import numpy as np
import matplotlib.pyplot as plt
# Unlike alloys, composites (like Carbon Fiber Reinforced Polymer - CFRP) are macroscopic mixtures. The "Rule of Mixtures" is the governing equation for estimating the Elastic Modulus ($E$) based on the volume fraction of fibers.

# Material Properties (in GPa)
E_fiber = 230.0  # Carbon Fiber
E_matrix = 3.5   # Epoxy Resin

# Create array of Volume Fractions (0% to 100% fiber)
V_f = np.linspace(0, 1, 100)
V_m = 1 - V_f  # Volume fraction of matrix

# 1. Calculate Upper Bound (Voigt Model - Parallel Loading)
# Good for longitudinal loading
E_upper = (V_f * E_fiber) + (V_m * E_matrix)

# 2. Calculate Lower Bound (Reuss Model - Series Loading)
# Good for transverse loading
E_lower = 1 / ((V_f / E_fiber) + (V_m / E_matrix))

# 3. Plotting
plt.figure(figsize=(10, 6))
plt.plot(V_f, E_upper, label='Longitudinal Stiffness (Upper Bound)', color='navy', linewidth=2)
plt.plot(V_f, E_lower, label='Transverse Stiffness (Lower Bound)', color='firebrick', linewidth=2)

# Annotation
plt.title('Composite Stiffness: Rule of Mixtures (CFRP)')
plt.xlabel('Volume Fraction of Fiber ($V_f$)')
plt.ylabel('Elastic Modulus (GPa)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Highlight a specific design point (e.g., 60% fiber)
idx = (np.abs(V_f - 0.6)).argmin()
plt.plot(V_f[idx], E_upper[idx], 'ko')
plt.text(V_f[idx], E_upper[idx] + 10, f'{E_upper[idx]:.1f} GPa', ha='center')

plt.show()