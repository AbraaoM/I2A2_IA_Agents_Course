from ai_agent.agent_config import get_agent
import pandas as pd
from ai_agent.tools.admissao_abril import read_admissao_abril
from ai_agent.tools.afastamentos import read_afastamentos
from ai_agent.tools.aprendiz import read_aprendiz
from ai_agent.tools.ativos import read_ativos
from ai_agent.tools.base_dias_uteis import read_base_dias_uteis
from ai_agent.tools.base_sindicato_valor import read_base_sindicato_valor
from ai_agent.tools.desligados import read_desligados
from ai_agent.tools.estagio import read_estagio
from ai_agent.tools.exterior import read_exterior
from ai_agent.tools.ferias import read_ferias
from ai_agent.tools.utils import generate_vr_mensal_excel
from ai_agent.tools.vr_mensal import read_vr_mensal, add_vr_mensal

def agent_process() -> pd.DataFrame:

    tools = [
        read_admissao_abril,
        read_afastamentos,
        read_aprendiz,
        read_ativos,
        read_base_dias_uteis,
        read_base_sindicato_valor,
        read_desligados,
        read_estagio,
        read_exterior,
        read_ferias,
        read_vr_mensal,
        add_vr_mensal,
        generate_vr_mensal_excel
    ]

    query = """
            
            """

    agent = get_agent(tools)

    response = agent.invoke({"input": query})

    return response['output']