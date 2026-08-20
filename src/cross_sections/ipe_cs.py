import math

from cross_sections.base_classes import CrossSection


class IPEProfile(CrossSection):
    """
    Example for I-sections where curves differ by axis.
    Logic based on DB SE-A Table 6.2 for S235-S355.
    """

    def __init__(self, h, b, tw, tf):
        super().__init__()
        self.h = h
        self.b = b
        self.tw = tw
        self.tf = tf

        # Simplified logic for IPE (usually h/b > 1.2 and tf < 40mm)
        if (h / b) > 1.2:
            self.buckling_curves = {'y': 'a', 'z': 'b'}
        else:
            self.buckling_curves = {'y': 'b', 'z': 'c'}

        self._calculate_properties()

    def _calculate_properties(self):
        """Compute area and bending inertias for a symmetric I-section."""
        web_height = self.h - 2 * self.tf
        flange_area = self.b * self.tf
        web_area = web_height * self.tw

        self.area = 2 * flange_area + web_area
        self.A = self.area

        # Strong axis y-y: centroidal inertia of the two flanges + web
        flange_centroid_offset = self.h / 2.0 - self.tf / 2.0
        self.Iy = 2 * (
            self.b * self.tf**3 / 12.0 + self.b * self.tf * flange_centroid_offset**2
        ) + self.tw * web_height**3 / 12.0

        # Weak axis z-z: through the web center, parallel to flanges
        self.Iz = 2 * (self.tf * self.b**3 / 12.0) + self.tw**3 * web_height / 12.0

        self.iy = math.sqrt(self.Iy / self.area)
        self.iz = math.sqrt(self.Iz / self.area)
        self.radius_gyration_y = self.iy
        self.radius_gyration_z = self.iz

    def __str__(self):
        return f"IPEProfile(h={self.h}, b={self.b}, tw={self.tw}, tf={self.tf})"