#%% INITIALIZE RHINO INSIDE
# This must be run before importing any Rhino modules
import rhinoinside
rhinoinside.load()

# Now we can safely import the .NET and Rhino libraries
import System
import Rhino

#%% DEFINE HEADLESS GEOMETRY FUNCTION
def generate_headless_beam(b: float, h: float, L: float, filepath: str) -> bool:
    """
    Uses Rhino.Inside to generate a 3D structural beam headlessly
    and saves it directly to a .3dm file.
    """
    # Create a new headless Rhino document
    doc: Rhino.RhinoDoc = Rhino.RhinoDoc.CreateHeadless(None)
    
    # Define base rectangle profile on the YZ plane
    plane: Rhino.Geometry.Plane = Rhino.Geometry.Plane.WorldYZ
    interval_y: Rhino.Geometry.Interval = Rhino.Geometry.Interval(-b / 2.0, b / 2.0)
    interval_z: Rhino.Geometry.Interval = Rhino.Geometry.Interval(-h / 2.0, h / 2.0)
    
    rect: Rhino.Geometry.Rectangle3d = Rhino.Geometry.Rectangle3d(plane, interval_y, interval_z)
    profile_curve: Rhino.Geometry.Curve = rect.ToNurbsCurve()
    
    # Extrude the profile along the X axis (curve normal)
    # The third argument 'True' automatically caps the extrusion into a solid
    extrusion: Rhino.Geometry.Extrusion = Rhino.Geometry.Extrusion.Create(profile_curve, L, True)
    
    # Convert Extrusion object to a standardized Brep (Solid)
    solid_brep: Rhino.Geometry.Brep = extrusion.ToBrep(True)
    
    # Add the solid to the document's object table
    doc.Objects.AddBrep(solid_brep)
    
    # Define write options and save the file
    write_options: Rhino.FileIO.FileWriteOptions = Rhino.FileIO.FileWriteOptions()
    success: bool = doc.Write3dmFile(filepath, write_options)
    
    # Clean up memory to prevent memory leaks in automated pipelines
    doc.Dispose()
    
    return success

#%% DEMONSTRATION
if __name__ == "__main__":
    # Parameters derived from our previous optimization script
    b_opt: float = 0.145
    h_opt: float = 0.290
    L_span: float = 5.0
    
    # Define absolute path for the output file
    output_file: str = "C:\\dev\\structural-analysis\\examples\\optimized_beam.3dm"
    
    print("Initializing Rhino.Inside geometry generation...")
    result: bool = generate_headless_beam(b_opt, h_opt, L_span, output_file)
    
    if result:
        print(f"Successfully generated and saved closed Brep to: {output_file}")
    else:
        print("Error: Failed to save the .3dm file.")