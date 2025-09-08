from langchain_core.tools import tool
from singletons import dataframes

@tool
def read_ativos_all() -> str:
    """Lê todos os registros do DataFrame ATIVOS."""
    try:
        df = dataframes.dataframes.get("ativos")
        if df is None or df.empty:
            return "DataFrame 'ativos' não encontrado ou vazio."
        return df.to_string()
    except Exception as e:
        return f"Erro ao ler ativos: {str(e)}"

@tool
def read_ativos_by_matricula(matricula: int) -> str:
    """Lê registro específico do DataFrame ATIVOS por matrícula."""
    try:
        df = dataframes.dataframes.get("ativos")
        if df is None or df.empty:
            return "DataFrame 'ativos' não encontrado ou vazio."
        
        filtered_df = df[df['MATRICULA'] == matricula]
        if filtered_df.empty:
            return f"Nenhum registro encontrado para matrícula: {matricula}"
        
        return filtered_df.to_string()
    except Exception as e:
        return f"Erro ao buscar matrícula {matricula}: {str(e)}"