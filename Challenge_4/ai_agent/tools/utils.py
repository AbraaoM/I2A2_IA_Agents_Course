from langchain_core.tools import tool
import pandas as pd
from io import StringIO

@tool
def response_to_df(response: str) -> pd.DataFrame:
    """
    Tenta converter uma resposta tabular (CSV ou Markdown) em DataFrame pandas.
    Limpa separadores e espaços dos nomes das colunas e dos valores das células.
    """
    def clean_cell(cell):
        if isinstance(cell, str):
            return cell.strip().replace('|', '').strip()
        return cell

    # Tenta ler como CSV
    try:
        df = pd.read_csv(StringIO(response))
        df.columns = [clean_cell(col) for col in df.columns]
        df = df.applymap(clean_cell)
        return df
    except Exception:
        print("Não foi possível converter a resposta em DataFrame CSV.")
        pass
    # Tenta ler como tabela Markdown
    try:
        df = pd.read_table(StringIO(response), sep="|", engine="python")
        # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = [clean_cell(col) for col in df.columns]
        df = df.applymap(clean_cell)
        return df
    except Exception:
        print("Não foi possível converter a resposta em DataFrame.")
        pass
    return None