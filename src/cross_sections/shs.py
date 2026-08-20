# %% SQUARE HOLLOW SECTION
import math
from cross_sections.base_classes import CrossSection

class SquareHollowSection(CrossSection):
    """
    Represents a Square Hollow Section (SHS) / Perfil Tubular Cuadrado.
    """
    def __init__(self, B: float, t: float, process="hot"):
        """
        :param B: Outer width/height (mm)
        :param t: Wall thickness (mm)
        :param process: "hot" (Curve a) or "cold" (Curve c)
        """
        super().__init__()
        self.B = B
        self.t = t
        self.b_inner = B - 2 * t
        
        # Table 6.2 DB SE-A: Hollow sections use same curves regardless of shape
        curve = 'a' if process == "hot" else 'c'
        self.buckling_curves = {'y': curve, 'z': curve}
        
        self._calculate_properties()

    def _calculate_properties(self):
        # Area: Outer square minus inner square
        self.area = self.B**2 - self.b_inner**2
        
        # Moment of Inertia: (B^4 - b^4) / 12
        inertia = (self.B**4 - self.b_inner**4) / 12
        self.Iy = self.Iz = inertia
        
        # Radius of gyration
        radius_gyration = math.sqrt(inertia / self.area)
        self.radius_gyration_y = radius_gyration
        self.radius_gyration_z = radius_gyration

    def __str__(self) -> str:
        return f"SquareHollowSection(B={self.B}, t={self.t})"