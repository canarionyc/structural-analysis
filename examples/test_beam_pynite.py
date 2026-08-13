
from Pynite import FEModel3D
help(FEModel3D)

beam = FEModel3D()
beam.add_node('N1', 0, 0, 0)
beam.add_node('N2', 20, 0, 0)

# Define properties and elements
beam.add_material('Steel', E=2e11, G=77e9, nu=0.3, rho=7850)
help(beam.add_member)
beam.add_member(name='M1',i_node='N1',j_node='N2', material_name='Steel', Iy=1e-4, Iz=1e-4, J=1e-5, A=0.01)

# Apply supports and loads
beam.def_support('N1', True, True, True, True, True, True) # Fixed
beam.add_member_pt_load('M1', 'Fy', -1000, 10) # 1000 N downward at midspan

beam.analyze()
# PyNite handles the SciPy matrix math for you and outputs the exact shear/moments!