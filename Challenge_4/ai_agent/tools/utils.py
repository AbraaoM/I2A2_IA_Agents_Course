from langchain_core.tools import tool
import os
from singletons import dataframes

@tool
def generate_vr_mensal_excel() -> str:
    """
    Gera um arquivo Excel com os dados do DataFrame VR MENSAL.
    
    Returns:
        str: Caminho do arquivo Excel salvo.
    """
    try:
        # Obter DataFrame VR MENSAL do singleton
        df = dataframes.dataframes["vr_mensal"]
        
        if df.empty:
            return "Erro: DataFrame VR MENSAL está vazio."
        
        # Nome fixo do arquivo
        filename = "VR MENSAL 05.2025.xlsx"
        
        # Salva o DataFrame como um arquivo Excel
        df.to_excel(filename, index=False)
        
        return f"✅ Arquivo Excel gerado: {os.path.abspath(filename)} com {len(df)} registros."
        
    except KeyError:
        return "Erro: DataFrame VR MENSAL não encontrado no singleton."
    except Exception as e:
        return f"Erro ao gerar Excel: {str(e)}"
