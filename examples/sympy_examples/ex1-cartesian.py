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
# upward and clockwise positive

# %% params
params={
'L': 9.0,  # Length of beam (m)
# a= 5.0   # Position of point load (m)
'A': 0.01,  # Area (m^2)
'P': -12 ,  # Magnitude of point load (N)
'E': 210000,  # Young's modulus (Pa) - typical for steel
'G': 81000,  # Shear modulus (Pa) - typical for steel
'Iy': 1e-4 ,  # Moment of inertia (m^4)
'Iz': 1e-4 ,  # Moment of inertia (m^4)
    'J': 1e-4 ,  # Moment of inertia (m^4)
    'nu': 0.3,  # Poisson
    'rho': 8750
}

# %%
import numpy as np
import sympy as sp
from sympy.physics.continuum_mechanics.beam import Beam

from sympy import symbols

# down is positive force and clockwise is positive moment
# E, I = symbols('E, I', nonneg=True)


b1 = Beam(params['L'], params['E'], params['I'])

b1.apply_load(params['P'], params['L'], -1)
# b1.apply_load(8, 0, 0, end=5)
# b1.apply_load(50, 5, -2)
print(b1.load)

# b1.bc_deflection.append((0, 0))
# b1.bc_slope.append((0, 0))

# help(b1.apply_support)
p0, m0 = b1.apply_support(0, type='fixed')
print(p0, m0)

b1.boundary_conditions
# %%

# Pass those variables into the solver!
b1.solve_for_reaction_loads(p0,m0)
# %%
print(b1.applied_loads)

print("Reaction Loads:", b1.reaction_loads)
# reactions = list(b1.reaction_loads.keys())
# %%
# Force the notebook to render the plot
plot_object = b1.draw()
plot_object.show()

# %%
shear_curve = b1.shear_force()
print("Example 1 Shear Force:", shear_curve)
piecewise_shear = shear_curve.rewrite(sp.Piecewise)
clean_shear = sp.simplify(piecewise_shear)
b1.plot_shear_force()
# %%
moment_curve = b1.bending_moment()

piecewise_moment = moment_curve.rewrite(sp.Piecewise)
clean_moment = sp.simplify(piecewise_moment)

print("Piecewise Bending Moment:")
sp.pprint(clean_moment)

print("Example 1 Bending Moment:", moment_curve)
b1.plot_bending_moment()

# %%
print("Example 1 Reactions:", b1.reaction_loads)
print("Example 1 Load:", b1.load)

print("Example 1 Bending Moment:", b1.bending_moment())
print("Example 1 Deflection:", b1.deflection())
# b1.plot_shear_force()
# b1.plot_bending_moment()

# %%

b1.plot_loading_results(params)

# endregion

## region FEA
#%%
# from Pynite import FEModel3D
# beam1 = FEModel3D()
#
# # help(beam1.add_material)
#
# beam1.add_material('Steel', params['E'], params['G'], params['nu'], params['rho'])
# print(beam1.materials)
# # Add Section (m^2, m^4)
# beam1.add_section('MySection', params['A'], params['Iy'], params['Iz'], params['J'])
#
#
# beam1.add_node('N1', 0, 0, 0)
# beam1.add_node('N2', params['L'], 0, 0)
# beam1.add_member('M1', 'N1', 'N2', 'Steel', 'MySection')
# # Provide fixed-pinned supports
# # help(beam1.def_support)
# beam1.def_support('N1', True, True, True, False, True, False)
# beam1.def_support('N2', False, True, False, False, False, False)
# beam1.add_member_pt_load('M1', 'Fy', -12*1e3, params['L'], 'D')
#
# # Add load combinations
# beam1.add_load_combo('1D', {'D':1})
#
# # beam_si.add_member_pt_load('M1', 'Fy', P_N, loc_m, '1D')
#
# # %% Analyze the model
# beam1.analyze(check_statics=True)
#
#
# # %% Print reactions at each end of the beam
# print(f"Left Support Reaction: {beam1.nodes['N1'].RxnFY['1D']:.3f} N")
# print(f"Right Support Reacton: {beam1.nodes['N2'].RxnFY['1D']:.3f} N")
#
# # %% Print the max/min shears and moments in the beam
# print(f"Maximum Shear: {beam1.members['M1'].max_shear('Fy', '1D'):.3f} kN")
# print(f"Minimum Shear: {beam1.members['M1'].min_shear('Fy', '1D'):.3f} kN")
# print(f"Maximum Moment: {beam1.members['M1'].max_moment('Mz', '1D'):.3f} kN·m")
# print(f"Minimum Moment: {beam1.members['M1'].min_moment('Mz', '1D'):.3f} kN·m")
#
# # Print the max/min deflections in the beam
# print(f"Maximum Deflection: {beam1.members['M1'].max_deflection('dy', '1D'):.3f} m")
# print(f"Minimum Deflection: {beam1.members['M1'].min_deflection('dy', '1D'):.3f} m")
# #%%
# beam1.members['M1'].plot_shear('Fy', '1D')
# beam1.members['M1'].plot_moment('Mz', '1D')
# beam1.members['M1'].plot_deflection('dy', '1D')
#
# # endreggion