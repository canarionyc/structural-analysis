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
# # Creating Meshes
#
# This example demonstrates how a finite element mesh can be generated with ``sectionproperties``.

# %% [markdown]
# ## Import Modules
#
# We start by importing the necessary modules.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre import CompoundGeometry
from sectionproperties.pre.library import (
    box_girder_section,
    rectangular_hollow_section,
    rectangular_section,
)

# %% [markdown]
# ## Simple Mesh
#
# A mesh of a rectangle is created. The value provided to ``mesh_sizes`` is used to limit the maximum triangular area to this value.

# %%
geom = rectangular_section(d=50, b=50)
geom.create_mesh(mesh_sizes=10)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# We can find the maximum element size by looping through all the elements and computing the area of each element.

# %%
# initialise maximum area
max_area = 0

# loop through all finite elements
for el in sec.elements:
    res = el.geometric_properties()  # calculate area properties
    el_area = res[0]  # get the area
    max_area = max(max_area, el_area)  # update max_area

print(f"Max. triangular area = {max_area:.2f}")

# %% [markdown]
# ## Specifying Multiple ``mesh_sizes``
#
# This example creates a 100 x 9 SHS and shows how the mesh can be refined in specific regions.

# %%
shs = rectangular_hollow_section(d=100, b=100, t=9, r_out=22.5, n_r=8)

# %% [markdown]
# We will split the SHS geometry into corner regions and straight regions.

# %%
# vertical split at left hand corner
g1, g2 = shs.split_section(point_i=(22.5, 0), vector=(0, 1))
shs = CompoundGeometry(geoms=g1 + g2)  # reform geometry

# vertical split at right hand corner
g1, g2 = shs.split_section(point_i=(77.5, 0), vector=(0, 1))
shs = CompoundGeometry(geoms=g1 + g2)  # reform geometry

# vertical split at bottom corner
g1, g2 = shs.split_section(point_i=(0, 22.5), vector=(1, 0))
shs = CompoundGeometry(geoms=g1 + g2)  # reform geometry

# vertical split at top corner
g1, g2 = shs.split_section(point_i=(0, 77.5), vector=(1, 0))

# %% [markdown]
# We will combine the final geometry by sorting the list of split geometries objects. This will allow us to easily control the mesh size of each region. We will sort the geometry list by the ``y`` value of each geometry's control point.

# %%
geom_list = g1 + g2
geom_list.sort(key=lambda x: x.control_points[0][1])
shs = CompoundGeometry(geoms=geom_list)
shs.plot_geometry()

# %% [markdown]
# As shown above, regions 0, 3, 4 and 7 are the straight segments, while regions 1, 2, 5 and 6 are the corner segments.

# %% [markdown]
# We can generate a mesh with a constant maximum area across all regions by providing only one value to ``mesh_sizes``.

# %%
shs.create_mesh(mesh_sizes=5)
Section(geometry=shs).plot_mesh(materials=False)

# %% [markdown]
# Alternatively, we can specify a maximum area for each region. Note that providing a zero provides no constraint on the maximum area.

# %% nbsphinx-thumbnail={"output-index": 0}
mesh_sizes = [2.5, 1, 1, 5, 5, 2, 2, 0]

shs.create_mesh(mesh_sizes=mesh_sizes)
Section(geometry=shs).plot_mesh(materials=False)

# %% [markdown]
# ## Modifying the Minimum Angle
#
# We can change the minimum mesh vertex angle by specifying a value for `min_angle`, by default this is set to 30 degrees. Note that reducing the minimum angle will reduce the mesh quality, but may solve issues with the mesh algorithm not converging. See [here](https://www.cs.cmu.edu/~quake/triangle.q.html) for more information. Setting this value to number greater than 33 may cause issues with the meshing algorithm not converging.

# %%
geom.create_mesh(mesh_sizes=30, min_angle=33)
Section(geom).plot_mesh(materials=False)
geom.create_mesh(mesh_sizes=30, min_angle=5.7)
Section(geom).plot_mesh(materials=False)

# %% [markdown]
# ## Generating a ``coarse`` mesh

# %% [markdown]
# By setting the argument ``coarse=True``, all quality, area and angle constraints are ignored and a coarse mesh is generated. This can be useful if only geometric or plastic properties are desired (which are mesh independent). Note that if ``coarse=True``, the values provided to ``mesh_sizes`` and ``min_angle`` will be ignored.
#
# The following example compares the mesh generated for a box girder section, with and without quality constraints.

# %%
box = box_girder_section(d=1200, b_t=1200, b_b=400, t_ft=100, t_fb=80, t_w=50)

# %%
box.create_mesh(mesh_sizes=0)
Section(geometry=box).plot_mesh(materials=False)

# %%
box.create_mesh(mesh_sizes=0, coarse=True)
Section(geometry=box).plot_mesh(materials=False)
