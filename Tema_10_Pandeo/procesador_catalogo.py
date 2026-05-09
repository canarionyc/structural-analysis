# %% GOOGLE SHEETS BUCKLING PROCESSOR
import pandas as pd
import math

def calculate_buckling_resistance(D_mm: float, t_mm: float, L_cr_mm: float = 3450.0) -> float:
    """
    Calcula el N_b,Rd (Resistencia a pandeo) para un tubo circular (CHS)
    en acero S-275 según el DB SE-A (Curva 'a').
    """
    # Constantes
    E = 210000.0 # MPa
    fy = 275.0 # MPa
    gamma_M1 = 1.05
    alpha = 0.21 # Curva 'a' para tubos conformados en caliente
    
    # Propiedades geométricas
    inner_d = D_mm - 2 * t_mm
    A_mm2 = (math.pi / 4) * (D_mm**2 - inner_d**2)
    I_mm4 = (math.pi / 64) * (D_mm**4 - inner_d**4)
    i_mm = math.sqrt(I_mm4 / A_mm2)
    
    # Esbeltez y coeficientes de pandeo
    slenderness = L_cr_mm / i_mm
    lambda_1 = math.pi * math.sqrt(E / fy)
    lambda_bar = slenderness / lambda_1
    
    if lambda_bar <= 0.2:
        chi = 1.0
    else:
        phi = 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)
        chi = 1 / (phi + math.sqrt(phi**2 - lambda_bar**2))
        chi = min(chi, 1.0)
        
    # Capacidad (kN)
    Nb_Rd_kN = (chi * A_mm2 * fy) / (gamma_M1 * 1000)
    return Nb_Rd_kN

# %% MAIN EXECUTION BLOCK
if __name__ == "__main__":
    # 1. Transformamos la URL de "edit" a "export?format=csv" para que pandas pueda leerla directamente
    sheet_id = "1eHmX8KWvaoCTH3RKp7JTf3CpQ97Rl2OvI2ZNOiBIvVo"
    gid = "887358775"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    print(f"Descargando datos desde Google Sheets...")
    
    try:
        # Nota: El documento de Google Sheets debe tener los permisos en "Cualquier persona con el enlace puede leer"
        df = pd.read_csv(csv_url)
        
        # Limpiamos nombres de columnas por si tienen espacios (asumiendo que las columnas se llaman 'D' y 'e' o 't')
        df.columns = df.columns.str.strip()
        
        # 2. Comprobamos que existan las columnas necesarias
        col_diametro = 'D' if 'D' in df.columns else 'D (mm)'
        col_espesor = 'e' if 'e' in df.columns else 'e (mm)'
        
        if col_diametro not in df.columns or col_espesor not in df.columns:
            raise KeyError(f"No se encontraron las columnas de diámetro y espesor. Columnas detectadas: {list(df.columns)}")

        # 3. Calculamos N_b,Rd para una longitud de pandeo específica
        LONGITUD_PANDEO_MM = 3450.0 
        
        print(f"Calculando N_b,Rd para L_cr = {LONGITUD_PANDEO_MM} mm...")
        
        # Aplicamos la función fila por fila
        df['N_b,Rd (kN)'] = df.apply(
            lambda row: calculate_buckling_resistance(row[col_diametro], row[col_espesor], L_cr_mm=LONGITUD_PANDEO_MM), 
            axis=1
        )
        
        # Redondeamos a 1 decimal para mayor limpieza
        df['N_b,Rd (kN)'] = df['N_b,Rd (kN)'].round(1)
        
        # Mostramos una muestra del resultado
        print("\nResultado exitoso. Primeras filas:")
        print(df[[col_diametro, col_espesor, 'N_b,Rd (kN)']].head(10))
        
        # Opcional: Guardar el nuevo catálogo en tu base de datos DuckDB o a un CSV local
        df.to_csv('catalogo_actualizado.csv', index=False)
        
    except Exception as error:
        print(f"Error al procesar el archivo: {error}")
        print("Asegúrate de que la hoja de Google Sheets es pública ('Cualquier persona con el enlace').")