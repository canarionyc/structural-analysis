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
# # Torsion Constant of Trapezoidal Sections
#
# Trapezoidal elements or components of a cross-section are quite common in bridge structures, either concrete or steel composite construction. However, it’s common to determine the torsion constant of the trapezoidal section by using a rectangular approximation. For example, this is done in the Autodesk Structural Bridge Design software when there is a haunch in a [Steel Composite Beam](https://help.autodesk.com/view/SBRDES/ENU/?guid=ASBD_InProdAU_structure_tech_info_ti_torsion_Torsion_property_for_SAM_composite_beams_html).
#
# The question then arises, when is it appropriate to make the rectangular approximation to a trapezoidal section, and what might the expected error be?

# %% [markdown]
# ## Import Modules
#
# Here we bring in the rectangular and triangular primitive section shapes, and also the more generic ``shapely`` [Polygon](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html) object.

# %%
import matplotlib.pyplot as plt
import numpy as np
from shapely import Polygon

from sectionproperties.analysis import Section
from sectionproperties.pre import Geometry
from sectionproperties.pre.library import rectangular_section, triangular_section


# %% [markdown]
# ## Define the Calculation Engine
#
# It’s better to collect the relevant section property calculation in a single function. We are only interested in the torsion constant, so this is straightforward enough.

# %%
def get_section_j(
    geom: Geometry,
    ms: float,
    plot_geom: bool = False,
) -> float:
    """Retrieve the torsion constant given a geometry (geom) and mesh size (ms)."""
    geom.create_mesh(mesh_sizes=[ms])
    sec = Section(geometry=geom)

    if plot_geom:
        sec.plot_mesh(materials=False)

    sec.calculate_frame_properties()

    return sec.get_j()


# %% [markdown]
# ## Define the Mesh Density
#
# The number of elements per unit area is an important input to the calculations even though we are only examining ratios of the results. A nominal value of 100 is reasonable.

# %%
n = 100  # mesh density


# %% [markdown]
# ## Create and Analyse the Section
#
# This function accepts the width ``b`` and a slope ``s`` to create the trapezoid. Since we are only interested in relative results, the nominal dimensions are immaterial. There are a few ways to parametrize the problem, but it has been found that setting the middle height of trapezoid (i.e. the average height) to a unit value works fine.

# %%
def do_section(
    b: float,
    s: float,
    d_mid: float = 1.0,
    plot_geom=False,
) -> tuple[float, float, float, float]:
    """Calculates the torsion constant for a trapezoid and rectangle."""
    delta = s * d_mid
    d1 = d_mid - delta
    d2 = d_mid + delta

    # compute mesh size
    ms = d_mid * b / n

    # define the points of the trapezoid
    points = [
        (0, 0),
        (0, d1),
        (b, d2),
        (b, 0),
    ]

    # create geometry
    if s < 1.0:
        trap_geom = Geometry(geom=Polygon(points))
    else:
        trap_geom = triangular_section(h=d2, b=b)

    # calculate torsion constant (trapezoid)
    jt = get_section_j(geom=trap_geom, ms=ms, plot_geom=plot_geom)

    # calculate torsion constant (rectangle)
    rect_geom = rectangular_section(d=(d1 + d2) / 2, b=b)
    jr = get_section_j(geom=rect_geom, ms=ms, plot_geom=plot_geom)

    return jt, jr, d1, d2


# %% [markdown]
# ## Example Section
#
# The analysis for a particular section looks as follows:

# %%
b, s = 4.0, 0.3
jt, jr, d1, d2 = do_section(b=b, s=s, plot_geom=True)
print(f"{b=:.1f}; {s=:.1f}; {jr=:.3f}; {jt=:.3f}; {jr/jt=:.3f}")

# %% [markdown]
# ## Create Loop Variables
#
# The slope ``s`` is 0 for a rectangle, and 1 for a triangle. A range of ``s``, between 0.0 and 1.0, and a range of ``b``, between 1.0 and 10.0, are considered here (but can be extended).

# %%
b_list = np.logspace(0, np.log10(10.0), 10)
s_list = np.linspace(0.0, 1.0, 10)
j_rect = np.zeros((len(b_list), len(s_list)))
j_trap = np.zeros((len(b_list), len(s_list)))

# %% [markdown]
# ## The Main Loop
#
# Execute the double loop to get the ratios for combinations of ``s`` and ``b``.

# %%
for i, b in enumerate(b_list):
    for j, s in enumerate(s_list):
        jt, jr, d1, d2 = do_section(b=b, s=s)
        j_trap[i][j] = jt
        j_rect[i][j] = jr

# %% [markdown]
# ## Calculate the Ratios
#
# Courtesy of numpy, this is easy:

# %%
j_ratio = j_rect / j_trap

# %% [markdown]
# ## Plot the Results
#
# Here we highlight a few of the contours to illustrate the accuracy and behaviour of the approximation.

# %%
# setup plot
plt.figure(figsize=(12, 6))

# colorbar levels
levels = np.arange(start=0.5, stop=1.5, step=0.05)

# contour line plot
cs = plt.contour(
    s_list,
    b_list,
    j_ratio,
    levels=[0.95, 0.99, 1.00, 1.01, 1.05],
    colors=("k",),
    linestyles=(":",),
    linewidths=(1.2,),
)
plt.clabel(cs, colors="k", fontsize=10)

# filled contour plot
plt.contourf(s_list, b_list, j_ratio, 25, cmap="Wistia", levels=levels)

# plot settings
plt.minorticks_on()
plt.grid(which="both", ls=":")
plt.xlabel(r"Slope $s = (d_2-d_1)/(d_2+d_1); d_2\geq d_1, d_1\geq 0$")
plt.ylabel("Aspect $b/d_{ave}; d_{ave} = (d_1 + d_2)/2$")
plt.colorbar()
title = r"Accuracy of rectangular approximation to trapezoid torsion "
title += r"constant $J_{rect}\, /\, J_{trapz}$"
plt.title(title, multialignment="center")
plt.show()

# %% [markdown]
# As expected, when the section is rectangular ``s=0``, the error is small, but as it increases towards a triangle ``s=1``, the accuracy generally reduces. However, there is an interesting line at an aspect ratio of about 2.7 where the rectangular approximation is always equal to the trapezoid’s torsion constant.
