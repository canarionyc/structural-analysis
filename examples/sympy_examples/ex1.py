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

# %%
# %matplotlib inline


# %%
# region Example 1: Cantilever Beam with Distributed Load, Moment, and Point Load
# downward and counterclockwise positive

# %%
import numpy as np
import sympy as sp
from sympy.physics.continuum_mechanics.beam import Beam

from sympy import symbols

# down is positive force and clockwise is positive moment
E, I = symbols('E, I', nonneg=True)

b1 = Beam(9, E, I)

b1.apply_load(12, 9, -1)
# b1.apply_load(8, 0, 0, end=5)
# b1.apply_load(50, 5, -2)
print(b1.load)

# b1.bc_deflection.append((0, 0))
# b1.bc_slope.append((0, 0))

# help(b1.apply_support)
p0, m0 = b1.apply_support(0, type='fixed')
print(p0, m0)
# %%
b1.boundary_conditions

# Pass those variables into the solver!
b1.solve_for_reaction_loads(p0,m0)
# %%
b1.applied_loads

print("Reaction Loads:", b1.reaction_loads)
# reactions = list(b1.reaction_loads.keys())
# %%
# Force the notebook to render the plot
plot_object = b1.draw()
plot_object.show()

# %%
b1.shear_force()
b1.plot_shear_force()
# %%
b1.bending_moment()
b1.plot_bending_moment()

# %%
print("Example 1 Reactions:", b1.reaction_loads)
print("Example 1 Load:", b1.load)

print("Example 1 Bending Moment:", b1.bending_moment())
print("Example 1 Deflection:", b1.deflection())
# b1.plot_shear_force()
# b1.plot_bending_moment()

# %%
# 1. DO NOT convert the raw load curve (b1.load)
# Instead, extract the continuous Shear or Moment curves
shear_curve = b1.shear_force()
print("Example 1 Shear Force:", shear_curve)
moment_curve = b1.bending_moment()
print("Example 1 Bending Moment:", moment_curve)

# 2. Convert them safely to Piecewise
piecewise_shear = shear_curve.rewrite(sp.Piecewise)
piecewise_moment = moment_curve.rewrite(sp.Piecewise)

# 3. Simplify the result to group the intervals cleanly
clean_shear = sp.simplify(piecewise_shear)
clean_moment = sp.simplify(piecewise_moment)

print("Piecewise Bending Moment:")
sp.pprint(clean_moment)

# %%
params={
	# L: 10.0,  # Length of beam (m)
	# a: 4.0,   # Position of point load (m)
	# b: 6.0,
	# P: 1e3,   # Magnitude of point load (N)
	E: 2e11,  # Young's modulus (Pa) - typical for steel
	I: 1e-4   # Moment of inertia (m^4)
}

b1.plot_loading_results(params)

# endregion
