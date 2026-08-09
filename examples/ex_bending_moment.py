#%% setup
from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols

E, I = symbols('E, I')
R1, R2 = symbols('R1, R2')
b = Beam(30, E, I)
b.apply_load(-8, 0, -1)
b.apply_load(R1, 10, -1)
b.apply_load(R2, 30, -1)
b.apply_load(120, 30, -2)
b.bc_deflection = [(10, 0), (30, 0)]
b.solve_for_reaction_loads(R1, R2)

print(b.reaction_loads)

print(b.bending_moment())

# 8*SingularityFunction(x, 0, 1) - 6*SingularityFunction(x, 10, 1) - 120*SingularityFunction(x, 30, 0) - 2*SingularityFunction(x, 30, 1)