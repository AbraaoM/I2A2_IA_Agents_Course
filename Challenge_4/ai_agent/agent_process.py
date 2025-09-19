import pandas as pd
from singletons import dataframes
from langchain_core.runnables import RunnableLambda

from ai_agent.processors.processor_populate_vr_mensal import run_populate_vr_mensal_agent
from ai_agent.processors.processor_fill_admissoes_agent import run_fill_admissoes_agent
from ai_agent.processors.processor_calculate_days import run_calculate_days
from ai_agent.processors.processor_calculate_daily_cost import run_calculate_daily_cost
from ai_agent.processors.processor_calculate_total import run_calculate_total
from ai_agent.processors.processor_calculate_share import run_calculate_share
from ai_agent.tools.utils import generate_vr_mensal_excel

def agent_process() -> pd.DataFrame:
    
    populate_vr_mensal = RunnableLambda(lambda x: run_populate_vr_mensal_agent())
    generate_archive = RunnableLambda(lambda x: generate_vr_mensal_excel())
    fill_admissoes = RunnableLambda(lambda x: run_fill_admissoes_agent())
    calculate_days = RunnableLambda(lambda x: run_calculate_days())
    calculate_daily_cost = RunnableLambda(lambda x: run_calculate_daily_cost())
    calculate_total = RunnableLambda(lambda x: run_calculate_total())
    calculate_share = RunnableLambda(lambda x: run_calculate_share())

    vr_mensal_chain = populate_vr_mensal | fill_admissoes | calculate_days | calculate_daily_cost | calculate_total | calculate_share | generate_archive

    # executar cadeia
    response = vr_mensal_chain.invoke({})

    # debug
    print("DEBUG: type(response) =", type(response))
    try:
        # se for dict com 'output'
        if isinstance(response, dict) and 'output' in response:
            print("DEBUG: returning response['output']")
            return response['output']
        # se for dict sem 'output' — retornar inteiro para inspeção
        if isinstance(response, dict):
            print("DEBUG: returning full dict response")
            return response
        # se for string (mais provável), retornar diretamente
        print("DEBUG: returning raw response")
        return response
    except Exception as e:
        print("Erro ao formatar retorno:", e)
        return str(response)