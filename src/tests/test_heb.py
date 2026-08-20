# %% BASIC DEMONSTRATION
import os
from pprint import pprint





# import sys
# from pathlib import Path
# import importlib

# Path hack for direct execution
# src_path = str(Path(__file__).resolve().parents[2])
# if src_path not in sys.path:
#     sys.path.insert(0, src_path)

# from core_modules.materials import SteelMaterial
# from core_modules.steel_bar import SteelBar
from core_modules.checks import DBSEACheck
# from core_modules.buckling_result import BucklingResult
from cross_sections import he_cs
from cross_sections.he_cs import HEBProfile
print(HEBProfile.__doc__)
#%% new section
mynewsection = HEBProfile(h=200, b=100, tw=5, tf=8)
print(mynewsection)

vars(mynewsection)

#%% IPE 500 example
# Create an IPE 500 profile
steel_profiles_dir=r"C:\Program Files\SOFiSTiK\2026\SOFiSTiK Rhino Interface 2026\Contents\grasshopper\content\steel profiles"
pprint(os.listdir(steel_profiles_dir))

profile_type = "HEB"
profile_Id = "260"

heb_path = os.path.join(steel_profiles_dir, f"{profile_type} - DIN EN 10034.json")
print(heb_path)
assert os.path.exists(heb_path)

#%% Find HEB 260

import json
f=open(heb_path, 'r')

Id = "260"
cadinp_output = "Error loading profile."
with open(heb_path, 'r') as f:
    data = json.load(f)
    pprint(data)
    print(data.keys())
    # Navigate the JSON tree to reach ParameterMap -> 500
    if "ParameterMap" in data and Id in data["ParameterMap"]:
        print(data["ParameterMap"].keys())
        print(f"HEB {Id} found!")
        param_dict = data["ParameterMap"][Id]
        pprint(param_dict)
        # Extract the specific geometric parameters
        from operator import itemgetter

        h, b, tw, tf, r = itemgetter("h", "b", "tw", "tf", "r")(param_dict)
        print(h,b,tw,tf,r)

        # Format the output for the 00_materials.dat file
        cadinp_output = (
            f"$ Extracted from JSON: heb {Id}\n"
            f"SECT 1 TYPE I TITL 'heb {Id}'\n"
            f"PROF 1 b={b} h={h} tw={tw} tf={tf} r={r}"
        )
        if profile_type == "HEB":
            profile_instance = HEBProfile(h, b, tw, tf)
        print(profile_instance)
        pprint(vars(profile_instance))
    else:
        cadinp_output = f"Size {Id} not found in ParameterMap."