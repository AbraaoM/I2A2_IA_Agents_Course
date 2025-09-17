from typing import Dict, Any
from ai_agent.agent_config import get_agent
from ai_agent.tools.ativos import read_ativos_all, read_ativos_by_matricula
from ai_agent.tools.vr_mensal import read_vr_mensal, add_vr_mensal
from singletons import dataframes
import json
import time

def run_populate_vr_mensal_agent(competencia: str = "05/2025", max_matriculas: int = 10) -> Dict[str, Any]:
    """
    Agente que:
      - obtém todas as linhas de 'ativos' (read_ativos_all),
      - para cada matrícula com DESC_SITUACAO == 'Trabalhando' obtém sindicato (read_ativos_by_matricula),
      - adiciona uma linha base em vr_mensal via add_vr_mensal (somente se não existir para a competência).
    Retorna dict com status e resposta do agente.
    """
    tools = [read_ativos_all, read_ativos_by_matricula, read_vr_mensal, add_vr_mensal]

    prompt = f"""
Use APENAS as ferramentas disponíveis. NÃO gere texto livre — apenas chamadas de ferramenta.
Objetivo: popular o DataFrame VR_MENSAL com linhas base para competência "{competencia}".

Passos obrigatórios:
1) Chame read_ativos_all para obter todos os ativos.
2) Extraia MATRÍCULA e confirme que DESC_SITUACAO == "Trabalhando".
3) Para cada matrícula (limite {max_matriculas}):
   - Chame read_ativos_by_matricula(<matricula>) para obter dados detalhados e extrair 'Sindicato' se existir.
   - Chame read_vr_mensal('mostrar todas as linhas') para verificar se já existe linha para essa matrícula e competência "{competencia}".
   - Se NÃO existir, chame add_vr_mensal com TODOS os parâmetros nomeados (admissao pode ser string vazia, dias/valores zeros):
       add_vr_mensal(
         matricula=<MATRICULA>,
         admissao="",
         sindicato_colaborador="<SINDICATO>",
         competencia="{competencia}",
         dias=0,
         valor_diario_vr=0.0,
         total=0.0,
         custo_empresa=0.0,
         desconto_profissional=0.0,
         obs_geral=""
       )
   - Se já existir, pule.
4) Ao final, RETORNE APENAS um JSON válido com {{\"added\": [...], \"skipped\": [...]}} sem texto adicional.
"""

    print("📌 Executando agente: populate_vr_mensal (debug ligado)")
    print("Tools:", [t.name for t in tools])
    print("Prompt (resumido):", prompt[:800])

    agent = get_agent(tools)
    start = time.time()
    try:
        response = agent.invoke({"input": prompt})
        elapsed = time.time() - start
        print(f"⏱ Agent finished in {elapsed:.2f}s")
        out = response.get("output") if isinstance(response, dict) else str(response)
        # tentar parsear JSON final do agente (se o agente seguiu instrução)
        try:
            parsed = json.loads(out.strip())
        except Exception:
            parsed = {"raw_output": out}
        # mostrar estado atual do vr_mensal para debug
        try:
            df_vr = dataframes.dataframes.get("vr_mensal")
            print("VR_MENSAL rows:", len(df_vr) if df_vr is not None else 0)
        except Exception as e:
            print("Erro ao ler vr_mensal:", e)
        return {"status": "completed", "agent_response": response, "parsed": parsed}
    except Exception as e:
        print("Agent error:", e)
        return {"status": "error", "error": str(e)}