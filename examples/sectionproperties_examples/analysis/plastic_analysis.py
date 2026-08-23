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
# # Plastic Analysis

# %% [markdown]
# This example demonstrates how to perform a plastic analysis in `sectionproperties`.

# %% [markdown]
# ## Create Geometry and Section
#
# A monosymmetric I-section will be analysed, first we construct the geometry of the 200 mm deep section.

# %%
from sectionproperties.pre.library import mono_i_section

geom = mono_i_section(d=200, b_t=50, b_b=100, t_ft=12, t_fb=8, t_w=6, r=8, n_r=8)

# %% [markdown]
# Like geometric analyses, plastic analyses in `sectionproperties` are mesh independent.

# %%
from sectionproperties.analysis import Section

geom.create_mesh(mesh_sizes=0)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# ## Perfom Plastic Analysis
#
# A plastic analysis first requires a geometric analysis to be performed. Let's see what happens if we try to first run a plastic analysis.

# %% editable=true slideshow={"slide_type": ""} tags=["raises-exception"]
sec.calculate_plastic_properties()

# %% [markdown]
# Now we run the geometric analysis first.

# %%
sec.calculate_geometric_properties()
sec.calculate_plastic_properties()

# %% [markdown]
# ## Plastic Analysis Results

# %% [markdown]
# We can visualise the plastic centroid by calling the `plot_centroids()` method.

# %%
sec.plot_centroids()

# %% [markdown]
# `sectionproperties` will calculate the plastic section moduli of the cross-section during a plastic analysis. Assuming this section is made from steel ($f_y = 250$ MPa) and there are no local instabilities, we can compare the yield and plastic capacity of the cross-section.

# %%
fy = 250  # yield stress in MPa

# calculate yield moment for the top & bottom flanges
my_t = fy * sec.get_z()[0]
my_b = fy * sec.get_z()[1]

# calculate plastic moment about x-axis
mp = fy * sec.get_s()[0]

# print results
print(f"My_t = {my_t / 1e6:.1f} kN.m")
print(f"My_b = {my_b / 1e6:.1f} kN.m")
print(f"Mp = {mp / 1e6:.1f} kN.m")

# %% [markdown]
# Thus, the section will yield about it's top flange first at 36.4 kN.m. The plastic capacity of the section is reached at 46.2 kN.m (i.e. the entire cross-section is at yield stress).

# %% [markdown]
# The shape factors, i.e. the ratio between the plastic and elastic section moduli, can also be obtained.

# %%
print(f"SF_t = {sec.get_sf()[0]:.2f}")
print(f"SF_b = {sec.get_sf()[1]:.2f}")

# %% [markdown]
# ## Principal Axis Bending
#
# Plastic section analysis about principal bending axes are also computed. As angle section is analysed to demonstrate the difference between global and principal axis bending.

# %%
from sectionproperties.pre.library import angle_section

geom = angle_section(d=150, b=90, t=12, r_r=10, r_t=5, n_r=8)
geom.create_mesh(mesh_sizes=0)
sec = Section(geometry=geom)
sec.calculate_geometric_properties()
sec.calculate_plastic_properties()
sec.plot_centroids()

# %%
print(f"Sxx = {sec.get_s()[0]:.3e} mm3")
print(f"S11 = {sec.get_sp()[0]:.3e} mm3")
print(f"Syy = {sec.get_s()[1]:.3e} mm3")
print(f"S22 = {sec.get_sp()[1]:.3e} mm3")

# %% [markdown]
# As expected, the plastic section moduli about the 11-principal axis is larger than any about the global axes.
