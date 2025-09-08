from langchain_core.tools import tool
from ai_agent.agent_config import get_df_agent
from singletons import dataframes

@tool
def read_base_sindicato_valor(query: str) -> str:
    """Consulta informações no DataFrame BASE SINDICATO X VALOR."""
    df = dataframes.dataframes["base_sindicato_valor"]
    agent = get_df_agent(df)
    return agent.run({"input": query})