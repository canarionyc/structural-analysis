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
# # Geometric Analysis

# %% [markdown]
# This example demonstrates how to perform a geometric analysis in `sectionproperties`.

# %% [markdown]
# ## Steel I-Beam
#
# In this example, the geometric cross-section properties of a 200UB25.4 are obtained.

# %% [markdown]
# First we create the cross-section geometry.

# %%
from sectionproperties.pre.library import i_section

geom = i_section(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)

# %% [markdown]
# Next we must create a finite element mesh and a [Section()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section) object.

# %%
from sectionproperties.analysis import Section

geom.create_mesh(mesh_sizes=5)
sec = Section(geometry=geom)

# %% [markdown]
# We can check the mesh quality by calling the `display_mesh_info()` method, or by generating a plot of the mesh by using `plot_mesh()`.

# %%
sec.display_mesh_info()

# %% nbsphinx-thumbnail={"output-index": 0}
sec.plot_mesh(materials=False)

# %% [markdown]
# Note that in `sectionproperties`, the geometric properties are mesh independent. As a result, we can create a mesh with no area constraints by setting `mesh_sizes=0`.

# %%
geom.create_mesh(mesh_sizes=0)
sec = Section(geometry=geom)
sec.display_mesh_info()
sec.plot_mesh(materials=False)

# %% [markdown]
# We can now perform the geometric analysis by calling `calculate_geometric_properties()`.

# %%
sec.calculate_geometric_properties()

# %% [markdown]
# One easy way to view all the results that have been calculated to date, is to print them to the terminal by using `display_results()`.

# %%
sec.display_results(fmt=".0f")

# %% [markdown]
# ## Unconnected Sections
#
# `sectionproperties` can compute the geometric properties of unconnected sections. Note that a warping analysis cannot be undertaken on unconnected sections. This example analyses two 150PFC sections separated by 1 metre forming the flanges of a truss.

# %%
from sectionproperties.pre.library import channel_section

# create 150 pfc geometry
pfc = channel_section(d=150, b=75, t_f=9.5, t_w=6, r=10, n_r=8)
pfc.plot_geometry(legend=False)

# %% [markdown]
# We can analyse the section properties of a single PFC first, then compare the results to the combined section.

# %%
pfc.create_mesh(mesh_sizes=0)
sec_pfc = Section(geometry=pfc)
sec_pfc.calculate_geometric_properties()

# %% [markdown]
# Now we create the truss geometry by mirroring one PFC and offsetting the other.

# %%
# create compound geometry
geom = pfc.mirror_section(axis="y", mirror_point=(0, 0)) + pfc.shift_section(
    x_offset=1000,
)
geom.create_mesh(mesh_sizes=0)
sec_truss = Section(geometry=geom)
sec_truss.plot_mesh(materials=False)
sec_truss.calculate_geometric_properties()

# %% [markdown]
# Let's compare some of the calculated section properties:

# %%
area_ratio = sec_truss.get_area() / sec_pfc.get_area()
ixx_ratio = sec_truss.get_ic()[0] / sec_pfc.get_ic()[0]
iyy_ratio = sec_truss.get_ic()[1] / sec_pfc.get_ic()[1]
zyy_ratio = sec_truss.get_z()[2] / sec_pfc.get_z()[2]
ry_ratio = sec_truss.get_rc()[1] / sec_pfc.get_rc()[1]

# %% [markdown]
# We can format the results in a tabulated way by using the `rich` library.

# %%
from rich.console import Console
from rich.table import Table

# setup table
table = Table(title="Section Properties Comparison")
table.add_column("Property", justify="left", style="cyan", no_wrap=True)
table.add_column("PFC", justify="right", style="green")
table.add_column("Truss", justify="right", style="green")
table.add_column("Ratio", justify="right", style="green")

# add data to the table
table.add_row(
    "area",
    f"{sec_pfc.get_area():.0f}",
    f"{sec_truss.get_area():.0f}",
    f"{area_ratio:.2f}",
)
table.add_row(
    "ixx",
    f"{sec_pfc.get_ic()[0]:.3e}",
    f"{sec_truss.get_ic()[0]:.3e}",
    f"{ixx_ratio:.2f}",
)
table.add_row(
    "iyy",
    f"{sec_pfc.get_ic()[1]:.3e}",
    f"{sec_truss.get_ic()[1]:.3e}",
    f"{iyy_ratio:.2f}",
)
table.add_row(
    "zyy",
    f"{sec_pfc.get_z()[2]:.3e}",
    f"{sec_truss.get_z()[2]:.3e}",
    f"{zyy_ratio:.2f}",
)
table.add_row(
    "ry",
    f"{sec_pfc.get_rc()[1]:.0f}",
    f"{sec_truss.get_rc()[1]:.0f}",
    f"{ry_ratio:.2f}",
)

# print table
console = Console()
console.print(table)
