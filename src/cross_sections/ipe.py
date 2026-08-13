from ..cross_sections.base_classes import CrossSection

class IPEProfile(CrossSection):
    """
    Example for I-sections where curves differ by axis.
    Logic based on DB SE-A Table 6.2 for S235-S355.
    """
    def __init__(self, h, b, tw, tf):
        super().__init__()
        self.h = h
        self.b = b
        # Simplified logic for IPE (usually h/b > 1.2 and tf < 40mm)
        if (h / b) > 1.2:
            self.buckling_curves = {'y': 'a', 'z': 'b'}
        else:
            self.buckling_curves = {'y': 'b', 'z': 'c'}
        # ... calculation of A, iy, iz ...