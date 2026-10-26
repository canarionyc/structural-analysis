# Dimensionar un  soporte  sabiendo que  soportará un axil de 490  KN. Se  considera un soporte
# biempotrado con una longitud de 6.90m. El perfil elegido es un tubo de chapa simple, laminado
# en caliente S‐275‐JR gamma_c=1.4 y gamma_s=1.05.

from core_modules import SteelBar
from core_modules.materials import SteelMaterial
from core_modules.supports import SupportType
from cross_sections.chs import CircularHollowSection
from core_modules.checks import DBSEACheck

# %% TEST: DIMENSIONAMIENTO DE SOPORTE BIEMPOTRADO
# Definición de la carga y factores
gamma_c = 1.4
load_k = 490000  # N
Nd = load_k * gamma_c

# Configuración del material y perfil
material = SteelMaterial(grade="S275")

# Probamos el perfil óptimo encontrado
perfil_optimo = CircularHollowSection(d=193.7, t=6, process="hot")

# Definición de la barra con beta=0.5 (biempotrado)
soporte = SteelBar(
    material,
    perfil_optimo,
    length=6900,
    start_support=SupportType.FIXED,
    end_support=SupportType.FIXED,
    gamma_M1=1.05
)

# Ejecución de la comprobación
result = DBSEACheck.check_buckling(soporte, Nd)

print(f"Resultado para {perfil_optimo.d}x{perfil_optimo.t}:")
print(f" - Esbeltez reducida: {result.chi:.3f} (Chi) eje {result.axis}")
print(f" - Capacidad: {result.capacity_N/1000:.2f} kN")
print(f" - Aprovechamiento: {result.ratio:.2%}")