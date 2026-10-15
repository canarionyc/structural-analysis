import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Context: In alloys, the Hall-Petch relation states that yield strength increases as crystal grain size decreases. Structural engineers often analyze micrographs to determine average grain size.
#
# The Task: Generate a synthetic 2D "microstructure" using Voronoi tessellation (a mathematical way to simulate grain growth) and analyze the grain areas.

# 1. Generate Synthetic Grain Centers (Nucleation sites)
np.random.seed(42)
n_grains = 50
# Random points in a 100x100 micron window
points = np.random.rand(n_grains, 2) * 100

# 2. Compute Voronoi Tessellation (Simulates Grain Boundaries)
vor = Voronoi(points)

# 3. Visualize
fig, ax = plt.subplots(figsize=(8, 8))
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='black', line_width=2, point_size=0)

# Colorize grains to look like a micrograph
for region_index in vor.point_region:
    region = vor.regions[region_index]
    if not -1 in region and len(region) > 0:
        polygon = [vor.vertices[i] for i in region]
        plt.fill(*zip(*polygon), alpha=0.6)

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title('Synthetic Microstructure (Voronoi Tessellation)')
plt.xlabel(r'Position ($\mu m$)')
plt.ylabel(r'Position ($\mu m$)')
plt.show()

print("This simulation mimics how grains grow outward from random nucleation sites until they hit a neighbor.")