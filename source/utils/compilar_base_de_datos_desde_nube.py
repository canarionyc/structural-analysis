# %% Cell: DuckDB Compilation from Google Sheets
# import duckdb
import pandas as pd


def compilar_base_de_datos_desde_nube(SHEET_ID:str, GID: str, db_path: str):

    # Construct the direct download URLs
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

    print("Fetching data from Google Cloud...")
    print(url)
    # 2. Read directly into Pandas DataFrames
    try:
        df = pd.read_csv(url)
        
        # Optional: Strip whitespace from column names just in case
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"❌ Failed to fetch data. Check if the sheet is public. Error: {e}")
        return None

    # # 3. Compile the local DuckDB database
    # with duckdb.connect(db_path) as db:
    #     # Create strict tables
    #     db.execute("""
    #         CREATE TABLE IF NOT EXISTS prontuario (
    #             id_sistema VARCHAR PRIMARY KEY,
    #             descripcion VARCHAR
    #         );
    #     """)

       

    #     # Clear existing data in case you are re-running to update rules
    #     db.execute("DELETE FROM intensidades_admisibles")
       

    #     # Insert fresh data from the cloud
    #     db.execute("INSERT INTO prontuario SELECT * FROM df")
       

    # print(f"✅ DuckDB database successfully compiled at: {db_path}")
    return df

#%% test

# 1. Configuration: Replace with your actual IDs
SHEET_ID = "1pjAgZ-w26yN53RNQprhijJxRk2h0ln0Q0xWbFVthGbo"

# Replace these with the actual GIDs from your tabs
GID = "1503201646"  # Usually 0 for the first tab

# Execute the compilation

data=compilar_base_de_datos_desde_nube(SHEET_ID,GID, 'prontuarios.duckdb')
print(data)