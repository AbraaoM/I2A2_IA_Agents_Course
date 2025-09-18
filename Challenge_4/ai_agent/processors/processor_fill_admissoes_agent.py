from typing import Dict, Any
import json
import time
import re

from ai_agent.agent_config import get_agent
from ai_agent.tools.vr_mensal import read_vr_mensal, update_vr_mensal_row
from ai_agent.tools.admissao_abril import read_admissao_abril_by_matricula

def run_fill_admissoes_agent(max_matriculas: int = 500) -> Dict[str, Any]:
    """
    Invoca um agente que preenche ADMISSAO em vr_mensal:
     - usa read_vr_mensal para listar matrículas
     - para cada matrícula (até max_matriculas) chama read_admissao_abril_by_matricula
     - chama update_vr_mensal_row(matricula=<mat>, admissao="<data>" ou admissao="-")
     - retorna JSON parseado se presente ou saída bruta
    """
    tools = [read_vr_mensal, read_admissao_abril_by_matricula, update_vr_mensal_row]

    prompt = f"""
Use EXCLUSIVAMENTE as ferramentas disponíveis. NÃO gere texto livre — apenas faça chamadas de ferramenta.
Objetivo: preencher o campo ADMISSAO em todas as linhas do DataFrame VR_MENSAL.

Passos:
1) Chame read_vr_mensal para listar as matrículas.
2) Para cada matrícula (até {max_matriculas}):
   - Chame read_admissao_abril_by_matricula(<matricula>) e extraia data se existir.
   - Se existir, chame update_vr_mensal_row(matricula=<matricula>, admissao="<DATA_ENCONTRADA>")
   - Se NÃO existir, chame update_vr_mensal_row(matricula=<matricula>, admissao="-")
3) Ao final RETORNE APENAS UM JSON VÁLIDO (sem texto adicional) no formato:
   {{ "updated": [matriculas], "skipped": [matriculas_sem_alteracao] }}
"""

    agent = get_agent(tools)
    start = time.time()
    try:
        response = agent.invoke({"input": prompt})
    except Exception as e:
        return {"status": "error", "message": f"agent.invoke error: {e}"}

    # obter saída textual do agente
    out_text = response.get("output") if isinstance(response, dict) else str(response)

    # tentar parsear JSON final
    parsed = None
    try:
        parsed = json.loads(out_text.strip())
    except Exception:
        m = re.search(r"(\{.*\})", out_text, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(1))
            except Exception:
                parsed = None

    return {"status": "completed", "agent_parsed": parsed, "raw": out_text}