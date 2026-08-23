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
# # Stress Analysis

# %% [markdown]
# This example demonstrates how to perform a stress analysis in `sectionproperties`.

# %% [markdown]
# In this example we model a 150 x 100 x 6 RHS and subject it to various load cases.

# %% [markdown]
# ## Create Geometry and Section

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import rectangular_hollow_section

geom = rectangular_hollow_section(d=100, b=150, t=6, r_out=15, n_r=8)
geom.create_mesh(mesh_sizes=[2])
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# ## Geometric and Warping Analysis
#
# Because we will be subjecting this box section to torsion and shear, we must first conduct a geometric and warping analysis.

# %%
sec.calculate_geometric_properties()
sec.calculate_warping_properties()

# %% [markdown]
# ## Perform Stress Analysis
#
# The first load case applies the following loads:
#
# - Mxx = 5 kN.m
# - Vy = -10 kN
# - Mzz = 3 kN.m
#
# The second load case applies the following loads:
#
# - Myy = 15 kN.m
# - Vx = 30 kN
# - Mzz = 1.5 kN.m

# %%
case1 = sec.calculate_stress(mxx=5e6, vy=-10e3, mzz=3e6)
case2 = sec.calculate_stress(myy=15e6, vx=30e3, mzz=1.5e6)

# %% [markdown]
# ## Plot Streses
#
# `case1` and `case2` obtained from the stress analysis are [StressPost()](../../gen/sectionproperties.post.stress_post.StressPost.rst#sectionproperties.post.stress_post.StressPost) objects. We can plot stresses by using the `plot_stress()` and `plot_stress_vector()` methods that belongs to this object.

# %% [markdown]
# ### Case 1

# %%
# bending stress
case1.plot_stress(stress="m_zz")

# %%
# torsion stress vectors
case1.plot_stress_vector(stress="mzz_zxy")

# %%
# von mises stress
case1.plot_stress(stress="vm", cmap="YlOrRd", normalize=False)

# %% [markdown]
# ### Case 2

# %%
# shear stress
case2.plot_stress(stress="v_zxy")

# %%
# von mises stress
case2.plot_stress(stress="vm", cmap="YlOrRd", normalize=False)

# %% [markdown]
# Note that the colormap can be changed using one of those specified [here](https://matplotlib.org/stable/users/explain/colors/colormaps.html). Sequential colormaps are arguably more suited to examining von Mises stresses (always positive), whereas diverging colormaps are more insightful for stresses that can be positive and negative.
#
# The `normalize=True` argument places the centre of the colormap at zero stress.
