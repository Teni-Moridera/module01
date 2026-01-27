from __future__ import annotations

import csv
import io
import json
from typing import Tuple

from .validators import ValidationError


def export_report(report: dict, format: str) -> Tuple[str, str]:
    format = format.lower().strip()
    if format == "json":
        return json.dumps(report, ensure_ascii=False, indent=2), "application/json"
    if format == "csv":
        return _export_csv(report), "text/csv"
    if format == "txt":
        return _export_txt(report), "text/plain"

    raise ValidationError("Unsupported export format. Use json, csv, or txt.")


def _export_csv(report: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    for key, value in report.items():
        if isinstance(value, list):
            writer.writerow([key])
            if value:
                headers = list(value[0].keys())
                writer.writerow(headers)
                for item in value:
                    writer.writerow([item.get(h) for h in headers])
        else:
            writer.writerow([key, value])

    return output.getvalue()


def _export_txt(report: dict) -> str:
    lines = ["Report Summary"]
    for key, value in report.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append("  " + ", ".join(f"{k}={v}" for k, v in item.items()))
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)
