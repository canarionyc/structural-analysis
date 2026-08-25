"""Showcase the eurocodepy.crosssection helper module.

This submodule provides simple analytical cross-section models for:
- rectangular sections
- circular sections

and computes key geometric properties used in structural design.
"""
from math import pow, sqrt, pi
from eurocodepy import crosssection as cs
#help(cs)

#%% circular cs
D=300.0
circ = cs.CircularCrossSection(diameter=D)
print(circ)
print("Circular section")
print(f"  shape      : {circ.shape}")
print(f"  area       : {circ.area:.1f} mm²")
print(pi*D**2/4)
print(f"  I_y        : {circ.inertia_y:.1f} mm^4")
print(pi*D**4/64)
print(f"  I_z        : {circ.inertia_z:.1f} mm^4")
print(pi*D**4/64)
print(f"  W_y        : {circ.bend_mod_y:.1f} mm^3")
print(pi*D**3/32)
print(f"  W_z        : {circ.bend_mod_z:.1f} mm^3")

print(f"  radius_y   : {circ.radius_y:.3f} mm")
print(sqrt(circ.inertia_y/circ.area))
print(sqrt(pi*D**4/64/(pi*D**2/4)))

print(f"  radius_z   : {circ.radius_z:.3f} mm")
print(f"  polar_I    : {circ.polar_inertia:.1f} mm^4")
print()