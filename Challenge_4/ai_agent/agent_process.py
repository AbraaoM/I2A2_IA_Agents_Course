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

    query = "1. utilizando a ferramenta 'consultar_admissao_abril' liste as matrículas disponíveis."

    agent = get_agent(tools)

    response = agent.invoke({"input": query})

    return response['output']