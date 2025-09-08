from langchain_core.tools import tool
from ai_agent.agent_config import get_df_agent
from singletons import dataframes

@tool
def read_base_dias_uteis(query: str) -> str:
    """Consulta informações no DataFrame BASE DIAS ÚTEIS."""
    df = dataframes.dataframes["base_dias_uteis"]
    agent = get_df_agent(df)
    return agent.run({"input": query})