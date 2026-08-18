from sympy.diffgeom import Manifold, Patch, CoordSystem
from sympy import Symbol, symbols, Function, diff, sqrt, atan

# Define a 1D parametric space
m = Manifold('M', 1)
patch = Patch('P', m)
help(CoordSystem)
t_system = CoordSystem('t_sys', patch, [Symbol('t', real=True)])
print(t_system)

# Now you can extract the true base scalar and the true differential 1-form
t = t_system.coord_functions()[0]
dt = t_system.base_oneforms()[0]