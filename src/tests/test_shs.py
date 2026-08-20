# %% BASIC DEMONSTRATION
from cross_sections import shs


# import sys
# from pathlib import Path
# import importlib

# Path hack for direct execution
# src_path = str(Path(__file__).resolve().parents[2])
# if src_path not in sys.path:
#     sys.path.insert(0, src_path)

from core_modules.materials import SteelMaterial
from core_modules.steel_bar import SteelBar
from core_modules.checks import DBSEACheck
from core_modules.buckling_result import BucklingResult
from cross_sections import shs
from cross_sections.shs import SquareHollowSection


# %% Recreating the exact problem conditions
material = SteelMaterial(grade="S275")
print(material)

# importlib.reload(shs)
dir(shs)
help(shs.SquareHollowSection)
shs_150x6 = SquareHollowSection(B=150, t=6, process="hot")
print(shs_150x6)

# Using the classmethod for a fixed-fixed column (beta=0.5)
L = 6900 # mm
pilar = SteelBar.create_cantilever(material, shs_150x6, length=L)
pilar.beta = 0.5  # Manually overriding just for this quick test
print(pilar)
help(pilar)

Nd_calculo = 490000 * 1.4  # N

# %% Check Buckling
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