# %% IMPORTS
import math
from cross_sections.base_classes import CrossSection

# %% UPDATED HOLLOW SECTION WITH BUCKLING CURVE
class CircularHollowSection(CrossSection):
    def __init__(self, d: float, t: float, process="hot"):
        """
        :param process: "hot" for hot-finished (Curve a) or "cold" for cold-formed (Curve c)
        """
        super().__init__()
        self.d = d
        self.t = t
        self.inner_d = d - 2 * t
        # According to DB SE-A Table 6.2:
        curve = 'a' if process == "hot" else 'c'
        # Symmetric sections have the same curve for all axes
        self.buckling_curves = {'y': curve, 'z': curve}
        self._calculate_properties()

    def _calculate_properties(self):
        self.area = (math.pi / 4) * (self.d ** 2 - self.inner_d ** 2)
        self.I = (math.pi / 64) * (self.d ** 4 - self.inner_d ** 4)
        self.Iy = self.Iz = self.I
        self.radius_gyration_y = math.sqrt(self.I / self.area)  # Radius of gyration

# %% END-TO-END BUCKLING EXAMPLE
if __name__ == "__main__":
    import math

    # Toggle for bilingual output (Labels/Annotations)
    # Set to 'EN' for English, 'ES' for Spanish
    LANG = 'ES'

    UI_TEXT = {
        'EN': {
            'res_title': 'Structural Check Result',
            'f_y': 'Yield Strength',
            'utilization': 'Utilization Ratio',
            'status_pass': 'PASS',
            'status_fail': 'FAIL'
        },
        'ES': {
            'res_title': 'Resultado de la Comprobación Estructural',
            'f_y': 'Límite Elástico',
            'utilization': 'Ratio de Aprovechamiento',
            'status_pass': 'CUMPLE',
            'status_fail': 'NO CUMPLE'
        }
    }
    LANG = "EN"
    from ..cross_sections.chs import CircularHollowSection
    from core_modules import SteelMaterial
    from core_modules import SupportType
    from core_modules.steel_bar import SteelBar

    # 1. Define Material and Section (Cold-formed CHS)
    steel = SteelMaterial("S275")
    chs_section = CircularHollowSection(d=114.3, t=5.0, process="cold")

    # 2. Define Bar (Column 3m long, Pinned-Pinned)
    columna = SteelBar(
        material=steel,
        section=chs_section,
        length=3000,
        start_support=SupportType.PINNED,
        end_support=SupportType.PINNED
    )

    # 3. Apply Load (Nd = 150 kN compression)
    load_Nd = 150000
    result = DBSEACheck.check_buckling(columna, load_Nd)

    # %% BILINGUAL PLOT DATA STRUCTURE (as per your preference)
    plot_data = {
        "EN": {
            "title": "Buckling Analysis",
            "labels": {"x": "Slenderness", "y": "Reduction Factor (Chi)"},
            "annotations": f"Utilization: {result['ratio']:.2%}"
        },
        "ES": {
            "title": "Análisis de Pandeo",
            "labels": {"x": "Esbeltez", "y": "Factor de Reducción (Chi)"},
            "annotations": f"Aprovechamiento: {result['ratio']:.2%}"
        }
    }

    # Output result
    print(f"--- {UI_TEXT[LANG]['res_title']} ---")
    print(f"Chi (χ): {result['chi']:.3f}")
    print(f"Ratio: {result['ratio']:.2f}")