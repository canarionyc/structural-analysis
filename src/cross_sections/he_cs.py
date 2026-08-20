import math
from cross_sections.base_classes import CrossSection

class HEProfile(CrossSection):
    """
    Base class for Wide-Flange H-Sections (HEA, HEB, HEM).
    Logic based on Eurocode 3 (EN 1993-1-1) Table 6.2 for S235-S355 rolled steel.
    """

    def __init__(self, h, b, tw, tf):
        super().__init__()
        self.h = h
        self.b = b
        self.tw = tw
        self.tf = tf

        self._assign_buckling_curves()
        self._calculate_properties()

    def _assign_buckling_curves(self):
        """
        Assigns buckling curves based on EN 1993-1-1 Table 6.2 for rolled I-sections.
        HE beams often have h/b <= 1.2 up to size 300, and h/b > 1.2 for larger sizes.
        """
        if (self.h / self.b) > 1.2:
            if self.tf <= 40.0:
                self.buckling_curves = {'y': 'a', 'z': 'b'}
            else:
                self.buckling_curves = {'y': 'b', 'z': 'c'}
        else:
            if self.tf <= 100.0:
                self.buckling_curves = {'y': 'b', 'z': 'c'}
            else:
                self.buckling_curves = {'y': 'd', 'z': 'd'}

    def _calculate_properties(self):
        """
        Compute area and bending inertias for a symmetric I-section.
        Note: This ignores the root radius (r) for simplified geometric calculations,
        matching the provided IPE example.
        """
        web_height = self.h - 2 * self.tf
        flange_area = self.b * self.tf
        web_area = web_height * self.tw

        # Total Cross-sectional Area
        self.area = 2 * flange_area + web_area
        self.A = self.area

        # Strong axis y-y: centroidal inertia of the two flanges + web
        flange_centroid_offset = self.h / 2.0 - self.tf / 2.0
        
        flange_Iy = 2 * (
            (self.b * self.tf**3) / 12.0 + 
            (flange_area * flange_centroid_offset**2)
        )
        web_Iy = (self.tw * web_height**3) / 12.0
        
        self.Iy = flange_Iy + web_Iy

        # Weak axis z-z: inertia of the two flanges + web
        flange_Iz = 2 * ((self.tf * self.b**3) / 12.0)
        web_Iz = (web_height * self.tw**3) / 12.0
        
        self.Iz = flange_Iz + web_Iz

    # --- 2. Load JSON and Export to CSV ---
    def generate_catalog():
        json_filepath = 'HEB - DIN EN 10034.json'
        csv_filepath = 'heb_catalog.csv'

        # Load the SOFiSTiK cross-section JSON
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract the ParameterMap containing the geometrical inputs
        parameter_map = data.get("ParameterMap", {})

        # Define the columns we want in our output CSV
        headers = [
            'Profile', 'h_mm', 'b_mm', 'tw_mm', 'tf_mm', 'r_mm',
            'Area_mm2', 'Iy_mm4', 'Iz_mm4', 'Buckling_Curve_Y', 'Buckling_Curve_Z'
        ]

        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            # Iterate over all sizes (e.g., '100', '120', '200')
            for size, params in parameter_map.items():
                h = params.get('h')
                b = params.get('b')
                tw = params.get('tw')
                tf = params.get('tf')
                r = params.get('r', 0)  # Fallback to 0 if root radius is missing

                # Calculate the structural properties using the class
                profile = HEBProfile(h=h, b=b, tw=tw, tf=tf)

                # Write the flattened dictionary to the CSV
                writer.writerow({
                    'Profile': f"HEB {size}",
                    'h_mm': profile.h,
                    'b_mm': profile.b,
                    'tw_mm': profile.tw,
                    'tf_mm': profile.tf,
                    'r_mm': r,
                    'Area_mm2': round(profile.area, 2),
                    'Iy_mm4': round(profile.Iy, 2),
                    'Iz_mm4': round(profile.Iz, 2),
                    'Buckling_Curve_Y': profile.buckling_curves['y'],
                    'Buckling_Curve_Z': profile.buckling_curves['z']
                })

        print(f"Success! {len(parameter_map)} profiles written to {csv_filepath}")


class HEAProfile(HEProfile):
    """
    Class specifically for HEA (Light) profiles. 
    Inherits all geometric and buckling logic from HEProfile.
    """
    def __init__(self, h, b, tw, tf):
        super().__init__(h, b, tw, tf)
        self.profile_type = "HEA"


class HEBProfile(HEProfile):
    """
    Class specifically for HEB (Standard) profiles. 
    Inherits all geometric and buckling logic from HEProfile.
    """
    def __init__(self, h, b, tw, tf):
        super().__init__(h, b, tw, tf)
        self.profile_type = "HEB"