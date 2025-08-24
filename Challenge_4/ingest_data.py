import os
import pandas as pd
import unicodedata

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

def process_vr_mensal(dfs: dict[str, pd.DataFrame], df_key="VR MENSAL 05.2025"):
    if df_key in dfs:
        df = dfs[df_key]
        new_headers = df.iloc[0]
        df.columns = new_headers
        df = df.drop(df.index[[0,1]]).reset_index(drop=True)
        dfs[df_key] = df
    
        # Cria um DataFrame vazio com o mesmo cabeçalho
        df = pd.DataFrame(columns=df.columns)
        normalize_headers_df(df)

        dfs["vr mensal"] = df

def matriculas_vr_mensal(dfs: dict[str, pd.DataFrame], matricula_col="MATRICULA", vr_key="vr mensal"):
    if vr_key not in dfs:
        print(f"DataFrame '{vr_key}' não encontrado.")
        return

    vr_df = dfs[vr_key]
    # Percorre todos os outros DataFrames
    for key, df in dfs.items():
        if key == vr_key:
            continue
        if matricula_col in df.columns:
            # Cria um DataFrame apenas com as matrículas
            matriculas_df = pd.DataFrame(df[matricula_col])
            vr_df = pd.concat([vr_df, matriculas_df], ignore_index=True)
    # Remove duplicatas
    vr_df = vr_df.drop_duplicates(subset=[matricula_col]).reset_index(drop=True)
    dfs[vr_key] = vr_df

def normalize_headers_df(df: pd.DataFrame) -> pd.DataFrame:
    new_cols = []
    for col in df.columns:
        col_norm = unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('ASCII')
        new_cols.append(col_norm.upper())
    df.columns = new_cols
    return df

if __name__ == "__main__":
    dfs = ingest_excel_files()
    process_admissao_abril(dfs)
    process_base_dias_uteis(dfs)
    process_vr_mensal(dfs)
    matriculas_vr_mensal(dfs)
    
    print(dfs["vr mensal"])

    #for name, df in dfs.items():
     # print(f"DataFrame '{name}':")
      #print(df.head())
      #print("-" * 40)