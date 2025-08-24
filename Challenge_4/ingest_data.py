import os
import pandas as pd

def ingest_excel_files(input_dir="input_data") -> dict[str, pd.DataFrame]:
    dataframes = {}
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".xlsx"):
            file_path = os.path.join(input_dir, filename)
            df_name = os.path.splitext(filename)[0]
            try:
                df = pd.read_excel(file_path)
                df = df.fillna('')  # Substitui NaN por ''
                dataframes[df_name] = df
            except Exception as e:
                print(f"Erro ao ler {filename}: {e}")
    if not dataframes:
        print("Nenhum arquivo .xlsx encontrado.")
    return dataframes

def process_admissao_abril(dfs: dict[str, pd.DataFrame], df_key="ADMISSÃO ABRIL"):
    if df_key in dfs:
        df = dfs[df_key]
        last_col = df.columns[-1]
        df = df.rename(columns={last_col: "Observações"})
        dfs[df_key] = df

def process_base_dias_uteis(dfs: dict[str, pd.DataFrame], df_key="Base dias uteis"):
    if df_key in dfs:
        df = dfs[df_key]
        new_headers = df.iloc[0]
        df.columns = new_headers
        df = df.drop(df.index[[0,1]]).reset_index(drop=True)
        dfs[df_key] = df
    return



if __name__ == "__main__":
    dfs = ingest_excel_files()
    process_admissao_abril(dfs, df_key="ADMISSÃO ABRIL")
    process_base_dias_uteis(dfs, df_key="Base dias uteis")
    df = dfs["Base sindicato x valor"]
    print(df.columns)

    for name, df in dfs.items():
      print(f"DataFrame '{name}':")
      #print(df.head())
      #print("-" * 40)