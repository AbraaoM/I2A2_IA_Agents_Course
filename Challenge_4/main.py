from ingest_data import ingest_data
from ai_agent.agent_process import agent_process
from singletons import dataframes


if __name__ == "__main__":
    # Carregar os dados
    print("Carregando dados...")
    dfs = ingest_data()
    print(dfs["ativos"])
    dataframes.dataframes = dfs
    
    # Obter relatório mensal usando o agente
    # print("Gerando relatório mensal com agente...")
    # response = agent_process()

    # print(response)