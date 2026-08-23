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
# # Advanced Geometry Creation
#
# The below tutorial was created to demonstrate the creation of valid geometries for cross-section analysis by combining multiple shapes.
#
# Some key points to remember:
#
# 1. Geometries of two *different* materials should not overlap (this can create unpredictable results).
# 2. If two geometries of the *same* material are overlapping, then you should perform a union on the two sections.
# 3. Two different section geometries that share a common edge (facet) should also share the same nodes (do not leave "floating" nodes along common edges).
#
# These are general points to remember for any finite element analysis.

# %% [markdown]
# <div class="alert alert-warning">
#     
# ``sectionproperties`` will not prevent the creation of these ambiguous sections. The flexibility of ``shapely`` allows for a wide variety of intermediate modelling steps but the user must ensure that the final model is one that is appropriate for analysis.
#
# </div>

# %% [markdown]
# ## Creating Merged Sections
#
# For this example, we will create a custom section out of two similar I-sections.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import i_section

i_sec1 = i_section(d=250, b=150, t_f=13, t_w=10, r=12, n_r=12)
i_sec2 = i_sec1.rotate_section(angle=45)

# %%
i_sec1

# %%
i_sec2

# %% [markdown]
# Assign a unique material to each geometry.

# %%
from sectionproperties.pre import Material

# just some differing properties
mat1 = Material(
    name="Material_1",
    elastic_modulus=200e3,
    poissons_ratio=0.3,
    yield_strength=100,
    density=400,
    color="gold",
)
mat2 = Material(
    name="Material_2",
    elastic_modulus=150e3,
    poissons_ratio=0.2,
    yield_strength=100,
    density=200,
    color="blue",
)

i_sec1.material = mat1
i_sec2.material = mat2

# %% [markdown]
# Now, we can use the ``+`` operator to naively combine these two sections into a [CompoundGeometry()](../../gen/sectionproperties.pre.geometry.CompoundGeometry.rst#sectionproperties.pre.geometry.CompoundGeometry). Note, the two different materials.

# %%
i_sec1 + i_sec2

# %% [markdown]
# When we plot the geometry, we will see that even though we have two materials, the control points coincide with one another.

# %%
(i_sec1 + i_sec2).plot_geometry()

# %% [markdown]
# If we went a few steps further by creating a mesh and then plotting that mesh as part of an analysis section, we would see the unpredictable result of the mesh.

# %%
Section(geometry=(i_sec1 + i_sec2).create_mesh(mesh_sizes=[10])).plot_mesh()

# %% [markdown]
# ## Preventing Ambiguity
#
# To prevent ambiguity between geometries and their analytical regions, there are a few options we can take.
#
# We can perform a simple union operation, but that will lose the material information for one of our sections - whichever section comes first in the operation will have it's information preserved.
#
# In this example, we will use a ``|`` (union) with ``i_sec2`` taking precedence by being the first object in the operation.

# %%
i_sec2 | i_sec1

# %% [markdown]
# However, this is unsatisfactory as a solution. We want this section to more aptly represent a real section that might be created by cutting and welding two sections together.
#
# Lets say we want the upright I-section to be our main section and the diagonal section will be added on to it.
#
# It is sometimes possible to do this in a quick operation, one which does not create nodes in common at the intersection points.
#
# Here, we will simply "slice" ``i_sec2`` with ``i_sec1`` and add it to ``i_sec1``. This will create "floating nodes" along the common edges of ``i_sec2`` and ``i_sec1`` because the nodes are not a part of ``i_sec1``.

# %%
((i_sec2 - i_sec1) + i_sec1).plot_geometry()

# %% [markdown]
# Sometimes, we can get away with this as in this example. We can see in the plot that there are five distinct regions indicated with five control points.
#
# When we are "unlucky", sometimes gaps can be created (due to floating point errors) where the two sections meet and a proper hole might not be detected, resulting in an incorrect section.

# %% [markdown]
# ## Creating Nodes in Common
#
# It is best practice to *first* create nodes in common on both sections and *then* combine them. For this, an extra step is required.

# %%
cut_2_from_1 = i_sec1 - i_sec2  # locates intersection nodes
sec_1_nodes_added = cut_2_from_1 | i_sec1

# this can also be done in one line
sec_1_nodes_added = (i_sec1 - i_sec2) | i_sec1

# %% [markdown]
# Now, when we use [plot_geometry()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.plot_geometry), we can see the additional nodes added to "section 1".

# %%
sec_1_nodes_added.plot_geometry()

# %% [markdown]
# The additional nodes from the cut portion are now merged as part of the "section 1" geometry.
#
# At this point, we can use our "section 1 with additional nodes" to create our complete geometry.

# %%
analysis_geom = (i_sec2 - i_sec1) + sec_1_nodes_added
analysis_geom.plot_geometry()

# %% [markdown]
# And when we create our mesh and analysis section...

# %%
analysis_geom.create_mesh(mesh_sizes=[10])
analysis_sec = Section(geometry=analysis_geom)
analysis_sec.plot_mesh()

# %% [markdown]
# we can see that the mesh represents how we expect the section to be.

# %% [markdown]
# ## Avoiding Meshing Errors
#
# Here, we will simply combine two squares with the default material.

# %%
from sectionproperties.pre.library import rectangular_section

s1 = rectangular_section(d=1, b=1)
s2 = rectangular_section(d=0.5, b=0.5).shift_section(x_offset=1, y_offset=0.25)
geom = s1 + s2
geom

# %% [markdown]
# From the ``shapely`` vector representation, we can see that the squares are shaded red.
# This indicates an ["invalid" geometry from shapely's perspective](https://shapely.readthedocs.io/en/stable/manual.html#polygons) because there are two polygons that share an edge. For this geometry, the intention is to have two squares that are connected on one side and so the red shading provided by the ``shapely`` representation tells us that we are getting what we expect.
#
# Now, say this is not our final geometry and we actually want to have it rotated by 30 degrees.

# %%
geom = geom.rotate_section(angle=30)
geom

# %% [markdown]
# Here, the ``shapely`` representation may show as green, indicating a "valid" ``shapely`` geometry, or red as previous. This 
# uncertainty is due to floating point errors originating from the rotation, potentially causing these two polygons no longer share an edge.
#
# If we try to mesh this geometry, we may actually cause a crash with ``CyTriangle``, the meshing tool used behind-the-scenes by ``sectionproperties``.

# %%
# this may crash the kernel...
# geom.create_mesh(mesh_sizes=[0.2, 0.1])

# %% [markdown]
# The crash occurs because the distance between the two polygons is so small. Even though the shapes are separated, the space between them will not be able to be meshed. The same crash would occur if the polygons were overlapping by this same small distance.
#
# If we plot the geometry, we can see that each of the two squares has only four nodes and four facets and their relationship is only incidental. If their edges happen to perfectly align, they will be considered as one continuous section. If their edges do not perfectly align, they will be considered as discontinuous.

# %%
geom.plot_geometry(labels=("points", "facets", "control_points"))

# %% [markdown]
# To remedy this, take the same approach as in the preceding example by creating intermediate nodes where the two polygons intersect by using set operations. If we subtract ``s2`` from ``s1`` then we will have the larger square with intermediate nodes created.

# %%
(s1 - s2).plot_geometry(labels=("points",))

# %% [markdown]
# Now, if we build the compound geometry up from this larger square with the intermediate points, then our section will work.

# %%
geom_fixed = (s1 - s2) + s2
geom_fixed_rotated = geom_fixed.rotate_section(angle=30)
geom_fixed_rotated.create_mesh(mesh_sizes=[0.2, 0.1])
geom_fixed_rotated.plot_geometry(
    labels=(
        "points",
        "facets",
    ),
)
sec = Section(geometry=geom_fixed_rotated)
sec.display_mesh_info()

# %% [markdown]
# ## Creating Nested Geometries
#
# This example demonstrates creating nested geometries using two different approaches. These approaches reflect the differences between how ``shapely`` (geometry pre-processor) "perceives" geometry, how ``CyTriangle`` (meshing tool) "perceives" geometry, and how the modeller might adapt their input style depending on the situation.
#
# The nested geometry we are trying to create consists of three concentric squares with a hole at it's centre.
#
# In creating this geometry consider the following:
#
# - ``shapely`` has a concept of "z-ordering" where it is possible for one geometry to be "over" another geometry and for an overlap section to exist. When a hole is created in a polygon, it is only local to that polygon.

# %%
sq1 = rectangular_section(d=80, b=80, material=mat1).align_center()
sq2 = rectangular_section(d=100, b=100, material=mat2).align_center()
sq2 = sq2 - sq1
sq2 = sq2.shift_section(x_offset=-50, y_offset=-50).rotate_section(angle=30)

sq1 + sq2

# %% [markdown]
# - ``CyTriangle`` does not have a concept of "z-ordering" so there is only a single plane which may have regions of different materials (specified with control points). When a hole is created in the plane, it "punches" through "all" polygons in the plane.

# %%
# note the order in which the geometry is combined
Section(geometry=(sq2 + sq1).create_mesh(mesh_sizes=[5, 10])).plot_mesh()
Section(geometry=(sq1 + sq2).create_mesh(mesh_sizes=[5, 10])).plot_mesh()

# %% [markdown]
# To create the nested geometry using ``shapely``, the code would be as follows.

# %%
mat3 = Material(
    name="Material 3",
    elastic_modulus=100,
    poissons_ratio=0.3,
    yield_strength=10,
    density=1e-6,
    color="red",
)

sq1 = rectangular_section(d=100, b=100, material=mat1).align_center()
sq2 = rectangular_section(d=75, b=75, material=mat2).align_center()
sq3 = rectangular_section(d=50, b=50, material=mat3).align_center()
hole = rectangular_section(d=25, b=25).align_center()

compound = (
    (sq1 - sq2)  # create a big square with a medium hole in it and stack it over...
    + (sq2 - sq3)  # a medium square with a medium-small hole in it and stack it over...
    + (sq3 - hole)  # a medium-small square with a small hole in it.
)

compound

# %% [markdown]
# To create the nested geometry using the ``CyTriangle`` interface, the code would be as follows:

# %%
from sectionproperties.pre import CompoundGeometry

# points for four squares are created
points = [
    [-50.0, 50.0],  # square 1
    [50.0, 50.0],
    [50.0, -50.0],
    [-50.0, -50.0],
    [37.5, -37.5],  # square 2
    [37.5, 37.5],
    [-37.5, 37.5],
    [-37.5, -37.5],
    [25.0, -25.0],  # square 3
    [25.0, 25.0],
    [-25.0, 25.0],
    [-25.0, -25.0],
    [12.5, -12.5],  # square 4 (hole)
    [12.5, 12.5],
    [-12.5, 12.5],
    [-12.5, -12.5],
]

# facets trace each of the four squares
facets = [
    [0, 1],  # square 1
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],  # square 2
    [5, 6],
    [6, 7],
    [7, 4],
    [8, 9],  # square 3
    [9, 10],
    [10, 11],
    [11, 8],
    [12, 13],  # square 4 (hole)
    [13, 14],
    [14, 15],
    [15, 12],
]

# three squares
control_points = [[-43.75, 0.0], [-31.25, 0.0], [-18.75, 0.0]]
holes = [[0, 0]]

nested_compound = CompoundGeometry.from_points(
    points=points,
    facets=facets,
    control_points=control_points,
    holes=holes,
    materials=[mat1, mat2, mat3],
)

nested_compound

# %% [markdown]
# Notice how the ``shapely`` representation shows the squares overlapping each other instead of the squares fitting into the "hole below".
#
# Is one of these methods better than the other? Not necessarily. The ``shapely`` approach is suitable for manually creating the geometry, whereas the ``CyTriangle`` approach is suitable for reading in serialised data from a file, for example.
#
# And, for either case, when the compound geometry is meshed, we see this:

# %%
Section(geometry=compound.create_mesh(mesh_sizes=5)).plot_mesh()
Section(geometry=nested_compound.create_mesh(mesh_sizes=5)).plot_mesh()
