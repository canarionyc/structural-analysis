#%% Example of a simply supported beam with a point load.
# Units used for the model in this example are inches and kips

# Import `FEModel3D` from `Pynite`
from Pynite import FEModel3D

# Import 'Visualization' for rendering the model
from Pynite import Visualization
from test_python_package.utils import to_si, kip, u
# Create a new finite element model
beam = FEModel3D()

# Add nodes (14 ft apart)
beam.add_node('N1', 0, 0, 0)
beam.add_node('N2', 14*12, 0, 0)

# Define a material
E = 29000       # Modulus of elasticity (ksi)
G = 11200       # Shear modulus of elasticity (ksi)
nu = 0.3        # Poisson's ratio
rho = 2.836e-4  # Density (kci)
beam.add_material('Steel', E, G, nu, rho)

# Add a section with the following properties:
# Iy = 100 in^4, Iz = 150 in^4, J = 250 in^4, A = 20 in^2
beam.add_section('MySection', 20, 100, 150, 250)

#Add member
beam.add_member('M1', 'N1', 'N2', 'Steel', 'MySection')

# %% Provide simple supports
help(beam.def_support)
beam.def_support('N1', True, True, True, True, False, False)  # Constrained for torsion at 'N1'
beam.def_support('N2', True, True, True, False, False, False) # Not constrained for torsion at 'N2'

# Add a downward point load of 5 kips at the midspan of the beam
beam.add_member_pt_load('M1', 'Fy', -5, 7*12, 'D') # 5 kips Dead load
beam.add_member_pt_load('M1', 'Fy', -8, 7*12, 'L') # 8 kips Live load

# Add load combinations
beam.add_load_combo('1.4D', {'D':1.4})
beam.add_load_combo('1.2D+1.6L', {'D':1.2, 'L':1.6})

1.2*5+1.6*8

# %% Analyze the beam and perform a statics check
beam.analyze(check_statics=True)

# %% Print reactions at each end of the beam
R_left=beam.nodes['N1'].RxnFY['1.2D+1.6L']
R_right=beam.nodes['N2'].RxnFY['1.2D+1.6L']

print(f"Left Support Reaction: {R_left:.3f} kip")
print(f"Right Support Reacton: {R_right:.3f} kip")

print(f"Left Support Reaction: {to_si(R_left, kip, u.N):.3f} N")
print(f"Right Support Reacton: {to_si(R_right, kip, u.N):.3f} N")

# %% Print the max/min shears and moments in the beam
print(f"Maximum Shear: {beam.members['M1'].max_shear('Fy', '1.2D+1.6L'):.3f} kip")
print(f"Minimum Shear: {beam.members['M1'].min_shear('Fy', '1.2D+1.6L'):.3f} kip")
print(f"Maximum Moment: {beam.members['M1'].max_moment('Mz', '1.2D+1.6L')/12:.3f} kip-ft")
print(f"Minimum Moment: {beam.members['M1'].min_moment('Mz', '1.2D+1.6L')/12:.3f} kip-ft")

print(f"Maximum Shear: {to_si(beam.members['M1'].max_shear('Fy', '1.2D+1.6L'), kip, u.N):.3f} N")
print(f"Minimum Shear: {to_si(beam.members['M1'].min_shear('Fy', '1.2D+1.6L'), kip, u.N):.3f} N")
print(f"Maximum Moment: {to_si(beam.members['M1'].max_moment('Mz', '1.2D+1.6L')/12, kip*u.ft, u.N*u.m):.3f} N·m")
print(f"Minimum Moment: {to_si(beam.members['M1'].min_moment('Mz', '1.2D+1.6L')/12, kip*u.ft, u.N*u.m):.3f} N·m")

# Print the max/min deflections in the beam
print(f"Maximum Deflection: {beam.members['M1'].max_deflection('dy', '1.2D+1.6L'):.3f} in")
print(f"Minimum Deflection: {beam.members['M1'].min_deflection('dy', '1.2D+1.6L'):.3f} in")

# #%% Render the model
# from Pynite.Visualization import Renderer
# renderer = Renderer(beam)
# renderer.deformed_shape = True
# renderer.deformed_scale = 30
# renderer.render_loads = True
# renderer.combo_name = '1.2D+1.6L'
# renderer.render_model()

# %% Print the shear, moment, and deflection diagrams
beam.members['M1'].plot_shear('Fy', '1.2D+1.6L')
beam.members['M1'].plot_moment('Mz', '1.2D+1.6L')
beam.members['M1'].plot_deflection('dy', '1.2D+1.6L')

# The following lines can be uncommented to create a PDF report. Follow the instructions on the
# wiki under "Generating PDF Reports" to prevent errors. The report will be output to the Pynite
# folder unless the 'output_path' variable below is modified.

# from Pynite import Reporting
# Reporting.create_report(beam, output_filepath='./Pynite Report.html',
#     format='pdf', node_table=False, plate_table=False, plate_corner_forces=False,
#     plate_center_forces=False, plate_corner_membrane=False, plate_center_membrane=False)