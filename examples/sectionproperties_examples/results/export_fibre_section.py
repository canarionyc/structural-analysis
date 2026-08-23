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
# # Export to Fibre Section
#
# This example shows how to export a section to a fibre section that can be used in [suanPan](https://github.com/TLCFEM/suanPan).
#
# [suanPan](https://github.com/TLCFEM/suanPan) is a finite element analysis framework. Sections can be exported and used to perform nonlinear analysis of frame structures.
#
# There are three analysis types available.
#
# 1. '2D' ---> 2D planar analysis (axial force, bending moment). Elements: `B21`, `F21`.
# 2. '3D' ---> 3D spatial analysis (axial force, bending moment). Elements: `B31`, `F31`.
# 3. '3DOS' ---> 3D spatial analysis with warping and torsion (axial force, bending moment, torsion). Elements: `B31OS`.
#
# The section is discretised into triangular elements in `sectionproperties`. Each triangle can be deemed as a small cell/fibre. Its area and properties at the centre of the triangle are calculated and exported to create a fibre section.
#
# For '2D' and '3D' analyses, the location and area are used. For '3DOS' analysis, the additional warping function and its derivatives are used.
#
# ## The Export Function
#
# One shall call the function with a geometry object with mesh created.

# %%
from sectionproperties.post.fibre import to_fibre_section
from sectionproperties.pre.library import i_section

geom = i_section(d=203, b=133, t_f=7.8, t_w=5.8, r=8.9, n_r=8)
geom.create_mesh(mesh_sizes=10)

commands = to_fibre_section(geom, analysis_type="3DOS")

print(commands[:3000])

# %% [markdown]
# The output can be saved to a file and later be used to create beam elements.

# %%
# write the fibre section to a file
# uncomment below to write file
# with open('200UB25.4.sp', 'w') as f:
#     f.write(commands)

# write the main analysis file
# since we assigned '3DOS' analysis type,
# we need to use compatible elements, for example, 'B31OS'.
model = """# Example torsion analysis
node 1 0 0 0
node 2 1 0 0
material ElasticOS 1 200. .25
file 200UB25.4.sp
orientation B3DOSL 1 0. 0. 1.
element B31OS 1 1 2 1 1 6
fix2 1 E 1
displacement 1 0 1E-1 4 2
plainrecorder 1 Node RF4 2
plainrecorder 2 Element BEAMS 1
step static 1
set ini_step_size 1E-1
set fixed_step_size true
converger RelIncreDisp 1 1E-10 5 1
analyze
save recorder 1 2
exit
"""
# uncomment below to write file
# with open('torsion_analysis.sp', 'w') as f:
#     f.write(model)

# %% [markdown]
# For further details, check [this](https://tlcfem.github.io/suanPan-manual/3.2/Example/Structural/Statics/thin-walled-section/) example.

# %% [markdown]
# ## A Bit More Details
#
# ### Shift Section
#
# As the header states, the function computes properties in the local coordinate system of the section.
#
# For the above I-section, one may want to shift the section to the centroid of the section.
# The user shall explicitly perform this step.

# %%
geom.plot_geometry()

# %%
from sectionproperties.analysis import Section

sec = Section(geom)
sec.calculate_geometric_properties()
x, y = sec.get_c()
geom = geom.shift_section(-x, -y)  # or whatever shift you want
geom.create_mesh(mesh_sizes=5)
geom.plot_geometry()

# %% [markdown]
# ### Overwrite Material
#
# Material names shall be converted to material tags.
#
# One can provide such a mapping dictionary to the function.
# With the shifted geometry, one can do the following.

# %%
commands = to_fibre_section(geom, analysis_type="3DOS", material_mapping={"default": 1})
print(commands[:5000])

# %% [markdown]
# ## Run Analysis
#
# If `suanPan` is installed, one can run the analysis using the previously saved script.

# %%
# from os.path import exists

# write the fibre section to a file with material tag replaced
# uncomment below to write file
# with open('200UB25.4.sp', 'w') as f:
#     f.write(commands)

# run the analysis
# if which("suanpan") is not None:
#     from subprocess import run

#     result_available = True
#     run(["suanpan", "-f", "torsion_analysis.sp"])
# else:
#     result_available = exists("R1-RF42.txt")
#     print("suanPan is not installed.")
result_available = False

# %% [markdown]
# ## Plot Results
#
# The results are stored in `R1-RF42.txt` (**R**ecorder **1** --> **RF4** for node **2**) and `R2-BEAMS1.txt` (**R**ecorder **2** --> **BEAMS** for element **1**).
#
# The sixth component of `BEAMS` is the St. Venant torsion.

# %%
if result_available:
    import numpy as np
    from matplotlib import pyplot as plt

    data = np.loadtxt("R1-RF42.txt")
    twist = data[:, 0] * 0.1
    torque = data[:, 1]
    plt.plot(twist, torque)
    plt.xlabel("twist (rad)")
    plt.ylabel("total torque")
    plt.legend(["200UB25.4"])
    plt.tight_layout()
    plt.show()

# %%
if result_available:
    data = np.loadtxt("R2-BEAMS1.txt")
    twist = data[:, 0] * 0.1
    torque = data[:, 6]
    ref_torque = twist * 80 * 62.7e3  # G=80, J=62.7
    plt.plot(twist, torque)
    plt.plot(twist, ref_torque)
    plt.xlabel("twist (rad)")
    plt.ylabel("St. Venant torsion")
    plt.legend(["numerical", "theoretical"])
    plt.tight_layout()
    plt.show()
