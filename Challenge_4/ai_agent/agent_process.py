import pandas as pd
from singletons import dataframes

from ai_agent.processors.processor_populate_vr_mensal import run_populate_vr_mensal_agent
from ai_agent.processors.processor_fill_admissoes_agent import run_fill_admissoes_agent
from ai_agent.processors.processor_calculate_days import run_calculate_days


def agent_process() -> pd.DataFrame:

    run_populate_vr_mensal_agent()
    run_fill_admissoes_agent()
    run_calculate_days()

    print(dataframes.dataframes["vr_mensal"][["MATRICULA", "DIAS"]])