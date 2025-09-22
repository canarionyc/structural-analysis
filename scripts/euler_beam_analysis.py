# %% Euler Beam Point Load Analysis
"""
Analysis of a simply supported beam with a point load using symbolic computation.
This script demonstrates the derivation of beam deflection and slope formulas.
"""

# Import common structural analysis functionality
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autoimport import import_all
import_all()

# %% Setup symbols and problem definition
print("=== Euler Beam Point Load Analysis ===")
print("Analyzing a simply supported beam with point load P at distance 'a' from left support")

# Create constraint that enforces a <= L
constraint = sp.Le(a, L)
print(f"Constraint: {constraint}")

# Define the relationship b = L - a
b_relation = sp.Eq(b, L - a)
print(f"Relationship: {b_relation}")

# %% Reaction calculations
print("\n=== Reaction Analysis ===")

# For equilibrium: Sum of vertical forces = 0, Sum of moments = 0
# R_A + R_B = P
# R_A * L = P * a  (taking moments about B)

R_A_formula = P * a / L
R_B_formula = P * b / L

print(f"Reaction at A: R_A = {R_A_formula}")
print(f"Reaction at B: R_B = {R_B_formula}")

# %% Moment function definition
print("\n=== Moment Functions ===")

# For 0 <= x < a: M(x) = R_A * x
M1 = R_A_formula * x
print(f"Moment for 0 ≤ x < a: M1(x) = {M1}")

# For a <= x <= L: M(x) = R_A * x - P * (x - a)
M2 = R_A_formula * x - P * (x - a)
print(f"Moment for a ≤ x ≤ L: M2(x) = {M2}")

# %% Integration to find slope and deflection
print("\n=== Integration for Slope and Deflection ===")

# Define integration constants
C1, C2, C3, C4 = sp.symbols('C1 C2 C3 C4')

# Integrate EI * v''(x) = M(x) to get slope
# For 0 <= x < a
v1_prime = sp.integrate(M1 / (E * I), x) + C1
print(f"Slope v1'(x) = {v1_prime}")

# For a <= x <= L
v2_prime = sp.integrate(M2 / (E * I), x) + C2
print(f"Slope v2'(x) = {v2_prime}")

# Integrate again to get deflection
v1 = sp.integrate(v1_prime, x) + C3
v2 = sp.integrate(v2_prime, x) + C4

print(f"Deflection v1(x) = {v1}")
print(f"Deflection v2(x) = {v2}")

# %% Apply boundary conditions
print("\n=== Boundary Conditions ===")

# Boundary conditions:
# 1. v(0) = 0 (simply supported at A)
# 2. v(L) = 0 (simply supported at B)
# 3. v1(a) = v2(a) (continuity of deflection)
# 4. v1'(a) = v2'(a) (continuity of slope)

eqs = [
    v1.subs(x, 0),  # v(0) = 0
    v2.subs(x, L),  # v(L) = 0
    sp.simplify(v1.subs(x, a) - v2.subs(x, a)),  # continuity at x=a
    sp.simplify(v1_prime.subs(x, a) - v2_prime.subs(x, a))  # slope continuity at x=a
]

print("Boundary condition equations:")
for i, eq in enumerate(eqs, 1):
    print(f"{i}. {eq} = 0")

# %% Solve for integration constants
print("\n=== Solving for Integration Constants ===")

try:
    sol = sp.solve(eqs, (C1, C2, C3, C4), dict=True)[0]
    print("Solution found:")
    for const, value in sol.items():
        print(f"{const} = {value}")
        
    # %% Calculate slope at left end
    print("\n=== Slope at Left End ===")
    
    # Slope at left end (x=0)
    theta_A = v1_prime.subs(C1, sol[C1]).subs(x, 0)
    theta_A = sp.simplify(theta_A.subs(b, L - a))
    
    print("θ_A (slope at left end) =")
    sp.pprint(theta_A)
    
    # Compare with known formula
    theta_A_formula = P*a*b*(L+b)/(6*E*I*L)
    print(f"\nCompare to formula: P*a*b*(L+b)/(6*E*I*L)")
    print(f"Formula gives: {theta_A_formula}")
    
    # Check if they're equal
    difference = sp.simplify(theta_A - theta_A_formula.subs(b, L - a))
    print(f"Difference: {difference}")
    print(f"Proof correct: {difference == 0}")
    
except Exception as e:
    print(f"Error solving system: {e}")
    print("This might be due to the complexity of the symbolic system.")

print("\n=== Analysis Complete ===")