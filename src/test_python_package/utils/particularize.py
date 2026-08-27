import sympy as sp
import warnings
from sympy import assuming, assumptions

def replace(solutions, params):
    """
    Substitutes string-keyed parameters into SymPy equations, 
    but only if the numerical values obey the symbols' mathematical assumptions.
    """
    # 1. Convert to a SymPy Dict if a standard Python dict was passed.
    # This guarantees we can easily access .free_symbols across all equations.
    is_std_dict = isinstance(solutions, dict)
    sym_sols = sp.Dict(solutions) if is_std_dict else solutions
    
    safe_params = {}
    
    # 2. Extract the exact memory-hashed symbols
    for sym in sym_sols.free_symbols:
        if sym.name in params:
            val = params[sym.name]
            
            # 3. Validate assumptions
            if sym.is_positive and not val > 0:
                warnings.warn(f"Rejected {sym.name}={val}: Must be positive.")
                continue
            if sym.is_negative and not val < 0:
                warnings.warn(f"Rejected {sym.name}={val}: Must be negative.")
                continue
            if sym.is_nonnegative and not val >= 0:
                warnings.warn(f"Rejected {sym.name}={val}: Must be non-negative.")
                continue
            if sym.is_integer and not float(val).is_integer():
                warnings.warn(f"Rejected {sym.name}={val}: Must be an integer.")
                continue
                
            # If all checks pass, link the exact Symbol object to the value
            safe_params[sym] = val
            
    # 4. Perform the loop-free C-level substitution
    result = sym_sols.subs(safe_params)
    
    # 5. Return the result in the exact same type the user provided
    return dict(result) if is_std_dict else result