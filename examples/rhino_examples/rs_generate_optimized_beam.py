#%% IMPORT LIBRARIES
import rhinoscriptsyntax as rs

#%% DEFINE GEOMETRY GENERATOR
def generate_optimized_beam(b: float, h: float, L: float) -> str:
    """
    Generates a simply supported 3D beam solid in Rhino 
    based on optimized structural dimensions.
    """
    # Define the four corners of the cross-section centered on the YZ plane
    p0: list[float] = [0.0, -b / 2.0, -h / 2.0]
    p1: list[float] = [0.0, b / 2.0, -h / 2.0]
    p2: list[float] = [0.0, b / 2.0, h / 2.0]
    p3: list[float] = [0.0, -b / 2.0, h / 2.0]
    
    # Create the rectangular profile curve
    corners: list[list[float]] = [p0, p1, p2, p3, p0]
    profile: str = rs.AddPolyline(corners)
    
    # Define extrusion path along the X axis for the length of the span
    path_start: list[float] = [0.0, 0.0, 0.0]
    path_end: list[float] = [L, 0.0, 0.0]
    path_curve: str = rs.AddLine(path_start, path_end)
    
    # Extrude the profile along the path
    beam_surface: str = rs.ExtrudeCurve(profile, path_curve)
    
    # Cap the open ends to create a valid closed polysurface (solid)
    # rs.CapPlanarHoles modifies the object in place and returns a boolean
    is_capped: bool = rs.CapPlanarHoles(beam_surface)
    
    if not is_capped:
        print("Warning: Failed to cap the beam surface.")
    
    # Cleanup construction curves ONLY
    rs.DeleteObject(profile)
    rs.DeleteObject(path_curve)
    
    # The original beam_surface ID now points to the finished solid
    return beam_surface

#%% DEMONSTRATION
if __name__ == "__main__":
    # Optimal parameters passed from our scipy.optimize result
    # (Using arbitrary values here for the physical demonstration)
    b_opt: float = 0.145
    h_opt: float = 0.290
    L_span: float = 5.0
    
    # Clear the active document for a clean slate
    rs.DeleteObjects(rs.AllObjects())
    
    # Generate the physical beam geometry
    beam_id: str = generate_optimized_beam(b_opt, h_opt, L_span)
    
    # Adjust viewport to fit the new geometry
    rs.ZoomExtents()
    
    print(f"Generated optimized structural beam with ID: {beam_id}")