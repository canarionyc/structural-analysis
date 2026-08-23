# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Retrieving Section Properties

# %% [markdown]
# This example demonstrates how to retrieve cross-section properties in `sectionproperties`. It is suggested that you are familiar with [How Material Properties Affect Results](../../user_guide/results.rst#how-material-properties-affect-results) before reading this example.

# %% [markdown]
# ## Geometric-only Properties
#
# This section retrieves the frame properties for a 150 x 100 x 8 UA stiffened by a 125 x 12 plate at its base.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import angle_section, rectangular_section

angle = angle_section(d=150, b=100, t=8, r_r=12, r_t=5, n_r=8)
plate = rectangular_section(d=12, b=125)
geom = angle + plate.shift_section(x_offset=-12.5, y_offset=-12)
geom.create_mesh(mesh_sizes=[10, 25])
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# We can perform a frame analysis and use the various `get` methods to retrieve the cross-section properties required for a frame analysis.

# %%
sec.calculate_frame_properties()
area = sec.get_area()
ixx_c, iyy_c, ixy_c = sec.get_ic()
phi = sec.get_phi()
j = sec.get_j()

# %%
print(f"Area = {area:.1f} mm2")
print(f"Ixx = {ixx_c:.3e} mm4")
print(f"Iyy = {iyy_c:.3e} mm4")
print(f"Ixy = {ixy_c:.3e} mm4")
print(f"Principal axis angle = {phi:.1f} deg")
print(f"Torsion constant = {j:.3e} mm4")

# %% [markdown]
# ## Composite Properties
#
# To demonstrate how to retrieve cross-section properties from a composite analysis, a reinforced concrete beam will be modelled.
#
# First we create our concrete and steel material properties.

# %%
from sectionproperties.pre import Material

concrete = Material(
    name="Concrete",
    elastic_modulus=30.1e3,
    poissons_ratio=0.2,
    yield_strength=32,
    density=2.4e-6,
    color="lightgrey",
)
steel = Material(
    name="Steel",
    elastic_modulus=200e3,
    poissons_ratio=0.3,
    yield_strength=500,
    density=7.85e-6,
    color="grey",
)

# %% [markdown]
# Next we define our reinforced concrete geometry, generate a mesh and a `Section` object.

# %%
from sectionproperties.pre.library import concrete_rectangular_section

geom = concrete_rectangular_section(
    d=600,
    b=300,
    dia_top=16,
    area_top=200,
    n_top=3,
    c_top=20,
    dia_bot=20,
    area_bot=310,
    n_bot=3,
    c_bot=30,
    n_circle=8,
    conc_mat=concrete,
    steel_mat=steel,
)

geom.create_mesh(mesh_sizes=2500)
sec = Section(geometry=geom)
sec.plot_mesh()

# %% [markdown]
# In this case, we are interested in obtaining the uncracked axial rigidity, flexural rigidity and torsional rigidity. We will therefore conduct a frame analysis.

# %%
props = sec.calculate_frame_properties()

# %% [markdown]
# Note that we cannot retrieve the geometric second moments of area as in the previous example because we have conducted a composite analysis (i.e. provided material properties).

# %% editable=true slideshow={"slide_type": ""} tags=["raises-exception"]
sec.get_ic()

# %% [markdown]
# The above error message is helpful, informing us that we should instead use `get_eic()`.

# %%
# get relevant modulus weighted properties
eixx, _, _ = sec.get_eic()
ea = sec.get_ea()
ej = sec.get_ej()

# print results
print(f"Axial rigidity (E.A): {ea:.3e} N")
print(f"Flexural rigidity (E.I): {eixx:.3e} N.mm2")

# note we are usually interested in G.J not E.J
# geometric analysis required for effective material properties
sec.calculate_geometric_properties()
gj = sec.get_g_eff() / sec.get_e_eff() * ej
print(f"Torsional rigidity (G.J): {gj:.3e} N.mm2")

# %% [markdown]
# Note that transformed cross-section properties are often required for design purposes. We can use the `e_ref` argument to provide either a material of elastic modulus to obtain transformed properties in `sectionproperties`.

# %%
print(f"E.I = {eixx:.3e} N.mm2")
print(f"I = {sec.get_eic(e_ref=concrete)[0]:.3e} mm4")
print(f"I = {sec.get_eic(e_ref=30.1e3)[0]:.3e} mm4")

# %% [markdown]
# Note that the transformed second moment of area includes the contribution of the steel and is therefore larger than that of a 600D x 300W rectangle.

# %%
print(f"I_rect = {300 * 600**3 / 12:.3e} mm4")

# %% [markdown]
# Finally, we can print the transformed section properties using the `display_transformed_results()` method.

# %%
sec.display_transformed_results(e_ref=concrete, fmt=".3e")
