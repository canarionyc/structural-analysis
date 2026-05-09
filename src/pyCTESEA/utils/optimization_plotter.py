# %% IMPORTS AND SETUP
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

root_dir = Path.cwd()
src_dir = root_dir / 'src'
print(root_dir)
print(src_dir)
sys.path.append(str(src_dir))
print(sys.path)
# %%
from ..core_modules.materials import SteelMaterial
from ..core_modules.steel_bar import SteelBar
from ..core_modules.checks import DBSEACheck
from ..cross_sections.chs import CircularHollowSection


# %% BILINGUAL PLOT CONFIGURATION
LANG = 'ES'  # Toggle between 'EN' and 'ES'

PLOT_METADATA = {
    "EN": {
        "title": "Buckling Optimization: Design Space Exploration",
        "x_label": "Cross-Sectional Area (cm²) [Proportional to Mass]",
        "y_label": "Utilization Ratio ($N_{Ed} / N_{b,Rd}$)",
        "legend_valid": "Valid Profiles (Ratio ≤ 1.0)",
        "legend_invalid": "Failing Profiles",
        "legend_optimal": "Optimal Choice",
        "annotation_optimal": "Minimum Mass Solution\n{name}",
        "zone_safe": "Safe Zone",
        "zone_fail": "Failure Zone"
    },
    "ES": {
        "title": "Optimización a Pandeo: Exploración del Espacio de Diseño",
        "x_label": "Área de la Sección Transversal (cm²) [Proporcional a la Masa]",
        "y_label": "Ratio de Aprovechamiento ($N_{Ed} / N_{b,Rd}$)",
        "legend_valid": "Perfiles Válidos (Ratio ≤ 1.0)",
        "legend_invalid": "Perfiles que Fallan",
        "legend_optimal": "Elección Óptima",
        "annotation_optimal": "Solución de Mínima Masa\n{name}",
        "zone_safe": "Zona Segura",
        "zone_fail": "Zona de Fallo"
    }
}

# %% SIZING ENGINE CLASS
class SizingEngine:
    """Evaluates a catalog of profiles to find the optimal buckling resistance."""
    
    def __init__(self, load_Nd: float, length: float, beta: float):
        self.load_Nd = load_Nd
        self.length = length
        self.beta = beta
        self.material = SteelMaterial(grade="S275") # Según requerimiento
        
        # Catálogo comercial típico (Diámetro, Espesor)
        self.catalog = [
            (114.3, 3.6), (114.3, 5.0), (139.7, 4.0), (139.7, 5.0),
            (139.7, 8.0), (139.7, 10.0), (159.0, 6.0), (159.0, 8.0),
            (168.3, 6.0), (168.3, 8.0), (193.7, 6.0), (193.7, 8.0),
            (219.1, 6.0), (219.1, 8.0), (244.5, 6.0), (244.5, 8.0)
        ]

    def evaluate_catalog(self) -> pd.DataFrame:
        results = []
        for d, t in self.catalog:
            # 1. Instanciar sección y barra
            seccion = CircularHollowSection(d=d, t=t, process="hot")
            barra = SteelBar(
                material=self.material,
                section=seccion,
                length=self.length,
                beta=self.beta,
                gamma_M1=1.05
            )
            
            # 2. Comprobación
            # Asumimos que check_buckling devuelve el dataclass BucklingResult
            res = DBSEACheck.check_buckling(barra, self.load_Nd, axis='y')
            
            # 3. Guardar resultados
            results.append({
                "Name": f"CHS {d}x{t}",
                "Area_cm2": seccion.area / 100, # asumiendo que tu clase lo da en mm2
                "Ratio": res.ratio,
                "Capacity_kN": res.capacity_N / 1000
            })
            
        return pd.DataFrame(results)

# %% VISUALIZATION ENGINE (WITH AUTO-REPEL)
import matplotlib.pyplot as plt
import pandas as pd
from adjustText import adjust_text


def plot_design_space(df: pd.DataFrame):
    """Generates the optimization plot using bilingual metadata and auto-repelling labels."""

    meta = PLOT_METADATA[LANG]

    # Clasificar datos
    valid = df[df['Ratio'] <= 1.0]
    invalid = df[df['Ratio'] > 1.0]
    optimal = valid.loc[valid['Area_cm2'].idxmin()]

    plt.figure(figsize=(10, 6))

    # Zonas de fondo
    plt.axhspan(0, 1.0, color='lightgreen', alpha=0.15, label=meta["zone_safe"])
    plt.axhspan(1.0, df['Ratio'].max() + 0.2, color='salmon', alpha=0.15, label=meta["zone_fail"])
    plt.axhline(1.0, color='red', linestyle='--', linewidth=1.5)

    # Nubes de puntos
    plt.scatter(valid['Area_cm2'], valid['Ratio'], color='forestgreen', s=60, label=meta["legend_valid"], zorder=3)
    plt.scatter(invalid['Area_cm2'], invalid['Ratio'], color='darkred', s=60, marker='x', label=meta["legend_invalid"],
        zorder=3)

    # Resaltar el óptimo (Lo mantenemos estático para darle prioridad de diseño)
    plt.scatter(optimal['Area_cm2'], optimal['Ratio'], color='gold', s=300, marker='*', edgecolors='black',
        label=meta["legend_optimal"], zorder=5)
    plt.annotate(
        meta["annotation_optimal"].format(name=optimal['Name']),
        (optimal['Area_cm2'], optimal['Ratio']),
        xytext=(15, 50), textcoords='offset points',
        fontweight='bold', color='darkgoldenrod',
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="darkgoldenrod", lw=1, alpha=0.8),
        zorder=10
    )

    # 1. Recopilar etiquetas para ajustar dinámicamente
    texts = []
    for i, row in df.iterrows():
        # Filtramos para no etiquetar todos los perfiles, solo los relevantes en la frontera
        if abs(row['Area_cm2'] - optimal['Area_cm2']) < 15 and row['Ratio'] < 1.5:
            # Añadimos el objeto de texto a la lista, no usamos offset fijo
            t = plt.text(row['Area_cm2'], row['Ratio'], row['Name'], fontsize=8, alpha=0.8)
            texts.append(t)

    # 2. Motor de repulsión (ggrepel equivalente)
    adjust_text(texts,
        arrowprops=dict(arrowstyle="-", color='gray', lw=0.5, alpha=0.6),
        expand_points=(1.2, 1.2),
        expand_text=(1.05, 1.05))

    # Estética
    plt.title(meta["title"], fontsize=14, pad=15)
    plt.xlabel(meta["x_label"], fontsize=12)
    plt.ylabel(meta["y_label"], fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc="upper right")
    plt.tight_layout()

    return(plt)

# %% MAIN EXECUTION BLOCK
if __name__ == "__main__":
    # Datos del problema (Soporte Biempotrado)
    load_design = 490000 * 1.4 # N
    length_bar = 6900 # mm
    beta_factor = 0.5 # Biempotrado
    
    # 1. Ejecutar motor de dimensionado
    print(f"--- Iniciando Sizing Engine (Idioma: {LANG}) ---")
    engine = SizingEngine(load_Nd=load_design, length=length_bar, beta=beta_factor)
    df_results = engine.evaluate_catalog()
    
    # 2. Imprimir comprobación en consola
    optimal_row = df_results[df_results['Ratio'] <= 1.0].sort_values(by='Area_cm2').iloc[0]
    print("\nResultado Óptimo Encontrado:")
    print(f" - Perfil: {optimal_row['Name']}")
    print(f" - Área: {optimal_row['Area_cm2']:.2f} cm2")
    print(f" - Aprovechamiento: {optimal_row['Ratio']:.2%}")
    
    # 3. Generar visualización
    plt=plot_design_space(df_results)

    # plt.savefig('optimization_result.png', dpi=300)
    plt.savefig('optimization_result.svg', format='svg')
    plt.show()