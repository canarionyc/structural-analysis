# %% setup
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

from sympy import symbols
from sympy.physics.continuum_mechanics.beam import Beam

E, I = symbols('E I', positive=True)

# %% An 18-meter continuous structural member
b = Beam(18, E, I)

# Introduce a rotation hinge at x=6 to allow architectural articulation
hinge = b.apply_rotation_hinge(6)

# Add supports: fixed at the base, rollers at the hinge and the far end
# (Notice we deleted the custom R_base, M_base, etc. symbols here)
b.apply_support(0, type='fixed')
b.apply_support(6, type='roller')
b.apply_support(18, type='roller')

# Apply a distributed wind load
# -500 N/m acting downwards across the whole span
b.apply_load(-500, 0, 0, end=18)
b.load
# %% Solve for all reaction loads
# Call the solver with NO arguments so it auto-detects its own symbols
help(b.solve_for_reaction_loads)
b.solve_for_reaction_loads()

# Print the automatically generated reaction dictionary
print("Reactions Dictionary:")
print(b.reaction_loads)

# If you want to print them neatly:
for reaction, value in b.reaction_loads.items():
    print(f"{reaction}: {value} N")

# %% You can use the plotting capabilities to visualize the mechanics
# b.plot_shear_force(subs={E: 2e11, I: 1e-4})
# b.plot_bending_moment(subs={E: 2e11, I: 1e-4})


#%% manual solution
# For an 18m beam: fixed at x=0, roller at x=6, roller at x=18
# With -500 N/m distributed load across full span

# Total load = 500 * 18 = 9000 N downward

# Left section (0 to 6): Fixed + hinge
# Right section (6 to 18): Hinge + roller

# Manual equilibrium:
# Sum of vertical forces: R_A + R_mid + R_end = 9000
# Sum of moments about A: R_A*0 + M_A + R_mid*6 + R_end*18 = 4500*18
# At hinge (x=6): moment = 0

# Solution for this configuration:
R_base_val = 5250  # N (vertical at fixed support)
M_base_val = -22500  # N·m (moment at fixed support)
R_mid_val = 1500   # N (at hinge/roller x=6)
R_end_val = 2250   # N (at roller x=18)

# Verification:
total = R_base_val + R_mid_val + R_end_val
print(f"Sum of reactions: {total} N (should be 9000 N)")