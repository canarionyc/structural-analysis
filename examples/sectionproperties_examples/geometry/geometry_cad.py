# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Geometry from CAD
#
# This example demonstrates loading ``Geometry`` and ``CompoundGeometry`` objects from ``.dxf`` and ``.3dm`` (rhino) files.

# %% [markdown]
# ## Import Modules
#
# We start by importing the necessary modules.

# %%
import os
from pprint import pp

from sectionproperties.analysis import Section
from sectionproperties.pre import CompoundGeometry, Geometry

# %% [markdown]
# ## Load from ``.dxf``

# %% [markdown]
# ### ``Geometry`` object
#
# We can load a single region from a ``.dxf`` file by using the [Geometry.from_dxf()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.from_dxf) method.

# %%
import pyprojroot
#help(pyprojroot)
print(pyprojroot.here())

# %%

# help(os.path.join)

cad_files_dir=os.path.join(r'C:\repos\section-properties-master\docs', "_static", "cad_files")
assert os.path.exists(cad_files_dir)
pp(os.listdir(cad_files_dir))
# %%
import shapely.geometry
import cad_to_shapely as c2s
dir(c2s)
help(c2s)
help(c2s.examples)

from c2s import utils
import c2s.utils
help(c2s.utils)

# %%
geom = Geometry.from_dxf(dxf_filepath=os.path.join(cad_files_dir, "box_section.dxf"))
geom.plot_geometry()
# %% [markdown]
# To display the section, we mesh the geometry and plot the mesh.

# %% nbsphinx-thumbnail={"output-index": 0}
geom.create_mesh(mesh_sizes=[0.5])
Section(geometry=geom).plot_mesh(materials=False)

# %% [markdown]
# Note that loading multiple regions from a `.dxf` file is not currently supported. A possible work around could involve saving each region as a separate `.dxf` file, importing each region individually using `Geometry.from_dxf()`, then combining the regions using the `+` operator.

# %% [markdown]
# ## Load from ``.3dm``

# %% [markdown]
# ### ``Geometry`` object
#
# We can load a single region from a ``.3dm`` file by using the [Geometry.from_3dm()](../../gen/sectionproperties.pre.geometry.Geometry.rst#sectionproperties.pre.geometry.Geometry.from_3dm) method.

# %%
help(Geometry.from_3dm)

geom = Geometry.from_3dm(filepath=os.path.join(cad_files_dir, "rhino.3dm"))
geom.plot_geometry()
geom = geom.rotate_section(angle=90)  # rotate for viewability
geom.plot_geometry()
# %% [markdown]
# To display the section, we mesh the geometry and plot the mesh.

# %%
geom.create_mesh(mesh_sizes=[0.005])
Section(geometry=geom).plot_mesh(materials=False)

# %% [markdown]
# ### ``CompoundGeometry`` object
#
# We can load multiple regions from a ``.3dm`` file by using the [CompoundGeometry.from_3dm()](../../gen/sectionproperties.pre.geometry.CompoundGeometry.rst#sectionproperties.pre.geometry.CompoundGeometry.from_3dm) method.

# %%
geom = CompoundGeometry.from_3dm(filepath=os.path.join(cad_files_dir, "rhino_compound.3dm"))
geom.plot_geometry()
geom = geom.rotate_section(angle=90)  # rotate for viewability
geom.plot_geometry()
# %% [markdown]
# To display the section, we mesh the geometry and plot the mesh.

# %%
geom.create_mesh(mesh_sizes=[0.005])
Section(geometry=geom).plot_mesh(materials=False)