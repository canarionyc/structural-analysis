from sympy import symbols
from sympy.physics.continuum_mechanics.beam import Beam3D

# Define structural parameters (including Shear Modulus G and Area A for 3D)
l, E, G, I, A = symbols('l E G I A')

# Initialize a 3D structural element
b3d = Beam3D(l, E, G, I, A)

q, m = symbols('q m')

# Apply a uniform distributed wind load along the Y-axis
b3d.apply_load(q, start=0, order=0, dir="y")

# Apply an asymmetric fabric tension moment causing twisting along the Z-axis
b3d.apply_moment_load(m, start=0, order=1, dir="z")

# Establish boundary conditions: fixed at both ends (deflection and slope are 0)
b3d.bc_slope = [(0, [0, 0, 0]), (l, [0, 0, 0])]
b3d.bc_deflection = [(0, [0, 0, 0]), (l, [0, 0, 0])]

# Extract the 3D shear force and bending moment vectors [x, y, z]
print("3D Shear Force Vector [Fx, Fy, Fz]:")
print(b3d.shear_force())

print("\n3D Bending Moment Vector [Mx, My, Mz]:")
print(b3d.bending_moment())