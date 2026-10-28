"""TCP connect scanning with a bounded thread pool."""

from __future__ import annotations

import socket
import time
from concurrent.futures import ThreadPoolExecutor

from .models import CLOSED, FILTERED, OPEN, HostReport, PortResult
from .validators import validate_host, validate_threads, validate_timeout

_SERVICES = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns", 80: "http",
    110: "pop3", 143: "imap", 443: "https", 445: "smb", 3306: "mysql",
    3389: "rdp", 5432: "postgresql", 5900: "vnc", 6379: "redis", 8080: "http-alt",
}


def scan_port(host: str, port: int, timeout: float = 1.0) -> PortResult:
    """Attempt a TCP connection to host:port and classify the outcome."""
    service = _SERVICES.get(port, "")
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return PortResult(host, port, OPEN, service)
    except ConnectionRefusedError:
        return PortResult(host, port, CLOSED, service)
    except socket.timeout:
        return PortResult(host, port, FILTERED, service)
    except OSError:
        # Unreachable network, name resolution failure, etc.
        return PortResult(host, port, FILTERED, service)


def scan_host(
    host: str,
    ports: list[int],
    timeout: float = 1.0,
    threads: int = 50,
) -> HostReport:
    """Scan many ports on one host concurrently. Results are sorted by port."""
    host = validate_host(host)
    timeout = validate_timeout(timeout)
    threads = validate_threads(threads)

    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=threads) as pool:
        results = list(pool.map(lambda p: scan_port(host, p, timeout), ports))
    return HostReport(host=host, results=sorted(results, key=lambda r: r.port), duration_s=time.monotonic() - started)
