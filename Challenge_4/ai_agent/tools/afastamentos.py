from langchain_core.tools import tool
from ai_agent.agent_config import get_df_agent
from singletons import dataframes

@tool
def read_afastamentos(query: str) -> str:
    """Consulta informações no DataFrame AFASTAMENTOS."""
    df = dataframes.dataframes["afastamentos"]
    agent = get_df_agent(df)
    return agent.run({"input": query})