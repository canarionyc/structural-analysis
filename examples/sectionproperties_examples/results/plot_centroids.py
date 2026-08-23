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
# # Plot Centroids

# %% [markdown]
# This example demonstrates how to plot centroids in `sectionproperties`.
#
# The `plot_centroids()` method will display a plot of the finite element mesh along with any centroids that have been calculated:
#
# - Geometric analysis - geometric centroid and principal axes
# - Warping analysis - shear centre
# - Plastic analysis - plastic centroid

# %% [markdown]
# This example will plot the centroids for a 200 mm deep and 12 mm thick bulb section with a 10 mm radius.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import bulb_section

geom = bulb_section(d=200, b=50, t=12, r=10, n_r=8)
geom.create_mesh(mesh_sizes=20)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# ## Geometric Analysis

# %%
sec.calculate_geometric_properties()
sec.plot_centroids()

# %% [markdown]
# ## Warping Analysis
#
# Note that the title and transparency can be changed by specifying `title` and `alpha` respectively.

# %%
sec.calculate_warping_properties()
sec.plot_centroids(title="Geometric & Warping Centroids", alpha=0.2)

# %% [markdown]
# ## Plastic Analysis

# %%
sec.calculate_plastic_properties()
sec.plot_centroids()
