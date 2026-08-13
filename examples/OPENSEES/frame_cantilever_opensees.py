# OpenSees -- Open System for Earthquake Engineering Simulation
# Basic Frame Example
# -----------------------
#  2D Elastic Cantilever Beam
#  Single Nodal Load, Static Analysis

import openseespy.opensees as ops
import opsvis as opsv
import matplotlib.pyplot as plt
help(ops)

#%% params setup
help(ops.OpenSeesParameter)
# %% 1. MODEL GENERATION

ops.wipe()

# Create ModelBuilder: 2 dimensions, 3 DOFs per node (X, Y, Theta_Z)
help(ops.model)
ops.model("BasicBuilder", "-ndm", 2, "-ndf", 3)

# Define Geometry (Length = 100 inches, split into 4 elements)
L = 100.0
ops.node(1, 0.0,   0.0)
ops.node(2, 25.0,  0.0)
ops.node(3, 50.0,  0.0)
ops.node(4, 75.0,  0.0)
ops.node(5, 100.0, 0.0)

# Set Boundary Conditions: Node 1 is fully fixed (X, Y, Rotation)
ops.fix(1, 1, 1, 1)

# Define Material and Section Properties (e.g., Steel)
A = 10.0      # Cross-sectional Area
E = 29000.0   # Young's Modulus (Mpa)
I = 200.0     # Moment of Inertia

# Define Geometric Transformation (Linear for small deflections)
transfTag = 1
ops.geomTransf('Linear', transfTag)

# Define Elements: elasticBeamColumn(eleTag, iNode, jNode, A, E, I, transfTag)
ops.element('elasticBeamColumn', 1, 1, 2, A, E, I, transfTag)
ops.element('elasticBeamColumn', 2, 2, 3, A, E, I, transfTag)
ops.element('elasticBeamColumn', 3, 3, 4, A, E, I, transfTag)
ops.element('elasticBeamColumn', 4, 4, 5, A, E, I, transfTag)

# Define Loads: Point Load at the free end (Node 5)
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
# load(nodeTag, Fx, Fy, Mz) -> 10 kips downwards
ops.load(5, 0.0, -10.0, 0.0)


# %% 2. ANALYSIS GENERATION

ops.system("BandSPD")       # Use Banded Symmetric Positive Definite solver
ops.numberer("RCM")         # Reverse Cuthill-McKee algorithm
ops.constraints("Plain")    # Plain constraint handler
ops.algorithm("Linear")     # Linear algorithm
ops.integrator("LoadControl", 1.0) # Apply load in one step
ops.analysis("Static")      # Static analysis


# %% 3. PERFORM ANALYSIS & PRINT RESULTS

ops.analyze(1)

# Print Tip Displacements
disp_node5 = ops.nodeDisp(5)
print(f"Tip Displacement (Node 5):")
print(f"  DX = {disp_node5[0]:.5f}")
print(f"  DY = {disp_node5[1]:.5f}")
print(f"  Rot= {disp_node5[2]:.5f} rad\\n")

# Print Base Reactions
ops.reactions()
rxn_node1 = ops.nodeReaction(1)
print(f"Base Reactions (Node 1):")
print(f"  Fx = {rxn_node1[0]:.2f}")
print(f"  Fy = {rxn_node1[1]:.2f}")
print(f"  Mz = {rxn_node1[2]:.2f}")


# %% 4. VISUALIZATION

print("\nGenerating visualizations...")

# Plot the deformed shape (Exaggerated for visibility)
opsv.plot_model(node_labels=1, element_labels =1, node_supports=True)
help(opsv.plot_defo)
opsv.plot_defo(sfac=False, nep=17, unDefoFlag=1, fmt_defo={'color': 'blue', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, fmt_undefo={'color': 'green', 'linestyle': (0, (1, 5)), 'linewidth': 1.2, 'marker': '', 'markersize': 1}, fmt_defo_faces={'linewidths': 1, 'edgecolors': 'k', 'alpha': 0.5}, fmt_undefo_faces={'linewidths': 1, 'linestyles': 'dotted', 'edgecolors': 'g', 'facecolors': 'w', 'alpha': 0.5}, interpFlag=1, endDispFlag=0, fmt_nodes={'color': 'red', 'linestyle': 'None', 'linewidth': 1.2, 'marker': 's', 'markersize': 6}, Eo=0, az_el=(-60.0, 30.0), fig_wi_he=False, fig_lbrt=False, node_supports=True, ax=False)



# ----------------------------------------------------
# EXTRACTING MAXIMUM BEAM STRESS
# ----------------------------------------------------

# Assuming your beam depth (h) is, for example, 10 inches
# The distance to the extreme fiber (c) is half the depth
c = 10.0 / 2.0

# Get the internal forces at the start of Element 1 (which connects to the wall)
# basicForce returns: [Axial, Shear, Moment at i, Moment at j]
ele1_forces = ops.eleResponse(1, 'basicForce')

P = ele1_forces[0]  # Axial force
M = ele1_forces[2]  # Bending moment at the wall (node i)

# Calculate extreme fiber stresses
# Top fiber stress (assuming downward load creates tension at top)
sigma_top = (P / A) + (M * c / I)

# Bottom fiber stress (compression)
sigma_bottom = (P / A) - (M * c / I)

print(f"--- Stress at the Built-in Support ---")
print(f"Axial Force (P):  {P:.2f} kips")
print(f"Bending Mom (M):  {M:.2f} kip-in")
print(f"Top Fiber Stress: {sigma_top:.2f} ksi")
print(f"Bot Fiber Stress: {sigma_bottom:.2f} ksi")



plt.show()