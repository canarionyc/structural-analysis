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
# # Retrieving Stresses

# %% [markdown]
# This example will demonstrate the [get_stress_at_points()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section.get_stress_at_points) method, which get can be used to obtain the stress at one or multiple points within the cross-section.

# %% [markdown]
# ## 150 x 100 x 6 RHS
#
# The first section will look at a 150 x 100 x 6 RHS and sample the stress at both a single point, and along two lines. We start by creating the geometry, mesh and `Section` object.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import rectangular_hollow_section

geom = rectangular_hollow_section(d=100, b=150, t=6, r_out=15, n_r=8)
geom.create_mesh(mesh_sizes=3)
sec = Section(geometry=geom)

# %% [markdown]
# Here we will define the point and two lines along which we would like to sample the stress.
#
# - Point: `x = 100`, `y = 97`
# - Line 1: `x = 3`, `y = 20 to 80` (sample 10 points)
# - Line 2: `x = 0 to 150`, `y = 3` (sample 50 points)

# %%
import numpy as np

pt = (144, 6)
x1 = [3] * 10
y1 = np.linspace(20, 80, 10)
x2 = np.linspace(0, 150, 50)
y2 = [3] * 50

# %% [markdown]
# We will overlay the finite element mesh with a plot of the point and two lines. 

# %%
import matplotlib.pyplot as plt

ax = sec.plot_mesh(materials=False, render=False)
ax.plot(pt[0], pt[1], "r*", label="Point")
ax.plot(x1, y1, "bo-", label="Line 1")
ax.plot(x2, y2, "go-", label="Line 2")
ax.legend()
plt.show()

# %% [markdown]
# Before extracting the stresses, we must first perform a geometric and warping analysis.

# %%
sec.calculate_geometric_properties()
sec.calculate_warping_properties()

# %% [markdown]
# ### Point
#
# For this first sample location we describe a complex load case, plot the von Mises stress and extract the stress at the point.

# %%
load_case = {
    "n": -50e3,
    "mxx": 5e6,
    "myy": 10e6,
    "vx": 5e3,
    "vy": 15e3,
    "mzz": 5e6,
}

stress = sec.calculate_stress(**load_case)
stress.plot_stress(stress="vm", cmap="viridis", normalize=False)

# %%
sig = sec.get_stress_at_points(pts=[pt], **load_case)[0]
print(f"sig_zz = {sig[0]:.2f} MPa")
print(f"tau_xz = {sig[1]:.2f} MPa")
print(f"tau_yz = {sig[2]:.2f} MPa")

# %% [markdown]
# We can confirm that the von Mises stress matches that shown on the above plot by using the following formula:
#
# $\sigma_{vm} = \sqrt{(\sigma_{zz})^2 + 3(\sigma_{z,xy})^2}$
#
# where $\sigma_{z,xy} = \sqrt{(\sigma_{xz})^2 + (\sigma_{yz})^2}$ is the resultant shear stress.

# %%
sig_vm = np.sqrt(sig[0] ** 2 + 3 * (np.sqrt(sig[1] ** 2 + sig[2] ** 2)) ** 2)
print(f"sig_vm = {sig_vm:.2f} MPa")

# %% [markdown]
# ### Line 1
#
# For the first line, we place the RHS under a single bending moment - we expect to see a linear distribution of stress down the web.

# %%
# zip points into a list of tuples
pts = list(zip(x1, y1, strict=False))

# extract stresses along the line
sigs = sec.get_stress_at_points(pts=pts, mxx=10e6)

# we are only interested in the first of three stresses (normal stress)
sig_zz = [x[0] for x in sigs]

# %% [markdown]
# We can now generate a plot of the normal stress with y-coordinate.

# %%
fig, ax = plt.subplots()
ax.plot(sig_zz, y1, "kx-")
ax.set_xlabel("Normal Stress [MPa]")
ax.set_ylabel("y-coordinate [mm]")
plt.show()

# %% [markdown]
# ### Line 2
#
# For the second line, we place the RHS under a single shear force - we expect to see a roughly parabolic distribution of stress along the plate.

# %%
# zip points into a list of tuples
pts = list(zip(x2, y2, strict=False))

# extract stresses along the line
sigs = sec.get_stress_at_points(pts=pts, vx=100e3)

# we are only interested in the second of three stresses (x-shear stress)
# note we also ignore None results (outside geometry)
tau_xz = [x[1] for x in sigs if x is not None]

# %% [markdown]
# We can now generate a plot of the x-shear stress with x-coordinate. Note that the first two and last two points are outside the section.

# %%
fig, ax = plt.subplots()
ax.plot(x2[2:-2], tau_xz, "kx-")
ax.set_xlabel("x-coordinate [mm]")
ax.set_ylabel("Shear Stress [MPa]")
plt.show()

# %% [markdown]
# ## Rectangular Section
#
# This second section will apply shear forces and torsion to a 100 mm x 100 mm rectangular section. The relevant stress contours will be plotted and the shear stress plotted along a central slice. We start by creating the geometry, mesh and `Section` object.

# %%
from sectionproperties.pre.library import rectangular_section

geom = rectangular_section(d=100, b=100)
geom.create_mesh(mesh_sizes=50)
sec = Section(geometry=geom)

# %% [markdown]
# Next we perform a geometric and warping analysis, and apply the loads.

# %%
sec.calculate_geometric_properties()
sec.calculate_warping_properties()
s = sec.calculate_stress(mzz=1e6, vx=10e3, vy=10e3)

# %% [markdown]
# We will generate several stress plots to show the stress field.

# %%
s.plot_stress_vector(stress="zxy", cmap="viridis", normalize=False)

# %%
s.plot_stress(stress="zxy", cmap="viridis", normalize=False)

# %% [markdown]
# We will generate a vertical slice down the centre of the rectangle and extract the stresses along 50 points of this line.

# %%
xs = [50] * 50
ys = np.linspace(0, 100, 50)
sigs = sec.get_stress_at_points(
    pts=list(zip(xs, ys, strict=False)),
    mzz=1e6,
    vx=10e3,
    vy=10e3,
)
tau_xz = [x[1] for x in sigs]
tau_yz = [x[2] for x in sigs]

# %% [markdown]
# We can now plot the x and y components of shear stress along this line.

# %%
fig, ax = plt.subplots()
ax.plot(ys, tau_xz, "k-", label="$\\tau_{xz}$")
ax.plot(ys, tau_yz, "k--", label="$\\tau_{yz}$")
ax.set_xlabel("y-coordinate [mm]")
ax.set_ylabel("Stress [MPa]")
ax.set_ylim(-4, 8)
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
ax.grid()
plt.show()
