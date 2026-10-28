"""Input validation for hosts, ports, and scan settings."""

from __future__ import annotations

import ipaddress
import re

MAX_PORT = 65535
_HOSTNAME_RE = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$")


class ValidationError(ValueError):
    """Raised when user input is invalid."""


def parse_ports(spec: str) -> list[int]:
    """Parse '22,80,8000-8100' into a sorted, de-duplicated list of ports."""
    ports: set[int] = set()
    for raw in spec.split(","):
        part = raw.strip()
        if not part:
            continue
        if "-" in part:
            start_s, _, end_s = part.partition("-")
            start, end = _to_port(start_s), _to_port(end_s)
            if start > end:
                raise ValidationError(f"Port range {part!r} is reversed")
            ports.update(range(start, end + 1))
        else:
            ports.add(_to_port(part))
    if not ports:
        raise ValidationError("No ports given")
    return sorted(ports)


def _to_port(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise ValidationError(f"Not a port number: {text!r}") from exc
    if not 1 <= value <= MAX_PORT:
        raise ValidationError(f"Port out of range 1-{MAX_PORT}: {value}")
    return value


def validate_host(host: str) -> str:
    """Accept an IP address or a DNS hostname; return it stripped."""
    candidate = host.strip()
    try:
        ipaddress.ip_address(candidate)
        return candidate
    except ValueError:
        pass
    if _HOSTNAME_RE.match(candidate):
        return candidate
    raise ValidationError(f"Not a valid IP address or hostname: {host!r}")


def is_private_target(host: str) -> bool:
    """True if the host is loopback, link-local, or private (RFC 1918 / ULA).

    Hostnames are not resolved here, so they are treated as non-private.
    """
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        return host.lower() in {"localhost"}
    return addr.is_loopback or addr.is_private or addr.is_link_local


def validate_timeout(value: float) -> float:
    if not 0.05 <= value <= 60:
        raise ValidationError("Timeout must be between 0.05 and 60 seconds")
    return value


def validate_threads(value: int) -> int:
    if not 1 <= value <= 500:
        raise ValidationError("Threads must be between 1 and 500")
    return value
