import pandas as pd
from singletons import dataframes

from ai_agent.processors.processor_populate_vr_mensal import run_populate_vr_mensal_agent
from ai_agent.processors.processor_fill_admissoes_agent import run_fill_admissoes_agent
from ai_agent.processors.processor_calculate_days import run_calculate_days
from ai_agent.processors.processor_calculate_daily_cost import run_calculate_daily_cost


def agent_process() -> pd.DataFrame:
    print(dataframes.dataframes["base_sindicato_valor"])

    run_populate_vr_mensal_agent()
    run_fill_admissoes_agent()
    run_calculate_days()
    run_calculate_daily_cost()

    print(dataframes.dataframes["vr_mensal"][["MATRICULA", "DIAS", "ADMISSAO", "VALOR DIARIO VR"]])