# %% [markdown]
# # Exercise 1: Small-Deflexion of Rectangular Plates
# **Focus:** Chapter 2 - Navier & Lévy Solutions
# **Objective:** Visualize the deflection of a simply supported rectangular plate 
# using the Navier Double Fourier Series and analyze its convergence.

# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =====================================================================
# 1. DEFINE THE PHYSICS & NAVIER EVALUATOR
# =====================================================================
def navier_deflection(x, y, a, b, q0, D, terms=10):
    """
    Computes the transverse deflection w(x, y) using Navier's method.
    'terms' dictates how many odd sine waves are superimposed.
    """
    w = np.zeros_like(x)
    for m in range(1, terms * 2, 2):  # Only odd terms (1, 3, 5...) contribute to a uniform load
        for n in range(1, terms * 2, 2):
            coeff = (16 * q0) / (np.pi**6 * D * m * n)
            denom = ((m / a)**2 + (n / b)**2)**2
            w += coeff * np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b) / denom
    return w

# =====================================================================
# 2. SET UP MATERIAL & GEOMETRIC PARAMETERS
# =====================================================================
# Geometry (meters)
a, b = 2.0, 1.5      
thickness = 0.01     

# Material Properties (Standard Steel)
E = 200e9            # Young's modulus in Pa (N/m^2)
nu = 0.3             # Poisson's ratio

# Load
q0 = 5000.0          # Uniform distributed load (5 kPa)

# Calculate Flexural Rigidity (D)
D = (E * thickness**3) / (12 * (1 - nu**2))

# =====================================================================
# 3. GENERATE MESH & COMPUTE DEFLECTION
# =====================================================================
# Discretize the plate into a grid
X_vec = np.linspace(0, a, 50)
Y_vec = np.linspace(0, b, 50)
X, Y = np.meshgrid(X_vec, Y_vec)

# Compute deflection mapping (using 20 summation terms for high accuracy)
W = navier_deflection(X, Y, a, b, q0, D, terms=20)

# Convert deflection to millimeters for readability
W_mm = W * 1000  

# Output the maximum deflection at the center of the plate
w_max = navier_deflection(a/2, b/2, a, b, q0, D, terms=20) * 1000
print(f"Maximum Deflection (at center): {w_max:.3f} mm")

# =====================================================================
# 4. 3D VISUALIZATION
# =====================================================================
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, W_mm, cmap='plasma', edgecolor='none', alpha=0.9)

ax.set_title(f"Navier Solution: Plate Deflection ($q_0$ = {q0/1000} kPa)", pad=20, fontsize=14)
ax.set_xlabel("Length a (m)", labelpad=10)
ax.set_ylabel("Width b (m)", labelpad=10)
ax.set_zlabel("Deflection w (mm)", labelpad=10)

# Invert Z-axis so deflection bows downward (physically intuitive)
ax.invert_zaxis() 

# Add a color bar
fig.colorbar(surf, shrink=0.5, aspect=10, label="Deflection (mm)")

plt.show()