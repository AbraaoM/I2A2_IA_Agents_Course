import pandas as pd
from typing import Dict, Any, Optional
from singletons import dataframes

def _find_col(df: Optional[pd.DataFrame], candidates):
    if df is None:
        return None
    for c in df.columns:
        if str(c).upper() in (x.upper() for x in candidates):
            return c
    for c in df.columns:
        up = str(c).upper()
        for cand in candidates:
            if cand.upper() in up:
                return c
    return None

def run_calculate_share(round_digits: int = 2) -> Dict[str, Any]:
    """
    Para cada linha em vr_mensal:
      - obtém TOTAL (ou calcula como VALOR_DIARIO_VR * DIAS quando TOTAL ausente)
      - preenche CUSTO_EMPRESA = 80% do total
      - preenche DESCONTO_PROFISSIONAL = 20% do total
    Atualiza o singleton vr_mensal e retorna resumo.
    """
    vr = dataframes.dataframes.get("vr_mensal")
    if vr is None or vr.empty:
        return {"status": "error", "message": "vr_mensal ausente ou vazio"}

    total_col = _find_col(vr, ["TOTAL", "VALOR_TOTAL", "TOTAL_VR"])
    valor_col = _find_col(vr, ["VALOR_DIARIO_VR", "VALOR DIARIO VR", "VALOR_DIARIO", "VALOR_VR"])
    dias_col = _find_col(vr, ["DIAS", "DIAS_UTEIS", "DIAS UTEIS"])

    # nomes alvo (cria se não existirem)
    custo_col = "CUSTO_EMPRESA"
    desconto_col = "DESCONTO_PROFISSIONAL"
    if custo_col not in vr.columns:
        vr[custo_col] = 0.0
    if desconto_col not in vr.columns:
        vr[desconto_col] = 0.0

    updated = 0
    for idx, row in vr.iterrows():
        # obter total
        total_val = None
        if total_col and pd.notna(row.get(total_col)):
            try:
                total_val = float(row.get(total_col))
            except Exception:
                total_val = None

        if total_val is None and valor_col:
            # tentar calcular total = valor * dias
            v_raw = row.get(valor_col)
            d_raw = row.get(dias_col) if dias_col else None
            try:
                v = float(v_raw) if (v_raw is not None and not pd.isna(v_raw)) else 0.0
            except Exception:
                v = 0.0
            try:
                d = int(d_raw) if (d_raw is not None and not pd.isna(d_raw)) else 0
            except Exception:
                try:
                    d = int(float(d_raw))
                except Exception:
                    d = 0
            total_val = round(v * d, round_digits)

        if total_val is None:
            total_val = 0.0

        custo = round(total_val * 0.80, round_digits)
        desconto = round(total_val * 0.20, round_digits)

        cur_custo = row.get(custo_col)
        cur_desconto = row.get(desconto_col)
        try:
            cur_custo_f = float(cur_custo) if (cur_custo is not None and not pd.isna(cur_custo)) else None
        except Exception:
            cur_custo_f = None
        try:
            cur_desconto_f = float(cur_desconto) if (cur_desconto is not None and not pd.isna(cur_desconto)) else None
        except Exception:
            cur_desconto_f = None

        if cur_custo_f is None or round(cur_custo_f, round_digits) != custo or cur_desconto_f is None or round(cur_desconto_f, round_digits) != desconto:
            vr.at[idx, custo_col] = custo
            vr.at[idx, desconto_col] = desconto
            updated += 1

    dataframes.dataframes["vr_mensal"] = vr
    return {"status": "completed", "updated": updated, "total_rows": len(vr)}