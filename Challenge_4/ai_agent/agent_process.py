from ai_agent.tools.processment import (
    consultar_admissao_abril,
    consultar_afastamentos,
    consultar_aprendiz,
    consultar_ativos,
    consultar_base_dias_uteis,
    consultar_base_sindicato_valor,
    consultar_desligados,
    consultar_estagio,
    consultar_exterior,
    consultar_ferias,
    consultar_vr_mensal
)
from ai_agent.tools.utils import (
    response_to_df,
    df_to_excel,
    df_to_csv,
    gerar_planilha_excel
)
from ai_agent.agent_config import get_agent
import pandas as pd

def agent_process() -> pd.DataFrame:

    tools = [
        consultar_admissao_abril,
        consultar_afastamentos,
        consultar_aprendiz,
        consultar_ativos,
        consultar_base_dias_uteis,
        consultar_base_sindicato_valor,
        consultar_desligados,
        consultar_estagio,
        consultar_exterior,
        consultar_ferias,
        consultar_vr_mensal,
        response_to_df,
        df_to_excel,
        df_to_csv,
        gerar_planilha_excel
    ]

    query = """
    Execute as seguintes tarefas na ordem EXATA para gerar o RELATÓRIO VR MENSAL:

    1. Use a ferramenta 'consultar_admissao_abril' com a query: "liste todas as matrículas com suas respectivas datas de admissão em formato tabular"

    2. Use a ferramenta 'consultar_estagio' com a query: "liste todas as matrículas dos estagiários"

    3. Use a ferramenta 'consultar_afastamentos' com a query: "liste todas as matrículas com status de afastamento"

    4. Identifique quais matrículas estão nas admissões de abril MAS NÃO estão na lista de estagiários.

    5. Para cada matrícula que NÃO é estagiário, determine:
    - Número da matrícula
    - Data de admissão correspondente  
    - Status de afastamento (SIM se consta na lista de afastamentos, NÃO caso contrário)

    6. Monte um CSV COMPLETO com TODAS as matrículas filtradas seguindo EXATAMENTE este formato:
    MATRICULA,DATA_ADMISSAO,AFASTADO
    35741,07/04/2024,NÃO
    35774,22/04/2024,SIM
    35722,02/04/2024,NÃO
    ... (continuar com TODAS as matrículas restantes)

    7. Use a ferramenta 'gerar_planilha_excel' passando o CSV completo do passo 6 com nome "relatorio_vr_mensal_abril".

    REQUISITOS OBRIGATÓRIOS DO DESAFIO:
    - OBJETIVO: Relatório VR mensal para colaboradores admitidos em abril
    - EXCLUIR: Todos os estagiários (matrícula 27.0 e outras identificadas)
    - INCLUIR: Status de afastamento (coluna AFASTADO: SIM/NÃO)
    - FORMATO: Planilha Excel com colunas MATRICULA, DATA_ADMISSAO, AFASTADO
    - FILTRO: Apenas colaboradores (não estagiários) admitidos em abril
    - DADOS: Usar informações reais dos DataFrames carregados

    VALIDAÇÃO:
    - Total esperado: 83 admissões - 27 estagiários = 56 colaboradores válidos
    - Formato de data: dd/mm/aaaa
    - Status afastamento: SIM ou NÃO (baseado na consulta de afastamentos)
    - NÃO pule nenhuma matrícula válida

    Execute TODAS as ferramentas na ordem especificada e processe os dados completos para gerar o relatório VR mensal conforme especificado no desafio.
    """

    agent = get_agent(tools)

    response = agent.invoke({"input": query})

    return response['output']