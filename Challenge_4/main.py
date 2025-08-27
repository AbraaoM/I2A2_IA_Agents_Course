from ingest_data import ingest_data
from ai_agent.agent_process import construir_vr_mensal
from singletons import dataframes


if __name__ == "__main__":
    dfs = ingest_data()
    dataframes.dataframes = dfs
    response = construir_vr_mensal()
    print(response)