# %%
from sympy import symbols, Function, diff
from sympy.calculus.euler import euler_equations

# %% Define symbols and the displacement function y(x)
x = symbols('x')
EI, P = symbols('EI P')
y = Function('y')(x)

# %% Define the Lagrangian Density (L)
# y.diff(x, 2) is the curvature y''
L = 0.5 * EI * y.diff(x, 2)**2 - 0.5 * P * y.diff(x)**2

# Generate the Euler-Lagrange Equation
# This returns a list of equations (one for each dependent function)
buckling_ode = euler_equations(L, y, x)

print(buckling_ode)
# Output: [Eq(EI*Derivative(y(x), (x, 4)) + P*Derivative(y(x), (x, 2)), 0)]