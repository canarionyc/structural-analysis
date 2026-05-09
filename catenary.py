#%%
import numpy as np
import matplotlib.pyplot as plt

# Configuration toggle
LANG = 'EN' # Toggle 'EN' or 'ES'

# Bilingual dictionary for the plot
plot_text = {
    'EN': {
        'title': 'Catenary Curve (Arch)',
        'xlabel': 'Horizontal Distance (m)',
        'ylabel': 'Height (m)',
        'annot': 'Lowest point'
    },
    'ES': {
        'title': 'Curva Catenaria (Arco)',
        'xlabel': 'Distancia Horizontal (m)',
        'ylabel': 'Altura (m)',
        'annot': 'Punto más bajo'
    }
}

#%%
# Calculate the structural curve
a = 5.0
catenary_x = np.linspace(-10, 10, 100)
catenary_y = a * np.cosh(catenary_x / a)


# Plotting the curve
plt.figure(figsize=(8, 5))
plt.plot(catenary_x, catenary_y, color='blue')

# Apply bilingual labels using the dictionary
plt.title(plot_text[LANG]['title'])
plt.xlabel(plot_text[LANG]['xlabel'])
plt.ylabel(plot_text[LANG]['ylabel'])

plt.annotate(plot_text[LANG]['annot'], xy=(0, a), xytext=(0, a + 5),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.grid(True)
plt.show()

