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
# # Composite Analysis

# %% [markdown]
# This example highlights how material properties allow composite analysis in `sectionproperties`.

# %% [markdown]
# ## Geometric vs. Composite
#
# The default analysis type in `sectionproperties` is purely geometric, i.e. cross-section properties are reported based on the geometry only. In this analysis, all geometries are assigned the *default material*:

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import rectangular_section

rect_geom = rectangular_section(d=100, b=50)
rect_geom.material

# %% [markdown]
# The default material has a unit elastic modulus, yield strength and density, and a Poisson's ratio of zero.

# %% [markdown]
# Geometric-only analysis allows geometric properties to be obtained:

# %%
rect_geom.create_mesh(mesh_sizes=10)  # create mesh
rect_sec = Section(geometry=rect_geom)
rect_sec.calculate_geometric_properties()
ixx, iyy, ixy = rect_sec.get_ic()  # get second moments of area
print(f"Ixx = {ixx:.5e} mm4")

# %% [markdown]
# When a material property gets added to a geometry, the analysis becomes *composite*. 

# %%
from sectionproperties.pre import Material

# assign steel to the geometry
steel = Material(
    name="Steel",
    elastic_modulus=200e3,
    poissons_ratio=0.3,
    density=7.85e-6,
    yield_strength=500,
    color="grey",
)
rect_geom.material = steel

# recreate mesh and section
rect_geom.create_mesh(mesh_sizes=10)
rect_sec = Section(geometry=rect_geom)
rect_sec.calculate_geometric_properties()

# %% [markdown]
# Cross-section properties are now modulus weighted as the assumption is that there are multiple regions with multiple different material properties. We can no longer obtain geometric-only properties:

# %% editable=true slideshow={"slide_type": ""} tags=["raises-exception"]
ixx, iyy, ixy = rect_sec.get_ic()  # get second moments of area

# %% [markdown] editable=true slideshow={"slide_type": ""}
# In this case, we need to get the modulus weighted second moments of area. Note we can still extract geometric properties by using a reference elastic modulus.

# %%
# get modulus weighted second moments of area
eixx, eiyy, eixy = rect_sec.get_eic()
print(f"E.Ixx = {eixx:.5e} N.mm2")

# use reference elastic modulus to get transformed properties
ixx, iyy, ixy = rect_sec.get_eic(e_ref=steel)
print(f"Ixx = {ixx:.5e} mm4")

# %% [markdown]
# ## Steel-Timber Composite Section
#
# The following section models a composite timber floor and steel beam section. A universal steel beam (310UB40.4) is modelled with a 100D x 600W timber panel placed on its top flange.

# %% [markdown]
# ### Create the Materials

# %%
# create the steel material
steel = Material(
    name="Steel",
    elastic_modulus=200e3,
    poissons_ratio=0.3,
    density=7.85e-6,
    yield_strength=500,
    color="grey",
)

# create the timber material
timber = Material(
    name="Timber",
    elastic_modulus=8e3,
    poissons_ratio=0.35,
    yield_strength=20,
    density=0.78e-6,
    color="burlywood",
)

# %% [markdown]
# ### Create the Geometry

# %%
from sectionproperties.pre.library import i_section

# universal steel beam
ub = i_section(d=304, b=165, t_f=10.2, t_w=6.1, r=11.4, n_r=8, material=steel)

# timber floor panel
panel = rectangular_section(d=100, b=600, material=timber)
panel = panel.align_center(align_to=ub).align_to(other=ub, on="top")

# combine geometry
geom = ub + panel

# %% [markdown]
# ## Create Mesh and Section Object

# %%
# 10 mm2 mesh for UB, 500 mm2 mesh for timber
geom.create_mesh(mesh_sizes=[10, 500])
sec = Section(geometry=geom)
sec.plot_mesh()

# %% [markdown]
# ### Perform Analysis

# %%
sec.calculate_geometric_properties()
sec.calculate_warping_properties()
sec.calculate_plastic_properties()

# %% [markdown]
# ### Display Analysis Results

# %% [markdown]
# We can plot the various centroids found by the analyses.

# %%
sec.plot_centroids()

# %% [markdown]
# We can also print all the calculated section properties to the terminal, note that because have conducted a composite analysis, modulus weighted properties are displayed.

# %%
sec.display_results()

# %% [markdown]
# We can also get transformed properties by specifying a reference material.

# %%
ixx_timber, _, _ = sec.get_eic(e_ref=timber)
ixx_steel, _, _ = sec.get_eic(e_ref=steel)
print(f"Ixx,t = {ixx_timber:.3e} mm4")
print(f"Ixx,s = {ixx_steel:.3e} mm4")

# %% [markdown]
# Further, we can display the transformed results with respect to an elastic modulus by calling the `display_transformed_results()` method. Here we print the transformed section properties with respect to the timber.

# %%
sec.display_transformed_results(e_ref=timber)

# %% [markdown]
# A plastic analysis for composite sections will calculate plastic moments rather than plastic section moduli. The plastic moment assumes all geometry fibres reach the yield strength.

# %%
mp_xx, _ = sec.get_mp()
print(f"Mp = {mp_xx / 1e6:.1f} kN.m")

# %% [markdown]
# ### Stress Analysis

# %%
stress = sec.calculate_stress(n=-100e3, mxx=-120e6, vy=-75e3)

# %%
stress.plot_stress(stress="m_zz")

# %%
stress.plot_stress(stress="vm")

# %% [markdown]
# We can plot only a specific list of materials by including the `material_list` argument. In the above plot it is difficult to see the stress in the timber so we set `material_list=[timber]`.

# %%
stress.plot_stress(stress="vm", material_list=[timber])
