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
# # Assigning Materials

# %% [markdown]
# This examples showcases how material properties can be assigned to geometries in `sectionproperties`.
#
# First we must import the [Material()](../../gen/sectionproperties.pre.pre.Material.rst#sectionproperties.pre.pre.Material) object.

# %%
from sectionproperties.pre import Material

# %% [markdown]
# Materials in `sectionproperties` require the following properties:
#
# - Name [`string`]
# - Elastic modulus [`float`]
# - Poisson's ratio [`float`]
# - Density (mass per unit volume) [`float`]
# - Yield strength [`float`]
# - Color (see [here](https://matplotlib.org/stable/gallery/color/named_colors.html) for a list of named colors) [`string`]

# %% [markdown]
# For example, the following creates a typical steel material, using consistent Newtown and millimetre units:

# %%
steel = Material(
    name="Steel",
    elastic_modulus=200e3,  # N/mm^2 (MPa)
    poissons_ratio=0.3,  # unitless
    density=7.85e-6,  # kg/mm^3
    yield_strength=500,  # N/mm^2 (MPa)
    color="grey",
)
print(steel)
# %% [markdown]
# The below examples highlight a number of ways materials can be assigned to geometries in `sectionproperties`.

# %% [markdown]
# ## Assign material to a `shapely` geometry
#
# The [Geometry()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry) constructor takes an optional material argument.

# %%
from shapely import Polygon

from sectionproperties.analysis import Section
from sectionproperties.pre import Geometry

# assign steel to a shapely polygon
poly = Polygon([(0, 0), (5, 2), (3, 7), (1, 6)])
geom = Geometry(geom=poly, material=steel)
geom.create_mesh(mesh_sizes=1)
Section(geometry=geom).plot_mesh()

# %% [markdown]
# ## Assign material to arbitrary geometry
#
# The [Geometry.from_points()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.from_points) method also takes an optional material argument.

# %%
# create list of points, facets and holes
points = [(0, 0), (10, 5), (15, 15), (5, 10), (6, 6), (9, 7), (7, 9)]
facets = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 4)]
control_points = [(4, 4)]
holes = [(7, 7)]

# create geometry object, specifying material
geom = Geometry.from_points(
    points=points,
    facets=facets,
    control_points=control_points,
    holes=holes,
    material=steel,
)
geom.create_mesh(mesh_sizes=1)
Section(geometry=geom).plot_mesh()

# %% [markdown]
# ## Assign material to geometry from the section library
#
# All methods in the [section library](../../gen/sectionproperties.pre.library.rst#module-sectionproperties.pre.library) take an optional material argument.

# %%
from sectionproperties.pre.library import polygon_hollow_section

geom = polygon_hollow_section(d=200, t=6, n_sides=8, r_in=20, n_r=12, material=steel)
geom.create_mesh(mesh_sizes=10)
Section(geometry=geom).plot_mesh()

# %% [markdown]
# ## Assigning a material after creating a geometry
#
# A geometry’s material may be altered at any time by simply assigning a new `Material` to the `.material` attribute of the `Geometry` object.

# %%
from sectionproperties.pre.library import rectangular_section

# create a rectangular section with the default material
geom = rectangular_section(d=16, b=100)
geom.create_mesh(mesh_sizes=10)
sec=Section(geometry=geom)
sec.plot_mesh();
sec.display_mesh_info()
# %% assign steel to the geometry, remesh and recreate the Section object
geom.material = steel
geom.create_mesh(mesh_sizes=10)
sec=Section(geometry=geom)
sec.plot_mesh();
sec.display_mesh_info()

# %% [markdown]
# ## Assigning materials to `CompoundGeometry` objects
#
# A `CompoundGeometry` does not have a `.material` attribute and therefore, a `Material` cannot be directly assigned. Since a `CompoundGeometry` is simply a combination of `Geometry` objects, the material should be assigned to each individual `Geometry` object that make up the `CompoundGeometry`.

# %%
# create a timber material
timber = Material(
    name="Timber",
    elastic_modulus=8e3,
    poissons_ratio=0.35,
    density=6.5e-7,
    yield_strength=20,
    color="burlywood",
)

# create individual geometries with material properties applied
beam = rectangular_section(d=35, b=170, material=timber)
plate1 = rectangular_section(d=35, b=16, material=steel)
plate2 = rectangular_section(d=35, b=16, material=steel)

# combine geometries, maintaining assigned materials
geom = (
    beam
    + plate1.align_to(other=beam, on="left")
    + plate2.align_to(other=beam, on="right")
)
geom.plot_geometry(title="Compound geometry")
# %% mesh and plot
geom.create_mesh(mesh_sizes=[20, 10, 10])
sec=Section(geometry=geom)
sec.plot_mesh();
sec.display_mesh_info()


# %% [markdown]
# Materials can also be changed after the fact by looping through the `Geometry` objects contained with the `CompoundGeometry` object.

# %%
# create CompoundGeometry without materials
rect1 = rectangular_section(d=10, b=10)
rect2 = rectangular_section(d=20, b=20).align_to(other=rect1, on="right")
geom = rect1 + rect2
geom.create_mesh(mesh_sizes=[1])
sec=Section(geometry=geom)
sec.plot_mesh();
sec.display_mesh_info()

# %% [markdown]
# ### Change Materials
# %% [markdown]
# Create a list of materials
mat_list = [steel, timber]

# loop through Geometry objects in CompoundGeometry to change materials
for geometry, mat in zip(geom.geoms, mat_list, strict=False):
    geometry.material = mat

# remesh and recreate Section object
sec=Section(geometry=geom)
sec.plot_mesh();
sec.display_mesh_info()

# %% [markdown]
# For more information, see [Assigning Material Properties](../../user_guide/geometry.rst#assigning-material-properties).