# %% [markdown]
# ## Rectangular Concrete Section
#
# The following example calculates the geometric properties of a rectangular reinforced concrete section.
from sectionproperties.analysis import Section
# %% [markdown]
# ### Import Modules
#
# We start by importing the [concrete_rectangular_section()](../../gen/sectionproperties.pre.library.concrete_sections.concrete_rectangular_section.rst#sectionproperties.pre.library.concrete_sections.concrete_rectangular_section) function from the section library, and the [Material()](../../gen/sectionproperties.pre.pre.Material.rst#sectionproperties.pre.pre.Material) object to define our concrete and steel materials.

# %%
from sectionproperties.pre import Material
help(Material)
dir(Material)
from sectionproperties.pre.library import concrete_rectangular_section

# %% [markdown]
# ### Create Geometry
#
# Create a 600 deep by 300 wide rectangular concrete beam, reinforced with:
#
# - 3 x 16 mm bars top (32 mm cover)
# - 3 x 20 mm bars bottom (42 mm cover)
# - 3 x 12 mm bars each side (57 mm cover)
#
# The circular reinforcement is discretised with 16 points.
#
# The following material properties are used:
#
# **32 MPa Concrete**
#
# - Elastic modulus = 30.1 GPa
# - Poisson's ratio = 0.2
# - Density = 2400 kg/m$^3$ = 2.4 x 10$^{-6}$ kg/mm$^3$
# - Yield Strengh = 32 MPa
#
# **500 MPa Steel**
#
# - Elastic modulus = 200 GPa
# - Poisson's ratio = 0.3
# - Density = 7850 kg/m$^3$ = 7.85 x 10$^{-6}$ kg/mm$^3$
# - Yield Strengh = 500 MPa

# %% concrete material
# define the concrete material
concrete = Material(
    name="Concrete",
    elastic_modulus=30.1e3,
    poissons_ratio=0.2,
    density=2.4e-6,
    yield_strength=32,
    color="lightgrey",
)
print(concrete)

#%% define the steel material
steel = Material(
    name="Steel",
    elastic_modulus=200e3,
    poissons_ratio=0.3,
    yield_strength=500,
    density=7.85e-6,
    color="grey",
)
print(steel)
# %% create the geometry
geom = concrete_rectangular_section(
    d=600,
    b=300,
    dia_top=16,
    area_top=200,
    n_top=3,
    c_top=32,
    dia_bot=20,
    area_bot=310,
    n_bot=3,
    c_bot=42,
    dia_side=12,
    area_side=110,
    n_side=3,
    c_side=57,
    n_circle=16,
    conc_mat=concrete,
    steel_mat=steel,
)
geom.plot_geometry(title="Rectangular reinforced concrete section");
# %% [markdown]
# ### Create Mesh and ``Section`` object
#
# Create a mesh with a mesh size of 200 mm$^2$ and plot the mesh.

# %%
geom.create_mesh(mesh_sizes=[200])
sec = Section(geometry=geom)
sec.plot_mesh()

# %% [markdown]
# ### Perform an Analysis
#
# We perform only a geometric analysis on the reinforced concrete section.

# %%
sec.calculate_geometric_properties()
sec.display_results('.2g')
# %% [markdown]
# ### Calculate Gross Effective Moment of Inertia
#
# We can calculate the gross effective moment of inertia by obtaining the flexural rigidity ($\sum E.I$) of the section and dividing it by the elastic modulus of the concrete. We compare this to the moment of inertia of a rectangular section of the same dimensions.

# %%
ei = sec.get_eic(e_ref=concrete)
print(f"I_eff = {ei[0]:.3e} mm4")
print(f"I_rec = {(300 * 600**3 / 12):.3e} mm4")