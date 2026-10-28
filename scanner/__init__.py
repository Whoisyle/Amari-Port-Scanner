"""Amari Port Scanner: a small, standard-library-only TCP connect scanner."""

from .models import HostReport, PortResult
from .presets import PRESETS
from .scanner import scan_host, scan_port
from .validators import ValidationError, is_private_target, parse_ports

__all__ = [
    "PRESETS",
    "HostReport",
    "PortResult",
    "ValidationError",
    "is_private_target",
    "parse_ports",
    "scan_host",
    "scan_port",
]
__version__ = "0.2.0"
