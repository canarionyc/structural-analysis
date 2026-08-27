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
# # Display Results

# %% [markdown]
# This example demonstrates how to display results in `sectionproperties`.
#
# A 165.1 x 5.4 CHS will be analysed and the differences in the [display_results()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section.display_results) output highlighted.

# %% [markdown]
# ## Create Geometry and Section

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import circular_hollow_section

geom = circular_hollow_section(d=165.1, t=5.4, n=64)
geom.create_mesh(mesh_sizes=10)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# The `display_results()` method will print all the results that have been calculated for the `Section` object. If an analysis has not been conducted, no results will display.

# %%
sec.display_results()

# %%
sec.calculate_geometric_properties()
sec.display_results('.2g')

# %% [markdown]
# The formatting can be changed by passing a formatting string to the `fmt` argument, see [here](https://docs.python.org/3/library/string.html#format-specification-mini-language) for more information on string formatting.

# %%
sec.display_results(fmt=".1f")

# %% [markdown]
# When more analyses are conducted, more results are displayed.

# %%
sec.calculate_warping_properties()
sec.calculate_plastic_properties()
sec.display_results('.2g')

# %% [markdown]
# Because we have not specified any material properties, the displayed properties are purely geometric. If we assign a steel material to the CHS, we will see some results change to material property weighted values (see [here](../../user_guide/results.rst#how-material-properties-affect-results) for more information on how material properties affect results). We can also print the transformed results using the `display_transformed_results()` method.

# %%
from sectionproperties.pre import Material

# create steel material
steel = Material(
    name="Steel",
    elastic_modulus=200e3,  # N/mm^2 (MPa)
    poissons_ratio=0.3,  # unitless
    density=7.85e-6,  # kg/mm^3
    yield_strength=500,  # N/mm^2 (MPa)
    color="grey",
)
geom.material = steel  # assign steel to the CHS

# remesh and recreate Section object
geom.create_mesh(mesh_sizes=5)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)
sec.display_mesh_info()

# %% perform analysis and display results
sec.calculate_geometric_properties()
sec.calculate_warping_properties()
sec.calculate_plastic_properties()
sec.display_results(fmt=".3g")
sec.display_transformed_results(e_ref=steel, fmt=".3g")