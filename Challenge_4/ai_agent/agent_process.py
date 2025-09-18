import pandas as pd
from singletons import dataframes

from ai_agent.processors.processor_populate_vr_mensal import run_populate_vr_mensal_agent
from ai_agent.processors.processor_fill_admissoes_agent import run_fill_admissoes_agent


def agent_process() -> pd.DataFrame:

    run_populate_vr_mensal_agent()
    run_fill_admissoes_agent()

    print(dataframes.dataframes.get("vr_mensal"))