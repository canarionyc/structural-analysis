import sympy as sp

# 1. Define equations with strict mathematical assumptions
L = sp.Symbol('L', positive=True)  # Length must be positive
P = sp.Symbol('P')                 # Load has no assumptions
a = sp.Symbol('a', positive=True)
R_A = sp.Symbol('R_A')

reactions = {R_A: (L*P - P*a)/L}

# 2. Our JSON parameters (Notice L is negative, which violates the physics!)
json_params = {'L': -10.0, 'a': 4.0, 'P': 1000.0}

safe_params = {}
rejected_params = {}

# 3. The Logic: Check assumptions before mapping
for sym in reactions[R_A].free_symbols:
    if sym.name in json_params:
        val = json_params[sym.name]
        
        # Check against the assumption properties
        if sym.is_positive and val <= 0:
            rejected_params[sym.name] = val
        elif sym.is_negative and val >= 0:
            rejected_params[sym.name] = val
        # Add more assumption checks here as needed...
        else:
            # If it passes, map the string to the actual SymPy object
            safe_params[sym] = val

# 4. Execute
print("Safe to substitute:", safe_params)
print("Rejected due to assumptions:", rejected_params)

# Only substitute the safe values
num_reactions = {R_A: reactions[R_A].subs(safe_params)}
print("Resulting Equation:", num_reactions)