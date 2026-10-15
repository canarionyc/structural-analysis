# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Solving Beam Bending Problems using Singularity Functions
# This script contains the foundational examples from the SymPy Continuum 
# Mechanics beam tutorial. Each example is isolated in its own cell for 
# interactive execution.
#

# %%
import sympy as sp
from sympy.physics.continuum_mechanics.beam import Beam

# Initialize pretty printing for the interactive window
sp.init_printing(use_unicode=True)

# %% [markdown]
# ## Example 1: Cantilever Beam
# A cantilever beam 9 meters in length has a distributed constant load of 8 kN/m
# applied downward from the fixed end over a 5 meter distance. A counterclockwise
# moment of 50 kN-m is applied 5 meters from the fixed end. Lastly, a downward
# point load of 12 kN is applied at the free end of the beam.
#
# *Note: This example uses a sign convention where downward forces and 
# counterclockwise moments are positive.*

# %% [raw]
#        y
#        ^
#        |
#    \\\\|
#    \\\\|    8 kN/m
#    \\\\|_________________
#    \\\\|| | | | | | | | |             12 kN
#    \\\\|V V V V V V V V V               |
#    \\\\|________________|_______________V
#    \\\\|                |               |
#    \\\\o - - - - - - - -↺ 50 kN-m - - - | - - -> x
#    \\\\|________________|_______________|
#    \\\\|                                :
#    \\\\|----------------|---------------|
#               5.0 m            4.0 m

# %%
E, I = sp.symbols('E I', positive=True)
b1 = Beam(9, E, I)

# Apply boundary conditions manually (fixed at x = 0 means 0 deflection and 0 slope)
b1.bc_deflection.append((0, 0))
b1.bc_slope.append((0, 0))

# Create unknown reaction variables for the fixed support
R, M = sp.symbols('R M')

# Apply reaction loads
b1.apply_load(R, 0, -1)
b1.apply_load(M, 0, -2)

# Apply external loads
b1.apply_load(8, 0, 0, end=5) # 8 kN/m distributed load from x=0 to x=5
b1.apply_load(50, 5, -2)      # 50 kN-m counterclockwise moment at x=5
b1.apply_load(12, 9, -1)      # 12 kN downward point load at x=9

b1.load

# %%
# Solve for the reaction forces explicitly looking for R and M
b1.solve_for_reaction_loads(R, M)

print("Example 1 Reactions:", b1.reaction_loads)

# %%
print("\nExample 1 Bending Moment Equation:")
sp.pprint(b1.bending_moment())

# %%
# Define sample values for the constants

params = {
    E: 2e11,  # Young's modulus (Pa) - typical for steel
    I: 1e-4  # Moment of inertia (m^4)
}
b1.plot_deflection(params)
b1.plot_slope(params)
b1.plot_shear_force(params)
b1.plot_bending_moment()

# %% [markdown]
# ## Example 2: Beam with Two Simple Supports and Overhang
# There is a beam of length 30 meters. A point load of magnitude 8 N is applied 
# from the top of the beam at the starting point. There are two simple supports 
# below the beam at x=10 and x=30. A moment of magnitude 120 Nm is applied in 
# the counter-clockwise direction at the end of the beam.
#

# %% [raw]
#   || 8 N                                       ↺ 120 Nm
#   \/______________________________________________|
#   |_______________________________________________|
#               /\                                 /\
#   |------------|---------------------------------|
#       10 m                  20 m
#

# %%
E, I = sp.symbols('E I', positive=True)
R1, R2 = sp.symbols('R1 R2')
b2 = Beam(30, E, I)

# Apply simple supports (deflection is restricted at the supports)
b2.bc_deflection.append((10, 0))
b2.bc_deflection.append((30, 0))

# Apply external loads and reaction forces
b2.apply_load(8, 0, -1)     # 8 N downward load at x=0
b2.apply_load(R1, 10, -1)   # Reaction load at first support x=10
b2.apply_load(R2, 30, -1)   # Reaction load at second support x=30
b2.apply_load(120, 30, -2)  # 120 Nm counterclockwise moment at x=30

# Solve for the reactions
b2.solve_for_reaction_loads(R1, R2)
b2.reaction_loads

print("Example 2 Reactions:", b2.reaction_loads)
print("\nExample 2 Deflection Equation:")
sp.pprint(b2.deflection())

# %%
# Define sample values for the constants

params = {
    E: 2e11,  # Young's modulus (Pa) - typical for steel
    I: 1e-4  # Moment of inertia (m^4)
}
b2.plot_shear_force(params);
b2.plot_bending_moment();
b2.plot_slope(params);
b2.plot_deflection(params);

# %% [markdown]
# ## Example 3: Composite/Stepped Beam with Varying Moment of Inertia
# A cantilever beam of length 4 meters. For the first 2 meters its moment of 
# inertia is 1.5 * I, and I for the rest. A point load of magnitude 20 N is 
# applied from the top at its free end.
#

# %%
E, I = sp.symbols('E I', positive=True)

# Create two beam segments with their respective moments of inertia
segment_1 = Beam(2, E, 1.5 * I)
segment_2 = Beam(2, E, I)

# Join the segments fixed end-to-end to create a 4m composite beam
b3 = segment_1.join(segment_2, via="fixed")

# Apply boundary conditions using the auto-generating apply_support method
b3.apply_support(0, type="fixed")

# Apply the downward load at the free end (total length = 4)
b3.apply_load(20, 4, -1)

# Solve for the reactions (no arguments needed because apply_support was used)
b3.solve_for_reaction_loads()

print("Example 3 Reactions Dictionary:")
print(b3.reaction_loads)

# Plot the deflection directly if desired
# p = b3.plot_deflection(subs={E: 2e11, I: 1e-4})
