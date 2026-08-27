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
# # Retrieving Section Properties

# %% [markdown]
# This example demonstrates how to retrieve cross-section properties in `sectionproperties`. It is suggested that you are familiar with [How Material Properties Affect Results](../../user_guide/results.rst#how-material-properties-affect-results) before reading this example.

# %% [markdown]
# ## Geometric-only Properties
#
# This section retrieves the frame properties for a 150 x 100 x 8 UA stiffened by a 125 x 12 plate at its base.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import angle_section, rectangular_section

angle = angle_section(d=150, b=100, t=8, r_r=12, r_t=5, n_r=8)
plate = rectangular_section(d=12, b=125)
geom = angle + plate.shift_section(x_offset=-12.5, y_offset=-12)
geom.create_mesh(mesh_sizes=[10, 25])
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# We can perform a frame analysis and use the various `get` methods to retrieve the cross-section properties required for a frame analysis.

# %%
sec.calculate_frame_properties()
area = sec.get_area()
ixx_c, iyy_c, ixy_c = sec.get_ic()
phi = sec.get_phi()
j = sec.get_j()

# %%
print(f"Area = {area:.1f} mm2")
print(f"Ixx = {ixx_c:.3e} mm4")
print(f"Iyy = {iyy_c:.3e} mm4")
print(f"Ixy = {ixy_c:.3e} mm4")
print(f"Principal axis angle = {phi:.1f} deg")
print(f"Torsion constant = {j:.3e} mm4")