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
# # Peery - Beams in Complex Bending
#
# This example calculates the section properties of two different beams given in examples from 'Aircraft Structures', by Peery. These cases have known results, and the output from ``sectionproperties`` can be compared for accuracy. These examples represent a more rigourous *proof* against a *real* problem. Only results that have values in the reference material are tested here.
#
# BibTeX entry for reference:
#
# ```
# @Book{Peery,
#     title = {Aircraft Structures},
#     author = {David J. Peery},
#     organization = {Pensylvania State University},
#     publisher = {McGraw-Hill Book Company},
#     year = {1950},
#     edition = {First},
#     ISBN = {978-0486485805}
# }
# ```

# %% [markdown]
# We start by importing the modules required for this example.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import nastran_sections

# %% [markdown]
# ## Example 1 - Section 6.2: Symmetric Bending
#
# This is a symmetric I-section with no lateral supports, undergoing pure uni-directional cantilever bending. Note that the units here are **inches**, to match the text.
#
# We'll use a very coarse mesh to highlight the mesh-independent nature of geometric analyses.

# %%
geom = nastran_sections.nastran_i(dim_1=6, dim_2=3, dim_3=3, dim_4=1, dim_5=1, dim_6=1)
geom = geom.shift_section(y_offset=-3)
geom.create_mesh(mesh_sizes=0.25)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# Perform a geometric analysis on the section, and plot the centroids. We don't need warping analysis for these simple checks as we only require bending stresses.

# %%
sec.calculate_geometric_properties()
sec.plot_centroids()

# %% [markdown]
# Directly from the example, we know that the second moment of inertia resisting the bending is 43.3 in$^4$.

# %%
print(f"Ix = {sec.section_props.ixx_g:.2f} in4")

# %% [markdown]
# This result directly matches the reference.
#
# In the example, the maximum bending moment on the beam is 80,000 in-lbs. We can apply this moment to the section, and evaluate stress.

# %%
stress = sec.calculate_stress(mxx=8e5)

# %% [markdown]
# Next we can extract the maximum stress from the section. Let's go ahead and look at the calculated stress plot. Refer to the stress example for details.

# %%
numerical_result = max(stress.get_stress()[0]["sig_zz"])
print(f"Numerical Result = {numerical_result:.1f} psi")
stress.plot_stress(stress="zz")

# %% [markdown]
# The reference reports the maximum stress as 55,427.3 psi, whereas the numerical result in reported as 55,384.6 psi. This discrepancy is due to the rounding of the second moment of inertia used in the reference.

# %%
stress_ref = 8e5 * 3 / 43.3
stress_theory = 8e5 * 3 / (43 + 1 / 3)
print(stress_ref)
print(stress_theory)

# %% [markdown]
# This example is admittedly more simple, but it's still a nice check for the basics on validity of the package.

# %% [markdown]
# ## Example 1 - Section 7.2: Unsymmetric Bending
#
# Moving on to something a bit more advanced... This is an unsymmetric Z-section with no lateral supports. Note that units here are **inches**, to match the text.

# %%
geom = nastran_sections.nastran_zed(dim_1=4, dim_2=2, dim_3=8, dim_4=12)
geom = geom.shift_section(x_offset=-5, y_offset=-6)
geom = geom.create_mesh(mesh_sizes=0.25)
sec = Section(geometry=geom)

# %%
sec.calculate_geometric_properties()
sec.plot_centroids()

# %% [markdown]
# Checking each property against the reference text:

# %%
props = sec.section_props
print("    Property | Theoretical | Numerical")
print(f"    ixx_g    | {693.3:<12.1f}| {props.ixx_g:<.1f}")
print(f"    iyy_g    | {173.3:<12.1f}| {props.iyy_g:<.1f}")
print(f"    ixy_g    | {-240:<12.1f}| {props.ixy_g:<.1f}")
print(f"    i11_c    | {787:<12.1f}| {props.i11_c:<.1f}")
print(f"    i22_c    | {79.5:<12.1f}| {props.i22_c:<.1f}")

# %% [markdown]
# The section properties look sufficiently accurate, so we can move on to some stress analysis.
#
# The load applied in the reference is -100,000 in-lbs about the x-axis, and 10,000 in-lbs about the y-axis.
#
# To obtain stresses at specific points, we can use the [get_stress_at_points()](../../gen/sectionproperties.analysis.section.Section.rst#sectionproperties.analysis.section.Section.get_stress_at_points) method.

# %% [markdown]
# Check stresses at locations A, B and C (see [validation](../../user_guide/validation.rst) for more details).

# %%
pt_a = (-5, 4)
pt_b = (-5, 6)
pt_c = (1, 6)

stresses = sec.get_stress_at_points(pts=[pt_a, pt_b, pt_c], mxx=-1e5, myy=1e4)

# %% [markdown]
# ### Point A

# %%
text_result_a = 1210
numerical_result_a = stresses[0]
print(f"Text Result (A) = {text_result_a:.2f} psi")
print(f"Numerical Result (A) = {numerical_result_a[0]:.2f} psi")

# %% [markdown]
# ### Point B

# %%
text_result_b = 580
numerical_result_b = stresses[1]
print(f"Text Result (B) = {text_result_b:.2f} psi")
print(f"Numerical Result (B) = {numerical_result_b[0]:.2f} psi")

# %% [markdown]
# ### Point C

# %%
text_result_c = -2384
numerical_result_c = stresses[2]
print(f"Text Result (C) = {text_result_c:.2f} psi")
print(f"Numerical Result (C) = {numerical_result_c[0]:.2f} psi")

# %% [markdown]
# ### Stress Plot
#
# Looking at total axial stress over the section.

# %%
stress = sec.calculate_stress(mxx=-1e5, myy=1e4)
stress.plot_stress(stress="zz")
