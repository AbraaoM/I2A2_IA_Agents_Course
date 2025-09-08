from langchain_core.tools import tool
from ai_agent.agent_config import get_df_agent
from singletons import dataframes

@tool
def read_admissao_abril(query: str) -> str:
    """Consulta informações no DataFrame ADMISSÃO ABRIL."""
    df = dataframes.dataframes["admissao_abril"]
    agent = get_df_agent(df)
    return agent.run({"input": query})