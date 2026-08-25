#%% eurocodepy
import eurocodepy
help(eurocodepy)
import eurocodepy.utils as ecu
dir(ecu)

#%% rectangular section
help(ecu.RectangularCrossSection)

# from eurocodepy.utils import RectangularCrossSection


w=50; h=100
my_section = ecu.RectangularCrossSection(width=w, height=h)

print(my_section.area)
print(my_section.inertia_y)
print(w**3*h/12)

print(my_section.bend_mod_y)
print(my_section.inertia_y/(w/2))

assert my_section.bend_mod_y==my_section.inertia_y/(w/2)

print("inertia_z", my_section.inertia_z)
print(h**3*w/12)

print("bend_mod_z", my_section.bend_mod_z)
print(h**3*w/12/(h/2))
assert my_section.bend_mod_z==my_section.inertia_z/(h/2)


print(my_section.polar_inertia)
print(w**3*h/12+h**3*w/12)

#%% rectangular cs
from eurocodepy import crosssection as cs
w=300.0; h=500.0
rect = cs.RectangularCrossSection(width=w, height=h)
print(rect)
print("Rectangular section")
print(f"  shape      : {rect.shape}")
print(f"  area       : {rect.area:.1f} mm²")
print(f"  I_y        : {rect.inertia_y:.1f} mm^4")
print(w**3*h/12)
print(f"  I_z        : {rect.inertia_z:.1f} mm^4")
print(h**3*w/12)
print(f"  W_y        : {rect.bend_mod_y:.1f} mm^3")
print(w**2*h/6)
print(f"  W_z        : {rect.bend_mod_z:.1f} mm^3")
print(h**2*w/6)

print(f"  radius_y   : {rect.radius_y:.3f} mm")
sqrt(rect.inertia_y/rect.area)
print(f"  radius_z   : {rect.radius_z:.3f} mm")
sqrt(rect.inertia_z/rect.area)

print(f"  polar_I    : {rect.polar_inertia:.1f} mm^4")
print()