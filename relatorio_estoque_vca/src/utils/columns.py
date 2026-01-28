from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd


def guess_col(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    lowered = {col.lower(): col for col in df.columns}
    for candidate in candidates:
        key = candidate.lower()
        if key in lowered:
            return lowered[key]
    return None
