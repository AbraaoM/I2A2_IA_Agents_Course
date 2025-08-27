from ai_agent.tools.utils import response_to_df
from ai_agent.tools.processment import (
    consultar_estagio, 
    consultar_admissao_abril, 
    consultar_afastamentos
)
from ai_agent.agent_config import get_agent
import pandas as pd

def construir_vr_mensal() -> pd.DataFrame:

    agent = get_agent([
        consultar_estagio, 
        consultar_admissao_abril, 
        consultar_afastamentos,
        response_to_df
    ])

    return agent.invoke({"input": "Capture informações relevantes. " \
        "Utilize apenas dados tabulares na resposta, os títulos das colunas deve ser em letra maiúscula. " \
        "As datas devem usar o formato dd/mm/aaaa." \
        "Não devem ser incluídos os estagiários. "
        "O retorno deve ser em formato de dataframe. " })
    
    # 1. Buscar todas as matrículas relevantes
    # print("Buscando o matrículas...")
    # response_matriculas = consultar_admissao_abril.invoke(
    #     "Capture informações relevantes? " \
    #     "Utilize apenas dados tabulares na resposta, os títulos das colunas deve ser em letra maiúscula. " \
    #     "As datas devem usar o formato dd/mm/aaaa." \
    #     "Não devem ser incluídos os estagiários. " \
    # )
    # df_vr = response_to_df.invoke(response_matriculas)

    # 2. Remover os estagiários

    # # 2. Buscar datas de admissão para cada matrícula
    # print("Buscando Datas de admissão")
    # datas_admissao = []
    # for matricula in df_vr["MATRICULA"]:
    #     resp = consultar_admissao_abril.invoke(
    #         f"Qual a data de admissão da matrícula {matricula}? Responda apenas com a data, o formato deve ser dd/mm/aaaa, caso não seja possível definir a data responda -"
    #     )
    #     datas_admissao.append(resp.strip())
    # df_vr["DATA_ADMISSAO"] = datas_admissao

    # # 3. Buscar status de afastamento para cada matrícula
    # status_afastamento = []
    # for matricula in df_vr["MATRICULA"]:
    #     resp = consultar_afastamentos.invoke(
    #         f"A matrícula {matricula} está afastada? Responda apenas com 'SIM' ou 'NÃO'."
    #     )
    #     status_afastamento.append(resp.strip())
    # df_vr["AFASTADO"] = status_afastamento

    # Adicione outras colunas conforme necessário...