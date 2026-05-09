"""
Constants and tables derived from the Spanish Technical Building Code (CTE DB SE-A).
"""

# DB SE-A Table 6.3: Imperfection factors for buckling curves
BUCKLING_CURVES = {
    'a0': 0.13,
    'a': 0.21,
    'b': 0.34,
    'c': 0.49,
    'd': 0.76
}

# In the future, you can add things like:
PARTIAL_SAFETY_FACTORS = {'gamma_M0': 1.05, 'gamma_M1': 1.05, 'gamma_M2': 1.25}