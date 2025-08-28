from ai_agent.tools.processment import consultar_admissao_abril
from ai_agent.tools.utils import response_to_df
from ai_agent.agent_config import get_agent
import pandas as pd

def agent_process() -> pd.DataFrame:

    tools = [
        consultar_admissao_abril,
        response_to_df
    ]

    query_matriculas = "1. utilizando a ferramenta 'consultar_admissao_abril' liste as matrículas disponíveis."

    agent = get_agent(tools)

    response = agent.invoke({"input": query_matriculas})

    return response['output']