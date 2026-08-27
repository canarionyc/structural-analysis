#%% 1. Setup and imports
import os
import matplotlib

# matplotlib.use("Agg") # FigureCanvasAgg is non-interactive, and thus cannot be shown

import matplotlib.pyplot as plt
#%%
import sectionproperties
# from pydoc import doc
# doc(sectionproperties)

help(sectionproperties)
dir(sectionproperties)


from sectionproperties import analysis
dir(analysis)

from sectionproperties.analysis import Section
help(Section)
from sectionproperties.pre import Material
help(Material)


#%%
from sectionproperties.pre.library import rectangular_section
help(rectangular_section)

# create a 50 x 100 rectangle and mesh it
d=100; b=50
geom = rectangular_section(d=d, b=b)
geom.plot_geometry();
#%%
geom.create_mesh(mesh_sizes=[5]);

# run a geometric analysis
sec = Section(geometry=geom)
help(sec.calculate_geometric_properties)
sec.calculate_geometric_properties()
# sec.calculate_warping_properties()
sec.plot_mesh(materials=False)

dir(sec)
# get some results
area = sec.get_area()
print(f"Area = {area:.0f} mm²")
print(f"Expected Area = {d*b:.0f} mm²")

#%% centroids
help(sec.get_c)
cx,cy=sec.get_c()
print(f"Centroid = ({cx:.0f}, {cy:.0f}) mm")

from scipy import integrate
dir(integrate)
help(integrate.quad)

integrate.quad(lambda x, depth: depth*x, 0, b, args=(d,))/area
integrate.quad(lambda base, y: base*y, 0, d, args=(b,))/area

#%%  cross-section centroidal second moments of area.
help(sec.get_ic)
ixx_c, iyy_c, ixy_c = sec.get_ic()
print(f"Ixx = {ixx_c:.0f} mm⁴, Iyy = {iyy_c:.0f} mm⁴")
print(f"Ixy = {ixy_c:.0f} mm⁴")



#%% Second moments of area about the global axis
dir(sec)
help(sec.get_ig)
(ixx_g, iyy_g, ixy_g) = sec.get_ig()
print(f"Ixx_g = {ixx_g:.0f} mm⁴, Iyy_g = {iyy_g:.0f} mm⁴")
print(f"Ixy_g = {ixy_g:.0f} mm⁴")

print(f"Ixx_g_formula = {b*(d**3)/12:.0f} mm⁴, Iyy_g_formula = {d*(b**3)/12:.0f} mm⁴")
print(f"Ixy_g = {0:.0f} mm⁴")

print(ixx_c + area*sec.section_props.cy**2, ixx_g)
print(iyy_c + area*sec.section_props.cx**2, iyy_g)

#%% one dimensional integrals
from scipy import integrate
dir(integrate)
help(integrate.quad)
ixx_g_num, err = integrate.quad(lambda y: b*y**2, 0, d)
print(f"Numerical Ixx = {ixx_g_num:.0f} mm⁴, Error = {err:.0f} mm⁴")

iyy_g_num, err = integrate.quad(lambda x: d*x**2, 0, b)
print(f"Numerical Iyy = {iyy_g_num:.0f} mm⁴, Error = {err:.0f} mm⁴")



#%% two dimensional integrals

help(integrate.dblquad)
f=lambda y,x: x*y

ixy_g_num, err = integrate.dblquad(f, 0, b, 0, d)
print(f"Numerical Ixy = {ixy_g_num:.0f} mm⁴, Error = {err:.0f} mm⁴")
ixy_g
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
from sectionproperties.pre.library import i_section
help(i_section)
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