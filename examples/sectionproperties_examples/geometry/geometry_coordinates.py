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
# # Geometry from Coordinates
#
# The following example demonstrates how geometry objects can be created from a list of points, facets, holes and control points. 
#
# A straight angle section with a plate at its base is created from a list of points and facets. 
#
# The bottom plate is assigned a separate control point meaning two discrete regions are created. Creating separate regions allows the user to control the mesh size in each region and assign material properties to different regions.

# %% [markdown]
# ## Import Modules
#
# We start by importing the [CompoundGeometry()](../../gen/sectionproperties.pre.geometry.CompoundGeometry.rst#sectionproperties.pre.geometry.CompoundGeometry) object to create the geometry, and the [Section()](../../gen/sectionproperties.analysis.section.rst#module-sectionproperties.analysis.section) object for analysis.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre import CompoundGeometry

# %% [markdown]
# ## Create Geometry
#
# We will define some parameters that describe the geometry of the section.

# %%
w_a = 1  # width of angle leg
w_p = 2  # width of bottom plate
d = 2  # depth of section
t = 0.1  # thickness of section

# %% [markdown]
# We can now build a list of points, facets and control points.

# %%
# list of points describing the geometry
points = [
    (w_p * -0.5, 0),  # bottom plate
    (w_p * 0.5, 0),
    (w_p * 0.5, t),
    (w_p * -0.5, t),
    (t * -0.5, t),  # inverted angle section
    (t * 0.5, t),
    (t * 0.5, d - t),
    (w_a - 0.5 * t, d - t),
    (w_a - 0.5 * t, d),
    (t * -0.5, d),
]

# list of facets (edges) describing the geometry connectivity
facets = [
    (0, 1),  # bottom plate
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),  # inverted angle section
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 4),
]

# list of control points (points within each region)
control_points = [
    (0, t * 0.5),  # bottom plate
    (0, d - t),  # inverted angle section
]

# %% [markdown]
# We can now use the [CompoundGeometry.from_points()](../../gen/sectionproperties.pre.geometry.CompoundGeometry.rst#sectionproperties.pre.geometry.CompoundGeometry.from_points) method to build our geometry. We use the ``CompoundGeometry`` variation of this method as we have two distinct regions. If there was only one region (i.e. one control point), we would use the ``Geometry`` version of this method.

# %%
geom = CompoundGeometry.from_points(
    points=points,
    facets=facets,
    control_points=control_points,
)
geom.plot_geometry();

# %% [markdown]
# ## Create Mesh and ``Section``
#
# For this mesh, we use a smaller refinement for the bottom plate region.

# %%
geom.create_mesh(mesh_sizes=[0.0005, 0.001])

sec = Section(geometry=geom)
sec.plot_mesh(materials=False);

# %% [markdown]
# ## Perform an Analysis
#
# We perform geometric, warping and plastic analyses.

# %%
sec.calculate_geometric_properties()
sec.calculate_warping_properties()
sec.calculate_plastic_properties()

# %% [markdown]
# ## Plot Centroids
#
# We can plot the calculated centroids using the [plot_centroids()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section.plot_centroids) method.

# %%
sec.plot_centroids();

# %% [markdown]
# Because we performed geometric, warping and plastic analyses we see the following results in the above plot:
#
# - Geometric analysis - elastic centroid, principal axes
# - Warping analysis - shear centre
# - Plastic analysis - plastic centroids
