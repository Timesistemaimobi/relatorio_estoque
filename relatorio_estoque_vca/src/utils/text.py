from __future__ import annotations


def normalize_key(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().upper().split())
