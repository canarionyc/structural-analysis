import sympy as sp

x = sp.symbols('x')

# Let's say this is your load equation
# 8 N/m distributed load starting at x=0
load_eq = 8 * sp.SingularityFunction(x, 0, 0)

# Convert it to Piecewise
piecewise_load = load_eq.rewrite(sp.Piecewise)

print(piecewise_load)
# Output: Piecewise((8, x >= 0), (0, True))