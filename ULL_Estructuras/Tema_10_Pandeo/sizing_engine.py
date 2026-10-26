# %% DATABASE SETUP (DuckDB)
import duckdb
import pandas as pd

# Connect to an in-memory database
import pyprojroot
root = pyprojroot.here()
# print(root)
catalog_path = root.joinpath('data/chs_catalog.db')
print(catalog_path)

# %% Best practice: Use a context manager to ensure the lock is released
with duckdb.connect(str(catalog_path)) as con:
# 1. Create the table with explicit numeric columns to avoid string parsing later
    con.execute("""
    DROP TABLE IF EXISTS chs_catalog;
        CREATE TABLE if not exists chs_catalog (
            name VARCHAR,
            diameter_mm DOUBLE,
            thickness_mm DOUBLE,
            area_cm2 DOUBLE,
            inertia_cm4 DOUBLE
        )
    """)

    # 2. Populate the database
    catalog_data = [
        ("CHS 114.3x3.6", 114.3, 3.6, 12.5, 190.0),
        ("CHS 114.3x5.0", 114.3, 5.0, 17.2, 251.0),
        ("CHS 139.7x4.0", 139.7, 4.0, 17.1, 392.0),
        ("CHS 139.7x5.0", 139.7, 5.0, 21.2, 479.0),
        ("CHS 168.3x4.0", 168.3, 4.0, 20.6, 696.0),
        ("CHS 168.3x6.3", 168.3, 6.3, 32.1, 1040.0)
    ]

    con.executemany("INSERT INTO chs_catalog VALUES (?, ?, ?, ?, ?)", catalog_data)
    con.close()
# %% amplification function
import numpy as np


def amplification_func(P, EI, L, epsilon_0):
    """
    Calculates the additional lateral deflection (y_max) at the center
    of a Fixed-Fixed column due to second-order effects (P-Delta).

    Parameters:
    P          : Applied axial load [N]
    EI         : Flexural rigidity [N*m^2]
    L          : Physical length of the column [m]
    epsilon_0  : Initial geometric bow/imperfection [m]

    Returns:
    y_max      : Additional elastic deflection [m]
    """
    # 1. The theoretical Euler critical load for the Fixed-Fixed case
    # Note: Lk = 0.5L, so (pi^2 * EI) / (0.5L)^2 = 4 * pi^2 * EI / L^2
    p_critical = (4 * np.pi ** 2 * EI) / (L ** 2)

    # 2. Check for physical singularity (avoiding division by zero)
    if P >= p_critical:
        return float('inf')

    # 3. The Variational result for the amplification of the initial bow
    # y_max = epsilon_0 * [ (P/P_cr) / (1 - P/P_cr) ]
    # which simplifies to the expression below:
    y_max = epsilon_0 * (P / (p_critical - P))

    return y_max

# %% UPDATED SIZING ENGINE WITH SQL
def sizing_engine_sql(load, l, e_mod, fy, gamma, eps):
    # REPLACE THE STRING PARSING WITH THIS SQL QUERY
    # We calculate the radius_outer and SI units directly in the database engine
    query = """
        SELECT 
            name, 
            area_cm2 * 1e-4 AS A, 
            inertia_cm4 * 1e-8 AS I, 
            (diameter_mm / 2000) AS radius_outer
        FROM chs_catalog
    """

    # Fetch data as a list of dictionaries or a DataFrame
    with duckdb.connect(str(catalog_path)) as con:

# Lock is released here automatically
        df = con.execute(query).fetchdf()

        all_data = []

        for _, tube in df.iterrows():
            A = tube['A']
            I = tube['I']
            radius_outer = tube['radius_outer']  # Clean, numeric, and SI-ready!

            W_el = I / radius_outer

            try:
                delta_max = amplification_func(load, e_mod * I, l, eps)
            except ZeroDivisionError:
                delta_max = float('inf')

            # Stress Calculation
            sigma_comp = load / A
            sigma_bend = (load * (delta_max + eps)) / W_el
            total_stress_mpa = (sigma_comp + sigma_bend) / 1e6

            is_safe = total_stress_mpa <= (fy / gamma / 1e6)

            all_data.append({
                "Name": tube["name"],
                "Area_cm2": A * 1e4,
                "TotalStress_MPa": total_stress_mpa,
                "Safe": is_safe
            })

    return all_data


#%% Execute
results = sizing_engine_sql(P_APPLIED, LENGTH, E_MODULUS, YIELD_STRESS, GAMMA_M1, IMPERFECTION)

# Print summary
for res in results:
    status = "SAFE" if res["Safe"] else "FAIL"
    print(f"Profile: {res['Name']:<15} | Stress: {res['TotalStress_MPa']:>7.2f} MPa | {status}")

# %% PLOTTING THE PROFILE SEARCH SPACE
import matplotlib.pyplot as plt
import numpy as np


def plot_profile_space(results_data, fy, gamma):
    # Convert results to a DataFrame for easier plotting
    df_plot = pd.DataFrame(results_data)

    # Design limits
    design_strength = (fy / gamma) / 1e6  # MPa

    plt.figure(figsize=(11, 7))

    # 1. Plot the "Yield Ceiling"
    plt.axhline(y=design_strength, color='#d62728', linestyle='--', linewidth=2,
        label=f'Yield Limit ({design_strength:.1f} MPa)')

    # 2. Separate Safe and Unsafe points for coloring
    safe = df_plot[df_plot['Safe'] == True]
    unsafe = df_plot[df_plot['Safe'] == False]

    # 3. Plot the profiles
    plt.scatter(unsafe['Area_cm2'], unsafe['TotalStress_MPa'], color='red', s=80, edgecolors='black',
        label='Unsafe (Buckling/Yield)')
    plt.scatter(safe['Area_cm2'], safe['TotalStress_MPa'], color='green', s=120, edgecolors='black',
        label='Safe Region')

    # 4. Highlight the "Optimal" (Minimum Area among Safe)
    if not safe.empty:
        optimal = safe.loc[safe['Area_cm2'].idxmin()]
        plt.scatter(optimal['Area_cm2'], optimal['TotalStress_MPa'], color='gold', s=300, marker='*',
            edgecolors='black', label='OPTIMAL CHOICE', zorder=5)
        plt.annotate("Minimum Mass Solution", (optimal['Area_cm2'], optimal['TotalStress_MPa']), xytext=(15, -15),
            textcoords='offset points', fontweight='bold', color='darkgoldenrod')

    # 5. Labeling and Annotations
    for i, row in df_plot.iterrows():
        plt.annotate(row['Name'], (row['Area_cm2'], row['TotalStress_MPa']), xytext=(8, 8), textcoords='offset points',
            fontsize=9, alpha=0.7)

    # Aesthetics
    plt.title("Structural Design Space: Total Stress vs. Section Area", fontsize=14)
    plt.xlabel("Cross-Sectional Area ($cm^2$)", fontsize=12)
    plt.ylabel("Total Combined Stress ($\\sigma_{tot}$) [MPa]", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)

    # Shading the "Failure Zone"
    plt.fill_between([df_plot['Area_cm2'].min() - 5, df_plot['Area_cm2'].max() + 5], design_strength,
        df_plot['TotalStress_MPa'].max() + 50, color='red', alpha=0.05, label="Failure Zone")

    plt.xlim(df_plot['Area_cm2'].min() - 2, df_plot['Area_cm2'].max() + 2)
    plt.legend(loc='upper right', frameon=True, shadow=True)
    plot_path = root.joinpath('Tema_10_Pandeo/sizing_engine_plot.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()


# Run the plot
plot_profile_space(results, YIELD_STRESS, GAMMA_M1)