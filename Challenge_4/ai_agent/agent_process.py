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
    Execute as seguintes tarefas na ordem:

    1. Use a ferramenta 'consultar_admissao_abril' para obter todas as matrículas disponíveis.

    2. Organize as matrículas em formato CSV com cabeçalho:
    MATRICULA
    35741
    35774
    35722
    (... todas as outras matrículas)

    3. Use a ferramenta 'gerar_planilha_excel' para criar uma planilha Excel com os dados organizados.
       - Nome do arquivo: "matriculas_admissao_abril"
       - Formato: uma matrícula por linha

    Execute AMBAS as ferramentas para completar a tarefa.
    """

    agent = get_agent(tools)

    response = agent.invoke({"input": query})

    return response['output']