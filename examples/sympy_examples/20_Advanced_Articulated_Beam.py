# %% setup
import sympy as sp
from sympy.physics.continuum_mechanics.beam import Beam

E, I = sp.symbols('E I', positive=True)

# 1. Construct the articulated geometry using the join() method
# This prevents the 'oo' SingularityFunction bug!
b1 = Beam(6, E, I)
b2 = Beam(12, E, I)

# Join the two segments. SymPy will automatically treat 'b' as an 18m beam.
b = b1.join(b2, via="hinge")
print(b)
# 2. Apply supports and CAPTURE the auto-generated variables!
# (Notice the commas used to unpack the tuples returned by SymPy)
R_0, M_0 = b.apply_support(0, type='fixed')
R_6 = b.apply_support(6, type='roller')
R_18 = b.apply_support(18, type='roller')

# Apply the distributed wind load across the entire span
b.apply_load(-500, 0, 0, end=18)

# 3. Solve for all reaction loads
# The solver will now smoothly calculate the internal boundary conditions
help(b.solve_for_reaction_loads)
b.solve_for_reaction_loads(R_0, M_0, R_6, R_18)
#%% solution
print("Reactions Dictionary:")
for reaction, value in b.reaction_loads.items():
    print(f"{reaction}: {value} N")

#%%

help(b.plot_bending_moment)