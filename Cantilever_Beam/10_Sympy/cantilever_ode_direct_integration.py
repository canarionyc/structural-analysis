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
# # Cantilever Beam: Direct ODE Integration using SymPy
#
# This notebook solves the Euler-Bernoulli beam differential equations directly using
# pure SymPy integration and ODE solvers, without relying on `sympy.physics.continuum_mechanics`.
#
# ## Sign Conventions (Standard Cartesian / Structural Mechanics)
# * **Coordinate System:**
#   * $x$: along the beam axis ($x = 0$ at clamped root, $x = L$ at free tip).
#   * $y$: vertical axis, **positive upwards** ($\uparrow$).
# * **Kinematics:**
#   * Deflection $v(x)$: **positive upwards** ($\uparrow$). Downward sag is $v(x) < 0$.
#   * Slope / Rotation $\theta(x) = \frac{dv}{dx}$: **positive counter-clockwise** ($\circlearrowleft$).
#     A downward-sloping beam has $\theta(x) < 0$ (**clockwise** $\circlearrowright$).
# * **Applied Loads:**
#   * Distributed load $q(x)$: **positive upwards** ($\uparrow$). Gravity/downward load is $q < 0$.
#   * Concentrated tip load $P$: **positive upwards** ($\uparrow$). Downward tip load is $P < 0$.
#   * Applied tip moment $M_{\text{tip}}$: **positive counter-clockwise** ($\circlearrowleft$).
# * **Internal Force Relations:**
#   1. $\frac{d V}{dx} = q(x)$   (Load - Shear relation)
#   2. $\frac{d M}{dx} = V(x)$   (Shear - Moment relation)
#   3. $\frac{d \theta}{dx} = \frac{M(x)}{E I}$ (Moment - Curvature relation: $M > 0$ is sagging / smiley face)
#   4. $\frac{d v}{dx} = \theta(x)$ (Rotation - Deflection relation)
#
# Combined 4th-order ODE:
# $$E I \frac{d^4 v}{dx^4} = q(x)$$

# %%
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

try:
    from IPython.display import display
except ImportError:
    display = sp.pprint

# Pretty-print mathematical symbols in output
sp.init_printing(use_unicode=True)

# %% [markdown]
# ## 1. Fully Symbolic Analytical Solution
# We define symbolic parameters and solve for constants of integration $C_1, C_2, C_3, C_4$.

# %%
# Define symbolic variables
x, L, E, I = sp.symbols('x L E I', positive=True)
q = sp.symbols('q', real=True)         # Uniform distributed load (positive upward)
P = sp.symbols('P', real=True)         # Concentrated tip load at x = L (positive upward)
M_tip = sp.symbols('M_tip', real=True) # Concentrated moment at x = L (counter-clockwise)

# Integration constants
C1, C2, C3, C4 = sp.symbols('C1 C2 C3 C4', real=True)

# 1. Shear force: dV/dx = q(x)  =>  V(x) = integrate(q, x) + C1
V_sym = q * x + C1

# 2. Bending moment: dM/dx = V  =>  M(x) = integrate(V, x) + C2
M_sym = sp.integrate(V_sym, x) + C2

# 3. Slope / Rotation: d(theta)/dx = M / (EI)  =>  theta(x) = integrate(M / (EI), x) + C3
theta_sym = sp.integrate(M_sym / (E * I), x) + C3

# 4. Deflection: dv/dx = theta  =>  v(x) = integrate(theta, x) + C4
v_sym = sp.integrate(theta_sym, x) + C4

print("Indefinite forms with constants:")
display(sp.Eq(sp.Symbol('V(x)'), V_sym))
display(sp.Eq(sp.Symbol('M(x)'), M_sym))
display(sp.Eq(sp.Symbol('theta(x)'), theta_sym))
display(sp.Eq(sp.Symbol('v(x)'), v_sym))

# %% [markdown]
# ### Boundary Conditions for a Cantilever Beam
# For a cantilever clamped at $x = 0$ and free at $x = L$:
#
# * **At clamped root ($x = 0$):**
#   * Deflection is zero: $v(0) = 0$
#   * Slope is zero: $\theta(0) = 0$
#
# * **At free tip ($x = L$):**
#   * On a $+x$ cut face, internal shear acts downward ($-V(L)$) and internal moment acts CCW ($+M(L)$).
#   * Equilibrium with upward force $P$ and CCW moment $M_{\text{tip}}$:
#     $$V(L) = -P, \quad M(L) = M_{\text{tip}}$$

# %%
# Set up system of boundary condition equations
bcs = [
    sp.Eq(v_sym.subs(x, 0), 0),
    sp.Eq(theta_sym.subs(x, 0), 0),
    sp.Eq(M_sym.subs(x, L), M_tip),
    sp.Eq(V_sym.subs(x, L), -P)
]

# Solve for the 4 integration constants
constants_sol = sp.solve(bcs, (C1, C2, C3, C4))
print("Solved Integration Constants:")
for const, val in constants_sol.items():
    print(f"  {const} = {val}")

# Substitute constants back into expressions
V_final = sp.simplify(V_sym.subs(constants_sol))
M_final = sp.simplify(M_sym.subs(constants_sol))
theta_final = sp.simplify(theta_sym.subs(constants_sol))
v_final = sp.simplify(v_sym.subs(constants_sol))

print("\n--- Final Analytical Expressions ---")
print("Shear V(x):")
display(V_final)
print("Moment M(x):")
display(M_final)
print("Rotation theta(x):")
display(theta_final)
print("Deflection v(x):")
display(v_final)

# %% [markdown]
# ### Support Reactions at Clamped Root ($x = 0$)
# The external reaction force $R_0$ (positive upward $\uparrow$) and clamping moment $M_0$ (positive CCW $\circlearrowleft$)
# exerted by the wall on the beam:
#
# * **Vertical Force Equilibrium:** $R_0 + \int_0^L q(x)\,dx + P = 0 \implies R_0 = V(0) = -L q - P$
# * **Moment Equilibrium about $x = 0$:** $M_0 + \int_0^L q(x) x\,dx + P L + M_{\text{tip}} = 0 \implies M_0 = -M(0)$

# %%
R_0 = V_final.subs(x, 0)     # Vertical reaction force (positive upward)
M_0 = -M_final.subs(x, 0)    # Clamping reaction moment (positive CCW)

print("Vertical Reaction Force R_0 at x=0 (positive upward):")
display(R_0)
print("Reaction Clamping Moment M_0 at x=0 (positive CCW):")
display(M_0)

# Tip deflection (x = L)
v_tip = sp.simplify(v_final.subs(x, L))
print("Tip Deflection v(L):")
display(v_tip)

# %% [markdown]
# ## 2. Alternative Method: Using `sp.dsolve` on the 4th-Order ODE
# We can also solve the boundary value problem directly in one shot with `sp.dsolve`:

# %%
w = sp.Function('w')
ode_4th = sp.Eq(E * I * w(x).diff(x, 4), q)

# Solve with boundary conditions
ics_dict = {
    w(0): 0,
    w(x).diff(x).subs(x, 0): 0,
    w(x).diff(x, 2).subs(x, L): M_tip / (E * I),
    w(x).diff(x, 3).subs(x, L): -P / (E * I)
}

dsolve_sol = sp.dsolve(ode_4th, w(x), ics=ics_dict)
print("Solution from sp.dsolve:")
display(sp.simplify(dsolve_sol.rhs))

# Verify equivalence with direct integration
assert sp.simplify(dsolve_sol.rhs - v_final) == 0
print("Verification passed: dsolve solution matches direct integration exactly.")

# %% [markdown]
# ## 3. Numerical Evaluation & Engineering Diagram Plots
# Let us substitute realistic structural parameters (e.g., steel cantilever beam).

# %%
# Define numerical parameter dictionary
params_num = {
    L: 9.0,          # Beam length in meters
    E: 210e9,        # Young's modulus (Pa = N/m^2 for structural steel)
    I: 1e-4,         # Second moment of area Iz (m^4)
    q: -2500.0,      # Distributed self-weight/dead load: -2.5 kN/m (downward)
    P: -12000.0,     # Point load at tip: -12 kN (downward)
    M_tip: 0.0       # Tip moment: 0 N*m
}

# Evaluate symbolic functions numerically
V_num = sp.lambdify(x, V_final.subs(params_num), 'numpy')
M_num = sp.lambdify(x, M_final.subs(params_num), 'numpy')
theta_num = sp.lambdify(x, theta_final.subs(params_num), 'numpy')
v_num = sp.lambdify(x, v_final.subs(params_num), 'numpy')

L_val = params_num[L]
x_vals = np.linspace(0, L_val, 500)

V_vals = np.broadcast_to(V_num(x_vals), x_vals.shape).astype(float)
M_vals = np.broadcast_to(M_num(x_vals), x_vals.shape).astype(float)
theta_vals = np.broadcast_to(theta_num(x_vals), x_vals.shape).astype(float)
v_vals = np.broadcast_to(v_num(x_vals), x_vals.shape).astype(float) * 1e3  # Convert deflection to mm

# Print key engineering values
print(f"Reaction Force R_0:     {float(R_0.subs(params_num))/1e3:10.2f} kN")
print(f"Reaction Moment M_0:    {float(M_0.subs(params_num))/1e3:10.2f} kN*m")
print(f"Max Tip Deflection:     {v_vals[-1]:10.2f} mm")
print(f"Max Tip Slope:          {theta_vals[-1]*1e3:10.4f} mrad")

# %%
# Plot Shear, Moment, Slope, and Deflection diagrams
fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

# 1. Shear Force Diagram
axes[0].plot(x_vals, V_vals / 1e3, color='#1f77b4', lw=2)
axes[0].fill_between(x_vals, 0, V_vals / 1e3, color='#1f77b4', alpha=0.15)
axes[0].set_ylabel('Shear $V(x)$ [kN]')
axes[0].grid(True, linestyle='--', alpha=0.6)
axes[0].set_title('Cantilever Beam Analysis (Direct SymPy Integration)', fontsize=14, fontweight='bold')

# 2. Bending Moment Diagram
axes[1].plot(x_vals, M_vals / 1e3, color='#d62728', lw=2)
axes[1].fill_between(x_vals, 0, M_vals / 1e3, color='#d62728', alpha=0.15)
axes[1].set_ylabel('Moment $M(x)$ [kN·m]')
axes[1].grid(True, linestyle='--', alpha=0.6)

# 3. Slope / Rotation Diagram
axes[2].plot(x_vals, theta_vals * 1e3, color='#2ca02c', lw=2)
axes[2].fill_between(x_vals, 0, theta_vals * 1e3, color='#2ca02c', alpha=0.15)
axes[2].set_ylabel('Slope $\\theta(x)$ [mrad]')
axes[2].grid(True, linestyle='--', alpha=0.6)

# 4. Deflection Diagram
axes[3].plot(x_vals, v_vals, color='#9467bd', lw=2.5)
axes[3].fill_between(x_vals, 0, v_vals, color='#9467bd', alpha=0.15)
axes[3].set_ylabel('Deflection $v(x)$ [mm]')
axes[3].set_xlabel('Position along beam $x$ [m]')
axes[3].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4. Piecewise Integration for Intermediate Point Loads (at $x = a$)
# If a point load $P_a$ acts at an intermediate location $x = a$ ($0 < a < L$),
# we split the beam into two segments:
# * **Segment 1 ($0 \le x \le a$):** Shear includes $P_a$
# * **Segment 2 ($a \le x \le L$):** Shear has no $P_a$
#
# We enforce continuity at $x = a$:
# 1. Deflection continuity: $v_1(a) = v_2(a)$
# 2. Slope continuity: $\theta_1(a) = \theta_2(a)$
# 3. Moment continuity: $M_1(a) = M_2(a)$
# 4. Shear jump condition: $V_1(a) - V_2(a) = -P_a$

# %%
a, P_a = sp.symbols('a P_a', real=True)

# Segment 1: x in [0, a]
# Segment 2: x in [a, L]
# Let us formulate the bending moment directly from equilibrium:
# For any x: M(x) = applied load contributions to the right of x
M_seg1 = -P_a * (a - x)
M_seg2 = 0

# Deflection equations: E*I*v''(x) = M(x)
# Segment 1:
theta1 = sp.integrate(M_seg1 / (E * I), x) + sp.Symbol('D1')
v1 = sp.integrate(theta1, x) + sp.Symbol('D2')

# Segment 2:
theta2 = sp.integrate(M_seg2 / (E * I), x) + sp.Symbol('D3')
v2 = sp.integrate(theta2, x) + sp.Symbol('D4')

# Boundary and continuity equations:
pw_bcs = [
    sp.Eq(v1.subs(x, 0), 0),               # Clamped deflection at root
    sp.Eq(theta1.subs(x, 0), 0),           # Clamped slope at root
    sp.Eq(v1.subs(x, a), v2.subs(x, a)),   # Deflection continuity at x=a
    sp.Eq(theta1.subs(x, a), theta2.subs(x, a)) # Slope continuity at x=a
]

D_sol = sp.solve(pw_bcs, (sp.Symbol('D1'), sp.Symbol('D2'), sp.Symbol('D3'), sp.Symbol('D4')))
v1_sol = sp.simplify(v1.subs(D_sol))
v2_sol = sp.simplify(v2.subs(D_sol))

print("Piecewise Deflection (Intermediate Load P_a at x = a):")
print("Segment 1 (0 <= x <= a):")
display(v1_sol)
print("Segment 2 (a <= x <= L) [rigid body continuation]:")
display(v2_sol)
