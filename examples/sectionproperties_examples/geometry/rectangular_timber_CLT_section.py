# %% [markdown]
# ## Rectangular Timber CLT Section
#
# The following example calculates the geometric properties of a rectangular timber crosslaminated section.

# %% [markdown]
# ### Import Modules
#
# We start by importing the [timber_rectangular_section()](../../gen/sectionproperties.pre.library.timber_sections.clt_rectangular_section.rst#sectionproperties.pre.library.timber_sections.clt_rectangular_section) function from the section library, and the [Material()](../../gen/sectionproperties.pre.pre.Material.rst#sectionproperties.pre.pre.Material) object to define our timber material.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre import Material
from sectionproperties.pre.library import clt_rectangular_section

# %% [markdown]
# ### Create Geometry
#
# Create a 120 deep by 1000 wide cross-laminated timber slab.
#
# The following material properties are used:
#
# **SPF-Timber - Parallel-to-grain**
#
# - Elastic modulus = 9500 MPa
# - Poisson's ratio = 0.35
# - Density = 4400 kg/m$^3$
# - Yield Strengh = 5.5 MPa
#
# **SPF-Timber - Perpendicular-to-grain**
#
# - Elastic modulus = 317 MPa
# - Poisson's ratio = 0.35
# - Density = 4400 kg/m$^3$
# - Yield Strengh = 5.5 MPa

# %%
timber0 = Material(
    name="Timber0",
    elastic_modulus=9.5e3,
    poissons_ratio=0.35,
    density=4.4e-7,
    yield_strength=5.5,
    color="burlywood",
)

timber90 = Material(
    name="Timber90",
    elastic_modulus=317,
    poissons_ratio=0.35,
    density=4.4e-7,
    yield_strength=5.5,
    color="orange",
)

# %% [markdown]
# ### Create the geometry - Major (x-) axis bending

# %%
geom_maj = clt_rectangular_section(
    d=[40, 40, 40], layer_mat=[timber0, timber90, timber0], b=1000
)

# %% [markdown]
# #### Create Mesh and ``Section`` object
#
# Create a mesh with a mesh size of 200 mm$^2$ and plot the mesh.

# %%
geom_maj.create_mesh(mesh_sizes=[200])
sec_maj = Section(geometry=geom_maj)
sec_maj.plot_mesh()

# %% [markdown]
# #### Perform an Analysis
#
# We perform only a geometric analysis on the timber CLT section.

# %%
sec_maj.calculate_geometric_properties()

# %% [markdown]
# #### Calculate Gross Effective Moment of Inertia
#
# We can calculate the gross effective moment of inertia by obtaining the flexural rigidity ($\sum E.I$) of the section and dividing it by the elastic modulus of the reference timber (i.e. Timber0).

# %%
ei_maj = sec_maj.get_eic(e_ref=timber0)
print(f"I_eff,x,major = {ei_maj[0]:.3e} mm4")

# %% [markdown]
# ### Create the geometry - Minor (z-) axis bending

# %%
geom_min = clt_rectangular_section(
    d=[40, 40, 40], layer_mat=[timber90, timber0, timber90], b=1000
)

# %% [markdown]
# #### Create Mesh and ``Section`` object
#
# Create a mesh with a mesh size of 200 mm$^2$ and plot the mesh.

# %%
geom_min.create_mesh(mesh_sizes=[200])
sec_min = Section(geometry=geom_min)
sec_min.plot_mesh()

# %% [markdown]
# #### Perform an Analysis
#
# We perform only a geometric analysis on the timber CLT section.

# %%
sec_min.calculate_geometric_properties()

# %% [markdown]
# #### Calculate Gross Effective Moment of Inertia
#
# We can calculate the gross effective moment of inertia by obtaining the flexural rigidity ($\sum E.I$) of the section and dividing it by the elastic modulus of the reference timber (i.e. Timber0).

# %%
ei_min = sec_min.get_eic(e_ref=timber0)
print(f"I_eff,x,minor = {ei_min[0]:.3e} mm4")