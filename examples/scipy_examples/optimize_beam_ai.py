""" 
We will write a script to minimize the cross-sectional area $A = b \cdot h$ of a simply supported rectangular beam subjected to a uniform distributed load $q$ over span $L$. The optimization space is bounded by three physical limits:Bending Stress (Moment): $\sigma_{max} = \frac{6 \cdot M_{max}}{b \cdot h^2} \le \sigma_{allow}$Shear Stress: $\tau_{max} = \frac{3 \cdot V_{max}}{2 \cdot b \cdot h} \le \tau_{allow}$Serviceability (Deflection): $\delta_{max} = \frac{5 \cdot q \cdot L^4}{384 \cdot E \cdot I} \le \delta_{allow}$
 """
#%% IMPORT LIBRARIES
import json
import numpy as np
from scipy.optimize import minimize, Bounds, NonlinearConstraint
import matplotlib.pyplot as plt

#%% DEFINE PARAMETERS
# Beam physical and material parameters (Steel)
L: float = 5.0                # Span (m)
q: float = 20000.0            # Distributed load (N/m)
E: float = 200e9              # Young's modulus (Pa)
sigma_allow: float = 250e6    # Allowable bending stress (Pa)
tau_allow: float = 145e6      # Allowable shear stress (Pa)
delta_allow: float = L / 300.0 # Allowable deflection (m)

#%% DEFINE OBJECTIVE AND CONSTRAINTS
# x = [b, h] (width, height in meters)

def objective(x: list[float]) -> float:
    """Minimize cross-sectional area to reduce weight and cost."""
    b: float = x[0]
    h: float = x[1]
    return b * h

def bending_stress(x: list[float]) -> float:
    b: float = x[0]
    h: float = x[1]
    M_max: float = (q * L**2) / 8.0
    return (6.0 * M_max) / (b * h**2)

def shear_stress(x: list[float]) -> float:
    b: float = x[0]
    h: float = x[1]
    V_max: float = (q * L) / 2.0
    return (3.0 * V_max) / (2.0 * b * h)

def deflection(x: list[float]) -> float:
    b: float = x[0]
    h: float = x[1]
    I: float = (b * h**3) / 12.0
    return (5.0 * q * L**4) / (384.0 * E * I)

def constraint_funcs(x: list[float]) -> np.ndarray:
    """
    Returns array of constraints. 
    NonlinearConstraint requires all values to be >= 0 for the lower bound.
    """
    return np.array([
        sigma_allow - bending_stress(x),
        tau_allow - shear_stress(x),
        delta_allow - deflection(x),
        2.0 * x[0] - x[1]  # Geometric constraint: h <= 2b
    ])

nlc = NonlinearConstraint(constraint_funcs, 0, np.inf)

#%% RUN OPTIMIZATION
# Initial guess [b, h]
x0: list[float] = [0.1, 0.2]

# Bounds: minimum width 0.05m, minimum height 0.1m, max limits 0.5m x 1.0m
bounds = Bounds([0.05, 0.1], [0.5, 1.0])

result = minimize(objective, x0, bounds=bounds, constraints=nlc, method='trust-constr')

b_opt: float = float(result.x[0])
h_opt: float = float(result.x[1])
area_opt: float = b_opt * h_opt

print(f"Optimization Status: {result.message}")
print(f"Optimal Width (b): {b_opt:.4f} m")
print(f"Optimal Height (h): {h_opt:.4f} m")
print(f"Optimal Area: {area_opt:.4f} m^2")

#%% BILINGUAL PLOTTING SETUP
# Language toggle switch
LANG: str = "ES"

# English JSON structure
plot_json_en: str = """
{
    "title": "Beam Cross Section Optimization Space",
    "xlabel": "Width b (m)",
    "ylabel": "Height h (m)",
    "label_optimal": "Optimal Dimensions",
    "annotation": "Global Minimum"
}
"""

plot_dict: dict = json.loads(plot_json_en)

# Update with Spanish terms (no utf-8 accents) if toggle is set
if LANG == "ES":
    plot_json_es: str = """
    {
        "title": "Espacio de Optimizacion de Seccion Transversal",
        "xlabel": "Ancho b (m)",
        "ylabel": "Alto h (m)",
        "label_optimal": "Dimensiones Optimas",
        "annotation": "Minimo Global"
    }
    """
    plot_dict.update(json.loads(plot_json_es))

#%% GENERATE PLOT
# Create a meshgrid to visualize the area in the optimization space
b_vals: np.ndarray = np.linspace(0.05, 0.5, 100)
h_vals: np.ndarray = np.linspace(0.1, 1.0, 100)
B, H = np.meshgrid(b_vals, h_vals)
Area = B * H

plt.figure(figsize=(8, 6))
contour = plt.contourf(B, H, Area, 50, cmap='viridis', alpha=0.7)
cbar = plt.colorbar(contour)
cbar.set_label("Area (m^2)")

# Mark the optimal point found by scipy
plt.plot(b_opt, h_opt, 'ro', label=plot_dict["label_optimal"], markersize=8)
plt.annotate(plot_dict["annotation"], (b_opt, h_opt), 
             xytext=(b_opt + 0.05, h_opt + 0.1),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))

plt.title(plot_dict["title"])
plt.xlabel(plot_dict["xlabel"])
plt.ylabel(plot_dict["ylabel"])
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()