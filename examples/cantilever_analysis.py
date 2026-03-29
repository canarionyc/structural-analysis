# %% Cantilever Beam Analysis
"""
Analysis of a cantilever beam with various loading conditions.
Demonstrates the use of autoimport for different structural analysis scenarios.
"""

# Import common structural analysis functionality
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autoimport import import_all
import_all()

# %% Problem Setup
print("=== Cantilever Beam Analysis ===")
print("Analyzing a cantilever beam with different loading conditions")

# Additional symbols for this analysis
w = sp.symbols('w', positive=True)  # Distributed load
F = sp.symbols('F', real=True)      # End force

# %% Case 1: Point load at free end
print("\n=== Case 1: Point load P at free end ===")

# For a cantilever beam with point load P at free end:
# - Maximum deflection at free end
# - Maximum moment at fixed end

max_deflection_point = P * L**3 / (3 * E * I)
max_moment_point = P * L

print("Maximum deflection (at free end):")
sp.pprint(max_deflection_point)
print("\nMaximum moment (at fixed end):")
sp.pprint(max_moment_point)

# %% Case 2: Uniformly distributed load
print("\n=== Case 2: Uniformly distributed load w ===")

# For a cantilever beam with uniform load w:
max_deflection_uniform = w * L**4 / (8 * E * I)
max_moment_uniform = w * L**2 / 2

print("Maximum deflection (at free end):")
sp.pprint(max_deflection_uniform)
print("\nMaximum moment (at fixed end):")
sp.pprint(max_moment_uniform)

# %% Case 3: Combined loading
print("\n=== Case 3: Combined point load and distributed load ===")

# Superposition principle
total_deflection = max_deflection_point + max_deflection_uniform
total_moment = max_moment_point + max_moment_uniform

print("Total maximum deflection:")
sp.pprint(total_deflection)
print("\nTotal maximum moment:")
sp.pprint(total_moment)

# %% Numerical Example with Units
print("\n=== Numerical Example with Units ===")

# Define concrete beam properties
L_val = 3.0 * ureg.meter
P_val = 500 * ureg.newton
w_val = 200 * ureg.newton / ureg.meter
E_val = 30e9 * ureg.pascal  # Concrete modulus
I_val = 50e-6 * ureg.meter**4

print("Beam properties:")
print(f"Length: {L_val}")
print(f"Point load: {P_val}")
print(f"Distributed load: {w_val}")
print(f"Young's modulus: {E_val}")
print(f"Moment of inertia: {I_val}")

# Calculate numerical results
def_point_num = P_val * L_val**3 / (3 * E_val * I_val)
def_uniform_num = w_val * L_val**4 / (8 * E_val * I_val)
total_def_num = def_point_num + def_uniform_num

print(f"\nDeflection from point load: {def_point_num.to('millimeter'):.2f}")
print(f"Deflection from distributed load: {def_uniform_num.to('millimeter'):.2f}")
print(f"Total deflection: {total_def_num.to('millimeter'):.2f}")

# Check allowable deflection (L/250 is a common limit)
allowable_def = L_val / 250
print(f"Allowable deflection (L/250): {allowable_def.to('millimeter'):.2f}")

if total_def_num > allowable_def:
    print("⚠️  WARNING: Deflection exceeds allowable limit!")
else:
    print("✅ Deflection is within allowable limits")

# %% Visualization
print("\n=== Creating Deflection Plot ===")

# Create numerical arrays for plotting
x_vals = np.linspace(0, float(L_val.magnitude), 100)
L_num = float(L_val.magnitude)
P_num = float(P_val.magnitude)
w_num = float(w_val.magnitude)
E_num = float(E_val.magnitude)
I_num = float(I_val.magnitude)

# Calculate deflection along the beam length
deflections_point = []
deflections_uniform = []

for x_val in x_vals:
    # Point load deflection
    if x_val <= L_num:
        v_point = P_num * x_val**2 * (3*L_num - x_val) / (6 * E_num * I_num)
    else:
        v_point = 0
    
    # Uniform load deflection
    v_uniform = w_num * x_val**2 * (6*L_num**2 - 4*L_num*x_val + x_val**2) / (24 * E_num * I_num)
    
    deflections_point.append(v_point)
    deflections_uniform.append(v_uniform)

deflections_total = np.array(deflections_point) + np.array(deflections_uniform)

# Create the plot
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(x_vals, np.array(deflections_point) * 1000, 'b-', label='Point load', linewidth=2)
plt.plot(x_vals, np.array(deflections_uniform) * 1000, 'r-', label='Distributed load', linewidth=2)
plt.plot(x_vals, deflections_total * 1000, 'k--', label='Total', linewidth=2)
plt.xlabel('Distance from fixed end (m)')
plt.ylabel('Deflection (mm)')
plt.title('Cantilever Beam Deflection')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 1, 2)
# Show the beam with loads
beam_height = 0.1
plt.fill_between([0, L_num], [-beam_height/2, -beam_height/2], [beam_height/2, beam_height/2], 
                 color='lightgray', label='Beam')
# Fixed support
plt.plot([0, 0], [-beam_height, beam_height], 'k-', linewidth=8, label='Fixed support')
# Point load arrow
plt.arrow(L_num, beam_height, 0, -beam_height/2, head_width=0.1, head_length=0.05, 
          fc='blue', ec='blue', label='Point load')
# Distributed load arrows
for i in range(0, int(L_num*10), 2):
    x_arrow = i/10
    plt.arrow(x_arrow, beam_height/2, 0, -beam_height/4, head_width=0.05, head_length=0.02, 
              fc='red', ec='red', alpha=0.7)

plt.xlim(-0.5, L_num + 0.5)
plt.ylim(-0.5, 0.5)
plt.xlabel('Distance from fixed end (m)')
plt.ylabel('Height (m)')
plt.title('Beam Loading Diagram')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Analysis Complete ===")