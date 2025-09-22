# %% setup
# Import common structural analysis functionality
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autoimport import import_all
import_all()

# Example: Basic structural analysis computation
print("=== Basic Structural Analysis Example ===")
print(f"Creating a simple beam of length L = {L}")

# Example calculation: deflection of a simply supported beam with point load
print("\nCalculating deflection for a simply supported beam with point load P at distance 'a' from left support")
deflection_formula = P * a * b * (L**2 - b**2 - a**2) / (6 * E * I * L)
print("Deflection at load point:", deflection_formula)
