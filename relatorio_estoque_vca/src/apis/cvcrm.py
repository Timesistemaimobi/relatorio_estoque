from __future__ import annotations

import time
from typing import List

import pandas as pd
import requests

from ..utils.money import parse_ptbr_money

API_URL = "https://vca.cvcrm.com.br/api/v1/cadastros/empreendimentos/{emp_id}/tabelasdepreco/detalhada"


def _extract_valor(dado: dict) -> float:
    for serie in dado.get("series", []) or []:
        if serie.get("nome") == "VALOR DO IMOVEL":
            try:
                return float(serie.get("valor"))
            except (TypeError, ValueError):
                break
    return parse_ptbr_money(dado.get("valor_total"))


def fetch_precos_por_unidade(emp_id: int, email: str, token: str, retries: int = 3) -> pd.DataFrame:
    headers = {
        "accept": "application/json",
        "email": email,
        "token": token,
    }
    params = {"tabelasemjson": "true"}
    last_error: Exception | None = None

    for attempt in range(retries):
        try:
            response = requests.get(API_URL.format(emp_id=emp_id), headers=headers, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()
            if payload.get("codigo") != 200:
                raise ValueError(f"Resposta inesperada da API CVCRM: {payload.get('codigo')}")
            rows: List[dict] = []
            for tabela in payload.get("tabelas", []) or []:
                for dado in tabela.get("dados", []) or []:
                    if "idunidade" not in dado:
                        continue
                    rows.append({
                        "idunidade": dado.get("idunidade"),
                        "valor": _extract_valor(dado),
                    })
            df = pd.DataFrame(rows)
            df["idunidade"] = pd.to_numeric(df["idunidade"], errors="coerce")
            return df.dropna(subset=["idunidade"])
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(1 + attempt)
                continue
            raise exc
    if last_error:
        raise last_error
    return pd.DataFrame(columns=["idunidade", "valor"])
