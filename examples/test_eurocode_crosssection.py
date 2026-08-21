"""Showcase the eurocodepy.crosssection helper module.

This submodule provides simple analytical cross-section models for:
- rectangular sections
- circular sections

and computes key geometric properties used in structural design.
"""

from eurocodepy import crosssection as cs
help(cs)

def demo_rectangular() -> None:
    rect = cs.RectangularCrossSection(width=300.0, height=500.0)
    print("Rectangular section")
    print(f"  shape      : {rect.shape}")
    print(f"  area       : {rect.area:.1f} mm²")
    print(f"  I_y        : {rect.inertia_y:.1f} mm^4")
    print(f"  I_z        : {rect.inertia_z:.1f} mm^4")
    print(f"  W_y        : {rect.bend_mod_y:.1f} mm^3")
    print(f"  W_z        : {rect.bend_mod_z:.1f} mm^3")
    print(f"  radius_y   : {rect.radius_y:.3f} mm")
    print(f"  radius_z   : {rect.radius_z:.3f} mm")
    print(f"  polar_I    : {rect.polar_inertia:.1f} mm^4")
    print()


def demo_circular() -> None:
    circ = cs.CircularCrossSection(diameter=300.0)
    print("Circular section")
    print(f"  shape      : {circ.shape}")
    print(f"  area       : {circ.area:.1f} mm²")
    print(f"  I_y        : {circ.inertia_y:.1f} mm^4")
    print(f"  I_z        : {circ.inertia_z:.1f} mm^4")
    print(f"  W_y        : {circ.bend_mod_y:.1f} mm^3")
    print(f"  W_z        : {circ.bend_mod_z:.1f} mm^3")
    print(f"  radius_y   : {circ.radius_y:.3f} mm")
    print(f"  radius_z   : {circ.radius_z:.3f} mm")
    print(f"  polar_I    : {circ.polar_inertia:.1f} mm^4")
    print()


if __name__ == "__main__":
    demo_rectangular()
    demo_circular()