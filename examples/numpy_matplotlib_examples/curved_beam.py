#%%
import numpy as np
import matplotlib.pyplot as plt

# Toggle switch for language ('EN' or 'ES')
LANG = 'EN'

#%%
# Define arch geometry
theta = np.linspace(0, np.pi, 100)
R = 2.0  # Radius in meters
x = R * np.cos(theta)
y = R * np.sin(theta)

# Simplified Bending Moment distribution for a point load P at the crown
# M(theta) is roughly proportional to the deviation from the thrust line
M = 1.5 * (np.sin(theta) - 2/np.pi)

# Coordinates for plotting the moment diagram normal to the arch
x_M = (R + M) * np.cos(theta)
y_M = (R + M) * np.sin(theta)

# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# Toggle switch for language ('EN' or 'ES')
LANG = 'EN'


def plot_lever_arms_crown():
    # Bilingual dictionary for annotations and labels
    texts = {
        'EN': {
            'title': 'Lever Arms: Node j at the Crown',
            'node_j': 'Node j (Crown)',
            'cut': r'Cut Section ($\phi$)',
            'fx': '$F_{xj}$',
            'fy': '$F_{yj}$',
            'arm_fx': r'Lever arm for $F_{xj}$: $R(1 - \cos\phi)$',
            'arm_fy': r'Lever arm for $F_{yj}$: $R\sin\phi$',
            'radius': 'R',
            'angle': r'$\phi$'
        },
        'ES': {
            'title': 'Brazos de Palanca: Nodo j en la Clave',
            'node_j': 'Nodo j (Clave)',
            'cut': r'Sección de Corte ($\phi$)',
            'fx': '$F_{xj}$',
            'fy': '$F_{yj}$',
            'arm_fx': r'Brazo para $F_{xj}$: $R(1 - \cos\phi)$',
            'arm_fy': r'Brazo para $F_{yj}$: $R\sin\phi$',
            'radius': 'R',
            'angle': r'$\phi$'
        }
    }

    # Parameters
    R = 10.0
    phi_deg = 45.0  # Angle for the cut section
    phi_rad = np.radians(phi_deg)

    # Arch geometry (Quarter circle from crown down to springing)
    theta = np.linspace(0, np.pi / 2, 100)
    # Parametric equations measuring phi from the vertical
    x_arch = R * np.sin(theta)
    y_arch = R * np.cos(theta)

    # Coordinates
    node_j = (0, R)
    cut_x = R * np.sin(phi_rad)
    cut_y = R * np.cos(phi_rad)
    origin = (0, 0)

    # Initialize plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot arch
    ax.plot(x_arch, y_arch, 'k-', linewidth=3)

    # Plot origin and reference axes
    ax.plot([0, 0], [0, R + 2], 'k-.', alpha=0.5)  # Vertical centerline
    ax.plot([0, R + 2], [0, 0], 'k-.', alpha=0.5)  # Horizontal base

    # Plot Node j and Cut Section
    ax.plot(*node_j, 'ko', markersize=8)
    ax.text(0.5, R + 0.2, texts[LANG]['node_j'], fontsize=12, fontweight='bold')

    ax.plot(cut_x, cut_y, 'ro', markersize=8)
    ax.text(cut_x + 0.5, cut_y + 0.2, texts[LANG]['cut'], color='red', fontsize=12)

    # Draw Forces at Node j
    ax.arrow(0, R, 2.5, 0, head_width=0.3, head_length=0.4, fc='blue', ec='blue')
    ax.text(2.8, R, texts[LANG]['fx'], color='blue', fontsize=14, va='center')

    ax.arrow(0, R, 0, 2.5, head_width=0.3, head_length=0.4, fc='green', ec='green')
    ax.text(0, R + 2.8, texts[LANG]['fy'], color='green', fontsize=14, ha='center')

    # Draw Lever Arms
    # Lever arm for Fxj (Vertical drop)
    ax.plot([cut_x, cut_x], [cut_y, R], 'b--', linewidth=2)
    ax.plot([0, cut_x], [R, R], 'b:', alpha=0.5)  # reference horizontal
    ax.text(cut_x + 0.2, (R + cut_y) / 2, texts[LANG]['arm_fx'], color='blue', fontsize=12)

    # Lever arm for Fyj (Horizontal deviation)
    ax.plot([0, cut_x], [cut_y, cut_y], 'g--', linewidth=2)
    ax.text(cut_x / 2, cut_y - 0.5, texts[LANG]['arm_fy'], color='green', fontsize=12, ha='center')

    # Draw Radius and Angle
    ax.plot([0, cut_x], [0, cut_y], 'gray', linestyle='-')
    ax.text(cut_x / 2 - 0.5, cut_y / 2 - 0.5, texts[LANG]['radius'], color='gray', fontsize=12)

    # Angle arc
    angle_arc = Arc((0, 0), R * 0.4, R * 0.4, angle=0, theta1=90 - phi_deg, theta2=90, color='orange', linewidth=2)
    ax.add_patch(angle_arc)
    ax.text(R * 0.1, R * 0.3, texts[LANG]['angle'], color='orange', fontsize=14)

    # Formatting
    ax.set_aspect('equal')
    ax.set_xlim(-1, R + 4)
    ax.set_ylim(-1, R + 4)
    ax.set_title(texts[LANG]['title'], fontsize=14, pad=20)
    ax.axis('off')

    plt.tight_layout()
    savefig_path = f'img/lever_arms_crown_{LANG}.png'
    plt.savefig(savefig_path, dpi=300)
    plt.show()


plot_lever_arms_crown()
#%%
# Bilingual dictionaries for plot labels
texts = {
    'EN': {
        'title': 'Curved Beam (Arch) - Bending Moment Visualization',
        'xlabel': 'Horizontal Distance (m)',
        'ylabel': 'Vertical Height (m)',
        'arch': 'Arch Geometry',
        'moment': 'Bending Moment Diagram',
        'load': 'Point Load P'
    },
    'ES': {
        'title': 'Viga Curva (Arco) - Visualización del Momento Flector',
        'xlabel': 'Distancia Horizontal (m)',
        'ylabel': 'Altura Vertical (m)',
        'arch': 'Geometría del Arco',
        'moment': 'Diagrama de Momento Flector',
        'load': 'Carga Puntual P'
    }
}

# Generate the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'k-', linewidth=3, label=texts[LANG]['arch'])
plt.plot(x_M, y_M, 'r--', label=texts[LANG]['moment'])

# Fill the area between the arch and the moment diagram
plt.fill_between(x, y, y_M, color='red', alpha=0.2)

# Add point load arrow at the crown
plt.arrow(0, R + 0.6, 0, -0.5, head_width=0.15, head_length=0.15, fc='blue', ec='blue')
plt.text(0.15, R + 0.4, texts[LANG]['load'], color='blue', fontsize=12, fontweight='bold')

# Formatting
plt.title(texts[LANG]['title'], fontsize=14)
plt.xlabel(texts[LANG]['xlabel'], fontsize=12)
plt.ylabel(texts[LANG]['ylabel'], fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle=':', alpha=0.7)
plt.axis('equal')

export_path = f'img/curved_beam_moment_{LANG}.png'
plt.savefig(export_path, dpi=300, bbox_inches='tight')

plt.show()