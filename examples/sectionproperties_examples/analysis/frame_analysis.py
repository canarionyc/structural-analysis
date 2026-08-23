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
# # Frame Analysis

# %% [markdown]
# This example demonstrates how to perform a frame analysis in `sectionproperties`.
#
# A `frame` analysis calculates only the cross-section properties required for a frame analysis:
#
# - Cross-section area
# - Second moments of area about the centroidal axis
# - Torsion constant
# - Principal axis angle
#
# As a result, it is significantly more efficient than conducting both `geometric` and `warping` analyses, which is ususally required to obtain the above results.

# %% [markdown]
# This example will analyse a 12-sided polygonal hollow section and compare the time taken for a typical warping analysis with that taken for a frame analysis.

# %% [markdown]
# ## Create Geometry and Section

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import polygon_hollow_section

geom = polygon_hollow_section(d=600, t=12, n_sides=12, r_in=20, n_r=8)
geom.create_mesh(mesh_sizes=20)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# ## Geometric and Warping Analysis
#
# First we can time how long it takes to perform a geometric and warping analysis.

# %%
import time

start = time.time()
sec.calculate_geometric_properties()
sec.calculate_warping_properties()
end = time.time()
gw_time = end - start

# %% [markdown]
# We can print the time taken and the torsion constant to compare results.

# %%
print(f"Geometric/Warping Time = {gw_time:.4f} secs")
print(f"J = {sec.get_j():.3e} mm4")

# %% [markdown]
# ## Frame Analysis
#
# Now we can time how long it takes to perform a frame analysis.

# %%
start = time.time()
sec.calculate_frame_properties()
end = time.time()
f_time = end - start

# %% [markdown]
# Again, we can print the time taken and the torsion constant.

# %%
print(f"Frame Time = {f_time:.4f} secs")
print(f"J = {sec.get_j():.3e} mm4")

# %% [markdown]
# By not calculating shear functions, shear & warping integrals etc. required for a full warping analysis, significant time is saved if the user only wants frame properties.
