#%% IMPORT LIBRARIES
import json
import os
from pprint import pprint

# h: Total depth (or height) of the cross-section.
#
# b: Total width of the flange.
#
# tw: Thickness of the web (the vertical middle section).
#
# tf: Thickness of the flange (the horizontal top and bottom sections).
#
# r: Root radius (the rounded corner between the web and the flange).

#%% CONFIGURATION
# Exact path to the SOFiSTiK JSON library you found

json_path = r"C:\Program Files\SOFiSTiK\2026\SOFiSTiK Rhino Interface 2026\Contents\grasshopper\content\steel profiles\IPE - DIN EN 10034.json"
profile_size = "500"
cadinp_output = "Error loading profile."

#%% EXECUTION
assert os.path.exists(json_path)

f=open(json_path, 'r')

with open(json_path, 'r') as f:
    data = json.load(f)
    pprint(data)
    # Navigate the JSON tree to reach ParameterMap -> 500
    if "ParameterMap" in data and profile_size in data["ParameterMap"]:
        ipe = data["ParameterMap"][profile_size]
        pprint(ipe)
        # Extract the specific geometric parameters
        from operator import itemgetter

        h, b, tw, tf = itemgetter("h", "b", "tw", "tf")(ipe)

        # Format the output for the 00_materials.dat file
        cadinp_output = (
            f"$ Extracted from JSON: IPE {profile_size}\n"
            f"SECT 1 TYPE I TITL 'IPE {profile_size}'\n"
            f"PROF 1 {b} {h} {tw} {tf}"
        )
    else:
        cadinp_output = f"Size {profile_size} not found in ParameterMap."

# Print the result to the component output
print(cadinp_output)