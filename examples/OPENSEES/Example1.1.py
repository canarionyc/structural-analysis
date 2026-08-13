# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
# ---

# %%
# OpenSees -- Open System for Earthquake Engineering Simulation
# Pacific Earthquake Engineering Research Center
# http://opensees.berkeley.edu/
#
# Basic Truss Example 1.1
# -----------------------
#  2d 3 Element Elastic Truss
#  Single Nodal Load, Static Analysis
# 
# Example Objectives
# ------------------
#  Simple Introduction to OpenSees
# 
# Units: kips, in, sec
#
# Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
# Date: June 2017

# region setup

# %%
import os
print(os.getcwd())
# os.chdir(r"examples/OPENSEES")

# from openseespywin.opensees import *

import openseespy.opensees as ops
help(ops)
# from openseespy.opensees import *

# endregion


# region Start of model generation


# remove existing model
# ops.wipe()


# %%
help(ops.model)
ops.model("BasicBuilder", "-ndm",2, "-ndf",2)

# create nodes & add to Domain - command: node nodeId xCrd yCrd
ops.node(1, 0.0,    0.0)
ops.node(2, 144.0,  0.0)
ops.node(3, 168.0,  0.0)
ops.node(4,  72.0, 96.0)

# set the boundary conditions - command: fix nodeID xRestrnt? yRestrnt?
ops.fix(1, 1, 1)
ops.fix(2, 1, 1)
ops.fix(3, 1, 1)

# Define materials for truss elements

# Create Elastic material prototype - command: uniaxialMaterial Elastic matID E
ops.uniaxialMaterial("Elastic", 1, 3000.0)


# %%

# Create truss elements - command: element truss trussID node1 node2 A matID
ops.element("truss", 1, 1, 4, 10.0, 1)
ops.element("truss", 2, 2, 4,  5.0, 1)
ops.element("truss", 3, 3, 4,  5.0, 1)


# %%

# create a Linear TimeSeries (load factor varies linearly with time) - command: timeSeries Linear $tag
ops.timeSeries("Linear", 1)

# create a Plain load pattern - command: pattern Plain $tag $timeSeriesTag { $loads }
ops.pattern("Plain", 1, 1, "-fact", 1.0)
# create the nodal load - command: load nodeID xForce yForce
ops.load(4, 100.0, -50.0)


# %%
#printModel()
ops.printModel("-JSON", "-file", "Example1.1.json")

# endregion



# region Start of analysis generation

# %%

# create the system of equation, a SPD using a band storage scheme
help(ops.system)
# ops.system("BandSPD") # Banded Symmetric Positive Definite solver.
ops.system("FullGeneral")

# create the DOF numberer, the reverse Cuthill-McKee algorithm
ops.numberer("RCM")

# create the constraint handler, a Plain handler is used as homo constraints
ops.constraints("Plain")

# create the solution algorithm, a Linear algorithm is created
ops.algorithm("Linear")

# create the integration scheme, the LoadControl scheme using steps of 1.0
ops.integrator("LoadControl", 1.0)

# create the analysis object 
ops.analysis("Static")


# endregion


# region Start of recorder generation

# %%

# create a Recorder object for the nodal displacements at node 4
ops.recorder("Node", "-file", "example.out", "-time", "-node", 4, "-dof", 1, 2, "disp")
ops.recorder("Element", "-file", "eleGlobal.out", "-time", "-ele", 1, 2, 3, "forces")
ops.recorder("Element", "-file", "eleLocal.out", "-time", "-ele", 1, 2, 3, "basicForces")


# endregion


# region Finally perform the analysis


# %%
ops.analyze(1)

#  region Print Stuff to Screen

# print the current state at node 4 and at all elements
#print("node 4 displacement: ", nodeDisp(4))
ops.printModel("node", 4)
ops.printModel("ele")
ops.printModel()
# ----------------------------------------------------
# PRINTING RESULTS DIRECTLY TO CONSOLE
# ----------------------------------------------------

# 1. Print Displacements at Node 4
# nodeDisp returns a list of [x_disp, y_disp]
disp_node4 = ops.nodeDisp(4)
print(f"Node 4 Displacements: DX = {disp_node4[0]:.5f}, DY = {disp_node4[1]:.5f}")

# 2. Print Reactions at the Supports (Nodes 1, 2, 3)
# You must call ops.reactions() first to tell the engine to calculate them
ops.reactions()

rxn_node1 = ops.nodeReaction(1)
rxn_node2 = ops.nodeReaction(2)
rxn_node3 = ops.nodeReaction(3)

print(f"Node 1 Reactions: FX = {rxn_node1[0]:.2f}, FY = {rxn_node1[1]:.2f}")
print(f"Node 2 Reactions: FX = {rxn_node2[0]:.2f}, FY = {rxn_node2[1]:.2f}")
print(f"Node 3 Reactions: FX = {rxn_node3[0]:.2f}, FY = {rxn_node3[1]:.2f}")


# 3. Print the Global Stiffness Matrix
print("\n--- Global Stiffness Matrix [K] ---")
ops.printA()

# Note: You can also save it to a file if it is too large for the console
# ops.printA('-file', 'StiffnessMatrix.out')

# ops.wipe()

# This will return the actual stiffness matrix as a Python list!
K_matrix = ops.printA('-ret')
print(K_matrix)

# endregion

# region plotting


# %%
# Import the visualization framework
import opsvis as opsv
import matplotlib.pyplot as plt
help(opsv)
dir(opsv)
print("Generating visualizations...")

# 1. Plot the Undeformed Model (shows geometry and node/element tags)
opsv.plot_model(node_labels=1, element_labels=1,node_supports=True)

# 2. Plot the Deformed Shape (sfac is the scale factor to exaggerate bending)
opsv.plot_defo(sfac=100)

# Explicitly passing the 8 positional arguments to satisfy the Python 3.12 signature
opsv.plot_loads_2d(
    11,                 # nep: Number of arrows for distributed loads
    1.0,                # sfac: Scale factor for the arrows
    False,              # fig_wi_he: Figure width/height override
    False,              # fig_lbrt: Figure bounds override
    {'color': 'black'}, # fmt_model_loads: Dictionary for formatting
    True,               # node_supports: Draws the pinned/roller triangles
    1,                  # truss_node_offset: Visual offset for joints
    False               # ax: Matplotlib axis override
)

opsv.plt.show()
plt.show()

# 3. Plot the Axial Forces! (Red = Tension, Blue = Compression)
# help(opsv.plot_stress_2d)
# help(opsv.sig_out_per_node)
# opsv.sig_out_per_node(how_many='sxx')
# opsv.plot_stress_2d( )

opsv.plot_reactions()
# Force the plots to display on your screen
opsv.plt.savefig('my_truss.png')

plt.show()

# endregion
# region Truss Element Results
# First, ensure you have the Area (A) of your truss members.
# For example, if A = 10.0:
A = 10.0

print("--- Truss Element Results ---")
# Loop through all elements in the model
for ele_tag in ops.getEleTags():
    # 'basicForce' returns the internal axial force [P] for a truss element
    # (Index 0 is the actual force value)
    axial_force = ops.eleResponse(ele_tag, 'basicForce')[0]

    # Calculate the stress (Sigma = P / A)
    axial_stress = axial_force / A

    # Print the results
    print(f"Element {ele_tag}:")
    print(f"  Force:  {axial_force:.2f} kN")
    print(f"  Stress: {axial_stress:.2f} MPa\n")
# endregion

# %% [markdown]
# That is the complete arsenal of `opsvis`! It is a fantastic, purpose-built library for structural engineers.
#
# Instead of treating them as an alphabetical list, it helps to group these functions by **where you are in your workflow**. Here is a breakdown of what these tools do and when to deploy them:
#
# ### 1. Pre-Analysis: "Did I build this right?"
#
# Before you ever hit `ops.analyze()`, you should use these to verify your geometry, boundary conditions, and loads. Catching a misplaced decimal point here saves hours of debugging later.
#
# * **`plot_model`**: The most basic wireframe. Shows nodes, elements, and their tags.
# * **`plot_supports_and_loads_2d`**: Highly recommended! This draws your truss, places little triangles for your pinned/roller supports, and draws arrows for your applied forces.
# * **`plot_extruded_shapes_3d`**: If you assigned actual cross-sections (like an I-beam or circular pipe) instead of just areas, this renders a volumetric 3D view of your structure.
# * **`plot_fiber_section`**: OpenSees allows you to build complex cross-sections out of individual "fibers" (useful for reinforced concrete). This plots the cross-section slice to ensure your rebar is where you think it is.
#
# ### 2. Post-Analysis: Global Kinematics
#
# Once the solver finishes, use these to look at how the entire structure moved.
#
# * **`plot_defo`**: Plots the deformed shape. You almost always need to pass a scale factor (`sfac=100`) because steel micro-strains are invisible at a 1:1 scale.
# * **`plot_mode_shape`**: If you run an Eigenvalue analysis (for earthquakes or wind vibrations), this plots how the building naturally wants to sway or twist.
# * **`plot_reactions`** / **`plot_reactions_2d`**: Draws force vectors at your support nodes showing exactly how the ground is pushing back against your structure.
#
# ### 3. Post-Analysis: Internal Mechanics
#
# These dive into the individual beams and columns to show what is happening inside the material.
#
# * **`plot_stress_2d`**: Plots the internal forces. While it says "stress", in a 2D frame/truss it is often used to plot the Axial Force, Shear, or Bending Moment diagrams directly onto the members.
# * **`plot_strain`**: Maps the deformation gradients.
#
# ### The Outlier: `plt`
#
# You might have noticed `plt` sitting at the bottom of the list. That isn't actually an OpenSees function; it is `matplotlib.pyplot`. `opsvis` kindly exposes the underlying Matplotlib engine so you can easily call `opsv.plt.show()` or `opsv.plt.savefig('my_truss.png')` without needing to import Matplotlib separately.
#
# ---
#
# Would you like to drop `plot_supports_and_loads_2d` and `plot_reactions_2d` into your current script to see a full visual check of the 100 kN force pushing down on your portal frame?