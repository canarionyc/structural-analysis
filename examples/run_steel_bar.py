# %% IMPORTS
from core_modules import SteelBar

from cross_sections.chs import CircularHollowSection

# %% EXAMPLE OF USAGE
# Define a cantilever beam (Empotrado-Libre)
material = SteelMaterial("S275")
seccion_tubo = CircularHollowSection(d=100, t=5)

# Specifying the attachment system: Fixed at start, Free at end
viga_en_voladizo = SteelBar(
    material,
    seccion_tubo,
    length=2000,
    start_support=SupportType.FIXED,
    end_support=SupportType.FREE
)

l_cr = viga_en_voladizo.get_effective_length()
print(f"Longitud real: {viga_en_voladizo.L} mm")
print(f"Longitud de pandeo (L_cr): {l_cr} mm (beta={l_cr / viga_en_voladizo.L})")