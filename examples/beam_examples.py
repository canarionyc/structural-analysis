# %% Imports and Setup
from sympy import symbols
from sympy.physics.continuum_mechanics.beam import Beam

# %% Example 1: Cantilever Beam with Distributed Load, Moment, and Point Load
E, I = symbols('E, I')
b1 = Beam(9, E, I)

b1.apply_load(12, 9, -1)
b1.apply_load(8, 0, 0, end=5)
b1.apply_load(50, 5, -2)

b1.bc_deflection.append((0, 0))
b1.bc_slope.append((0, 0))

R, M = symbols('R, M')
b1.apply_load(R, 0, -1)
b1.apply_load(M, 0, -2)

b1.solve_for_reaction_loads(R, M)
print("Example 1 Reactions:", b1.reaction_loads)
print("Example 1 Load:", b1.load)
print("Example 1 Shear Force:", b1.shear_force())
print("Example 1 Bending Moment:", b1.bending_moment())
# b1.plot_shear_force()
# b1.plot_bending_moment()

# %% Example 2: Simply Supported Beam with Overhang and Point Moment
E, I = symbols('E, I')
R1, R2 = symbols('R1, R2')
b2 = Beam(30, E, I)

b2.apply_load(8, 0, -1)
b2.apply_load(R1, 10, -1)
b2.apply_load(R2, 30, -1)
b2.apply_load(120, 30, -2)

b2.bc_deflection.append((10, 0))
b2.bc_deflection.append((30, 0))

b2.solve_for_reaction_loads(R1, R2)
print("Example 2 Reactions:", b2.reaction_loads)
print("Example 2 Bending Moment:", b2.bending_moment())

# %% Example 3: Beam with Variable Elastic Modulus / Moment of Inertia
E, I = symbols('E, I')
R1, R2 = symbols('R1, R2')
b3 = Beam(3, E, I)

b3.apply_load(R1, 0, -1)
b3.apply_load(R2, 3, -1)
b3.apply_load(10, 1, -1)
b3.apply_load(10, 2, -1)

b3.bc_deflection.append((0, 0))
b3.bc_deflection.append((3, 0))

b3.solve_for_reaction_loads(R1, R2)

# Set variable E and I across segments
b3.composite_deflection(data=[(0, 1, 2*E, I), (1, 2, E, 2*I), (2, 3, E, I)])
print("Example 3 Composite Deflection:", b3.deflection())

# %% Example 4: Fixed-Fixed Beam with Linear (Ramp) Load
E, I = symbols('E, I')
R1, R2, M1, M2 = symbols('R1, R2, M1, M2')
b4 = Beam(10, E, I)

b4.apply_load(R1, 0, -1)
b4.apply_load(M1, 0, -2)
b4.apply_load(R2, 10, -1)
b4.apply_load(M2, 10, -2)

# Linear distributed load from 0 to 10 with slope 2 (q(x) = 2x)
b4.apply_load(2, 0, 1, end=10)

b4.bc_deflection.append((0, 0))
b4.bc_slope.append((0, 0))
b4.bc_deflection.append((10, 0))
b4.bc_slope.append((10, 0))

b4.solve_for_reaction_loads(R1, R2, M1, M2)
print("Example 4 Reactions:", b4.reaction_loads)

# %% Example 5: Propped Cantilever with Parabolic Distributed Load
E, I = symbols('E, I')
R1, M1, R2 = symbols('R1, M1, R2')
b5 = Beam(6, E, I)

b5.apply_load(R1, 0, -1)
b5.apply_load(M1, 0, -2)
b5.apply_load(R2, 6, -1)

# Parabolic load q(x) = x^2 from x=0 to x=6
b5.apply_load(1, 0, 2, end=6)

b5.bc_deflection.append((0, 0))
b5.bc_slope.append((0, 0))
b5.bc_deflection.append((6, 0))

b5.solve_for_reaction_loads(R1, M1, R2)
print("Example 5 Reactions:", b5.reaction_loads)

# %% Example 6: Continuous Beam over Multiple Supports
E, I = symbols('E, I')
R1, R2, R3 = symbols('R1, R2, R3')
b6 = Beam(12, E, I)

b6.apply_load(R1, 0, -1)
b6.apply_load(R2, 6, -1)
b6.apply_load(R3, 12, -1)
b6.apply_load(10, 0, 0, end=12)

b6.bc_deflection.append((0, 0))
b6.bc_deflection.append((6, 0))
b6.bc_deflection.append((12, 0))

b6.solve_for_reaction_loads(R1, R2, R3)
print("Example 6 Reactions:", b6.reaction_loads)

# %% Example 7: Beam with Internal Pin Joint (Hinge)
E, I = symbols('E, I')
R1, M1, R2 = symbols('R1, M1, R2')
b7 = Beam(8, E, I)

b7.apply_load(R1, 0, -1)
b7.apply_load(M1, 0, -2)
b7.apply_load(R2, 8, -1)
b7.apply_load(20, 4, -1)

# Insert pin at x = 4
b7.apply_pin(4)

b7.bc_deflection.append((0, 0))
b7.bc_slope.append((0, 0))
b7.bc_deflection.append((8, 0))

b7.solve_for_reaction_loads(R1, M1, R2)
print("Example 7 Reactions:", b7.reaction_loads)

# %% Example 8: Beam with Spring Support
E, I, k = symbols('E, I, k')
R1, M1 = symbols('R1, M1')
b8 = Beam(5, E, I)

b8.apply_load(R1, 0, -1)
b8.apply_load(M1, 0, -2)
b8.apply_load(15, 5, -1)

# Spring support at x = 5 with stiffness k
b8.apply_support(5, type='spring', k=k)

b8.bc_deflection.append((0, 0))
b8.bc_slope.append((0, 0))

b8.solve_for_reaction_loads(R1, M1)
print("Example 8 Reactions:", b8.reaction_loads)

# %% Example 9: Beam with Guided / Sliding Support
E, I = symbols('E, I')
R1, M2 = symbols('R1, M2')
b9 = Beam(6, E, I)

b9.apply_load(R1, 0, -1)
b9.apply_load(M2, 6, -2)
b9.apply_load(12, 3, -1)

b9.bc_deflection.append((0, 0))
b9.bc_slope.append((6, 0))

b9.solve_for_reaction_loads(R1, M2)
print("Example 9 Reactions:", b9.reaction_loads)

# %% Example 10: Symbolic Beam with Parametric Dimensions and Loading
l, E, I, P = symbols('l, E, I, P')
R1, R2 = symbols('R1, R2')
b10 = Beam(l, E, I)

b10.apply_load(R1, 0, -1)
b10.apply_load(R2, l, -1)
b10.apply_load(P, l/2, -1)

b10.bc_deflection.append((0, 0))
b10.bc_deflection.append((l, 0))

b10.solve_for_reaction_loads(R1, R2)
print("Example 10 Reactions:", b10.reaction_loads)
print("Example 10 Midspan Deflection:", b10.deflection().subs('x', l/2))

# %% Example 11: Beam with Multiple Internal Hinges
l, E, I, q = symbols('l, E, I, q')
R1, R2, R3, M1 = symbols('R1, R2, R3, M1')
b11 = Beam(4*l, E, I)

b11.apply_load(R1, 0, -1)
b11.apply_load(M1, 0, -2)
b11.apply_load(R2, 2*l, -1)
b11.apply_load(R3, 4*l, -1)
b11.apply_load(q, 0, 0, end=4*l)

# Apply internal pin hinges at l and 3*l
b11.apply_pin(l)
b11.apply_pin(3*l)

b11.bc_deflection.append((0, 0))
b11.bc_slope.append((0, 0))
b11.bc_deflection.append((2*l, 0))
b11.bc_deflection.append((4*l, 0))

b11.solve_for_reaction_loads(R1, M1, R2, R3)
print("Example 11 Reactions:", b11.reaction_loads)

# %% Example 12: Superposition / Composite Loading with Deflection Evaluation
E, I = symbols('E, I')
R1, R2 = symbols('R1, R2')
b12 = Beam(10, E, I)

b12.apply_load(R1, 0, -1)
b12.apply_load(R2, 10, -1)
b12.apply_load(5, 2, 0, end=8)  # Distributed load
b12.apply_load(20, 5, -1)        # Concentrated force
b12.apply_load(-30, 8, -2)       # Concentrated moment

b12.bc_deflection.append((0, 0))
b12.bc_deflection.append((10, 0))

b12.solve_for_reaction_loads(R1, R2)
print("Example 12 Reactions:", b12.reaction_loads)
print("Example 12 Deflection Function:", b12.deflection())

# %% Example 13: Beam with Sliding Hinge (Internal Roller/Guide)
l, E, I, q1 = symbols('l, E, I, q1')
R1, M1, R2, M2 = symbols('R1, M1, R2, M2')
b13 = Beam(3*l, E, I)

b13.apply_load(R1, 0, -1)
b13.apply_load(M1, 0, -2)
b13.apply_load(R2, 3*l, -1)
b13.apply_load(M2, 3*l, -2)

b13.apply_load(10, l/3, -1)
b13.apply_load(q1, 2*l, 0, end=3*l)

# Internal sliding hinge at x = 5*l/2
b13.apply_sliding_hinge(5*l/2)

b13.bc_deflection.append((0, 0))
b13.bc_slope.append((0, 0))
b13.bc_deflection.append((3*l, 0))
b13.bc_slope.append((3*l, 0))

b13.solve_for_reaction_loads(R1, M1, R2, M2)
print("Example 13 Reactions:", b13.reaction_loads)