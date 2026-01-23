import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. Define the Lattice for BCC Iron (Alpha-Fe)
# Lattice parameter 'a' for Fe is approx 2.866 Angstroms
a = 2.866

# Atoms in BCC are at (0,0,0) and (0.5, 0.5, 0.5) in fractional coordinates
points = np.array([
    [0, 0, 0],
    [0.5, 0.5, 0.5]
])

# Convert fractional to cartesian coordinates
cartesian_points = points * a


# 2. Visualization
def plot_unit_cell(points, lattice_param):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot atoms
    ax.scatter(points[:, 0], points[:, 1], points[:, 2],
               s=2000, c='steelblue', alpha=1, edgecolors='k', label='Fe Atoms')

    # Draw Unit Cell Box edges
    r = [0, lattice_param]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s - e)) == r[1] - r[0]:
            ax.plot3D(*zip(s, e), color="black", linestyle='--')

    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.set_title(f'BCC Iron Unit Cell (a={lattice_param} Å)')
    plt.legend()
    plt.show()


# Helper libraries for drawing the box
from itertools import product, combinations

# 3. Calculate Density
# Atomic Mass of Fe = 55.845 g/mol
# Avogadro's number = 6.022e23
# Volume = a^3
molar_mass_fe = 55.845
n_atoms = 2  # BCC has 2 atoms per unit cell
volume_cm3 = (a * 1e-8) ** 3
mass_cell_grams = (n_atoms * molar_mass_fe) / 6.022e23

density = mass_cell_grams / volume_cm3

print(f"Computed Density of BCC Iron: {density:.3f} g/cm^3")
plot_unit_cell(cartesian_points, a)