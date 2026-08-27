#%% setup
#%%
import sectionproperties
help(sectionproperties)
dir(sectionproperties)
#%%
from sectionproperties.pre import library
from sectionproperties.pre.pre import DEFAULT_MATERIAL
print( DEFAULT_MATERIAL)
help(library)
dir(library)

#%% primitive sections


#%% rectangular section

from sectionproperties.pre.library import rectangular_section
help(rectangular_section)


#%%
w=50; h=100
rect = rectangular_section(d=h, b=w)
dir(rect)
rect.calculate_area()
rect.calculate_centroid()


rect.plot_geometry()