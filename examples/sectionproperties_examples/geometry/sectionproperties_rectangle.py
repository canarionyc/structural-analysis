#%%
import doctest

# This will run the examples found in the docstring of the class/function.
# It will print nothing if the tests pass, or error logs if they fail.
doctest.run_docstring_examples(RectangularCrossSection, globals(), verbose=True)
#%%
from sectionproperties.pre.library import rectangular_section

w=50; h=100
my_section = rectangular_section(d=h, b=w).plot_geometry()
dir(my_section)
help(rectangular_section)