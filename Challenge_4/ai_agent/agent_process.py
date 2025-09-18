import pandas as pd
from langchain_core.runnables import RunnableLambda

from ai_agent.processors.processor_populate_vr_mensal import run_populate_vr_mensal_agent as populate_vr_mensal_agent
from ai_agent.tools.utils import generate_vr_mensal_excel
from ai_agent.processors.processor_filter_vr_mensal_agent import run_filter_vr_mensal_agent


def agent_process() -> pd.DataFrame:
    
    populate_vr_mensal = RunnableLambda(lambda x: populate_vr_mensal_agent(max_matriculas=100))
    generate_archive = RunnableLambda(lambda x: generate_vr_mensal_excel())
    filter_vr_mensal = RunnableLambda(lambda x: run_filter_vr_mensal_agent(max_matriculas=100))

    vr_mensal_chain = populate_vr_mensal | filter_vr_mensal | generate_archive

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