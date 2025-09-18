import pandas as pd

from singletons import dataframes
import json
import time
from typing import Optional

def _detect_sindicato_col(df: pd.DataFrame) -> Optional[str]:
    for c in df.columns:
        if 'SINDICATO' in str(c).upper():
            return c
    for c in df.columns:
        if 'SIND' in str(c).upper():
            return c
    return None

def _detect_situacao_col(df: pd.DataFrame) -> Optional[str]:
    for c in df.columns:
        if 'DESC' in str(c).upper() and 'SITUAC' in str(c).upper():
            return c
    for c in df.columns:
        if 'SITUAC' in str(c).upper() or 'SITUA' in str(c).upper():
            return c
    return None

def run_populate_vr_mensal_agent(competencia: str = "05/2025"):
    """
    Copia matricula + sindicato do DataFrame 'ativos' para 'vr_mensal'.
    - Idempotente: não duplica matrículas.
    - Se matrícula já existe em vr_mensal e sindicato estiver vazio, atualiza com o novo valor.
    - Somente adiciona/considera registros cujo campo de situação contenha 'trabalh' (ex.: 'Trabalhando'),
      quando a coluna de situação existir no DataFrame 'ativos'.
    """
    ativos = dataframes.dataframes.get("ativos")
    if ativos is None or ativos.empty:
        raise ValueError("DataFrame 'ativos' não encontrado ou vazio.")

    vr_mensal = dataframes.dataframes.get("vr_mensal")
    if vr_mensal is None:
        # criar DataFrame mínimo
        vr_mensal = pd.DataFrame(columns=['MATRICULA', 'SINDICATO DO COLABORADOR', 'COMPETENCIA'])

    # garantir coluna MATRICULA em vr_mensal
    if 'MATRICULA' not in vr_mensal.columns:
        vr_mensal['MATRICULA'] = pd.Series(dtype='Int64')

    sind_col = _detect_sindicato_col(ativos)
    situ_col = _detect_situacao_col(ativos)
    added = 0
    updated = 0

    for _, row in ativos.iterrows():
        # somente considerar se situação indicar trabalhando (se coluna existir)
        if situ_col:
            situ_val = row.get(situ_col)
            if pd.isna(situ_val):
                continue
            try:
                s = str(situ_val).strip().lower()
            except Exception:
                s = ""
            if 'trabalh' not in s:  # filtra "Trabalhando" e variações
                continue

        raw_mat = row.get('MATRICULA')
        if pd.isna(raw_mat):
            continue
        try:
            matricula = int(raw_mat)
        except Exception:
            continue

        sindicato = None
        if sind_col:
            val = row.get(sind_col)
            if not pd.isna(val):
                sindicato = str(val).strip()

        # localizar existência (comparar como int)
        exists_idx = vr_mensal.index[vr_mensal['MATRICULA'].astype('Int64') == matricula].tolist() if not vr_mensal.empty else []

        if exists_idx:
            idx = exists_idx[0]
            # atualizar sindicato se vazio e novo disponível
            current = vr_mensal.at[idx, 'SINDICATO DO COLABORADOR'] if 'SINDICATO DO COLABORADOR' in vr_mensal.columns else None
            if (current is None or pd.isna(current) or str(current).strip() == "") and sindicato:
                vr_mensal.at[idx, 'SINDICATO DO COLABORADOR'] = sindicato
                updated += 1
        else:
            new_entry = {
                'MATRICULA': matricula,
                'SINDICATO DO COLABORADOR': sindicato,
                'COMPETENCIA': competencia,
            }
            vr_mensal = pd.concat([vr_mensal, pd.DataFrame([new_entry])], ignore_index=True)
            added += 1

    # gravar de volta no singleton
    dataframes.dataframes['vr_mensal'] = vr_mensal
    print(f"Populated vr_mensal — added: {added}, updated: {updated}, total_rows: {len(vr_mensal)}")
    return {"added": added, "updated": updated, "total_rows": len(vr_mensal)}