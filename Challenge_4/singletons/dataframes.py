import pandas as pd

from typing import Literal


DataFrameKeys = Literal[
  "admissao_abril",
    "afastamentos", 
    "aprendiz",
    "ativos",
    "base_dias_uteis",
    "base_sindicato_valor",
    "desligados",
    "estagio",
    "exterior",
    "ferias",
    "vr_mensal"
]

dataframes: dict[DataFrameKeys, pd.DataFrame] = {}