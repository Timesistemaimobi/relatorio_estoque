from __future__ import annotations

import pandas as pd

from .apis.cvcrm import fetch_precos_por_unidade
from .config import CVCRM_EMAIL, CVCRM_TOKEN, DATA_DIR, OUTPUT_FILE, TEMPLATE_DIR
from .excel.styles import load_styles
from .excel.writer import write_report
from .transform.aggregates import aggregate_for_report
from .transform.build_base import build_base
from .transform.prices import compute_avg_price_by_tipology
from .utils.columns import guess_col


def _require_column(df: pd.DataFrame, candidates: list[str], label: str) -> str:
    col = guess_col(df, candidates)
    if not col:
        cols = ", ".join(df.columns)
        raise ValueError(f"Não foi possível localizar coluna {label}. Colunas encontradas: {cols}")
    return col


def main() -> None:
    unidades = pd.read_csv(DATA_DIR / "unidade.csv", sep=";")
    bloqueios = pd.read_csv(DATA_DIR / "bloqueio.csv", sep=";")

    emp_id_col = _require_column(
        unidades,
        ["ID. Empreendimento", "ID Empreendimento", "IdEmpreendimento", "idempreendimento"],
        "ID do Empreendimento",
    )
    unit_id_col = _require_column(
        unidades,
        ["Código interno da unidade", "Codigo interno da unidade", "ID Unidade", "IdUnidade", "idunidade"],
        "ID da Unidade",
    )

    base_df = build_base(unidades, bloqueios)

    aggregates_by_emp: dict[str, dict] = {}
    avg_prices_by_emp: dict[str, dict] = {}
    price_cache: dict[int, pd.DataFrame] = {}

    for empreendimento, df_emp in base_df.groupby("Empreendimento"):
        emp_id = int(pd.to_numeric(df_emp[emp_id_col], errors="coerce").iloc[0])
        if emp_id not in price_cache:
            price_cache[emp_id] = fetch_precos_por_unidade(emp_id, CVCRM_EMAIL, CVCRM_TOKEN)
        df_prices = price_cache[emp_id]

        avg_prices_by_emp[empreendimento] = compute_avg_price_by_tipology(
            df_emp, df_prices, unit_id_col
        )
        aggregates_by_emp[empreendimento] = aggregate_for_report(df_emp)

    template_styles, col_widths = load_styles(str(TEMPLATE_DIR / "RELATORIO_TEMPLATE.xlsx"))
    write_report(str(OUTPUT_FILE), template_styles, col_widths, aggregates_by_emp, avg_prices_by_emp)


if __name__ == "__main__":
    main()
