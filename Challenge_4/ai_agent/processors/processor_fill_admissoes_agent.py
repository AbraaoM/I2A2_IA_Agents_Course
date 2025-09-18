import pandas as pd
from typing import Dict, Any
from singletons import dataframes


def _find_col(df: pd.DataFrame, candidates):
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


def run_fill_admissoes_agent() -> Dict[str, Any]:
    """
    Simples e direto: atualiza a coluna ADMISSAO em vr_mensal lendo admissao_abril do singleton.
    Se não encontrar data para uma matrícula, preenche com '-'.
    Não usa tools, escreve diretamente no singleton.
    """
    vr = dataframes.dataframes.get("vr_mensal")
    adm = dataframes.dataframes.get("admissao_abril")

    if vr is None or vr.empty:
        return {"status": "error", "message": "vr_mensal ausente ou vazio"}

    vr_mat = _find_col(vr, ["MATRICULA", "Matricula", "matricula"])
    if vr_mat is None:
        return {"status": "error", "message": "coluna matricula não encontrada em vr_mensal"}

    adm_mat = _find_col(adm, ["MATRICULA", "Matricula", "matricula"]) if adm is not None else None
    adm_date = _find_col(adm, ["DATA DE ADMISSAO", "ADMISSAO", "ADMISSÃO", "DATA_ADMISSAO"]) if adm is not None else None

    # garantir coluna ADMISSAO em vr_mensal
    if "ADMISSAO" not in vr.columns:
        vr["ADMISSAO"] = "-"

    updated = 0
    # criar índice para admissão se possível
    adm_index = None
    if adm is not None and adm_mat is not None:
        try:
            adm_index = adm.set_index(adm[adm_mat].astype(str))
        except Exception:
            adm_index = None

    for idx, row in vr.iterrows():
        mat = row.get(vr_mat)
        if pd.isna(mat):
            continue
        # normalizar matrícula para string chave
        try:
            mat_key = str(int(mat)) if float(mat).is_integer() else str(mat).strip()
        except Exception:
            mat_key = str(mat).strip()

        adm_value = "-"
        if adm is not None:
            if adm_index is not None:
                try:
                    rec = adm_index.loc[mat_key]
                    # rec pode ser Series ou DataFrame
                    val = rec.get(adm_date) if adm_date in adm.columns else None
                    if pd.notna(val):
                        adm_value = str(val)
                except Exception:
                    adm_value = "-"
            elif adm_mat is not None:
                mask = adm[adm_mat].astype(str).str.strip() == mat_key
                if mask.any() and adm_date in adm.columns:
                    val = adm.loc[mask].iloc[0].get(adm_date)
                    if pd.notna(val):
                        adm_value = str(val)

        if str(vr.at[idx, "ADMISSAO"]) != adm_value:
            vr.at[idx, "ADMISSAO"] = adm_value
            updated += 1

    dataframes.dataframes["vr_mensal"] = vr
    return {"status": "completed", "updated": updated, "total_rows": len(vr)}