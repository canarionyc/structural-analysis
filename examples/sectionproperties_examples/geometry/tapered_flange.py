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
#%% setup
from math import pi, sqrt
import pprint
help(pprint)
from pprint import pp
# %%
from sectionproperties import post
help(post)


# %% [markdown]
# # Section Library
#
# This examples shows how to use ``sectionproperties``'s section library to create geometry.

# %% [markdown]
# ## Circular Section
#
# The following example calculates the geometric, warping and plastic properties of a 50 mm diameter circle. The circle is discretised with 64 points and a mesh size of 2.5 mm$^2$.

# %% [markdown]
# ### Import Modules
#
# We start by importing the [circular_section](../../gen/sectionproperties.pre.library.primitive_sections.circular_section.rst#sectionproperties.pre.library.primitive_sections.circular_section) function from the section library, and the [Section()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section) object for analysis.

# %%
from sectionproperties.analysis import Section
help(Section)
dir(Section)
# %% [markdown]
# ## Tapered Flange Channel Section
#
# The following example calculates the geometric, warping and plastic properties of an imperial tapered flange section.

# %% [markdown]
# ### Import Modules
#
# We start by importing the [tapered_flange_channel](../../gen/sectionproperties.pre.library.steel_sections.tapered_flange_channel.rst#sectionproperties.pre.library.steel_sections.tapered_flange_channel) function from the section library (we have already imported the ``Section`` object).

# %%
from sectionproperties.pre.library import tapered_flange_channel
help(tapered_flange_channel)
# %% [markdown]
# ### Create Geometry
#
# Create a 10 inch deep by 3.5 inch wide tapered flange channel section.

# %% start a new console here
geom = tapered_flange_channel(
    d=10,
    b=3.5,
    t_f=0.575,
    t_w=0.475,
    r_r=0.575,
    r_f=0.4,
    alpha=8,
    n_r=16,
)
geom.plot_geometry(title="Flanged channel")
# %% [markdown]
# ### Create Mesh and ``Section`` object
#
# Create a mesh with a mesh size of 0.05 in$^2$ and plot the mesh.

# %%
geom.create_mesh(mesh_sizes=0.05)

#%%
sec = Section(geometry=geom)
dir(sec)
help(sec)
# %%
sec.plot_mesh(materials=False);
sec.display_mesh_info()
# %% [markdown]
# ### Perform an Analysis
#
# We perform geometric and warping analyses on the tapered flange channel.

# %% geometric properties
sec.calculate_geometric_properties()
sec.display_results('.2f')
# %% warping properties
sec.calculate_warping_properties()


# %% [markdown]
# ### Plot Centroids
#
# We can plot the various centroids with the [plot_centroids()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section.plot_centroids) method.

# %%
sec.plot_centroids()