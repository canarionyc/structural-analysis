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
# # Torsion Constant of a Rectangle

# %% [markdown]
# This example shows how `sectionproperties` can be used as part of a script to conduct multiple analyses. In this example, we examine how the torsion constant varies with the aspect ratio of a rectangle section.

# %% [markdown]
# ## Setup Analysis Parameters

# %%
import numpy as np

# list of aspect ratios to analyse (10^0 = 1 to 10^1.301 = 20)
# logspace used to concentrate data near aspect ratio = 1
aspect_ratios = np.logspace(0, 1.301, 50)
torsion_constants = []  # list of torsion constant results
area = 1  # cross-section area
n = 100  # approximate number of finite elements in each analysis

# %% [markdown]
# ## Analysis Loop

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import rectangular_section

for ar in aspect_ratios:
    # calculate rectangle dimensions
    d = np.sqrt(ar)
    b = 1 / d
    geom = rectangular_section(d=d, b=b)

    # create mesh and Section object
    ms = d * b / n
    geom.create_mesh(mesh_sizes=[ms])
    sec = Section(geometry=geom)

    # perform analysis
    sec.calculate_frame_properties()

    # save the torsion constant
    torsion_constants.append(sec.get_j())

# %% [markdown]
# ## Plot Results

# %%
import matplotlib.pyplot as plt

_, ax = plt.subplots()
ax.plot(aspect_ratios, torsion_constants, "k-")
ax.set_xlim(0, 21)
ax.set_ylim(0, 0.15)
ax.set_xlabel("Aspect Ratio [d/b]")
ax.set_ylabel("Torsion Constant [J]")
ax.set_title("Rectangular Section Torsion Constant")
ax.grid()
plt.show()
