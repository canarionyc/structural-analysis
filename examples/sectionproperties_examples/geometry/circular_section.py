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
from pprint import pp, pprint



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

#%% circular section
from sectionproperties.pre.library import circular_section
help(circular_section)
# %% [markdown]
# ### Create Geometry
#
# Create a 50 diameter circle discretised by 64 points and plot the geometry.

# %%
diameter: float = 50.0 # diameter
geom = circular_section(d=diameter, n=64)
geom.plot_geometry();

# %% [markdown]
# ### Create Mesh an ``Section`` object
#
# Create a mesh with a mesh size of 2.5 mm$^2$, a [Section()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section) object. We also display some mesh information and plot the finite element mesh.

# %%
geom.create_mesh(mesh_sizes=[2.5])

sec = Section(geometry=geom)
sec.display_mesh_info()
sec.plot_mesh(materials=False);

#%% section properties
help(sec.section_props)
sec_dict=sec.section_props.asdict()


# %% [markdown]
# ### Perform an Analysis
#
# We perform geometric, warping and plastic analyses. It is important to perform the geometric analysis first, as these results are required by the warping and plastic analyses.

# %%

sec.calculate_geometric_properties()
print(f"Area = {sec.get_area():.3f}")
print(f"Expected Area = {pi * (diameter / 2)**2:.3f}")
print(f"Perimeter = {sec.get_perimeter():.3f}")
print(f"Expected Perimeter = {2*pi*(diameter/2):.3f}")
sec.plot_centroids();

# %% warping
sec.calculate_warping_properties()

# %% plastic
sec.calculate_plastic_properties()

sec_dict=sec.section_props.asdict()
pp(sec_dict)
# %% [markdown]
# ### Display Results
#
# Print the results to the terminal using [display_results()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section.display_results).

# %%
help(sec.display_results)
sec.display_results('.2f')

# %%

# %% centroidal moments of inertia
help(sec.get_ic)
ixx_c, iyy_c, ixy_c = sec.get_ic()
print(f"Ixx + Iyy + Ixy = {ixx_c + iyy_c + ixy_c:.3f}")

#%% warping properties
help(sec.calculate_warping_properties)
sec.calculate_warping_properties()

help(sec.get_j)
j = sec.get_j()
print(f"J = {j:.3f}")

assert ixx_c + iyy_c + ixy_c == j
# %% [markdown]
# It is clear that for a circular section, the torsion constant is equal to the sum of second moments of area!