# %%
import matplotlib
# matplotlib.use('QtAgg')
# matplotlib.use('Agg') # non-interactive backend for testing




# matplotlib.use('TkAgg') # i didn't install tk, so this will fail, but it's just for testing purposes
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()


x = np.linspace(0, 2*np.pi, 100)
y = np.sin(3*x)
ax.plot(x, y)
ax.set_title('Sine Wave')
ax.set_xlabel('x')
ax.set_ylabel('sin(3x)')

plot_path = 'test_plot.png'
fig.savefig(plot_path)
#%% 
plt.show()

#%% 
print(f"Plot saved to: {plot_path}")
# %%
