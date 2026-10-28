"""Data structures for scan results."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

OPEN = "open"
CLOSED = "closed"
FILTERED = "filtered"


@dataclass(frozen=True)
class PortResult:
    """Outcome of probing one TCP port on one host."""

    host: str
    port: int
    state: str
    service: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class HostReport:
    """All port results for one host, plus timing."""

    host: str
    results: list[PortResult] = field(default_factory=list)
    duration_s: float = 0.0

    @property
    def open_ports(self) -> list[PortResult]:
        return [r for r in self.results if r.state == OPEN]

    def to_dict(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "duration_s": round(self.duration_s, 3),
            "open": [r.port for r in self.open_ports],
            "results": [r.to_dict() for r in self.results],
        }
