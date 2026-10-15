import sympy as sp

#%% 1. Define mathematical symbols
# We define them as real and positive to help SymPy's simplification engine
t = sp.Symbol('t', real=True)
r = sp.Symbol('r', real=True, positive=True)
c = sp.Symbol('c', real=True, positive=True)

#%% 2. Define the parametric curve x(t) as a 3D vector (a helix)
# x(t) = [r*cos(t), r*sin(t), c*t]
x = sp.Matrix([
    r * sp.cos(t),
    r * sp.sin(t),
    c * t
])

print("1. Parametric Curve x(t):")
sp.pprint(x)
print("\n" + "="*40 + "\n")

#%% 3. Compute the first derivative x'(t) (Velocity vector)
x_prime = sp.diff(x, t)

#%% 4. Compute the second derivative x''(t) (Acceleration vector)
x_double_prime = sp.diff(x_prime, t)

#%% 5. Compute the cross product: x'(t) x x''(t)
cross_product = x_prime.cross(x_double_prime)
cross_product.simplify()

print("2. Cross Product of x'(t) and x''(t):")
sp.pprint(cross_product)
print("\n" + "="*40 + "\n")

# %%6. Compute the magnitudes (Euclidean norms)
# Simplify is called immediately to resolve the trig identities (sin^2 + cos^2 = 1)
norm_cross = sp.simplify(cross_product.norm())
norm_x_prime = sp.simplify(x_prime.norm())

print("3. Norm of the Cross Product ||x' x x''||:")
sp.pprint(norm_cross)
print("\n4. Norm of the First Derivative ||x'||:")
sp.pprint(norm_x_prime)
print("\n" + "="*40 + "\n")

# %% 7. Assemble the final curvature formula
kappa = norm_cross / (norm_x_prime**3)
kappa_simplified = sp.simplify(kappa)

print("5. Final Evaluated Curvature (kappa):")
sp.pprint(kappa_simplified)