import sympy as sp


# 1. Define the parameter 't'
t = sp.Symbol('t', real=True)

# 2. Define x(t) and y(t) as arbitrary parametric functions
x = sp.Function('x')(t)
y = sp.Function('y')(t)

# Compute the first derivatives (velocity)
dx = sp.diff(x, t)
dy = sp.diff(y, t)

# 3. Define the increment of arc length (ds/dt)
# This is the magnitude of the velocity vector
ds_dt = sp.sqrt(dx**2 + dy**2)

# 4. Define the tangent angle theta(t)
# theta is the angle the tangent vector makes with the x-axis
theta = sp.atan(dy / dx)

# 5. Compute the increment of the radial angle (d(theta)/dt)
dtheta_dt = sp.diff(theta, t)

# Force SymPy to simplify the messy fraction division
dtheta_dt_simplified = sp.cancel(dtheta_dt)
print(dtheta_dt_simplified)
print("1. Rate of change of the tangent angle (dθ/dt):")
sp.pprint(dtheta_dt_simplified)
print("\n" + "="*50 + "\n")

# 6. Apply the fundamental definition of curvature: d(theta) / ds
kappa = dtheta_dt_simplified / ds_dt

print("2. Fundamental Intrinsic Curvature (dθ/ds):")
sp.pprint(kappa)