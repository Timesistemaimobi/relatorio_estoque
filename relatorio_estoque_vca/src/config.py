from __future__ import annotations

from datetime import date
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CVCRM_EMAIL = os.environ.get("CVCRM_EMAIL", "")
CVCRM_TOKEN = os.environ.get("CVCRM_TOKEN", "")

OUTPUT_FILE = OUTPUT_DIR / f"RELATÓRIO - ESTOQUE DE UNIDADES {date.today().strftime('%Y-%m-%d')}.xlsx"
