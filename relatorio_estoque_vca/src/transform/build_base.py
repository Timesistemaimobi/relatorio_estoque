from __future__ import annotations

import pandas as pd


def build_base(unidades_df: pd.DataFrame, bloqueios_df: pd.DataFrame) -> pd.DataFrame:
    unidades = unidades_df.copy()
    bloqueios = bloqueios_df.copy()

    bloqueio_cols = ["Empreendimento", "Etapa", "Bloco", "Unidade"]
    motivo_col = "Motivo do Bloqueio"
    if all(col in bloqueios.columns for col in bloqueio_cols):
        if "Data do Bloqueio" in bloqueios.columns:
            bloqueios["Data do Bloqueio"] = pd.to_datetime(
                bloqueios["Data do Bloqueio"], errors="coerce", dayfirst=True
            )
            bloqueios = bloqueios.sort_values("Data do Bloqueio")
        bloqueios = bloqueios.dropna(subset=[motivo_col])
        bloqueios[motivo_col] = bloqueios[motivo_col].astype(str).str.strip()
        bloqueios = bloqueios[bloqueios[motivo_col] != ""]
        bloqueios = bloqueios.drop_duplicates(subset=bloqueio_cols, keep="last")
    else:
        bloqueios = pd.DataFrame(columns=bloqueio_cols + [motivo_col])

    merged = unidades.merge(bloqueios[bloqueio_cols + [motivo_col]], on=bloqueio_cols, how="left")

    situacao = merged.get("Situação", "").astype(str).str.upper()
    status = pd.Series("DISPONÍVEL", index=merged.index)
    status = status.mask(situacao == "VENDIDA", "VENDIDA")
    status = status.mask(situacao == "RESERVADA", "RESERVADA")
    status = status.mask(merged[motivo_col].notna(), "BLOQUEADA")

    merged["STATUS_FINAL"] = status
    return merged
