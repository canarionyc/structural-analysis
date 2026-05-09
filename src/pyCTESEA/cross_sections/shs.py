# %% SQUARE HOLLOW SECTION
import math
from ..cross_sections.base_classes import CrossSection

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
        
        # Radius of gyration
        radius_gyration = math.sqrt(inertia / self.area)
        self.radius_gyration_y = radius_gyration
        self.radius_gyration_z = radius_gyration

# %% BASIC DEMONSTRATION
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Path hack for direct execution
    src_path = str(Path(__file__).resolve().parents[2])
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    from ..core_modules.materials import SteelMaterial
    from ..core_modules.steel_bar import SteelBar
    from ..core_modules.checks import DBSEACheck

    # Recreating the exact problem conditions
    material = SteelMaterial(grade="S275")
    shs_150x6 = SquareHollowSection(B=150, t=6, process="hot")
    
    # Using the classmethod for a fixed-fixed column (beta=0.5)
    # L = 6900 mm
    pilar = SteelBar.create_cantilever(material, shs_150x6, length=6900) 
    pilar.beta = 0.5 # Manually overriding just for this quick test
    
    Nd_calculo = 490000 * 1.4 # N

    result = DBSEACheck.check_buckling(pilar, Nd_calculo)
    
    print(f"--- Comprobación de SHS {shs_150x6.B}x{shs_150x6.t} ---")
    print(f"Área: {shs_150x6.area / 100:.2f} cm2")
    print(f"Capacidad (Nb_Rd): {result.capacity_N / 1000:.2f} kN")
    print(f"Carga de Diseño (Nd): {Nd_calculo / 1000:.2f} kN")
    print(f"Ratio de Aprovechamiento: {result.ratio:.2f}")
    
    if result.ratio <= 1.0:
        print("ESTADO: CUMPLE (La pieza resiste el pandeo)")
    else:
        print("ESTADO: FALLA")