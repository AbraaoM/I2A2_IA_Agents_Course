from ai_agent.agent_config import get_agent
import pandas as pd
from ai_agent.tools.admissao_abril import read_admissao_abril_all, read_admissao_abril_by_matricula
from ai_agent.tools.afastamentos import read_afastamentos
from ai_agent.tools.aprendiz import read_aprendiz
from ai_agent.tools.ativos import read_ativos_all, read_ativos_by_matricula
from ai_agent.tools.base_dias_uteis import read_base_dias_uteis
from ai_agent.tools.base_sindicato_valor import read_base_sindicato_valor
from ai_agent.tools.desligados import read_desligados
from ai_agent.tools.estagio import read_estagio
from ai_agent.tools.exterior import read_exterior
from ai_agent.tools.ferias import read_ferias
from ai_agent.tools.utils import generate_vr_mensal_excel
from ai_agent.tools.vr_mensal import read_vr_mensal, add_vr_mensal

def agent_process() -> pd.DataFrame:
    tools = [
        read_ativos_all,
        read_ativos_by_matricula,
        read_admissao_abril_all,
        read_admissao_abril_by_matricula,
        add_vr_mensal,
        generate_vr_mensal_excel
    ]

    query = """
        Utilize a tool add_vr_mensal para adicionar os seguintes dados ao DataFrame VR_MENSAL:
        Matrícula: Utilize a tool read_ativos_all para obter a lista de matriculas válidas e aplique a mesma lógica para todas as matrículas encontradas individualmente, criando uma linha para cada matrícula.
        Admissão: Busque a data de admissão usando a tool read_admissao_abril_by_matricula, se não encontrar preencher com 00/00/0000
        Sindicato do Colaborador: Usando a matricula busque o sindicato usando a tool read_ativos_by_matricula
        Competência: 05/2025
        Dias: 22
        Valor Diário VR: 25.00
        Total: 550.00
        Custo Empresa: 600.00
        Desconto Profissional: 50.00
        Obs Geral: Nenhuma observação adicional.
        Após adicionar os dados, utilize a ferramenta generate_vr_mensal_excel para gerar um arquivo Excel com o conteúdo atualizado do DataFrame VR_MENSAL.
        Forneça o caminho do arquivo Excel gerado como resposta.
            """

    agent = get_agent(tools)

    response = agent.invoke({"input": query})

    return response['output']