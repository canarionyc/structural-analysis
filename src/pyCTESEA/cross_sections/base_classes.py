# %% BASE CLASSES
from abc import ABC, abstractmethod

class CrossSection(ABC):
    """
    Clase base abstracta para todas las secciones transversales.
    Define el contrato obligatorio para que el DBSEACheck pueda operar.
    """
    def __init__(self):
        # Atributos base que toda sección DEBE tener
        self.buckling_curves = {'y': 'c', 'z': 'c'}

        self.radius_gyration_y = 0.0
        self.radius_gyration_z = 0.0


        self.area = 0.0  # Area (mm2)
        self.Iy = 0.0  # Inertia Y (mm4)
        self.Iz = 0.0  # Inertia Z (mm4)
        self.Wel_y = 0.0  # Elastic Modulus Y (mm3)
        self.Wpl_y = 0.0  # Plastic Modulus Y (mm3)
        self.section_class = 1  # Default class [cite: 102]
        # Now we store curves for both axes


    @abstractmethod
    def _calculate_properties(self):
        """
        Método abstracto. Obliga a cualquier clase hija (CHS, IPE, etc.) 
        a definir su propia lógica matemática para calcular el área y radios de giro.
        Si una clase hija no implementa este método, Python lanzará un error al instanciarla.
        """
        pass