# %% STEEL BAR CON ARQUITECTURA ROBUSTA

from .supports import SupportType

class SteelBar:
    """Represents a physical bar member."""

    # El constructor principal SOLO pide el dato matemático puro (beta)
    def __init__(self, material, section, length: float, beta: float = 1.0, gamma_M1: float = 1.05):
        self.material = material
        self.section = section
        self.length = length
        self.beta = beta
        self.gamma_M1 = gamma_M1

    # Constructor alternativo 1: Por condiciones de contorno (Amigable)
    @classmethod
    def from_supports(cls, material, section, length, start: SupportType, end: SupportType, gamma_M1=1.05):
        """Crea una barra calculando beta automáticamente desde los apoyos."""
        beta = cls._calculate_beta(start, end)
        # Llama al constructor principal
        return cls(material, section, length, beta, gamma_M1)

    # Constructor alternativo 2: Para un voladizo directo (Súper rápido)
    @classmethod
    def create_cantilever(cls, material, section, length, gamma_M1=1.05):
        """Crea una viga en voladizo (beta = 2.0)."""
        return cls(material, section, length, beta=2.0, gamma_M1=gamma_M1)

    @staticmethod
    def _calculate_beta(start: SupportType, end: SupportType) -> float:
        """Lógica interna para deducir beta. Fácil de expandir."""
        supports = {start, end}
        if SupportType.FIXED in supports and SupportType.PINNED in supports:
            return 0.7
        elif start == SupportType.FIXED and end == SupportType.FIXED:
            return 0.5
        elif start == SupportType.PINNED and end == SupportType.PINNED:
            return 1.0
        elif SupportType.FREE in supports and SupportType.FIXED in supports:
            return 2.0
        return 1.0

    def get_effective_length(self, axis='y'):
        return self.length * self.beta

if __name__ == "__main__":
    # %% IMPORTS
    from ..core_modules.steel_bar import SteelBar
    from ..core_modules.materials import SteelMaterial
    from cross_sections.chs import CircularHollowSection

    # %% EXAMPLE OF USAGE
    # Define a cantilever beam (Empotrado-Libre)
    material = SteelMaterial("S275")
    seccion_tubo = CircularHollowSection(d=100, t=5)

    # Specifying the attachment system: Fixed at start, Free at end
    viga_en_voladizo = SteelBar.from_supports(
        material,
        seccion_tubo,
        length=2000,
        start=SupportType.FIXED,
        end=SupportType.FREE
    )

    l_cr = viga_en_voladizo.get_effective_length()
    print(f"Longitud real: {viga_en_voladizo.length} mm")
    print(f"Longitud de pandeo (L_cr): {l_cr} mm (beta={l_cr / viga_en_voladizo.length})")