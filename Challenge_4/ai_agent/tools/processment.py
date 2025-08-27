from langchain_core.tools import tool
from ai_agent.agent_config import get_df_agent
from singletons import dataframes

@tool
def consultar_admissao_abril(query: str) -> str:
    """Consulta informações no DataFrame ADMISSÃO ABRIL."""
    df = dataframes.dataframes["ADMISSÃO ABRIL"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_afastamentos(query: str) -> str:
    """Consulta informações no DataFrame AFASTAMENTOS."""
    df = dataframes.dataframes["AFASTAMENTOS"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_aprendiz(query: str) -> str:
    """Consulta informações no DataFrame APRENDIZ."""
    df = dataframes.dataframes["APRENDIZ"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_ativos(query: str) -> str:
    """Consulta informações no DataFrame ATIVOS."""
    df = dataframes.dataframes["ATIVOS"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_base_dias_uteis(query: str) -> str:
    """Consulta informações no DataFrame Base dias uteis."""
    df = dataframes.dataframes["Base dias uteis"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_base_sindicato_valor(query: str) -> str:
    """Consulta informações no DataFrame Base sindicato x valor."""
    df = dataframes.dataframes["Base sindicato x valor"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_desligados(query: str) -> str:
    """Consulta informações no DataFrame DESLIGADOS."""
    df = dataframes.dataframes["DESLIGADOS"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_estagio(query: str) -> str:
    """Consulta informações no DataFrame ESTÁGIO."""
    df = dataframes.dataframes["ESTÁGIO"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_exterior(query: str) -> str:
    """Consulta informações no DataFrame EXTERIOR."""
    df = dataframes.dataframes["EXTERIOR"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_ferias(query: str) -> str:
    """Consulta informações no DataFrame FÉRIAS."""
    df = dataframes.dataframes["FÉRIAS"]
    agent = get_df_agent(df)
    return agent.run({"input": query})

@tool
def consultar_vr_mensal(query: str) -> str:
    """Consulta informações no DataFrame VR MENSAL 05.2025."""
    df = dataframes.dataframes["VR MENSAL 05.2025"]
    agent = get_df_agent(df)
    return agent.run({"input": query})