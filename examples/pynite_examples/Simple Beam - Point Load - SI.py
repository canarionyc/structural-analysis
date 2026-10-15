# %% Setup
import sympy as sp

from Pynite import FEModel3D



#%% 2. Convert Geometry & Load Inputs to SI (meters, Newtons)
L_m   = to_si(12*14, u.inch, u.m)
# P_N   = to_si(-10, kip, u.N)   # Assuming a 10 kip downward load
# loc_m = to_si(10, u.inch, u.m) # Placed at 10 inches

# 3. Convert Material Properties to SI (Pascals)
E_Pa  = to_si(29000, ksi, u.Pa)
G_Pa  = to_si(11200, ksi, u.Pa)
nu    = 0.3 # Poisson's ratio is dimensionless
# Convert weight density (kci) to mass density (kg/m^3)
# Note: PyNite expects mass density for dynamic analyses (divide weight by 9.81 m/s^2)
gamma_N_m3 = to_si(2.836e-4, kci, u.N / u.m**3)
rho_kg_m3  = gamma_N_m3 / 9.81

# 4. Convert Section Properties to SI (m^2, m^4)
A_m2  = to_si(20,  u.inch**2, u.m**2)
Iy_m4 = to_si(100, u.inch**4, u.m**4)
Iz_m4 = to_si(150, u.inch**4, u.m**4)
J_m4  = to_si(250, u.inch**4, u.m**4)

# %% Build and Solve the PyNite Model in SI
beam_si = FEModel3D()

# %% Add nodes in meters
beam_si.add_node('N1', 0, 0, 0)
beam_si.add_node('N2', L_m, 0, 0)

# %% Add Material (Pa, kg/m^3)
beam_si.add_material('Steel', E_Pa, G_Pa, nu, rho_kg_m3)
print(beam_si.materials)
# %% Add Section (m^2, m^4)
beam_si.add_section('MySection', A_m2, Iy_m4, Iz_m4, J_m4)

# %% Add member
beam_si.add_member('M1', 'N1', 'N2', 'Steel', 'MySection')

# %% Provide simple supports
beam_si.def_support('N1', True, True, True, True, False, False)
beam_si.def_support('N2', True, True, True, False, False, False)

#%% Add load

# Add a downward point load of 5 kips at the midspan of the beam
beam_si.add_member_pt_load('M1', 'Fy', to_si(-5, kip, u.N), to_si(7*12, u.inch, u.m), 'D') # 5 kips Dead load
beam_si.add_member_pt_load('M1', 'Fy', to_si(-8, kip, u.N), to_si(value=7 * 12, from_unit=u.inch, to_unit=u.m), 'L') # 8 kips Live load

# Add load combinations
beam_si.add_load_combo('1.4D', {'D':1.4})
beam_si.add_load_combo('1.2D+1.6L', {'D':1.2, 'L':1.6})

# beam_si.add_member_pt_load('M1', 'Fy', P_N, loc_m, '1.2D+1.6L')

# %% Analyze the model
beam_si.analyze(check_statics=True)

# %% Print reactions at each end of the beam
print(f"Left Support Reaction: {beam_si.nodes['N1'].RxnFY['1.2D+1.6L']:.3f} N")
print(f"Right Support Reacton: {beam_si.nodes['N2'].RxnFY['1.2D+1.6L']:.3f} N")

# %% Print the max/min shears and moments in the beam
print(f"Maximum Shear: {beam_si.members['M1'].max_shear('Fy', '1.2D+1.6L'):.3f} N")
print(f"Minimum Shear: {beam_si.members['M1'].min_shear('Fy', '1.2D+1.6L'):.3f} N")
print(f"Maximum Moment: {beam_si.members['M1'].max_moment('Mz', '1.2D+1.6L'):.3f} N·m")
print(f"Minimum Moment: {beam_si.members['M1'].min_moment('Mz', '1.2D+1.6L'):.3f} N·m")

# Print the max/min deflections in the beam
print(f"Maximum Deflection: {beam_si.members['M1'].max_deflection('dy', '1.2D+1.6L'):.3f} m")
print(f"Minimum Deflection: {beam_si.members['M1'].min_deflection('dy', '1.2D+1.6L'):.3f} m")

#%% Render the model
# from Pynite.Visualization import Renderer
# renderer = Renderer(beam_si)
# renderer.deformed_shape = True
# renderer.deformed_scale = 30
# renderer.render_loads = True
# renderer.combo_name = '1.2D+1.6L'
# renderer.render_model()

# %% Print the shear, moment, and deflection diagrams
beam_si.members['M1'].plot_shear('Fy', '1.2D+1.6L')
beam_si.members['M1'].plot_moment('Mz', '1.2D+1.6L')
beam_si.members['M1'].plot_deflection('dy', '1.2D+1.6L')