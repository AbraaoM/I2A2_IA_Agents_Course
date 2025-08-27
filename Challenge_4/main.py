from ingest_data import ingest_data
from ai_agent.agent_config import get_agent


if __name__ == "__main__":
    dfs = ingest_data()
    agent = get_agent(dfs["vr mensal"])
    print(agent.run("Quais são as 5 primeiras matrículas?"))