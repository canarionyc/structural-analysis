#%% setup
import sympy as sp
from sympy.physics.continuum_mechanics.beam import Beam
import json5


#&& 1. Parameter Initialization (from JSON)

# Assuming you are running this from a directory where the json is accessible
try:
    with open("../data/AISC_W10x54_wide_flange_steel_section_torsional_lateral_params.json", "r") as f:
        params_dict = json5.load(f)
except FileNotFoundError:
    # Fallback dictionary so the script runs regardless
    params_dict = {
        'L': 300, 'E': 29000, 'G': 11200, 'Iy': 103, 'JT': 1.51,
        'F': 5, 'T': 61.2
    }


#%% 2. Symbolic Setup
from sympy.core import S, Symbol, diff, symbols
from sympy.core.add import Add
from sympy.core.expr import Expr
from sympy.core.function import (Derivative, Function)
from sympy.core.mul import Mul
from sympy.core.relational import Eq
from sympy.core.sympify import sympify
from sympy.solvers import linsolve
from sympy.solvers.ode.ode import dsolve
from sympy.solvers.solvers import solve
from sympy.printing import sstr
from sympy.functions import SingularityFunction, Piecewise, factorial
from sympy.integrals import integrate
from sympy.series import limit
from sympy.plotting import plot, PlotGrid
from sympy.geometry.entity import GeometryEntity
from sympy.external import import_module
from sympy.sets.sets import Interval
from sympy.utilities.lambdify import lambdify
from sympy.utilities.decorator import doctest_depends_on
from sympy.utilities.iterables import iterable
import warnings


# Define the symbols we need
L, E, G, Iy, JT, F, T, x = sp.symbols('L E G Iy JT F T x', positive=True)

# Map our JSON values to the symbolic parameters for later substitution
param_subs = {
    L: params_dict['L'], E: params_dict['E'], G: params_dict['G'], 
    Iy: params_dict['Iy'], JT: params_dict['JT'], 
    F: params_dict['F'], T: params_dict['T']
}



# region lateral bending
#%% 3. CASE A: Pure Lateral Bending (Euler-Bernoulli)
print("--- CASE A: LATERAL BENDING (CANTILEVER) ---")
# Create a SymPy Beam object (Length, Young's Modulus, Moment of Inertia)
# We use Iy because the lateral load acts on the minor axis
lateral_beam = Beam(L, E, Iy)

# Define Boundary Conditions: Fixed at x = 0 (Deflection = 0, Slope = 0)
R0, M0 = lateral_beam.apply_support(0, type='fixed')

# Apply point load F at the free end (x = L). 
# The '-1' indicates a point load in SymPy's singularity function syntax
lateral_beam.apply_load(-F, L, -1) 
print(f"Applied Load: { lateral_beam.applied_loads }")

# print(lateral_beam._support_as_loads)
# Solve for the reaction forces at the fixed support
# R_0, M_0 = sp.symbols('R_0 M_0')

# help(help)
# help(tuple)
reactions = (R0, M0)

# x = lateral_beam.variable
l = lateral_beam.length
C3 = Symbol('C3')
C4 = Symbol('C4')
rotation_jumps = tuple(lateral_beam._rotation_hinge_symbols)
print("rotation_jumps", rotation_jumps)
deflection_jumps = tuple(lateral_beam._sliding_hinge_symbols)
print("deflection_jumps", deflection_jumps)

print("shear_force:", lateral_beam.shear_force())
shear_curve = limit(lateral_beam.shear_force(), x, l)
print(shear_curve)

print("bending_moment:", lateral_beam.bending_moment())
moment_curve = limit(lateral_beam.bending_moment(), x, l)
print(moment_curve)

#%% shear force equations
shear_force_eqs = []
print(lateral_beam._boundary_conditions['shear_force'])

for position, value in lateral_beam._boundary_conditions['shear_force']:
    eqs = lateral_beam.shear_force().subs(x, position) - value
    new_eqs = sum(arg for arg in eqs.args if not any(num.is_infinite for num in arg.args))
    shear_force_eqs.append(new_eqs)
print("shear_force_eqs:", shear_force_eqs)

#%% bending moment eqs
print(lateral_beam._boundary_conditions['bending_moment'])
bending_moment_eqs = []
for position, value in lateral_beam._boundary_conditions['bending_moment']:
    eqs = lateral_beam.bending_moment().subs(x, position) - value
    new_eqs = sum(arg for arg in eqs.args if not any(num.is_infinite for num in arg.args))
    bending_moment_eqs.append(new_eqs)
print("bending_moment_eqs:", bending_moment_eqs)

#%% slope equations
slope_eqs = []
slope_curve = integrate(lateral_beam.bending_moment(), x) + C3
print("slope_curve:",slope_curve)
print(lateral_beam._boundary_conditions['slope'])
for position, value in lateral_beam._boundary_conditions['slope']:
    eqs = slope_curve.subs(x, position) - value
    slope_eqs.append(eqs)
print("slope_eqs:", slope_eqs)

#%% deflection equations
deflection_eqs = []
deflection_curve = integrate(slope_curve, x) + C4
print("deflection_curve:", deflection_curve)
print(lateral_beam._boundary_conditions['deflection'])
for position, value in lateral_beam._boundary_conditions['deflection']:
    eqs = deflection_curve.subs(x, position) - value
    deflection_eqs.append(eqs)
print("deflection_eqs:", deflection_eqs)

#%% solution
print((C3, C4) + reactions + rotation_jumps + deflection_jumps)
solution = list((linsolve([shear_curve, moment_curve] + shear_force_eqs + bending_moment_eqs + slope_eqs
                          + deflection_eqs, (C3, C4) + reactions + rotation_jumps + deflection_jumps).args)[0])
print(solution)

reaction_index = 2 + len(reactions)
rotation_index = reaction_index + len(rotation_jumps)
reaction_solution = solution[2:reaction_index]
print("reaction_solution:", reaction_solution)

rotation_solution = solution[reaction_index:rotation_index]
print("rotation_solution:", rotation_solution)

deflection_solution = solution[rotation_index:]
print("deflection_solution:", deflection_solution)

lateral_beam._reaction_loads = dict(zip(reactions, reaction_solution))
print("reaction_loads:", lateral_beam.reaction_loads)

lateral_beam._rotation_jumps = dict(zip(rotation_jumps, rotation_solution))
print("rotation_jumps:", lateral_beam._rotation_jumps)

lateral_beam._deflection_jumps = dict(zip(deflection_jumps, deflection_solution))
print("deflection_jumps:", lateral_beam._deflection_jumps)

lateral_beam._load = lateral_beam._load.subs(lateral_beam._reaction_loads)
lateral_beam._load = lateral_beam._load.subs(lateral_beam._rotation_jumps)
lateral_beam._load = lateral_beam._load.subs(lateral_beam._deflection_jumps)

# lateral_beam.solve_for_reaction_loads(R0, M0)
print(lateral_beam.reaction_loads.keys())
# %% Get the symbolic expression for maximum deflection (at x = L)
# Deflection is natively negative (downward), so we take absolute value
max_deflection_expr = sp.Abs(lateral_beam.deflection().subs(x, L))

print(f"Symbolic Max Bending Deflection: {sp.simplify(max_deflection_expr)}")

# Evaluate numerically
max_lat_def_val = max_deflection_expr.subs(param_subs).evalf()
print(f"Numerical Max Bending Deflection: {max_lat_def_val:.4f} inches\n")

# endregion

# region axial torsional lateral beam

# 4. CASE B: Pure Axial Torsion (St. Venant)

print("--- CASE B: PURE AXIAL TORSION ---")
# Because we are ignoring warping (Cw = 0), the twist is uniformly resisted 
# entirely by the St. Venant torsional stiffness (G * JT).
# Formula: Angle of twist = (Torque * Length) / (Shear Modulus * Torsional Constant)

# Symbolic equation for max twist at the free end
max_twist_expr = (T * L) / (G * JT)

print(f"Symbolic Max Twist Angle (radians): {max_twist_expr}")

# Evaluate numerically
max_twist_rad = max_twist_expr.subs(param_subs).evalf()

# Convert radians to degrees for readability
max_twist_deg = max_twist_rad * (180 / sp.pi)
max_twist_deg_val = max_twist_deg.evalf()

print(f"Numerical Max Twist Angle: {max_twist_rad:.5f} rad ({max_twist_deg_val:.4f} degrees)")

# endregion