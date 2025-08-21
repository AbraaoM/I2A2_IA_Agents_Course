import os
import pandas as pd

def ingest_excel_files(input_dir="input_data"):
    dataframes = {}
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".xlsx"):
            file_path = os.path.join(input_dir, filename)
            df_name = os.path.splitext(filename)[0]
            try:
                df = pd.read_excel(file_path)
                dataframes[df_name] = df
            except Exception as e:
                print(f"Erro ao ler {filename}: {e}")
    if not dataframes:
        print("Nenhum arquivo .xlsx encontrado.")
    return dataframes

if __name__ == "__main__":
    dfs = ingest_excel_files()
    for name, df in dfs.items():
        print(f"DataFrame '{name}':")
        print(df.head())
        print("-" * 40)