# coding: utf8
#%%
import rhinoscriptsyntax as rs
import math

# Toggle switch for language ('EN' or 'ES')
LANG = 'EN'

#%%
def visualize_curved_beam_element():
    # Bilingual dictionary for annotations
    texts = {
        'EN': {
            'node_i': 'Node i (Fixed)',
            'node_j': 'Node j (Free)',
            'fx': 'F_xj',
            'fy': 'F_yj',
            'mj': 'M_j',
            'phi': 'Angle \u03C6',
            'radius': 'Radius R'
        },
        'ES': {
            'node_i': 'Nodo i (Fijo)',
            'node_j': 'Nodo j (Libre)',
            'fx': 'F_xj',
            'fy': 'F_yj',
            'mj': 'M_j',
            'phi': 'Ángulo \u03C6',
            'radius': 'Radio R'
        }
    }

    # Element parameters
    R = 10.0                 # Radius of curvature
    alpha_deg = 60.0         # Total subtended angle of the element
    alpha_rad = math.radians(alpha_deg)
    center = [0, 0, 0]
    
    # 1. Draw the curved beam
    plane = rs.WorldXYPlane()
    arc = rs.AddArc(plane, R, alpha_deg)
    # Add a pipe to give the beam visual thickness
    beam_pipe = rs.AddPipe(arc, 0, 0.4)
    if beam_pipe: rs.ObjectColor(beam_pipe, [120, 120, 120])
    
    # 2. Define and label nodes
    # Node j is the origin of phi (phi = 0)
    node_j = [R, 0, 0]
    # Node i is at phi = alpha
    node_i = [R * math.cos(alpha_rad), R * math.sin(alpha_rad), 0]
    
    rs.AddPoint(node_i)
    rs.AddPoint(node_j)
    rs.AddTextDot(texts[LANG]['node_i'], node_i)
    rs.AddTextDot(texts[LANG]['node_j'], [node_j[0], node_j[1] - 1, 0])
    
    # 3. Draw Force Vectors at Node j
    # Fx_j vector (Horizontal)
    fx_end = [R + 3, 0, 0]
    fx_arrow = rs.AddCurve([node_j, fx_end])
    rs.CurveArrows(fx_arrow, 2)
    rs.ObjectColor(fx_arrow, [255, 0, 0])  # Red for X
    rs.AddTextDot(texts[LANG]['fx'], fx_end)
    
    # Fy_j vector (Vertical)
    fy_end = [R, 3, 0]
    fy_arrow = rs.AddCurve([node_j, fy_end])
    rs.CurveArrows(fy_arrow, 2)
    rs.ObjectColor(fy_arrow, [0, 255, 0])  # Green for Y
    rs.AddTextDot(texts[LANG]['fy'], fy_end)
    
    # M_j moment (Curved Arrow)
    m_plane = rs.MovePlane(plane, node_j)
    m_arc = rs.AddArc(m_plane, 1.5, 270)
    rs.CurveArrows(m_arc, 2)
    rs.ObjectColor(m_arc, [0, 0, 255])     # Blue for Moment
    rs.AddTextDot(texts[LANG]['mj'], [R + 1.5, -1.5, 0])
    
    # 4. Draw Geometry Markings (Radius and Phi)
    phi_deg = 25.0  # Arbitrary intermediate angle to show phi
    phi_rad = math.radians(phi_deg)
    phi_pt = [R * math.cos(phi_rad), R * math.sin(phi_rad), 0]
    
    # Reference lines to center
    base_line = rs.AddLine(center, node_j)
    rs.ObjectColor(base_line, [150, 150, 150])
    
    rad_line = rs.AddLine(center, phi_pt)
    rs.ObjectColor(rad_line, [150, 150, 150])
    rs.AddTextDot(texts[LANG]['radius'], [R/2 * math.cos(phi_rad), R/2 * math.sin(phi_rad), 0])
    
    # Phi angle sweep
    phi_arc = rs.AddArc(plane, R * 0.3, phi_deg)
    rs.ObjectColor(phi_arc, [255, 150, 0]) # Orange for angle
    phi_text_pt = [R * 0.4 * math.cos(phi_rad/2), R * 0.4 * math.sin(phi_rad/2), 0]
    rs.AddTextDot(texts[LANG]['phi'], phi_text_pt)

    # Zoom to fit the generated geometry
    rs.ZoomExtents()

#%%
if __name__ == '__main__':
    visualize_curved_beam_element()