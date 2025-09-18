import pandas as pd
from langchain_core.runnables import RunnableLambda

from ai_agent.processors.processor_populate_vr_mensal import run_populate_vr_mensal_agent


def agent_process() -> pd.DataFrame:

    run_populate_vr_mensal_agent()