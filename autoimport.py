"""
autoimport.py - Common imports and functionality for pyStructuralAnalysis

This module provides convenient imports for common scientific computing libraries
used throughout the structural analysis notebooks and scripts.
"""

# Core scientific computing libraries
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pint

# Configure sympy for better output
sp.init_printing(order='lex')

# Create a unit registry for physical quantities
ureg = pint.UnitRegistry()

# Configure matplotlib for better plots
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# Make common symbols available
def create_structural_symbols():
    """Create commonly used structural analysis symbols"""
    # Geometric symbols
    x, y, z = sp.symbols('x y z', real=True)
    L, a, b, h = sp.symbols('L a b h', positive=True)
    
    # Material properties
    E, G, nu = sp.symbols('E G nu', positive=True)  # Young's modulus, shear modulus, Poisson's ratio
    
    # Section properties
    I, A, J = sp.symbols('I A J', positive=True)  # Moment of inertia, area, torsional constant
    
    # Loads and reactions
    P, q, M = sp.symbols('P q M', real=True)  # Point load, distributed load, moment
    R_A, R_B, M_A, M_B = sp.symbols('R_A R_B M_A M_B', real=True)  # Reactions
    
    return {
        'x': x, 'y': y, 'z': z,
        'L': L, 'a': a, 'b': b, 'h': h,
        'E': E, 'G': G, 'nu': nu,
        'I': I, 'A': A, 'J': J,
        'P': P, 'q': q, 'M': M,
        'R_A': R_A, 'R_B': R_B, 'M_A': M_A, 'M_B': M_B
    }

# Convenience function to import everything into global namespace
def import_all():
    """Import all common functionality into the calling namespace"""
    import inspect
    frame = inspect.currentframe().f_back
    
    # Import the libraries
    frame.f_globals['np'] = np
    frame.f_globals['plt'] = plt
    frame.f_globals['sp'] = sp
    frame.f_globals['ureg'] = ureg
    
    # Import common symbols
    symbols = create_structural_symbols()
    frame.f_globals.update(symbols)
    
    print("Imported: numpy as np, matplotlib.pyplot as plt, sympy as sp, pint unit registry as ureg")
    print("Available symbols:", ', '.join(symbols.keys()))

# Make the library imports available at module level
__all__ = ['np', 'plt', 'sp', 'ureg', 'create_structural_symbols', 'import_all']