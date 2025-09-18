from typing import Dict, Any
import json
import time

from ai_agent.agent_config import get_agent
from ai_agent.tools.vr_mensal import read_vr_mensal, delete_vr_mensal_row
from ai_agent.tools.ativos import read_ativos_by_matricula
from ai_agent.tools.estagio import read_estagio
from ai_agent.tools.aprendiz import read_aprendiz
from ai_agent.tools.afastamentos import read_afastamentos

def run_filter_vr_mensal_agent(max_matriculas: int = 500) -> Dict[str, Any]:
    """
    Delegue totalmente ao agente a identificação e remoção de matrículas em vr_mensal.
    - NÃO faz verificações locais.
    - O agente deve chamar delete_vr_mensal_row(...) para cada remoção.
    - Retorna o texto cru do agente e, se possível, o JSON parseado.
    """
    tools = [
        read_vr_mensal,
        read_ativos_by_matricula,
        read_estagio,
        read_aprendiz,
        read_afastamentos,
        delete_vr_mensal_row,
    ]

    prompt = f"""
Use EXCLUSIVAMENTE as ferramentas disponíveis. NÃO gere explicações — apenas faça chamadas de ferramenta.
Objetivo: para cada matrícula presente no DataFrame VR_MENSAL identifique e REMOVA linhas que sejam de:
  - diretor (cargo indicando 'diretor'),
  - estagiário,
  - aprendiz,
  - afastado.

Instruções operacionais:
1) Chame read_vr_mensal para listar as linhas.
2) Para cada matrícula (até {max_matriculas}):
   - Use read_ativos_by_matricula(<matricula>) para verificar cargo.
   - Use read_estagio(<matricula>), read_aprendiz(<matricula>) e read_afastamentos(<matricula>) para verificar presença nas bases.
   - Se decidir remover, CHAME delete_vr_mensal_row(matricula=<matricula>, competencia="").
3) Ao final RETORNE APENAS UM JSON VÁLIDO (sem texto adicional) no formato:
   {{ "removed": [123,124,...], "reasons": {{ "123": "diretor", "124": "estagiario" }} }}
"""

    print("▶ run_filter_vr_mensal_agent: invocando agente (delegando remoções)")
    agent = get_agent(tools)
    start = time.time()
    try:
        response = agent.invoke({"input": prompt})
        elapsed = time.time() - start
        print(f"⏱ Agent finished in {elapsed:.2f}s")
    except Exception as e:
        return {"status": "error", "message": f"agent.invoke error: {e}"}

    # extrair saída do agente
    out_text = ""
    if isinstance(response, dict):
        out_text = response.get("output") or response.get("result") or str(response)
    else:
        out_text = str(response)

    # tentar parsear JSON final retornado pelo agente
    parsed = None
    try:
        parsed = json.loads(out_text.strip())
    except Exception:
        import re
        m = re.search(r"(\{.*\})", out_text, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(1))
            except Exception:
                parsed = None

    return {"status": "completed", "agent_parsed": parsed, "raw": out_text}