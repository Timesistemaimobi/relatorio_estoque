from __future__ import annotations

import numpy as np


def parse_ptbr_money(value: object) -> float:
    if value is None:
        return np.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return np.nan
    cleaned = text.replace(".", "").replace(" ", "").replace("R$", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return np.nan
