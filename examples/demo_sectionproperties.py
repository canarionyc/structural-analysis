#%% 1. Setup and imports
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
#%%
import sectionproperties
print(sectionproperties.analysis.__file__)

help(sectionproperties)
dir(sectionproperties)

from sectionproperties.analysis import Section
help(Section)
from sectionproperties.pre import Material
from sectionproperties.pre.library import i_section, rectangular_section

#%% from sectionproperties.pre.library import rectangular_section
from sectionproperties.analysis import Section

# create a 50 x 100 rectangle and mesh it
geom = rectangular_section(d=100, b=50)
geom.create_mesh(mesh_sizes=[5])

# run a geometric analysis
sec = Section(geometry=geom)
sec.calculate_geometric_properties()

# get some results
area = sec.get_area()
ixx_c, iyy_c, ixy_c = sec.get_ic()
print(f"Area = {area:.0f} mm²")
print(f"Ixx = {ixx_c:.0f} mm⁴, Iyy = {iyy_c:.0f} mm⁴")

#%%

#%% 2. Define a material
steel = Material(
    name="S355",
    elastic_modulus=200e9,
    poissons_ratio=0.3,
    yield_strength=355e6,
    density=7850,
    color="lightgrey",
)

#%% 3. Create a rectangular section
rect = rectangular_section(d=0.30, b=0.20, material=steel)
rect = rect.create_mesh(mesh_sizes=[0.02])
rect_section = Section(rect)
rect_section.calculate_geometric_properties()
rect_section.calculate_warping_properties()

props_rect = rect_section.section_props
print("Rectangular section properties:")
print(f"  Area: {props_rect.area:.6f} m^2")
print(f"  Ixx: {props_rect.ixx_c:.3e} m^4")
print(f"  Iyy: {props_rect.iyy_c:.3e} m^4")
print(f"  Centroid: ({props_rect.cx:.4f}, {props_rect.cy:.4f}) m")

#%% 4. Create a more realistic steel I-section
beam = i_section(
    d=0.40,
    b=0.20,
    t_f=0.015,
    t_w=0.010,
    r=0.012,
    n_r=8,
    material=steel,
)
beam = beam.create_mesh(mesh_sizes=[0.01])
beam_section = Section(beam)
beam_section.calculate_geometric_properties()
beam_section.calculate_warping_properties()

props_beam = beam_section.section_props
print("\nI-section properties:")
print(f"  Area: {props_beam.area:.6f} m^2")
print(f"  Ixx: {props_beam.ixx_c:.3e} m^4")
print(f"  Iyy: {props_beam.iyy_c:.3e} m^4")
print(f"  Elastic section modulus Zxx: {props_beam.zxx_plus:.3e} m^3")

#%% 5. Plot the geometry
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

rect.plot_geometry(ax=axes[0])
axes[0].set_title("Rectangular section")
axes[0].set_aspect("equal")

beam.plot_geometry(ax=axes[1])
axes[1].set_title("I-section")
axes[1].set_aspect("equal")

plt.tight_layout()
if matplotlib.get_backend().lower().endswith("agg"):
    plt.savefig("sectionproperties_demo.png", dpi=150, bbox_inches="tight")
else:
    plt.show()