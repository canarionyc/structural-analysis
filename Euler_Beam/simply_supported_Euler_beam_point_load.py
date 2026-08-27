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
# # Simply supported Euler Beam under Point Load
# %% [markdown]
# Analysis of a simply supported beam with a point load using symbolic computation.
# This script demonstrates the derivation of beam deflection and slope formulas.
# %%
# Import common structural analysis functionality

import sympy as sp
from sympy import Dict, simplify, lambdify

# help(assumptions)
# help(assuming)

# Configure sympy for better output
sp.init_printing(order='lex')
# %%
x = sp.symbols('x', nonnegative=True)
L, b = sp.symbols('L b', positive=True)

print(L.is_positive)

# Material properties
E, G, nu = sp.symbols('E G nu', positive=True)  # Young's modulus, shear modulus, Poisson's ratio

# Section properties
I, A, J = sp.symbols('I A J', positive=True)  # Moment of inertia, area, torsional constant

# Loads and reactions
P, q, M = sp.symbols('P q M', real=True)  # Point load, distributed load, moment
R_0, R_L= sp.symbols('R_0 R_L', real=True)  # Reactions
# %%
# os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__name__))))
# from autoimport import import_all
# import_all()

L_val=10

# %%
# print("=== Euler Beam Point Load Analysis ===")
# print("Analyzing a simply supported beam with point load P at distance 'a' from left support")
#
# # Create constraint that enforces a <= L
# constraint = sp.Le(a, L)
# print(f"Constraint: {constraint}")
#
# # Define the relationship b = L - a
# b_relation = sp.Eq(b, L - a)
# print(f"Relationship: {b_relation}")
# %%
print("\n=== Reaction Analysis ===")

# help(sp.solve)
# 1. Use dict=True to guarantee a list of dictionaries
soln = sp.solve([
    R_0 + R_L - P,
    R_L * L - P * b
], [R_0, R_L], dict=True)

reaction_solns = soln[0]

# 2. Extract the first (and only) solution and cast it to a SymPy Dict
reaction_solns = Dict(soln[0])
print(reaction_solns)

help(simplify)
help(sp.together)
reaction_solns[R_0] = reaction_solns[R_0].simplify()
reaction_solns[R_L] = reaction_solns[R_L].simplify()
print(f"Reaction at A: R_0 = {reaction_solns[R_0]}")
print(f"Reaction at B: R_L = {reaction_solns[R_L]}")

# %% reactions_vals
import os
import json5
params_si_json =os.path.join("data", "params_si.json")

import importlib
# help(importlib)
from test_python_package.utils import particularize

# help(importlib.reload)
importlib.reload(particularize)
replace = particularize.replace
# help(replace)

with open(params_si_json,"r") as f:
    params=json5.load(f)

reaction_vals=replace(reaction_solns,params)
print(reaction_vals)
# %%
print("\n=== Moment Functions ===")

# For 0 <= x < a: M(x) = R_A * x
M1 = R_0 * x
M1=M1.subs(reaction_solns)
print(f"Moment for 0 ≤ x < a: M1(x) = {M1}")

# For a <= x <= L: M(x) = R_A * x - P * (x - a)
M2 = R_0 * x - P * (x - b)
M2=M2.subs(reaction_solns)
print(f"Moment for a ≤ x ≤ L: M2(x) = {M2}")
M2=simplify(M2)


assert M2-P*b*(L - x)/L==0

#
# x_vals=np.linspace(0,L_val,10)
# M1_vals=M1_func(x_vals)
print(M1.free_symbols)

M1_x=replace(M1,params)
M2_x=replace(M2,params)

M1_func=lambdify(x, M1_x)
M2_func=lambdify(x, M2_x)

# sp.plot(M1_x, (x, 0, params['b']))
# sp.plot(M2_x, (x, params['b'], params['L']))

M_x=sp.Piecewise((M1_x, x < params['b']), (M2_x, x >= params['b']))
sp.plot(M_x, (x, 0, params['L']))
# %%
print("\n=== Integration for Slope  ===")

# Define integration constants
C1, C2 = sp.symbols('C1 C2', real=True )

# Integrate EI * v''(x) = M(x) to get slope
# For 0 <= x < a
v1_prime = sp.integrate(M1 / (E * I), x) + C1
print(f"Slope v1'(x) = {v1_prime}")
v1_prime.together()

# For a <= x <= L
v2_prime = sp.integrate(M2 / (E * I), x) + C2
v2_prime.together()
print(f"Slope v2'(x) = {v2_prime}")

help(sp.integrate)


v_prime_x=replace(M_x / (E * I),params)

v_x=sp.integrate(v_prime_x, x)+sp.symbols('C3')
print(v_x)

# sp.plot(v_x, (x, 0, params['L']))

total_deflection=sp.integrate(v_prime_x, (x, 0, params['L']))
print(f"Total deflection = {total_deflection}")
# %%
print("\n=== Integration of Slope for Deflection ===")
C3, C4 = sp.symbols('C3 C4', real=True)
v1 = sp.integrate(v1_prime, x) + C3
v2 = sp.integrate(v2_prime, x) + C4

print(f"Deflection v1(x) = {v1}")
print(f"Deflection v2(x) = {v2}")

# %%
print("\n=== Boundary Conditions ===")

# Boundary conditions:
# 1. v(0) = 0 (simply supported at A)
# 2. v(L) = 0 (simply supported at B)
# 3. v1(a) = v2(a) (continuity of deflection)
# 4. v1'(a) = v2'(a) (continuity of slope)

eqs = [
    v1.subs(x, 0),  # v(0) = 0
    v2.subs(x, L),  # v(L) = 0
    sp.simplify(v1.subs(x, b) - v2.subs(x, b)),  # continuity at x=a
    sp.simplify(v1_prime.subs(x, b) - v2_prime.subs(x, b))  # slope continuity at x=a
]

print("Boundary condition equations:")
for i, eq in enumerate(eqs, 1):
    print(f"{i}. {eq} = 0")

# %%
print("\n=== Solving for Integration Constants ===")

soln = sp.solve(eqs, (C1, C2, C3, C4), dict=True)[0]
# sp.pprint(soln)
print("Solution found:")
for const, value in soln.items():
    print(f"{const} = {value}")

# %%


v1_prime=v1_prime.subs(soln).together()
v2_prime=v2_prime.subs(soln).together()
v1_prime_x=replace(v1_prime,params)
v2_prime_x=replace(v2_prime,params)

v_prime_x = sp.Piecewise((v1_prime_x, x < params['b']), (v2_prime_x, x >= params['b']))
sp.plot(v_prime_x, (x, 0, params['L']), title="Slope v'(x)", ylabel="Slope")

help(sp.solve)
#%%
from sympy import solveset, Interval

# help(sp.substitution)


sp.plot(v_prime_x, (x, 0, 10))
# Solve the piecewise expression explicitly within the Interval (-oo, 10)

help(Interval)
Interval(0,params['L'])
help(solveset)
v_prime_soln = solveset(v_prime_x, x, domain=Interval(0,params['L']))
print(v_prime_soln)
# 1. Convert the FiniteSet to a standard Python list
soln_list = list(v_prime_soln)

# 2. Extract the value you want (assuming you just want the first/only solution here)
extracted_val = soln_list[0]

# 3. Substitute the extracted numerical value into your Piecewise function
result = v_x.subs(x, extracted_val)

print(result) # maximum deflection

#help(sp.FiniteSet)

print(v_x)

# solveset(v1_prime, x, domain=Interval(0,L))

# %%
print("\n=== Slope at Left End ===")

# theta_A=sp.integrate(v_prime_x, (x, 0, params['L']))
# print(f"θ_A (slope at left end) = {theta_A}")
# The slope at the left end (x=0) is given by v1_prime_x evaluated at x=0
# Slope at left end (x=0)
theta_A_val = v1_prime_x.subs(x, 0).simplify()
print(f"θ_A (slope at left end) = {theta_A_val}")


# %%
theta_A_formula = -P * b * (L - b) * (2 * L - b) / (6 * E * I * L)
print(f"\nCompare to formula: P*a*b*(L+b)/(6*E*I*L)")
print(f"Formula gives: {theta_A_formula}")

theta_A_formula_val=replace(theta_A_formula,params)



# Check if they're equal
difference = theta_A_val - theta_A_formula_val
print(f"Difference: {difference}")
print(f"Proof correct: {difference == 0}")

print("\n=== Analysis Complete ===")

# %%
print("\n=== Deflection  ===")


#%%
v1=v1.subs(soln).together()
v2=v2.subs(soln).together()

v1_x=replace(v1,params)
v2_x=replace(v2,params)

v_x=sp.Piecewise((v1_x, x < params['b']), (v2_x, x >= params['b']))
sp.plot(v_x, (x, 0, params['L']), title="Deflection v(x)", ylabel="Deflection")