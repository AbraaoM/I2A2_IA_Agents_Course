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

def run_calculate_total(round_digits: int = 2) -> Dict[str, Any]:
    """
    Calcula TOTAL = VALOR_DIARIO_VR * DIAS para cada linha de vr_mensal.
    Atualiza a coluna 'TOTAL' no singleton.
    """
    vr = dataframes.dataframes.get("vr_mensal")
    if vr is None or vr.empty:
        return {"status": "error", "message": "vr_mensal ausente ou vazio"}

    valor_col = _find_col(vr, ["VALOR_DIARIO_VR", "VALOR DIARIO VR", "VALOR_DIARIO", "VALOR_VR", "VALOR"])
    dias_col = _find_col(vr, ["DIAS", "DIAS_UTEIS", "DIAS UTEIS"])

    target_col = "TOTAL"
    if target_col not in vr.columns:
        vr[target_col] = 0.0

    updated = 0
    for idx, row in vr.iterrows():
        # ler valores de forma segura
        v_raw = row.get(valor_col) if valor_col else None
        d_raw = row.get(dias_col) if dias_col else None

        try:
            v = float(v_raw) if (v_raw is not None and not pd.isna(v_raw)) else 0.0
        except Exception:
            v = 0.0
        try:
            d = int(d_raw) if (d_raw is not None and not pd.isna(d_raw)) else 0
        except Exception:
            # tentar float -> int
            try:
                d = int(float(d_raw))
            except Exception:
                d = 0

        total = round(v * d, round_digits)

        cur = row.get(target_col)
        try:
            cur_f = float(cur) if (cur is not None and not pd.isna(cur)) else None
        except Exception:
            cur_f = None

        if cur_f is None or round(cur_f, round_digits) != total:
            vr.at[idx, target_col] = total
            updated += 1

    dataframes.dataframes["vr_mensal"] = vr
    return {"status": "completed", "updated": updated, "total_rows": len(vr)}