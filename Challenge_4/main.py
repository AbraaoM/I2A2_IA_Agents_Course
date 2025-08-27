from ingest_data import ingest_data
from ai_agent.agent_process import agent_process
from singletons import dataframes


if __name__ == "__main__":
    dfs = ingest_data()
    dataframes.dataframes = dfs
    response = agent_process()
    print(response)