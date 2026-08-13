"""
OpenSees JSON Parser & Visualizer for Grasshopper
Inputs:
    json_path: string (Path to your params_ksi_in.json)
    run_analysis: bool (A toggle to run the solver)
Outputs:
    gh_nodes: Point3d objects representing the joints
    gh_elements: LineCurve objects representing the beams
    gh_labels: TextDot objects for node IDs
"""
import json
import openseespy.opensees as ops
import Rhino.Geometry as rg

# Initialize output lists for Grasshopper
gh_nodes = []
gh_elements = []
gh_labels = []

if run_analysis and json_path:
    # 1. Load the Geometry and Properties
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 2. Initialize Model
    ops.wipe()
    ops.model("BasicBuilder", "-ndm", data.get("dimensions", 2), "-ndf", 3)

    # Keep a dictionary of coordinates for drawing elements later
    node_coords = {}

    # 3. Parse Nodes & Generate Visual Points
    for n in data.get('nodes', []):
        node_id = n['id']
        x, y = n['coords'][0], n['coords'][1]
        z = n['coords'][2] if len(n['coords']) > 2 else 0.0
        
        # Build OpenSees Node
        ops.node(node_id, x, y)
        if any(n['fixity']):
            ops.fix(node_id, *n['fixity'])
            
        # Store for lines and Generate Rhino Geometry
        pt = rg.Point3d(x, y, z)
        node_coords[node_id] = pt
        
        gh_nodes.append(pt)
        # Create a floating text dot for the ID
        gh_labels.append(rg.TextDot(str(node_id), pt))

    # 4. Map Materials and Sections
    materials = {m['id']: m for m in data.get('materials', [])}
    sections = {s['id']: s for s in data.get('sections', [])}

    # 5. Parse Elements & Generate Visual Lines
    transfTag = 1
    ops.geomTransf('Linear', transfTag)

    for e in data.get('elements', []):
        if e['type'] == 'beam':
            ele_id = e['id']
            i_node, j_node = e['nodes'][0], e['nodes'][1]
            
            sec = sections[e['section_id']]
            mat = materials[sec['material_id']]
            A, E, I = sec['A'], mat['E'], sec['I']
            
            # Build OpenSees Element
            ops.element('elasticBeamColumn', ele_id, i_node, j_node, A, E, I, transfTag)
            
            # Generate Rhino Geometry
            p1 = node_coords[i_node]
            p2 = node_coords[j_node]
            gh_elements.append(rg.LineCurve(p1, p2))
            
            # Put an element ID label at the midpoint
            mid_pt = (p1 + p2) / 2.0
            gh_labels.append(rg.TextDot(f"E{ele_id}", mid_pt))

    print(f"Successfully loaded {len(gh_nodes)} nodes and {len(gh_elements)} elements.")
else:
    print("Toggle run_analysis to True and provide a valid json_path.")