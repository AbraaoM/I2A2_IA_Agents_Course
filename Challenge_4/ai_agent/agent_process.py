from ai_agent.tools.processment import (
    consultar_admissao_abril,
    consultar_afastamentos,
    consultar_aprendiz,
    consultar_ativos,
    consultar_base_dias_uteis,
    consultar_base_sindicato_valor,
    consultar_desligados,
    consultar_estagio,
    consultar_exterior,
    consultar_ferias,
    consultar_vr_mensal
)
from ai_agent.tools.utils import (
    response_to_df,
    df_to_excel,
    df_to_csv,
    gerar_planilha_excel
)
from ai_agent.agent_config import get_agent
import pandas as pd

def agent_process() -> pd.DataFrame:

    tools = [
        consultar_admissao_abril,
        consultar_afastamentos,
        consultar_aprendiz,
        consultar_ativos,
        consultar_base_dias_uteis,
        consultar_base_sindicato_valor,
        consultar_desligados,
        consultar_estagio,
        consultar_exterior,
        consultar_ferias,
        consultar_vr_mensal,
        response_to_df,
        df_to_excel,
        df_to_csv,
        gerar_planilha_excel
    ]

    query = """
            1. Crie um dataframe com as seguintes colunas:
            * Matrícula
            * Admissão
            * Sindicato do Colaborador
            * Competência
            * Dias
            * VALOR DIÁRIO VR
            * TOTAL
            * Custo empresa
            * Desconto profissional
            * OBS GERAL

            Se necessário preencha as colunas com uma string vazia.

            2. Utilizando a tool gerar_planilha_excel: 
            crie uma planilha excel com o nome "VR MENSAL 05.2025.xlsx" a partir do dataframe criado no passo 1.
            
            """

    agent = get_agent(tools)

    response = agent.invoke({"input": query})

    return response['output']