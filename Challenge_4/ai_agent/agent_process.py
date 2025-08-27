from ai_agent.agent_utils import response_to_df
from ai_agent.agent_tools import consultar_afastamentos, consultar_estagio
import pandas as pd

def agent_process() -> pd.DataFrame:
    response = consultar_estagio.invoke(
        "Quais são as matrículas? Utilize apenas dados tabulares na resposta, a resposta deve conter apenas uma coluna chamada 'MATRICULA'."
    )
    return response_to_df(response)