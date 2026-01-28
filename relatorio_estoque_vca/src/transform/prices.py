from __future__ import annotations

from typing import Dict

import pandas as pd


def compute_avg_price_by_tipology(
    df_units_emp: pd.DataFrame, df_prices: pd.DataFrame, unit_id_col: str
) -> Dict[str, float]:
    units = df_units_emp.copy()
    units[unit_id_col] = pd.to_numeric(units[unit_id_col], errors="coerce")
    merged = units.merge(df_prices, left_on=unit_id_col, right_on="idunidade", how="left")
    merged = merged.dropna(subset=["valor"])
    grouped = merged.groupby("Tipologia")["valor"].mean().round(2)
    return {str(tip): float(valor) for tip, valor in grouped.items()}
