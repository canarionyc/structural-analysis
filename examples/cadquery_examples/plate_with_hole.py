%reset -f
#%%
import os
from dotenv import load_dotenv
# print(f"PYTHONPATH={os.environ['PYTHONPATH']}")
load_dotenv(verbose=True)
print(f"OUTPUT_DIR={os.environ['OUTPUT_DIR']}")
import sys

#%% Add to path and import common functionality from autoimport.py
# This allows using predefined variables or functions if needed
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
# from autoimport import import_all
# import_all()

#%% Plate dimensions (example values, these could be linked to calculation results)
plate_length = L.value if 'L' in locals() else 500 # Use L from autoimport if available, else default
plate_width = 120
plate_thickness = 14
hole_diameter = d_bolt.value if 'd_bolt' in locals() else 22 # Use d_bolt from autoimport if available, else default
#%%
import cadquery as cq

# Create the plate with a single hole in the center
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness).faces(">Z").workplane().hole(hole_diameter)

#%% Define output directory and ensure it exists
# output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CAD_output")
output_dir = os.environ['OUTPUT_DIR']
os.makedirs(output_dir, exist_ok=True)

#%% Export the CAD model to STEP and STL formats
cq.exporters.export(plate, os.path.join(output_dir, "plate_with_hole.step"))
cq.exporters.export(plate, os.path.join(output_dir, "plate_with_hole.stl"))