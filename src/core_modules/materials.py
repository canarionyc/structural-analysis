# %% MATERIAL CLASS
class SteelMaterial:
    """Represents structural steel properties according to DB SE-A Section 4."""

    def __init__(self, grade="S235", thickness=16):
        self.grade = grade
        self.thickness = thickness
        # Common properties
        self.E = 210000  # N/mm2
        self.G = 81000  # N/mm2
        self.nu = 0.3
        self.rho = 7850  # kg/m3
        self.alpha = 1.2e-5

        self._set_mechanical_properties()

    def _set_mechanical_properties(self):
        """Sets fy and fu based on grade and thickness."""
        # Simplified lookup for common grades
        data = {
            "S235": {"fy": 235, "fu": 360},
            "S275": {"fy": 275, "fu": 410},
            "S355": {"fy": 355, "fu": 470}
        }
        props = data.get(self.grade, data["S235"])
        # DB SE-A reduces fy for thickness > 16mm
        if self.thickness > 16:
            self.fy = props["fy"] - 10
        else:
            self.fy = props["fy"]
        self.fu = props["fu"]