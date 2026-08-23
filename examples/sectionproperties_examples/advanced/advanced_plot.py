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
# # Advanced Plotting

# %% [markdown]
# All plots in `sectionproperties` allow keyword arguments to be passed to [plotting_context()](../..//gen/sectionproperties.post.post.plotting_context.rst#sectionproperties.post.post.plotting_context). This example shows one application of using the `plotting_context()` to generate a custom plot in a 2 x 2 arrangement.

# %% [markdown]
# ## Create Geometry and Perform Analysis

# %% [markdown]
# We start by creating the geometry for a 100 x 6 SHS.

# %%
from sectionproperties.pre.library import rectangular_hollow_section

geom = rectangular_hollow_section(d=100, b=100, t=6, r_out=15, n_r=8)

# %% [markdown]
# Next we create a mesh and a `Section` object.

# %%
from sectionproperties.analysis import Section

geom.create_mesh(mesh_sizes=[5])
sec = Section(geometry=geom)

# %% [markdown]
# We can now perform a stress analysis by applying a 10 kN.m torsion (after first running the geometric and warping analysis).

# %%
sec.calculate_geometric_properties()
sec.calculate_warping_properties()
stress = sec.calculate_stress(mzz=10e6)

# %% [markdown]
# ## Generate Plot
#
# We are going to generate a plot of the geometry, mesh, centroids and stress. In the first plot, we will setup the parameters of the entire figure. We make sure we set `render=False` to prevent the plot from displaying before we are finished. In the subsequent plots we pass the axis we would like to display the plot on.

# %%
import matplotlib.pyplot as plt

# plot the geometry
ax = geom.plot_geometry(
    labels=[],
    nrows=2,
    ncols=2,
    figsize=(12, 7),
    render=False,
)

# get the figure object from the first plot
fig = ax.get_figure()

# plot the mesh
sec.plot_mesh(materials=False, ax=fig.axes[1])

# plot the centroids
sec.plot_centroids(ax=fig.axes[2])

# plot the torsion stress
stress.plot_stress(
    stress="mzz_zxy",
    normalize=False,
    ax=fig.axes[3],
)

# finally display the plot
plt.show()
