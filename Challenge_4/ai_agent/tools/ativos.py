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
    """Lê registro específico do DataFrame ATIVOS por matrícula e retorna em formato JSON."""
    import json
    try:
        df = dataframes.dataframes.get("ativos")
        if df is None or df.empty:
            return json.dumps({"erro": "DataFrame 'ativos' não encontrado ou vazio."})

        filtered_df = df[df['MATRICULA'] == matricula]
        if filtered_df.empty:
            return json.dumps({"erro": f"Nenhum registro encontrado para matrícula: {matricula}"})

        # Retorna a primeira linha como dict (caso haja mais de uma, pega só a primeira)
        result = filtered_df.iloc[0].to_dict()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"erro": f"Erro ao buscar matrícula {matricula}: {str(e)}"})