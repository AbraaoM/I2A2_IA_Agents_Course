import os
import pandas as pd
import unicodedata
from models.DataFrameKeys import DataFrameKeys

def ingest_excel_files(input_dir="input_data") -> dict[DataFrameKeys, pd.DataFrame]:
    """
    Carrega arquivos Excel e mapeia para chaves padronizadas do DataFrameKeys.
    """
    # Mapeamento de nomes de arquivos para chaves padronizadas
    filename_to_key_mapping = {
        "ADMISSÃO ABRIL": "admissao_abril",
        "AFASTAMENTOS": "afastamentos",
        "APRENDIZ": "aprendiz",
        "ATIVOS": "ativos",
        "Base dias uteis": "base_dias_uteis",
        "Base sindicato x valor": "base_sindicato_valor",
        "DESLIGADOS": "desligados",
        "ESTÁGIO": "estagio",
        "EXTERIOR": "exterior",
        "FÉRIAS": "ferias",
        "VR MENSAL 05.2025": "vr_mensal"
    }
    
    dataframes = {}
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".xlsx") and not filename.startswith('.~'):
            file_path = os.path.join(input_dir, filename)
            df_name = os.path.splitext(filename)[0]
            
            # Mapear nome do arquivo para chave padronizada
            standard_key = filename_to_key_mapping.get(df_name)
            
            if not standard_key:
                print(f"⚠️ Arquivo não mapeado: {filename}")
                continue
            
            try:
                df = pd.read_excel(file_path)
                df = df.fillna('')  # Substitui NaN por ''
                dataframes[standard_key] = df
                print(f"✅ Carregado: {filename} -> {standard_key} ({df.shape[0]} linhas)")
            except Exception as e:
                print(f"❌ Erro ao ler {filename}: {e}")
    
    if not dataframes:
        print("Nenhum arquivo .xlsx encontrado.")
    
    return dataframes

def process_admissao_abril(dfs: dict[DataFrameKeys, pd.DataFrame]):
    """
    Processa o DataFrame de admissões de abril.
    """
    df_key = "admissao_abril"
    if df_key in dfs:
        df = dfs[df_key]
        last_col = df.columns[-1]
        df = df.rename(columns={last_col: "Observações"})
        dfs[df_key] = df
        print(f"📝 Processado: {df_key}")

def process_base_dias_uteis(dfs: dict[DataFrameKeys, pd.DataFrame]):
    """
    Processa o DataFrame de base de dias úteis.
    """
    df_key = "base_dias_uteis"
    if df_key in dfs:
        df = dfs[df_key]
        new_headers = df.iloc[0]
        df.columns = new_headers
        df = df.drop(df.index[[0,1]]).reset_index(drop=True)
        dfs[df_key] = df
        print(f"📝 Processado: {df_key}")

def process_vr_mensal(dfs: dict[DataFrameKeys, pd.DataFrame]):
    """
    Processa o DataFrame de VR mensal.
    """
    df_key = "vr_mensal"
    if df_key in dfs:
        df = dfs[df_key]
        new_headers = df.iloc[0]
        df.columns = new_headers
        df = df.drop(df.index[[0,1]]).reset_index(drop=True)
        
        # Normalizar headers
        df = normalize_headers_df(df)
        
        dfs[df_key] = df
        print(f"📝 Processado: {df_key}")

def matriculas_vr_mensal(dfs: dict[DataFrameKeys, pd.DataFrame], matricula_col="MATRICULA"):
    """
    Consolida matrículas de todos os DataFrames no VR mensal.
    """
    vr_key = "vr_mensal"
    if vr_key not in dfs:
        print(f"DataFrame '{vr_key}' não encontrado.")
        return

    vr_df = dfs[vr_key].copy()
    
    # Percorre todos os outros DataFrames
    for key, df in dfs.items():
        if key == vr_key:
            continue
        
        # Normalizar headers do DataFrame atual
        df_normalized = normalize_headers_df(df.copy())
        
        if matricula_col in df_normalized.columns:
            # Cria um DataFrame apenas com as matrículas válidas
            matriculas_validas = df_normalized[df_normalized[matricula_col] != ''][matricula_col]
            if not matriculas_validas.empty:
                matriculas_df = pd.DataFrame({matricula_col: matriculas_validas})
                vr_df = pd.concat([vr_df, matriculas_df], ignore_index=True)
    
    # Remove duplicatas
    if matricula_col in vr_df.columns:
        vr_df = vr_df.drop_duplicates(subset=[matricula_col]).reset_index(drop=True)
        dfs[vr_key] = vr_df
        print(f"🔄 Duplicatas removidas em {vr_key} ({vr_df.shape[0]} linhas únicas)")

def normalize_headers_df(df: pd.DataFrame) -> pd.DataFrame:
    new_cols = []
    for col in df.columns:
        col_norm = unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('ASCII')
        new_cols.append(col_norm.upper())
    df.columns = new_cols
    return df

def ingest_data():
    dfs = ingest_excel_files()
    process_admissao_abril(dfs)
    process_base_dias_uteis(dfs)
    process_vr_mensal(dfs)
    matriculas_vr_mensal(dfs)
    
    return (dfs)