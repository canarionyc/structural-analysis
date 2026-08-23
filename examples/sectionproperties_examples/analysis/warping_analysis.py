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
# # Warping Analysis

# %% [markdown]
# This example demonstrates how to perform a warping analysis in `sectionproperties`.

# %% [markdown]
# ## Channel Section
#
# This example will conduct a warping analysis on a 250PFC section.
#
# First we create the cross-section geometry.

# %%
from sectionproperties.pre.library import channel_section

geom = channel_section(d=250, b=90, t_f=15, t_w=8, r=12, n_r=8)

# %% [markdown]
# Next we must create a finite element mesh and a `Section` object. Unlike geometric and plastic analyses, the warping results are mesh dependent. As a general rule of thumb, we would like all plate sections to be at least several elements thick in order to resolve the variations in the warping and shear functions.

# %%
from sectionproperties.analysis import Section

geom.create_mesh(mesh_sizes=7)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# We can now perform the warping analysis by calling `calculate_warping_properties()`, note that a geometric analysis must be performed first. We also compare the `"direct"` solver with the `"cgs"` solver for speed.

# %%
import time

sec.calculate_geometric_properties()

# direct solver
start = time.time()
sec.calculate_warping_properties(solver_type="direct")
end = time.time()
print(f"Direct Solver Time = {end - start:.4f} secs")

# cgs solver
start = time.time()
sec.calculate_warping_properties(solver_type="cgs")
end = time.time()
print(f"CGS Solver Time = {end - start:.4f} secs")

# %% [markdown]
# We can plot the centroids to display the geometric centroid and shear centre using `plot_centroids()`.

# %% nbsphinx-thumbnail={"output-index": 0}
sec.plot_centroids()

# %% [markdown]
# We can also obtain the some relevant warping properties:
#
# - `J` - torsion constant
# - `Iw`/`Gamma` - warping constant
# - `As_y` - shear area for loading along the y-axis

# %%
print(f"J = {sec.get_j():.3e} mm4")
print(f"Iw = {sec.get_gamma():.3e} mm6")
print(f"As_y = {sec.get_as()[1]:.1f} mm2")

# %% [markdown]
# ## Unconnected Sections

# %% [markdown]
# Unlike geometric and plastic analysis, cross-sections analysed for warping must have strict connectivity. `sectionproperties` checks for connectivity prior to conducting a warping analysis and will throw an error if there is not full connectivity between all regions of the mesh.

# %%
from sectionproperties.pre.library import rectangular_section

# create an unconnected mesh
rect = rectangular_section(d=10, b=10)
geom = rect + rect.shift_section(x_offset=20)
geom.create_mesh(mesh_sizes=1)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %%
# geometric and plastic analyses can be conducted
sec.calculate_geometric_properties()
sec.calculate_plastic_properties()

# %% editable=true slideshow={"slide_type": ""} tags=["raises-exception"]
# warping analysis will fail
sec.calculate_warping_properties()
