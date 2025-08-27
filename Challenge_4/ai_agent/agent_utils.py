import pandas as pd
from io import StringIO

def response_to_df(response: str) -> pd.DataFrame:
    """
    Tenta converter uma resposta tabular (CSV ou Markdown) em DataFrame pandas.
    """
    # Tenta ler como CSV
    try:
        df = pd.read_csv(StringIO(response))
        return df
    except Exception:
        pass
    # Tenta ler como tabela Markdown
    try:
        df = pd.read_table(StringIO(response), sep="|", engine="python")
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception:
        pass
    return None