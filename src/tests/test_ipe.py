# %% BASIC DEMONSTRATION
import os
from cross_sections import shs


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
from cross_sections import ipe_cs
from cross_sections.ipe_cs import IPEProfile,CrossSection
help(IPEProfile)
#%% new section
mynewsection = IPEProfile(h=200, b=100, tw=5, tf=8)
print(mynewsection)

vars(mynewsection)

#%% IPE 500 example
# Create an IPE 500 profile
steel_profiles_dir=r"C:\Program Files\SOFiSTiK\2026\SOFiSTiK Rhino Interface 2026\Contents\grasshopper\content\steel profiles"
os.listdir(steel_profiles_dir)

ipe_path = os.path.join(steel_profiles_dir, "IPE - DIN EN 10034.json")
Id = "500"
cadinp_output = "Error loading profile."

#%% EXECUTION
import os
assert os.path.exists(ipe_path)
import json
from pprint import pprint

f=open(ipe_path, 'r')

with open(ipe_path, 'r') as f:
    data = json.load(f)
    pprint(data)
    print(data.keys())
    # Navigate the JSON tree to reach ParameterMap -> 500
    if "ParameterMap" in data and Id in data["ParameterMap"]:
        print(data["ParameterMap"].keys())
        print("IPE 500 found!")
        ipe_dict = data["ParameterMap"][Id]
        pprint(ipe_dict)
        # Extract the specific geometric parameters
        from operator import itemgetter

        h, b, tw, tf, r = itemgetter("h", "b", "tw", "tf", "r")(ipe_dict)
        print(h,b,tw,tf,r)

        # Format the output for the 00_materials.dat file
        cadinp_output = (
            f"$ Extracted from JSON: IPE {Id}\n"
            f"SECT 1 TYPE I TITL 'IPE {Id}'\n"
            f"PROF 1 b={b} h={h} tw={tw} tf={tf} r={r}"
        )

        ipe500 = IPEProfile(h, b, tw, tf)
        print(ipe500)
        print(vars(ipe500))
    else:
        cadinp_output = f"Size {Id} not found in ParameterMap."