# OpenSees -- Open System for Earthquake Engineering Simulation
# Basic Frame Example
# -----------------------
#  2D Elastic Cantilever Beam
#  Single Nodal Load, Static Analysis
import os.path

import openseespywin.opensees as ops
import opsvis as opsv
import matplotlib.pyplot as plt

from Parcial2.cercha import file_path

# help(ops)
# dir(ops)

# %% 1. MODEL GENERATION

ops.wipe()
# 3 dimensions, 6 DOFs per node
ops.model("BasicBuilder", "-ndm", 3, "-ndf", 6)

# Geometry
L = 5 # m	A typical 5-meter office floor span.
ops.node(1, 0.0,   0.0, 0.0)
ops.node(2, L/4,  0.0, 0.0)
ops.node(3, L/2,  0.0, 0.0)
ops.node(4, 3*L/4,  0.0, 0.0)
ops.node(5, L, 0.0, 0.0)

# Boundary Conditions (6 DOFs locked)
ops.fix(1, 1, 1, 1, 1, 1, 1)

Fy = -25_000.0 # N	A 2.5-ton load (a heavy SUV).
# 3D Material and Section Properties
A = 5000.0*1e-6  # mm² -> m**2	A medium-sized I-Beam.

E  = 200_000.0 * 1e6   # Pa  (200 GPa)
G  = 80769.230 * 1e6   # Pa  (80.7 GPa)
A  = 5000.0 * 1e-6     # m²  (Area uses 1e-6)
Iy = 30_000_000.0 * 1e-12 # m⁴  (Inertia uses 1e-12) -> equals 0.00003
Iz = 30_000_000.0 * 1e-12 # m⁴  (Inertia uses 1e-12) -> equals 0.00003
J  = 150_000.0 * 1e-12    # m⁴  (Torsion uses 1e-12)

# Geometric Transformation
transfTag = 1
# PASS AS SEPARATE ARGUMENTS
ops.geomTransf('Linear', transfTag, 0.0, 0.0, 1.0)

# Define Elements (elasticBeamColumn in 3D takes A, E, G, J, Iy, Iz)
ops.element('elasticBeamColumn', 1, 1, 2, A, E, G, J, Iy, Iz, transfTag)
ops.element('elasticBeamColumn', 2, 2, 3, A, E, G, J, Iy, Iz, transfTag)
ops.element('elasticBeamColumn', 3, 3, 4, A, E, G, J, Iy, Iz, transfTag)
ops.element('elasticBeamColumn', 4, 4, 5, A, E, G, J, Iy, Iz, transfTag)

# Loads (6 DOFs for the point load)
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
# load(nodeTag, Fx, Fy, Fz, Mx, My, Mz) -> 100 downwards in Y



ops.load(5, 0.0, Fy, 0.0, 0.0, 0.0, 0.0)

# Analysis Setup
ops.system("BandSPD")
ops.numberer("RCM")
ops.constraints("Plain")
ops.algorithm("Linear")
ops.integrator("LoadControl", 1.0)
ops.analysis("Static")

ops.analyze(1)
print(f"Tip Deflection in Y: {ops.nodeDisp(5, 2)}")

# Print Tip Displacements
disp_node5 = ops.nodeDisp(5)
print(f"Tip Displacement (Node 5):")
print(f"  DX = {disp_node5[0]:.5g}")
print(f"  DY = {disp_node5[1]:.5g}")
print(f"  DZ = {disp_node5[2]:.5g}\\n")
print(f"  Rx = {disp_node5[3]:.5g} rad\\n")
print(f"  Ry = {disp_node5[4]:.5g} rad\\n")
print(f"  Rz = {disp_node5[5]:.5g} rad\\n")

# %% classical verification
def get_Euler_max_deflection(Fy: float, L: float, E: float, Iz: float):
    return (Fy * L**3) / (3 * E * Iz)
calculated_Euler_max_deflextion = get_Euler_max_deflection(Fy, L, E, Iz)
print("Euler max deflection:", calculated_Euler_max_deflextion)
print(disp_node5[1]/calculated_Euler_max_deflextion)

# %% Print Base Reactions
ops.reactions()
rxn_node1 = ops.nodeReaction(1)
print(f"Base Reactions (Node 1):")
print(f"  Fx = {rxn_node1[0]:.2f}")
print(f"  Fy = {rxn_node1[1]:.2f}")
print(f"  Fz = {rxn_node1[2]:.2f}")
print(f"  Mx = {rxn_node1[3]:.2f}")
print(f"  My = {rxn_node1[4]:.2f}")
print(f"  Mz = {rxn_node1[5]:.2f}")




# %% Start of recorder generation

node_out= "node_%s.out".format("%y%m%d_%H%M%S")

# create a Recorder object for the nodal displacements at node 4
ops.recorder("Node", "-file", "example.out", "-time", "-node", 4, "-dof", 1, 2, "disp")
ops.recorder("Element", "-file", "eleGlobal.out", "-time", "-ele", 1, 2, 3, "forces")
ops.recorder("Element", "-file", "eleLocal.out", "-time", "-ele", 1, 2, 3, "basicForces")





# %% 4. VISUALIZATION

print("\nGenerating visualizations...")

# Plot the deformed shape (Exaggerated for visibility)
opsv.plot_model(node_labels=1, element_labels =1, node_supports=True)
# help(opsv.plot_defo)
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
M = ele1_forces[5]  # Bending moment at the wall (node i)

# Calculate extreme fiber stresses
# Top fiber stress (assuming downward load creates tension at top)
sigma_top = (P / A) + (M * c / Iz)

# Bottom fiber stress (compression)
sigma_bottom = (P / A) - (M * c / Iz)

print(f"--- Stress at the Built-in Support ---")
print(f"Axial Force (P):  {P:.2f} kips")
print(f"Bending Mom (M):  {M:.2f} kip-in")
print(f"Top Fiber Stress: {sigma_top:.2f} ksi")
print(f"Bot Fiber Stress: {sigma_bottom:.2f} ksi")



plt.show()