from __future__ import annotations

from typing import Dict, List, Tuple

import pandas as pd


AggregatedBlock = Tuple[str, int, List[Tuple[str, int]]]


def _tipologia_counts(df: pd.DataFrame) -> List[Tuple[str, int]]:
    counts = df["Tipologia"].value_counts(dropna=False)
    return [(str(tip), int(qtd)) for tip, qtd in counts.items()]


def aggregate_for_report(df_emp: pd.DataFrame) -> Dict[str, dict]:
    result: Dict[str, dict] = {}
    for etapa, df_etapa in df_emp.groupby("Etapa"):
        bloqueios_list: List[AggregatedBlock] = []
        status_list: List[AggregatedBlock] = []

        bloqueadas = df_etapa[df_etapa["STATUS_FINAL"] == "BLOQUEADA"]
        if not bloqueadas.empty:
            for motivo, df_motivo in bloqueadas.groupby("Motivo do Bloqueio"):
                tip_counts = _tipologia_counts(df_motivo)
                total = int(df_motivo.shape[0])
                bloqueios_list.append((str(motivo), total, tip_counts))

        for status in ["DISPONÍVEL", "RESERVADA", "VENDIDA"]:
            df_status = df_etapa[df_etapa["STATUS_FINAL"] == status]
            if df_status.empty:
                continue
            tip_counts = _tipologia_counts(df_status)
            total = int(df_status.shape[0])
            status_list.append((status, total, tip_counts))

        result[str(etapa)] = {
            "bloqueios": bloqueios_list,
            "status": status_list,
            "total": int(df_etapa.shape[0]),
        }
    return result
