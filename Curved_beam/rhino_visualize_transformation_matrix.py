# coding: utf8
#%%
import rhinoscriptsyntax as rs
import math

# Toggle switch for language ('EN' or 'ES')
LANG = 'EN'

#%%
def visualize_transformation_matrix():
    # Bilingual dictionary for annotations
    texts = {
        'EN': {
            'node_i': 'Node i (Reactions)',
            'node_j': 'Node j (Applied Forces)',
            'arm_x': 'Lever Arm \u0394x = R(1-cos\u03B1)',
            'arm_y': 'Lever Arm \u0394y = R sin\u03B1',
            'fxi': 'F_xi = -F_xj',
            'fyi': 'F_yi = -F_yj',
            'mi': 'M_i (Reaction Moment)'
        },
        'ES': {
            'node_i': 'Nodo i (Reacciones)',
            'node_j': 'Nodo j (Fuerzas Aplicadas)',
            'arm_x': 'Brazo \u0394x = R(1-cos\u03B1)',
            'arm_y': 'Brazo \u0394y = R sin\u03B1',
            'fxi': 'F_xi = -F_xj',
            'fyi': 'F_yi = -F_yj',
            'mi': 'M_i (Momento de Reacción)'
        }
    }

    # Element parameters
    R = 10.0
    alpha_deg = 60.0
    alpha_rad = math.radians(alpha_deg)
    plane = rs.WorldXYPlane()
    
    # Define Nodes
    node_j = [R, 0, 0]
    node_i = [R * math.cos(alpha_rad), R * math.sin(alpha_rad), 0]
    
    # 1. Draw the curved beam
    arc = rs.AddArc(plane, R, alpha_deg)
    beam_pipe = rs.AddPipe(arc, 0, 0.3)
    if beam_pipe: rs.ObjectColor(beam_pipe, [120, 120, 120])
    
    rs.AddPoint(node_i)
    rs.AddPoint(node_j)
    rs.AddTextDot(texts[LANG]['node_j'], [node_j[0] + 1, node_j[1] - 1, 0])
    rs.AddTextDot(texts[LANG]['node_i'], [node_i[0] - 1, node_i[1] + 1, 0])

    # 2. Draw the Lever Arms (Mapping the [T] matrix)
    # Find the corner to form the right triangle between i and j
    corner_pt = [R, R * math.sin(alpha_rad), 0]
    
    # Horizontal lever arm (Delta X) for the vertical force F_yj
    arm_x_line = rs.AddLine(node_i, corner_pt)
    rs.ObjectColor(arm_x_line, [255, 150, 0])  # Orange
    rs.CurveDashPattern(arm_x_line, [0.5, 0.5])
    rs.AddTextDot(texts[LANG]['arm_x'], [(node_i[0] + corner_pt[0])/2, corner_pt[1], 0])
    
    # Vertical lever arm (Delta Y) for the horizontal force F_xj
    arm_y_line = rs.AddLine(corner_pt, node_j)
    rs.ObjectColor(arm_y_line, [255, 150, 0])  # Orange
    rs.CurveDashPattern(arm_y_line, [0.5, 0.5])
    rs.AddTextDot(texts[LANG]['arm_y'], [corner_pt[0], (corner_pt[1] + node_j[1])/2, 0])

    # 3. Draw Reaction Force Vectors at Node i
    # F_xi is opposite to F_xj (points left)
    fxi_end = [node_i[0] - 3, node_i[1], 0]
    fxi_arrow = rs.AddCurve([node_i, fxi_end])
    rs.CurveArrows(fxi_arrow, 2)
    rs.ObjectColor(fxi_arrow, [255, 0, 0])
    rs.AddTextDot(texts[LANG]['fxi'], fxi_end)
    
    # F_yi is opposite to F_yj (points down)
    fyi_end = [node_i[0], node_i[1] - 3, 0]
    fyi_arrow = rs.AddCurve([node_i, fyi_end])
    rs.CurveArrows(fyi_arrow, 2)
    rs.ObjectColor(fyi_arrow, [0, 255, 0])
    rs.AddTextDot(texts[LANG]['fyi'], fyi_end)

    # M_i Reaction Moment (Curved Arrow)
    mi_plane = rs.MovePlane(plane, node_i)
    mi_arc = rs.AddArc(mi_plane, 2.0, 90)
    rs.CurveArrows(mi_arc, 1)  # Arrow at start to indicate resisting direction
    rs.ObjectColor(mi_arc, [0, 0, 255])
    rs.AddTextDot(texts[LANG]['mi'], [node_i[0] - 2, node_i[1] + 2, 0])

    # Zoom to fit
    rs.ZoomExtents()

#%%
if __name__ == '__main__':
    visualize_transformation_matrix()