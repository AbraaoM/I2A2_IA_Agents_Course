from langchain_core.tools import tool
from ai_agent.agent_config import get_df_agent
from singletons import dataframes

@tool
def read_vr_mensal(query: str) -> str:
    """Consulta informações no DataFrame VR MENSAL."""
    df = dataframes.dataframes["vr_mensal"]
    agent = get_df_agent(df)
    return agent.run({"input": query})