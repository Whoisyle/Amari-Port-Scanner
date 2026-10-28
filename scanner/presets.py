"""Named port sets for common service categories."""

from __future__ import annotations

PRESETS: dict[str, list[int]] = {
    "common": [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389, 5900, 8080],
    "web": [80, 443, 8000, 8080, 8443],
    "database": [1433, 1521, 3306, 5432, 6379, 27017],
    "remote": [22, 23, 3389, 5900, 5985, 5986],
    "mail": [25, 110, 143, 465, 587, 993, 995],
    "file": [20, 21, 139, 445, 2049],
}
