from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                return _as_list(parsed)
            except json.JSONDecodeError:
                pass
        return [item.strip() for item in text.split("|") if item.strip()]
    return [str(value).strip()]


def normalize_record(record: Dict[str, Any]) -> Tuple:
    required = ("id", "name", "department")
    missing = [key for key in required if not str(record.get(key, "")).strip()]
    if missing:
        raise ValueError(f"Service record missing required fields: {', '.join(missing)}")

    customer_types = _as_list(record.get("customer_types")) or ["citizen"]
    keywords = _as_list(record.get("keywords")) or [str(record["name"])]
    template = str(record.get("template") or "") or None
    outcome = str(record.get("outcome") or "service_outcome")

    return (
        str(record["id"]).strip(),
        str(record["name"]).strip(),
        str(record["department"]).strip(),
        customer_types,
        keywords,
        template,
        outcome,
    )


def load_records(source: str | Path) -> List[Tuple]:
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(path)

    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("services") or data.get("records") or []
        if not isinstance(data, list):
            raise ValueError("JSON service catalog must be a list or contain a services/records list")
        return [normalize_record(record) for record in data if isinstance(record, dict)]

    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            return [normalize_record(record) for record in reader]

    raise ValueError("Unsupported service catalog format; use JSON or CSV")


def merge_records(base: Iterable[Tuple], external: Iterable[Tuple]) -> List[Tuple]:
    merged: Dict[str, Tuple] = {str(row[0]): tuple(row) for row in base}
    for row in external:
        merged[str(row[0])] = tuple(row)
    return list(merged.values())
