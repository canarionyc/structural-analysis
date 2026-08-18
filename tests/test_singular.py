#%% setup
import numpy as np

#%% 1. Define Stiffness Values (The "Contrast")
k_rigid = 1e12  # A massive steel wall
k_soft = 1.0    # A tiny rubber band
k_rot = 1.0     # Rotational stiffness

#%% 2. Rotate the system by 30 degrees to mix the stiffnesses
theta = np.radians(30)
c, s = np.cos(theta), np.sin(theta)
R = np.array([
    [c, -s, 0],
    [s,  c, 0],
    [0,  0, 1]
])

# K_global = R * K_local * R.T
K_local = np.diag([k_rigid, k_soft, k_rot])
K_global = R @ K_local @ R.T

#%% 3. Apply a simple force (10 Newtons in X and Y)
F = np.array([10, 10, 0])

#%% 4. Solve for Displacements (u)
u = np.linalg.solve(K_global, F)
print(f"Displacements: {u}")
#%% 5. Diagnostic: Check the Condition Number and Residual Error
cond_num = np.linalg.cond(K_global)
error = np.linalg.norm(K_global @ u - F)

print(f"Condition Number: {cond_num:.2e}")
print(f"Residual Error: {error:.2e}")

# %% plotting setup
import pyvista as pv
import numpy as np

# --- Parameters ---
L = 3.0  # Length of the connections
theta_rigid = np.radians(30)   # The rigid direction (30 degrees)
theta_soft = np.radians(120)   # The soft direction (perpendicular, 120 degrees)

# --- Create Geometries ---
origin = np.array([0.0, 0.0, 0.0])

# 1. The Central Node
node = pv.Sphere(radius=0.2, center=origin)

# 2. The Rigid Constraint (Thick Cylinder + Wall)
# Calculate end point of the rigid link
rigid_end = np.array([L * np.cos(theta_rigid), L * np.sin(theta_rigid), 0.0])
rigid_link = pv.Cylinder(center=rigid_end/2, direction=rigid_end, radius=0.1, height=L)

# The rigid "wall" it attaches to
wall = pv.Plane(center=rigid_end, direction=rigid_end, i_size=2.0, j_size=2.0)

# 3. The Soft Constraint (A Helical Spring)
# Generate points for a helix along the X-axis first
t = np.linspace(0, 8 * np.pi, 500)  # 4 turns
spring_x = (t / (8 * np.pi)) * L
spring_y = 0.2 * np.cos(t)
spring_z = 0.2 * np.sin(t)

# Rotate the spring points to the 120 degree angle
spring_points = np.column_stack((
    spring_x * np.cos(theta_soft) - spring_y * np.sin(theta_soft),
    spring_x * np.sin(theta_soft) + spring_y * np.cos(theta_soft),
    spring_z
))
spring = pv.Spline(spring_points) # Create a smooth line from the points

# 4. The Soft Constraint Anchor (The missing wall!)
# Get the very last point of the spring to place the wall
spring_end_point = spring_points[-1]

# Create a smaller wall at the end of the spring, facing the node
spring_wall = pv.Plane(
    center=spring_end_point,
    direction=-spring_end_point, # Face back towards the origin
    i_size=1.0,
    j_size=1.0
)
#%% --- Plotting ---
plotter = pv.Plotter(title="Ill-Conditioned Node: Stiffness Contrast")
plotter.set_background('white')

# Add the Global Axes for reference
plotter.add_axes()
plotter.add_mesh(pv.Arrow(start=origin, direction=[2, 0, 0]), color='black', label='Global X')
plotter.add_mesh(pv.Arrow(start=origin, direction= [0, 2, 0]), color='black', label='Global Y')

# Add the components to the plot
plotter.add_mesh(node, color='gold', show_edges=True, label='Node (Degrees of Freedom)')
plotter.add_mesh(rigid_link, color='red', label='Rigid Link (k = 1e12)')
plotter.add_mesh(wall, color='gray', opacity=0.8, label='Rigid Anchor')
plotter.add_mesh(spring, color='blue', line_width=4, label='Soft Spring (k = 1.0)')
plotter.add_mesh(spring_wall, color='lightgray', opacity=0.8, label='Soft Anchor')

# Add a legend and setup camera
plotter.add_legend(bcolor='white', size=(0.3, 0.2))
plotter.view_xy()  # Set to 2D top-down view
plotter.camera.zoom(1.2)

# Show the interactive plot
plotter.show()