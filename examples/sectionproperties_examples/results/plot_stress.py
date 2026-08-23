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
# # Plotting Stresses

# %% [markdown]
# This example demonstrates how to plot stresses in `sectionproperties`.
#
# We will analyse an elliptical section under combined loading and demonstrate various stress plotting options. We start by creating the geometry, mesh and `Section` object.

# %%
from sectionproperties.analysis import Section
from sectionproperties.pre.library import elliptical_section

geom = elliptical_section(d_x=75, d_y=150, n=64)
geom.create_mesh(mesh_sizes=20)
sec = Section(geometry=geom)
sec.plot_mesh(materials=False)

# %% [markdown]
# Prior to conducting a stress analysis we must conduct a geometric and warping analysis, note the warping analysis is required because we will be applying shear and torsion loads.

# %%
sec.calculate_geometric_properties()
sec.calculate_warping_properties()

# %% [markdown]
# We will analyse the elliptical section under a complex loading case. The `calculate_stress()` method returns a `StressPost` object that we can use for post-processing purposes.

# %%
stress = sec.calculate_stress(
    n=100e3,
    mxx=10e6,
    myy=5e6,
    vx=25e3,
    vy=50e3,
    mzz=3e6,
)

# %% [markdown]
# ## Plot Stress Contours
#
# There are many stress plotting options available when using the [plot_stress()](../../gen/sectionproperties.post.stress_post.StressPost.rst#sectionproperties.post.stress_post.StressPost.plot_stress) method. In this example we will generate the following stress plots:
#
# **Primary Stress Plots:**
#
# - $\sigma_{zz,Myy}$ - normal stress resulting from the bending moment [`stress="myy_zz"`]
# - $\sigma_{zx,Vy}$ - x-component of the shear stress resulting from the shear force $V_y$ [`stress="vy_zx"`]
# - $\sigma_{zy,Vy}$ - y-component of the shear stress resulting from the shear force $V_y$ [`stress="vy_zy"`]
#
# **Combined Stress Plots:**
#
# - $\sigma_{zz}$ - combined normal stress resulting from all actions [`stress="zz"`]
# - $\sigma_{z,xy}$ - resultant shear stress resulting from all actions [`stress="zxy"`]
# - $\sigma_{11}$ - major principal stress resulting from all actions [`stress="11"`]
# - $\sigma_{33}$ - minor principal stress resulting from all actions [`stress="33"`]
# - $\sigma_{vm}$ - von Mises stress resulting from all actions [`stress="vm"`]
#
# A full list of contour plots can be seen [here](../../gen/sectionproperties.post.stress_post.StressPost.rst#sectionproperties.post.stress_post.StressPost.plot_stress).

# %% [markdown]
# ### Primary Stress Plots

# %%
stress.plot_stress(stress="myy_zz")

# %% [markdown]
# The colour bar number formatting can be changed by providing a formatting string `fmt`. The below plot displays numbers to two decimal places.

# %%
stress.plot_stress(stress="vy_zx", fmt="{x:.2f}")

# %%
stress.plot_stress(stress="vy_zy")

# %% [markdown]
# By default, the colour map is normalised such that the centre of the scale lies at zero stress. For plots that have primarily positive (or negative) stresses, such as the above, it can be useful to set `normalize=False`.

# %%
stress.plot_stress(stress="vy_zy", normalize=False)

# %% [markdown]
# Further, in these case it can also be useful to use a sequential colour map, rather than the default `coolwarm` which is diverging. Let's try the `"viridis"` colour map. More information on colour maps can be found [here](https://matplotlib.org/stable/users/explain/colors/colormaps.html).

# %%
stress.plot_stress(stress="vy_zy", cmap="viridis", normalize=False)

# %% [markdown]
# ### Combined Stress Plots

# %% [markdown]
# Note that the title and transparency can be changed by specifying `title` and `alpha` respectively.

# %%
stress.plot_stress(stress="zz", title="Normal Stress", alpha=0.2)

# %%
stress.plot_stress(stress="zxy", cmap="viridis", normalize=False)

# %% [markdown]
# The `stress_limits` argument can be used to modify the default limits of the colour bar. Say you wanted to identify regions in which the 11-principal stress exceeded 80 MPa, by setting `stress_limits=(0, 80)`, the regions with stresses outside these limits will not be plotted. The colour bar label can also be modified by setting `colorbar_label`.

# %%
stress.plot_stress(
    stress="11",
    cmap="viridis",
    stress_limits=(0, 80),
    normalize=False,
    fmt="{x:.2f}",
    colorbar_label="Principal Stress [MPa]",
)

# %%
stress.plot_stress(stress="33", cmap="viridis", normalize=False)

# %% editable=true nbsphinx-thumbnail={"output-index": 0} slideshow={"slide_type": ""}
stress.plot_stress(stress="vm", cmap="viridis", normalize=False)

# %% [markdown]
# ## Plot Stress Vectors
#
# There are many stress vector plotting options available when using the [plot_stress_vectors()](../../gen/sectionproperties.post.stress_post.StressPost.rst#sectionproperties.post.stress_post.StressPost.plot_stress_vector) method. In this example we will generate the following vector plots:
#
# - $\sigma_{z,xy,Mzz}$ - resultant shear stress resulting from the torsion moment [`stress="mzz_zxy"`]
# - $\sigma_{z,xy,Vy}$ - resultant shear stress resulting from the shear force $V_x$ [`stress="vy_zxy"`]
# - $\sigma_{z,xy}$ - resultant shear stress resulting from all actions [`stress="zxy"`]
#
# A full list of vector plots can be seen [here](../../gen/sectionproperties.post.stress_post.StressPost.rst#sectionproperties.post.stress_post.StressPost.plot_stress_vector).

# %%
stress.plot_stress_vector(stress="mzz_zxy", cmap="viridis", normalize=False)

# %%
stress.plot_stress_vector(
    stress="vy_zxy",
    cmap="viridis",
    normalize=False,
    fmt="{x:.2f}",
)

# %%
stress.plot_stress_vector(
    stress="zxy",
    cmap="viridis",
    normalize=False,
    colorbar_label="Stress [MPa]",
)

# %% [markdown]
# ## Plot Mohr's Circles
#
# The stress state at any point within the mesh can be further investigated with the [plot_mohrs_circles()](../../gen/sectionproperties.post.stress_post.StressPost.rst#sectionproperties.post.stress_post.StressPost.plot_mohrs_circles) method. In this case, we will choose the centre of the ellipse - (`x = 0`, `y = 0`).

# %%
stress.plot_mohrs_circles(x=0, y=0)

# %% [markdown]
# ## Plot Specific Materials
#
# It is possible to plot the stress contours of a specific list of materials, this is done by providing a desired list of `Material` objects to `material_list`.
#
# The following example will generate a composite section and showcase this feature.

# %%
from sectionproperties.pre import Material
from sectionproperties.pre.library import rectangular_section

mat_a = Material("a", 1, 0, 1, 1, color="b")
mat_b = Material("b", 10, 0, 1, 1, color="g")
mat_c = Material("c", 5, 0, 1, 1, color="r")
mat_d = Material("d", 2, 0, 1, 1, color="y")

a = rectangular_section(20, 20, mat_a)
b = rectangular_section(20, 20, mat_b).align_to(a, "right")
c = rectangular_section(20, 20, mat_c).align_to(a, "top")
d = rectangular_section(20, 20, mat_d).align_to(a, "top").align_to(a, "right")
geom = a + b + c + d
geom.create_mesh(10)
sec = Section(geom)
sec.plot_mesh()

# %%
sec.calculate_geometric_properties()
stress = sec.calculate_stress(n=10e3, mxx=1e6)

# %%
stress.plot_stress(stress="m_zz")

# %% [markdown]
# Suppose we want a higher fidelity understanding of the stress in material A (bottom left), we can set `material_list=[mat_a]` to only display material A in the stress plot.

# %%
stress.plot_stress(stress="m_zz", material_list=[mat_a])

# %% [markdown]
# We can also show both material A and C in the same plot using the same functionality.

# %%
stress.plot_stress(stress="m_zz", material_list=[mat_a, mat_c])
