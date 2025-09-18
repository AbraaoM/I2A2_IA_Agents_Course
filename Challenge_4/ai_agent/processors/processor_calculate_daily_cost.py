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

def run_calculate_daily_cost(default_valor: float = 0.0, debug: bool = False) -> Dict[str, Any]:
    """
    Preenche VALOR DIARIO VR em vr_mensal usando base_sindicato_valor.
    debug=True imprime informações úteis para diagnosticar por que não houve preenchimento.
    """
    vr_mensal_df = dataframes.dataframes.get("vr_mensal")
    base_sindicato_valor_df = dataframes.dataframes.get("base_sindicato_valor")

    if vr_mensal_df is None or base_sindicato_valor_df is None:
        raise ValueError("DataFrames 'vr_mensal' e 'base_sindicato_valor' devem estar carregados.")

    SIND_STATE_MAP = {
        "sitepd pr": ["pr", "parana", "paraná"],
        "sindppd rs": ["rs", "rio grande do sul"],
        "sindpd sp": ["sp", "sao paulo", "são paulo"],
        "sindpd rj": ["rj", "rio de janeiro"]
    }

    # detectar colunas relevantes
    vr_sind_col = _find_col(vr_mensal_df, ["SINDICATO DO COLABORADOR", "SINDICATO", "SIND"])
    base_state_col = _find_col(base_sindicato_valor_df, ["ESTADO", "UF", "SIGLA"])
    base_val_col = _find_col(base_sindicato_valor_df, ["VALOR", "VALOR_VR", "VALOR_DIARIO", "VALOR_DIARIO_VR", "VALOR DIARIO VR"])

    target_col = "VALOR DIARIO VR"
    if target_col not in vr_mensal_df.columns:
        vr_mensal_df[target_col] = float(default_valor)

    updated = 0
    for idx, row in vr_mensal_df.iterrows():
        sind_raw = ""
        if vr_sind_col and pd.notna(row.get(vr_sind_col)):
            sind_raw = str(row.get(vr_sind_col)).strip().lower()

        valor_diario = float(default_valor)

        # verificar cada mapa conhecido (ex: "sitepd pr")
        for key, terms in SIND_STATE_MAP.items():
            if key in sind_raw:
                # procurar valor no base pelo estado (qualquer termo do mapa)
                if base_state_col and base_val_col:
                    base_state_series = base_sindicato_valor_df[base_state_col].astype(str).str.lower()
                    mask = pd.Series(False, index=base_sindicato_valor_df.index)
                    for t in terms:
                        mask = mask | base_state_series.str.contains(t, na=False)
                    found = base_sindicato_valor_df.loc[mask]
                    if not found.empty:
                        try:
                            valor_diario = float(found.iloc[0][base_val_col])
                        except Exception:
                            valor_diario = float(default_valor)
                break

        # atualizar célula se necessário
        try:
            cur = row.get(target_col)
            cur_f = float(cur) if pd.notna(cur) else None
        except Exception:
            cur_f = None

        if cur_f is None or round(cur_f, 6) != round(valor_diario, 6):
            vr_mensal_df.at[idx, target_col] = float(valor_diario)
            updated += 1

    dataframes.dataframes["vr_mensal"] = vr_mensal_df
    return {"status": "completed", "updated": updated, "total_rows": len(vr_mensal_df)}

