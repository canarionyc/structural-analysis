# %% RESULT DATACLASS WITH VALIDATION
from dataclasses import dataclass

@dataclass
class BucklingResult:
    """
    Data structure to store the results of a buckling check.
    Includes built-in validation to ensure physical and structural consistency.
    """
    ratio: float
    capacity_N: float
    chi: float
    axis: str

    def __post_init__(self):
        # 1. Validate utilization ratio
        # Must be non-negative. Values > 1.0 mean the structural check fails.
        if self.ratio < 0:
            raise ValueError(f"El ratio de aprovechamiento no puede ser negativo. Valor recibido: {self.ratio}")

        # 2. Validate structural capacity
        # Capacity must be strictly positive to avoid division by zero later.
        if self.capacity_N <= 0:
            raise ValueError(f"La capacidad resistente (Nb_Rd) debe ser > 0. Valor recibido: {self.capacity_N}")

        # 3. Validate reduction factor (Chi)
        # Chi is a reduction coefficient bounded between >0 (infinite slenderness) and 1.0 (no reduction).
        if not (0 < self.chi <= 1.0):
            raise ValueError(f"El factor de pandeo (chi) debe estar en el intervalo (0, 1.0]. Valor recibido: {self.chi}")

        # 4. Validate axis selection
        if self.axis not in ('y', 'z'):
            raise ValueError(f"El eje de pandeo debe ser 'y' o 'z'. Valor recibido: '{self.axis}'")

# %% USAGE EXAMPLE
if __name__ == "__main__":
    print("Ejemplo de uso del dataclass BucklingResult:")

    # Instanciación correcta (Pieza que cumple)
    resultado_valido = BucklingResult(ratio=0.85, capacity_N=500000, chi=0.89, axis='y')
    print(f"Resultado válido - Ratio: {resultado_valido.ratio}")

    # Instanciación correcta (Pieza que falla, ratio > 1)
    resultado_falla = BucklingResult(ratio=1.45, capacity_N=200000, chi=0.45, axis='z')
    print(f"Resultado falla por carga - Ratio: {resultado_falla.ratio}")

    # Instanciación incorrecta (Lanzará ValueError por eje inválido)
    try:
        resultado_error = BucklingResult(ratio=0.5, capacity_N=100000, chi=1.2, axis='x')
    except ValueError as e:
        print(f"Error capturado: {e}")