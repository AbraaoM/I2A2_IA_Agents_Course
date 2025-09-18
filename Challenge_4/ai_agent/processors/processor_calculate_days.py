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

def run_calculate_days(competencia: Optional[str] = None, default_days: int = 22) -> Dict[str, Any]:
    """
    Para cada linha em vr_mensal:
     - lê sindicato e competencia (ou usa competencia passada)
     - busca DIAS em base_dias_uteis preferindo match por competencia + sindicato, fallback por competencia
     - atualiza coluna DIAS (ou cria) no singleton vr_mensal
    Retorna resumo simples.
    """
    vr = dataframes.dataframes.get("vr_mensal")
    base = dataframes.dataframes.get("base_dias_uteis")

    if vr is None or vr.empty:
        return {"status": "error", "message": "vr_mensal ausente ou vazio"}

    # detectar colunas em vr_mensal e base_dias_uteis
    sind_col = _find_col(vr, ["SINDICATO DO COLABORADOR", "SINDICATO", "SIND"])
    comp_col = _find_col(vr, ["COMPETENCIA", "COMPETÊNCIA", "COMP"])
    base_comp_col = _find_col(base, ["COMPETENCIA", "COMPETÊNCIA", "COMP"]) if base is not None else None
    base_sind_col = _find_col(base, ["SINDICATO", "SIND", "SINDICATO_DO_COLABORADOR"]) if base is not None else None
    base_days_col = _find_col(base, ["DIAS", "DIAS_UTEIS", "DIAS UTEIS", "DIAS_UTEIS"]) if base is not None else None

    # garantir coluna DIAS
    if "DIAS" not in vr.columns:
        vr["DIAS"] = 0

    updated = 0
    for idx, row in vr.iterrows():
        comp_val = competencia if competencia else (row.get(comp_col) if comp_col else None)
        comp_str = str(comp_val).strip() if comp_val is not None and not pd.isna(comp_val) else ""

        sind_val = row.get(sind_col) if sind_col else None
        sind_str = str(sind_val).strip() if sind_val is not None and not pd.isna(sind_val) else ""

        days_val = None
        if base is not None and base_days_col and base_comp_col:
            # tentar match por competencia + sindicato (se ambos existirem)
            if base_sind_col and sind_str:
                mask = base[base_comp_col].astype(str).str.strip() == comp_str
                mask &= base[base_sind_col].astype(str).str.lower().str.contains(sind_str.lower(), na=False)
                found = base.loc[mask]
                if not found.empty:
                    try:
                        days_val = int(found.iloc[0][base_days_col])
                    except Exception:
                        days_val = None
            # fallback por competencia apenas
            if days_val is None:
                mask2 = base[base_comp_col].astype(str).str.strip() == comp_str
                found2 = base.loc[mask2]
                if not found2.empty:
                    try:
                        days_val = int(found2.iloc[0][base_days_col])
                    except Exception:
                        days_val = None

        if days_val is None:
            days_val = int(default_days)

        try:
            current = int(row.get("DIAS") or 0)
        except Exception:
            current = 0

        if current != days_val:
            vr.at[idx, "DIAS"] = int(days_val)
            updated += 1

    dataframes.dataframes["vr_mensal"] = vr
    return {"status": "completed", "updated": updated, "total_rows": len(vr)}