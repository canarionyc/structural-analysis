#%% setup
import os
print(os.getcwd())
from time import strftime

import json
import sympy as sp
import math

def solve_truss_from_json(json_file_path):
    # 1. Parse the JSON File
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        
    model = data['StructuralAnalysisModel']
    nodes_data = model['geometry']['nodes']
    elems_data = model['geometry']['elements']
    
    # We will assume standard Example 1.1 conditions based on your files:
    # Nodes 1, 2, 3 are pinned (fixed X, fixed Y)
    # Node 4 is free, with a load of [100.0, -50.0]
    
    # 2. Extract Nodes
    nodes = {}
    for n in nodes_data:
        nodes[n['name']] = n['crd']
        
    # 3. Setup Global Stiffness Matrix [K] (8x8 for 4 nodes, 2 DOFs each)
    # We use SymPy matrices initialized to zero
    num_dofs = len(nodes) * 2
    K_global = sp.zeros(num_dofs, num_dofs)
    
    # Material E (Assuming 3000 based on standard OpenSees Example 1.1)
    E = 3000.0 
    
    print("Assembling Global Stiffness Matrix...")
    # 4. Assemble Stiffness Matrix
    for ele in elems_data:
        n1, n2 = ele['nodes']
        A = ele['A']
        
        # Coordinates
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        
        # Length and direction cosines
        L = math.hypot(x2 - x1, y2 - y1)
        c = (x2 - x1) / L
        s = (y2 - y1) / L
        
        # Local stiffness factor
        k = (A * E) / L
        
        # Element stiffness matrix (4x4)
        k_ele = sp.Matrix([
            [ c*c,  c*s, -c*c, -c*s],
            [ c*s,  s*s, -c*s, -s*s],
            [-c*c, -c*s,  c*c,  c*s],
            [-c*s, -s*s,  c*s,  s*s]
        ]) * k
        
        # Map to global DOFs
        dofs = [ (n1-1)*2, (n1-1)*2+1, (n2-1)*2, (n2-1)*2+1 ]
        
        for i in range(4):
            for j in range(4):
                K_global[dofs[i], dofs[j]] += k_ele[i, j]

    # 5. Apply Boundary Conditions and Loads
    # Nodes 1, 2, 3 are fixed -> DOFs 0, 1, 2, 3, 4, 5 are zero.
    # Node 4 is free -> DOFs 6, 7 are active.
    active_dofs = [6, 7]
    
    # Applied force vector at Node 4
    F_applied = sp.Matrix([100.0, -50.0])
    
    # Extract the reduced stiffness matrix for active DOFs
    K_reduced = K_global[active_dofs, active_dofs]
    
    print("Solving for Displacements...")
    # 6. Solve for Displacements (U = K^-1 * F)
    U_active = K_reduced.inv() * F_applied
    
    # Reconstruct full displacement vector
    U_full = sp.zeros(num_dofs, 1)
    U_full[6, 0] = U_active[0]
    U_full[7, 0] = U_active[1]
    
    print(f"Node 4 Displacements: DX = {U_active[0]:.5f}, DY = {U_active[1]:.5f}\\n")
    
    # 7. Calculate Reactions (R = K * U_full)
    Forces_total = K_global * U_full
    
    print("--- Reaction Forces ---")
    print(f"Node 1: RX = {Forces_total[0]:.2f}, RY = {Forces_total[1]:.2f}")
    print(f"Node 2: RX = {Forces_total[2]:.2f}, RY = {Forces_total[3]:.2f}")
    print(f"Node 3: RX = {Forces_total[4]:.2f}, RY = {Forces_total[5]:.2f}")
    
    # Verification (Sum of forces should equal applied load but in opposite direction)
    sum_rx = Forces_total[0] + Forces_total[2] + Forces_total[4]
    sum_ry = Forces_total[1] + Forces_total[3] + Forces_total[5]
    print("\\n--- Equilibrium Check ---")
    print(f"Sum FX Reactions: {sum_rx:.2f} (Applied: 100.0)")
    print(f"Sum FY Reactions: {sum_ry:.2f} (Applied: -50.0)")

# Run the function
if __name__ == "__main__":
    # Ensure the JSON file is in the same directory, or provide the full path
    solve_truss_from_json(r"C:\dev\structural-analysis\Example1.1.json")