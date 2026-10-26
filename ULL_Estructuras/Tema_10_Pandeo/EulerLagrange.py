# %% SYMBOLIC DERIVATION OF THE STABILITY OPERATOR
import sympy as sp
import numpy as np

# Define symbols with explicit physical assumptions
# This prevents 'Piecewise' and 'And' logical objects from poisoning the solve
x = sp.symbols('x', real=True)
L = sp.symbols('L', positive=True)
EI = sp.symbols('EI', positive=True)
P = sp.symbols('P', positive=True)
y_max = sp.symbols('y_max', real=True)
epsilon_0 = sp.symbols('epsilon_0', real=True)

y = sp.Function('y')(x)

# %% Define the Lagrangian Density (Strain Energy - Geometric Work)
# We use the fundamental mode shape for a Fixed-Fixed column
# y(x) = (delta/2) * (1 - cos(2*pi*x/L))
phi = (1 - sp.cos(2 * sp.pi * x / L))
y_trial = (y_max / 2) * phi
y0_trial = (epsilon_0 / 2) * phi

# Strain Energy U (Internal) and Potential of external load W
U =  (1/2) * EI * sp.integrate(sp.diff(y_trial, x, 2) ** 2, (x, 0, L))
W = (1/2) * P * sp.integrate(sp.diff(y_trial + y0_trial, x) ** 2 - sp.diff(y0_trial, x) ** 2, (x, 0, L))

# The Total Potential Energy
Pi = U - W

# %% Minimize with respect to y_max (The Variational Step)
dPi_dy = sp.diff(Pi, y_max)

solution_list = sp.solve(dPi_dy, y_max)
solution = solution_list[0]
print(f"Amplification Solution: {solution}")
# %% Convert the symbolic result into a fast numerical function
# This represents the Ayrton-Perry amplification derived from first principles
amplification_func = sp.lambdify((P, EI, L, epsilon_0), solution, 'numpy')

print(f"Derived Amplification Formula: {sp.simplify(solution)}")

# %% ENGINEERING PARAMETERS & CATALOG DEFINITION
# Material: S275 Steel
E_MODULUS = 210e9  # Pa
YIELD_STRESS = 275e6  # Pa
GAMMA_M1 = 1.05  # Partial safety factor
P_APPLIED = 490000.0  # 490 kN load
LENGTH = 3.45  # meters
IMPERFECTION = LENGTH / 300  # Standard L/300 bow

# Catalog: Circular Hollow Sections (Name, Area [cm2], Inertia [cm4])
# Values are typical for European CHS profiles
# tube_catalog = [
#     {"name": "CHS 114.3x3.6", "area_cm2": 12.5, "inertia_cm4": 190.0},
#     {"name": "CHS 114.3x5.0", "area_cm2": 17.2, "inertia_cm4": 251.0},
#     {"name": "CHS 139.7x4.0", "area_cm2": 17.1, "inertia_cm4": 392.0},
#     {"name": "CHS 139.7x5.0", "area_cm2": 21.2, "inertia_cm4": 479.0},
#     {"name": "CHS 168.3x4.0", "area_cm2": 20.6, "inertia_cm4": 696.0},
#     {"name": "CHS 168.3x6.3", "area_cm2": 32.1, "inertia_cm4": 1040.0},
# ]
# print(f"TUBE CATALOG: {tube_catalog}")

# %% CONSTRAINED OPTIMIZATION LOOP
def sizing_engine(catalog, load, l, e_mod, fy, gamma, eps, verbose=True):
    results = []

    for tube in catalog:
        # Convert units to SI (m, m2, m4)
        A = tube["area_cm2"] * 1e-4
        I = tube["inertia_cm4"] * 1e-8
        W_el = (I / (0.5 * 0.168))  # Elastic section modulus (approx for outer fiber)

        # 1. Calculate the amplified central deflection using derived physics
        try:
            delta_max = amplification_func(load, e_mod * I, l, eps)
        except ZeroDivisionError:
            continue  # Theoretical instability

        # 2. Combined Stress Check (Sigma = P/A + M/W)
        # Bending moment M = P * (delta_max + epsilon_0)
        total_moment = load * (delta_max + eps)
        sigma_comp = load / A
        sigma_bend = total_moment / W_el
        total_stress = sigma_comp + sigma_bend

        # 3. Design criteria: Stress < Design Strength
        is_safe = total_stress <= (fy / gamma)
        if verbose:
            print(f"Profile: {tube['name']}, Area: {tube["area_cm2"]:.2f} cm2, Stress: {total_stress / 1e6:.2f} MPa, Deflection: {delta_max * 1000:.2f} mm, Safe: {is_safe}")
        if is_safe:
            results.append({
                "Name": tube["name"],
                "Area": A,
                "Stress_MPa": total_stress / 1e6,
                "Deflection_mm": delta_max * 1000
            })

    # Find the profile with the minimum area (Weight optimization)
    if not results:
        return "No suitable profile found."

    optimal = min(results, key=lambda x: x['Area'])
    return optimal


# Execute sizing
final_selection = sizing_engine(tube_catalog, P_APPLIED, LENGTH, E_MODULUS, YIELD_STRESS, GAMMA_M1, IMPERFECTION)

print("-" * 30)
print(f"OPTIMAL TUBE SELECTION")
print("-" * 30)
for key, value in final_selection.items():
    print(f"{key}: {value}")

# %% UPDATED SIZING ENGINE & PLOTTING
import matplotlib.pyplot as plt

# We define the imperfection factor alpha (Curve 'a' = 0.21, 'b' = 0.34, etc.)
# These are the "reality check" factors that penalize slender sections
ALPHA = 0.21


# def extended_sizing_engine(catalog, load, l, e_mod, fy, gamma, eps):
#     all_data = []
#
#     for tube in catalog:
#         A = tube["area_cm2"] * 1e-4
#         I = tube["inertia_cm4"] * 1e-8
#         # Outer radius for stress calculation
#         radius_outer = (float(tube["name"].split('x')[0]) / 2) / 1000
#         W_el = I / radius_outer
#
#         # Physics: Amplified Deflection (Second-Order Effect)
#         try:
#             delta_max = amplification_func(load, e_mod * I, l, eps)
#         except ZeroDivisionError:
#             delta_max = np.inf
#
#         # Stress Calculation: Sigma = N/A + (N * (delta + e0)) / W
#         sigma_comp = load / A
#         sigma_bend = (load * (delta_max + eps)) / W_el
#         total_stress_mpa = (sigma_comp + sigma_bend) / 1e6
#
#         is_safe = total_stress_mpa <= (fy / gamma / 1e6)
#
#         all_data.append({
#             "Name": tube["name"],
#             "Area_cm2": tube["area_cm2"],
#             "TotalStress_MPa": total_stress_mpa,
#             "Safe": is_safe
#         })
#     return all_data


#%% Run the engine
results = extended_sizing_engine(tube_catalog, P_APPLIED, LENGTH, E_MODULUS, YIELD_STRESS, GAMMA_M1, IMPERFECTION)

# %% PLOTTING THE STABILITY SPACE
areas = [r["Area_cm2"] for r in results]
stresses = [r["TotalStress_MPa"] for r in results]
names = [r["Name"] for r in results]
colors = ['#2ca02c' if r["Safe"] else '#d62728' for r in results]

plt.figure(figsize=(10, 6))

# Plot the Yield Limit (The "Ceiling")
design_strength = (YIELD_STRESS / GAMMA_M1) / 1e6
plt.axhline(y=design_strength, color='blue', linestyle='--', label=f'Yield Limit ({design_strength:.1f} MPa)')

# Scatter plot of the profiles
plt.scatter(areas, stresses, c=colors, s=100, edgecolors='black', zorder=3)

# Annotate each point
for i, txt in enumerate(names):
    plt.annotate(txt, (areas[i], stresses[i]), xytext=(5, 5), textcoords='offset points', fontsize=9)

plt.title("Total Stress vs. Area (Fixed-Fixed Column)")
plt.xlabel("Cross-Sectional Area (cm²)")
plt.ylabel("Total Stress (MPa)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

# Highlight the "Safe" zone
plt.fill_between([min(areas) - 5, max(areas) + 5], 0, design_strength, color='green', alpha=0.05, label="Safe Zone")

plt.show()