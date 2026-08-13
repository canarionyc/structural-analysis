#%% SymPy Unit Conversion
# 1. Define missing US Customary units in SymPy
import sympy.physics.units as u
from sympy.physics.units import convert_to
kip = u.Quantity('kip')
# 1 lbf = 4.4482216 Newtons, so 1 kip = 4448.2216 N
# help(kip.set_global_relative_scale_factor)
kip.set_global_relative_scale_factor(4448.2216 , u.N)

# Define derived units (ksi, kci)
ksi = kip / u.inch**2
kci = kip / u.inch**3

def to_si(value, from_unit, to_unit):
    """
    Helper function to convert a value and strip the SymPy unit object,
    returning a clean Python float for PyNite to use.
    """
    expr = value * from_unit
    converted = convert_to(expr, to_unit)
    return float(converted / to_unit)