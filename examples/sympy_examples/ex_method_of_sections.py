#%%
import numpy as np
import matplotlib.pyplot as plt

import sympy as sp

#%% 1. Teach Global Equilibrium
R_A, R_B = sp.symbols('R_A R_B', real=True)

# Sum of forces in Y = 0
eq_Fy = sp.Eq(R_A + R_B - 1000, 0) 
# Sum of Moments about A = 0 (Assuming 10m beam, load at 5m)
eq_Ma = sp.Eq(R_B * 10 - 1000 * 5, 0)

reactions = sp.solve((eq_Fy, eq_Ma), (R_A, R_B))
print(f"Step 1: Solve Equilibrium: {reactions}")

#%% 2. Teach Method of Sections (Cut 1: 0 < x < 5)
x = sp.symbols('x', real=True)
V1, M1 = sp.symbols('V1 M1', real=True)

# Equilibrium of the left cut
eq_cut1_Fy = sp.Eq(reactions[R_A] - V1, 0)
eq_cut1_M  = sp.Eq(reactions[R_A]*x - M1, 0)

V1=sp.solve(eq_cut1_Fy)[0]
print(V1)

import sympy.solvers.solvers
help(sp.solve)
help(sympy.solvers.solvers.solve)
M1=sp.solve(eq_cut1_M, M1)[0]
print(f"Step 2: Section 1 (0 < x < 5): V = {V1}, M = {M1}")

#%% 3. Teach Method of Sections (Cut 2: 5 < x < 10)

V2, M2 = sp.symbols('V2 M2', real=True)

# Equilibrium of the right
eq_cut2_Fy = sp.Eq(reactions[R_A] - 1000 -V2 , 0)
eq_cut2_M  = sp.Eq(reactions[R_A]*x - 1000*(x - 5) - M2, 0)

cut2_soln=sp.solve((eq_cut2_Fy, eq_cut2_M), (V2, M2))
V2=cut2_soln[V2]
M2=cut2_soln[M2]
print(V2)
print(M2)
print(f"Step 3: Section 2 (5 < x < 10): V = {V2}, M = {M2}")

#%%
from sympy.functions.elementary.piecewise import Piecewise

help(Piecewise)

#help(sp.functions.elementary)

shear_force = sp.Piecewise( (V1, x < 5), (V2, x > 5))
print(shear_force)

bending_moment = sp.Piecewise( (M1, x < 5), (M2, x > 5))
print(bending_moment)

print(f"Shear Force: {shear_force}")
print(f"Bending Moment: {bending_moment}")
#%%
shear_func = sp.lambdify(x, shear_force, modules='numpy')
bending_func = sp.lambdify(x, bending_moment, modules='numpy')

x_vals = np.linspace(0, 10, 100)
shear_vals = shear_func(x_vals)
bending_vals = bending_func(x_vals)

fig, ax = plt.subplots(2,1  , figsize=(10, 8))
ax[0].plot(x_vals, shear_vals)
ax[0].set_title('Shear Force Diagram')
ax[0].set_xlabel('Position along the beam (m)')
ax[0].set_ylabel('Shear Force (N)')
ax[1].plot(x_vals, bending_vals)
ax[1].set_title('Bending Moment Diagram')
ax[1].set_xlabel('Position along the beam (m)')
ax[1].set_ylabel('Bending Moment (N*m)')
plt.tight_layout()
plt.show()

#%% deflection
# from sympy.integrals.integrals import Integral
EI = sp.symbols('EI', positive=True)

help(sp.Integral)
bending_moment_calc=sp.integrate(shear_force, x)

slope_calc=sp.integrate(bending_moment, x)
slope_func = sp.lambdify(x, slope_calc, modules='numpy')

slope_vals=slope_func(x_vals)

deflection_calc=sp.integrate(slope_calc, x)
deflection_func = sp.lambdify(x, deflection_calc, modules='numpy')

deflection_vals=deflection_func(x_vals)

import pandas as pd

df = pd.DataFrame({
    'x': x_vals,
    'deflection': deflection_vals
})