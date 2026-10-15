# %% 1. Setup and imports
import os
import matplotlib

# matplotlib.use("Agg") # FigureCanvasAgg is non-interactive, and thus cannot be shown

import matplotlib.pyplot as plt
# %%
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

# %%
from sectionproperties.pre.library import rectangular_section

help(rectangular_section)

# create a 50 x 100 rectangle and mesh it
d = 100;
b = 50
geom = rectangular_section(d=d, b=b)
geom.plot_geometry();
# %%
geom.create_mesh(mesh_sizes=[5]);

# run a geometric analysis
sec = Section(geometry=geom)
help(sec.calculate_geometric_properties)
sec.calculate_geometric_properties()
# sec.calculate_warping_properties()
sec.plot_mesh(materials=False)

help(sec.display_results)

sec.display_results('.2f')

# %%
fmt = '.2f'
# print cross-section area

area = sec.get_area()
print("area", f"{area:>{fmt}}")


# print cross-sec perimeter
try:
    perimeter = sec.get_perimeter()
    print("perimeter", f"{perimeter:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec mass (only if composite)
if sec.is_composite:
    try:
        mass = sec.get_mass()
        print("mass", f"{mass:>{fmt}}")

        ea = sec.get_ea()
        print("e.a", f"{ea:>{fmt}}")

        qx, qy = sec.get_q()
        print("qx", f"{qx:>{fmt}}")
        print("qy", f"{qy:>{fmt}}")

        eqx, eqy = sec.get_eq()
        print("e.qx", f"{eqx:>{fmt}}")
        print("e.qy", f"{eqy:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec ig
if not sec.is_composite:
    try:
        ixx_g, iyy_g, ixy_g = sec.get_ig()
        print("ixx_g", f"{ixx_g:>{fmt}}")
        print("iyy_g", f"{iyy_g:>{fmt}}")
        print("ixy_g", f"{ixy_g:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        eixx_g, eiyy_g, eixy_g = sec.get_eig()
        print("e.ixx_g", f"{eixx_g:>{fmt}}")
        print("e.iyy_g", f"{eiyy_g:>{fmt}}")
        print("e.ixy_g", f"{eixy_g:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec centroid
try:
    cx, cy = sec.get_c()
    print("cx", f"{cx:>{fmt}}")
    print("cy", f"{cy:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec ic
if not sec.is_composite:
    try:
        ixx_c, iyy_c, ixy_c = sec.get_ic()
        print("ixx_c", f"{ixx_c:>{fmt}}")
        print("iyy_c", f"{iyy_c:>{fmt}}")
        print("ixy_c", f"{ixy_c:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        eixx_c, eiyy_c, eixy_c = sec.get_eic()
        print("e.ixx_c", f"{eixx_c:>{fmt}}")
        print("e.iyy_c", f"{eiyy_c:>{fmt}}")
        print("e.ixy_c", f"{eixy_c:>{fmt}}")
    except RuntimeError:
        pass

#%% cross-section centroidal elastic section moduli.
if not sec.is_composite:
    help(sec.get_z)
    try:
        zxx_plus, zxx_minus, zyy_plus, zyy_minus = sec.get_z()
        print("zxx+", f"{zxx_plus:>{fmt}}")
        print("zxx-", f"{zxx_minus:>{fmt}}")
        print("zyy+", f"{zyy_plus:>{fmt}}")
        print("zyy-", f"{zyy_minus:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        ezxx_plus, ezxx_minus, ezyy_plus, ezyy_minus = sec.get_ez()
        print("e.zxx+", f"{ezxx_plus:>{fmt}}")
        print("e.zxx-", f"{ezxx_minus:>{fmt}}")
        print("e.zyy+", f"{ezyy_plus:>{fmt}}")
        print("e.zyy-", f"{ezyy_minus:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec my
if sec.is_composite:
    try:
        my_xx, my_yy = sec.get_my()
        print("my_xx", f"{my_xx:>{fmt}}")
        print("my_yy", f"{my_yy:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec rc
try:
    rx, ry = sec.get_rc()
    print("rx", f"{rx:>{fmt}}")
    print("ry", f"{ry:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec ip
if not sec.is_composite:
    try:
        i11_c, i22_c = sec.get_ip()
        print("i11_c", f"{i11_c:>{fmt}}")
        print("i22_c", f"{i22_c:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        ei11_c, ei22_c = sec.get_eip()
        print("e.i11_c", f"{ei11_c:>{fmt}}")
        print("e.i22_c", f"{ei22_c:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec phi
try:
    phi = sec.get_phi()
    print("phi", f"{phi:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec zp
if not sec.is_composite:
    try:
        z11_plus, z11_minus, z22_plus, z22_minus = sec.get_zp()
        print("z11+", f"{z11_plus:>{fmt}}")
        print("z11-", f"{z11_minus:>{fmt}}")
        print("z22+", f"{z22_plus:>{fmt}}")
        print("z22-", f"{z22_minus:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        ez11_plus, ez11_minus, ez22_plus, ez22_minus = sec.get_ezp()
        print("e.z11+", f"{ez11_plus:>{fmt}}")
        print("e.z11-", f"{ez11_minus:>{fmt}}")
        print("e.z22+", f"{ez22_plus:>{fmt}}")
        print("e.z22-", f"{ez22_minus:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec my_p
if sec.is_composite:
    try:
        my_11, my_22 = sec.get_my_p()
        print("my_11", f"{my_11:>{fmt}}")
        print("my_22", f"{my_22:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec rp
try:
    r11, r22 = sec.get_rp()
    print("r11", f"{r11:>{fmt}}")
    print("r22", f"{r22:>{fmt}}")
except RuntimeError:
    pass

# print effective material properties
if sec.is_composite:
    try:
        e_eff = sec.get_e_eff()
        g_eff = sec.get_g_eff()
        nu_eff = sec.get_nu_eff()
        print("e_eff", f"{e_eff:>{fmt}}")
        print("g_eff", f"{g_eff:>{fmt}}")
        print("nu_eff", f"{nu_eff:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec j
if not sec.is_composite:
    try:
        j = sec.get_j()
        print("j", f"{j:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        ej = sec.get_ej()
        print("e.j", f"{ej:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec sc
try:
    x_se, y_se = sec.get_sc()
    print("x_se", f"{x_se:>{fmt}}")
    print("y_se", f"{y_se:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec sc_p
try:
    x1_se, y2_se = sec.get_sc_p()
    print("x1_se", f"{x1_se:>{fmt}}")
    print("y2_se", f"{y2_se:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec sc_t
try:
    x_st, y_st = sec.get_sc_t()
    print("x_st", f"{x_st:>{fmt}}")
    print("y_st", f"{y_st:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec gamma
if not sec.is_composite:
    try:
        gamma = sec.get_gamma()
        print("gamma", f"{gamma:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        egamma = sec.get_egamma()
        print("e.gamma", f"{egamma:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec as
if not sec.is_composite:
    try:
        a_sx, a_sy = sec.get_as()
        print("a_sx", f"{a_sx:>{fmt}}")
        print("a_sy", f"{a_sy:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        ea_sx, ea_sy = sec.get_eas()
        print("e.a_sx", f"{ea_sx:>{fmt}}")
        print("e.a_sy", f"{ea_sy:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec as_p
if not sec.is_composite:
    try:
        a_s11, a_s22 = sec.get_as_p()
        print("a_s11", f"{a_s11:>{fmt}}")
        print("a_s22", f"{a_s22:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        ea_s11, ea_s22 = sec.get_eas_p()
        print("e.a_s11", f"{ea_s11:>{fmt}}")
        print("e.a_s22", f"{ea_s22:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec beta
try:
    beta_x_plus, beta_x_minus, beta_y_plus, beta_y_minus = sec.get_beta()
    print("beta_x+", f"{beta_x_plus:>{fmt}}")
    print("beta_x-", f"{beta_x_minus:>{fmt}}")
    print("beta_y+", f"{beta_y_plus:>{fmt}}")
    print("beta_y-", f"{beta_y_minus:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec beta_p
try:
    beta_11_plus, beta_11_minus, beta_22_plus, beta_22_minus = sec.get_beta_p()
    print("beta_11+", f"{beta_11_plus:>{fmt}}")
    print("beta_11-", f"{beta_11_minus:>{fmt}}")
    print("beta_22+", f"{beta_22_plus:>{fmt}}")
    print("beta_22-", f"{beta_22_minus:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec pc
try:
    x_pc, y_pc = sec.get_pc()
    print("x_pc", f"{x_pc:>{fmt}}")
    print("y_pc", f"{y_pc:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec pc_p
try:
    x11_pc, y22_pc = sec.get_pc_p()
    print("x11_pc", f"{x11_pc:>{fmt}}")
    print("y22_pc", f"{y22_pc:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec s/mp
if not sec.is_composite:
    try:
        sxx, syy = sec.get_s()
        print("sxx", f"{sxx:>{fmt}}")
        print("syy", f"{syy:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        mp_xx, mp_yy = sec.get_mp()
        print("mp_xx", f"{mp_xx:>{fmt}}")
        print("mp_yy", f"{mp_yy:>{fmt}}")

    except RuntimeError:
        pass

# print cross-sec sp/mp_p
if not sec.is_composite:
    try:
        s11, s22 = sec.get_sp()
        print("s11", f"{s11:>{fmt}}")
        print("s22", f"{s22:>{fmt}}")
    except RuntimeError:
        pass
else:
    try:
        mp_11, mp_22 = sec.get_mp_p()
        print("mp_11", f"{mp_11:>{fmt}}")
        print("mp_22", f"{mp_22:>{fmt}}")
    except RuntimeError:
        pass

# print cross-sec sf
try:
    sf_xx_plus, sf_xx_minus, sf_yy_plus, sf_yy_minus = sec.get_sf()
    print("sf_xx+", f"{sf_xx_plus:>{fmt}}")
    print("sf_xx-", f"{sf_xx_minus:>{fmt}}")
    print("sf_yy+", f"{sf_yy_plus:>{fmt}}")
    print("sf_yy-", f"{sf_yy_minus:>{fmt}}")
except RuntimeError:
    pass

# print cross-sec sf_p
try:
    sf_11_plus, sf_11_minus, sf_22_plus, sf_22_minus = sec.get_sf_p()
    print("sf_11+", f"{sf_11_plus:>{fmt}}")
    print("sf_11-", f"{sf_11_minus:>{fmt}}")
    print("sf_22+", f"{sf_22_plus:>{fmt}}")
    print("sf_22-", f"{sf_22_minus:>{fmt}}")
except RuntimeError:
    pass

# %%
dir(sec)
# get some results
area = sec.get_area()
print(f"Area = {area:.0f} mm²")
print(f"Expected Area = {d * b:.0f} mm²")

# %% centroids
help(sec.get_c)
cx, cy = sec.get_c()
print(f"Centroid = ({cx:.0f}, {cy:.0f}) mm")

from scipy import integrate

dir(integrate)
help(integrate.quad)

integrate.quad(lambda x, depth: depth * x, 0, b, args=(d,)) / area
integrate.quad(lambda y, base: base * y, 0, d, args=(b,)) / area

# %%  cross-sec centroidal second moments of area.
help(sec.get_ic)
ixx_c, iyy_c, ixy_c = sec.get_ic()
print(f"Ixx = {ixx_c:.0f} mm⁴, Iyy = {iyy_c:.0f} mm⁴")
print(f"Ixy = {ixy_c:.0f} mm⁴")

# %% Second moments of area about the global axis
dir(sec)
help(sec.get_ig)
(ixx_g, iyy_g, ixy_g) = sec.get_ig()
print(f"Ixx_g = {ixx_g:.0f} mm⁴, Iyy_g = {iyy_g:.0f} mm⁴")
print(f"Ixy_g = {ixy_g:.0f} mm⁴")

print(f"Ixx_c + A*cy^2 = {ixx_c + area * sec.section_props.cy ** 2:.0f} mm⁴, Ixx_g = {ixx_g:.0f} mm⁴")
print(f"Iyy_c + A*cx^2 = {iyy_c + area * sec.section_props.cx ** 2:.0f} mm⁴, Iyy_g = {iyy_g:.0f} mm⁴")

# %% one dimensional integrals about the global axis
from scipy import integrate

dir(integrate)
help(integrate.quad)
ixx_g_num, err = integrate.quad(lambda y: b * y ** 2, 0, d)
print(f"Numerical Ixx_g = {ixx_g_num:.0f} mm⁴, Error = {err:.0f} mm⁴")

iyy_g_num, err = integrate.quad(lambda x: d * x ** 2, 0, b)
print(f"Numerical Iyy_g = {iyy_g_num:.0f} mm⁴, Error = {err:.0f} mm⁴")

# %% two dimensional integrals

help(integrate.dblquad)
f = lambda y, x: x * y

ixy_g_num, err = integrate.dblquad(f, 0, b, 0, d)
print(f"Numerical Ixy_g = {ixy_g_num:.0f} mm⁴, Error = {err:.0f} mm⁴")
cx * cy * area
# %%

# %% 2. Define a material
steel = Material(
    name="S355",
    elastic_modulus=200e9,  # Pa
    poissons_ratio=0.3,
    yield_strength=355e6,  # Pa
    density=7850,  # kg/m^3
    color="lightgrey",
)
print(steel)

# %% 3. Create a rectangular section
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

# %% 4. Create a more realistic steel I-section
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

# %% 5. Plot the geometry
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