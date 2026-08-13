# region Example 0 Fixed-Roller beam with point load
# %% Using the sign convention of upward forces and clockwise moment being positive.
from sympy.physics.continuum_mechanics.beam import Beam
import sympy as sp
import numpy as np
from sympy import symbols

E, I = symbols('E, I', nonneg=True)
b = Beam(20, E, I)

# help(Beam.apply_support)
p0, m0 = b.apply_support(0, 'fixed')
p1 = b.apply_support(20, 'roller')

b.apply_load(-8, 10, -1)
# b.apply_load(100, 20, -2)
# print(b.applied_loads)



b.solve_for_reaction_loads(p0, m0, p1)
# %% print results
print("Reactions:",     b.reaction_loads)
print("Load:",           b.load)
b.plot_shear_force()

print("Bending Moment:", b.bending_moment())
print("Deflection:",     b.deflection())
# %% draw
p=b.draw()
p.show()

# %% manual solution using bc

x = sp.symbols('x', nonnegative=True)


shear_curve = b.shear_force()
print(shear_curve)

# 1. Strip out Dirac Delta functions (index < 0) from the shear curve
clean_shear = shear_curve
for term in clean_shear.atoms(sp.SingularityFunction):
    if term.args[2] < 0: # If the index is negative
        clean_shear = clean_shear.subs(term, 0)

# 2. Now convert to Piecewise
piecewise_shear = clean_shear.rewrite(sp.Piecewise)

print("Original Shear:\n", shear_curve)
print("\nClean Piecewise Shear:\n", piecewise_shear)

# %% pandas
import pandas as pd
import matplotlib.pyplot as plt
# help(sp.lambdify)
shear_func=  sp.lambdify(x, piecewise_shear, modules=['numpy'])

x_vals = np.linspace(0, 20, 100)
shear_vals = shear_func(x_vals)
result_df = pd.DataFrame({'x': x_vals, 'shear': shear_vals})
result_df.head()
result_df.plot(x='x', y='shear')
plt.show()

# %% moment

bending_curve=b.bending_moment()
print(bending_curve)

# -M_0*SingularityFunction(x, 0, 0) - R_0*SingularityFunction(x, 0, 1) - R_20*SingularityFunction(x, 20, 1) + 8*SingularityFunction(x, 10, 1) - 100*SingularityFunction(x, 20, 0)
# bending_curve.rewrite(sp.Piecewise)

# -M_0*Piecewise((1, x >= 0), (0, True)) - R_0*Piecewise((x, x >= 0), (0, True)) - R_20*Piecewise((x - 20, x >= 20), (0, True)) - 100*Piecewise((1, x >= 20), (0, True)) + 8*Piecewise((x - 10, x >= 10), (0, True))
piecewise_moment =bending_curve.rewrite(sp.Piecewise)
print(piecewise_moment)

# -M_0*Piecewise((1, x >= 0), (0, True)) - R_0*Piecewise((x, x >= 0), (0, True)) - R_20*Piecewise((x - 20, x >= 20), (0, True)) - 100*Piecewise((1, x >= 20), (0, True)) + 8*Piecewise((x - 10, x >= 10), (0, True))
clean_moment = sp.simplify(piecewise_moment)
clean_moment

#%% pandas
import pandas as pd
import matplotlib.pyplot as plt
help(sp.lambdify)
shear_func=  sp.lambdify(x, piecewise_shear, modules=['numpy'])
bending_func=  sp.lambdify(x, piecewise_moment, modules=['numpy'])

x_vals = np.linspace(0, 20, 100)
shear_vals = shear_func(x_vals)
result_df = pd.DataFrame({'x': x_vals, 'shear': shear_vals})

result_df.plot(x='x', y='shear')
plt.show()

bending_vals = bending_func(x_vals)




import matplotlib.pyplot as plt
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



# Piecewise((-M_0 - R_0*x - R_20*(x - 20) + 8*x - 180, x >= 20), (-M_0 - R_0*x + 8*x - 80, x >= 10), (-(M_0 + R_0*x), x >= 0), (0, True))
slope_curve = b.slope()
print(slope_curve)

help(sp.integrate)
C3=sp.Symbol('C3', real=True)
sp.integrate(bending_curve, x)+C3
sp.integrate(piecewise_moment, x)+C3

# C3 - M_0*SingularityFunction(x, 0, 1) - R_0*SingularityFunction(x, 0, 2)/2 - R_20*SingularityFunction(x, 20, 2)/2 + 4*SingularityFunction(x, 10, 2) - 100*SingularityFunction(x, 20, 1)
# eqs
# C3
# piecewise_deflection=deflection_curve.rewrite(sp.Piecewise)
# piecewise_deflection
# C3*x + C4 - M_0*Piecewise((x**2, x >= 0), (0, True))/2 - R_0*Piecewise((x**3, x >= 0), (0, True))/6 - R_20*Piecewise(((x - 20)**3, x >= 20), (0, True))/6 - 50*Piecewise(((x - 20)**2, x >= 20), (0, True)) + 4*Piecewise(((x - 10)**3, x >= 10), (0, True))/3
# sp.simpify(piecewise_deflection)
# Traceback (most recent call last):
#   File "<string>", line 1, in <module>
# AttributeError: module 'sympy' has no attribute 'simpify'
# sp.simpyfy(piecewise_deflection)
# Traceback (most recent call last):
#   File "<string>", line 1, in <module>
# AttributeError: module 'sympy' has no attribute 'simpyfy'
# sp.simplify(piecewise_deflection)
# Piecewise((C3*x + C4 - M_0*x**2/2 - R_0*x**3/6 - R_20*(x - 20)**3/6 - 50*(x - 20)**2 + 4*(x - 10)**3/3, x >= 20), (C3*x + C4 - M_0*x**2/2 - R_0*x**3/6 + 4*(x - 10)**3/3, x >= 10), (C3*x + C4 - M_0*x**2/2 - R_0*x**3/6, x >= 0), (C3*x + C4, True))
# print(solution)
# [0, 0, -2, 20, 10]
# reactions
# (R_0, M_0, R_20)
# Reactions: {R_0: -2, M_0: 20, R_20: 10}

# endregion