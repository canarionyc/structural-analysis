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
# # Geometry Manipulation
#
# This example will showcase the built-in geometry manipulation tools in ``sectionproperties``:
#
# - Align
# - Mirror
# - Rotate
# - Shift
# - Split
# - Offset

# %% [markdown]
# ## Import Modules
#
# We start by importing the [rectangular_section()](../../gen/sectionproperties.pre.library.primitive_sections.rectangular_section.rst#sectionproperties.pre.library.primitive_sections.rectangular_section), [channel_section()](../../gen/sectionproperties.pre.library.steel_sections.channel_section.rst#sectionproperties.pre.library.steel_sections.channel_section) and [rectangular_hollow_section()](../../gen/sectionproperties.pre.library.steel_sections.rectangular_hollow_section.rst#sectionproperties.pre.library.steel_sections.rectangular_hollow_section) functions

# %%
from sectionproperties.pre.library import (
    channel_section,
    rectangular_hollow_section,
    rectangular_section,
)

# %% [markdown]
# ## Align
#
# This example will align various rectangles to each other by using the [align_to()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.align_to) and [align_center()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.align_center) methods.

# %%
# create a central rectangle
rect_centre = rectangular_section(d=150, b=100)

# align a square to the central rectangle's right side
sq_right = rectangular_section(d=20, b=20).align_to(other=rect_centre, on="left")

# combine two geometries and plot
geom = rect_centre + sq_right
geom.plot_geometry()

# %%
# align a square to the middle of the central rectangle's top side
sq_center = (
    rectangular_section(d=20, b=20)
    .align_center(align_to=rect_centre)
    .align_to(other=rect_centre, on="top")
)

# combine with the previous geometry and plot
geom += sq_center
geom.plot_geometry()

# %%
# align a square to the centre of the central rectangle's right inner side
sq_right = (
    rectangular_section(d=20, b=20)
    .align_center(align_to=rect_centre)
    .align_to(other=rect_centre, on="right", inner=True)
)

# combine with the previous geometry and plot
geom = geom - sq_right + sq_right  # note we first subtract to avoid overlapping regions
geom.plot_geometry()

# %% [markdown]
# ## Mirror
#
# The following example demonstrates how geometry objects can be mirrored. Two 200PFCs are placed back-to-back by using the [mirror_section()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.mirror_section) method.

# %%
# create RHS PFC
pfc_right = channel_section(d=200, b=75, t_f=12, t_w=6, r=12, n_r=8)

# create LHS PFC by mirroring the RHS PFC
pfc_left = pfc_right.mirror_section(axis="y", mirror_point=(0, 0))

# combine the two PFCs into one geometry and plot the geometry
geom = pfc_right + pfc_left
geom.plot_geometry()

# %% [markdown]
# ## Rotate
#
# The following example rotates the above generated geometry counter-clockwise by 10 degrees by using the [rotate_section()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.rotate_section) method.

# %%
geom = geom.rotate_section(angle=10)
geom.plot_geometry()

# %% [markdown]
# ## Shift
#
# In this example we use the [calculate_extents()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.calculate_extents) method to get the coordinates of the bounding box of the above geometry. We use these coordinates to shift the geometry such that all ``x`` and ``y`` values are positive by shifting the bottom left corner of the bounding box to the origin. The [shift_section()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.shift_section) method is used to accomplish this.x

# %% nbsphinx-thumbnail={"output-index": 0}
x_min, _, y_min, _ = geom.calculate_extents()
geom_t = geom.shift_section(x_offset=-x_min, y_offset=-y_min)
geom_t.plot_geometry()

# %% [markdown]
# ## Split
#
# In this example, we use the [split_section()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.split_section) method to split the above geometry by a vertical line at ``x = 102``.

# %%
from sectionproperties.pre import CompoundGeometry

right_geoms, left_geoms = geom.split_section(point_i=(102, 0), vector=(0, 1))

# combine resultant geometries into a CompoundGeometry object
geom = CompoundGeometry(geoms=left_geoms + right_geoms)
geom.plot_geometry()

# %% [markdown]
# Note how control points are added automatically as required.

# %% [markdown]
# ## Offset
#
# In this example we show how we can erode and dilate the perimeters of geometry objects by using the [offset_perimeter()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.offset_perimeter) method.
#
# We start with a 100 x 50 x 6 RHS and create the following sections:
#
# 1. 2.0 mm external erosion
# 2. 1.0 mm external dilation
# 3. 1.5 mm external and internal erosion

# %%
rhs_base = rectangular_hollow_section(d=100, b=50, t=6, r_out=15, n_r=8)
rhs_base.plot_geometry(title="RHS Base")
rhs_base.offset_perimeter(amount=-2.0).plot_geometry(title="RHS 1")
rhs_base.offset_perimeter(amount=1.0).plot_geometry(title="RHS 2")
rhs_base.offset_perimeter(amount=-1.5, where="all").plot_geometry(title="RHS 3")
