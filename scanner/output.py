"""Render scan reports as console tables, JSON, or CSV."""

from __future__ import annotations

import csv
import io
import json

from .models import HostReport


def to_console(report: HostReport, show_closed: bool = False) -> str:
    rows = [r for r in report.results if show_closed or r.state == "open"]
    lines = [f"Scan report for {report.host} ({report.duration_s:.2f}s)"]
    if not rows:
        lines.append("No open ports found." if not show_closed else "No ports probed.")
        return "\n".join(lines)
    lines.append(f"{'PORT':>6}  {'STATE':<9}  SERVICE")
    for r in rows:
        lines.append(f"{r.port:>6}  {r.state:<9}  {r.service or '-'}")
    return "\n".join(lines)


def to_json(report: HostReport) -> str:
    return json.dumps(report.to_dict(), indent=2)


def to_csv(report: HostReport) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["host", "port", "state", "service"])
    for r in report.results:
        writer.writerow([r.host, r.port, r.state, r.service])
    return buffer.getvalue()
