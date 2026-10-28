# Amari Port Scanner

A small TCP connect port scanner written with the Python standard library only. It checks which ports accept connections on a host you are authorized to test, and reports the results as a table, JSON, or CSV.

> Only scan systems you own or have written permission to test. Scanning a public (non-private) address requires the explicit `--authorized` flag, and the scanner refuses without it.

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"          # or run directly with: python main.py
```

Requires Python 3.9 or newer.

## Usage

```bash
# List presets
python main.py presets

# Scan your own machine with the common preset
python main.py scan localhost --common

# Scan specific ports or ranges
python main.py scan 192.168.1.10 --ports 22,80,8000-8100

# Scan a named preset
python main.py scan 192.168.1.10 --preset web

# Export results
python main.py scan 192.168.1.10 --preset database --json out.json --csv out.csv

# Scan a public host you are authorized to test
python main.py scan example.com --ports 80,443 --authorized
```

Useful options:

| Option | Meaning |
|---|---|
| `--timeout SECONDS` | Per-port timeout (default 1.0) |
| `--threads N` | Concurrent connections (default 50, max 500) |
| `--show-closed` | Include closed and filtered ports in console output |

## How it classifies ports

- **open**: the TCP connection succeeded.
- **closed**: the host actively refused the connection.
- **filtered**: no answer before the timeout, or the host could not be reached. This can mean a firewall, but also a slow or offline host.

This is a connect scan. It completes the TCP handshake, so it is visible in the target's logs. It does not try to evade detection.

## Development

```bash
pip install -e ".[dev]"
python -m pytest
ruff check .
```

## Layout

```
main.py              # CLI
scanner/
  models.py          # PortResult, HostReport
  presets.py         # named port sets
  scanner.py         # TCP connect scanning with a thread pool
  validators.py      # port, host, timeout, and private-address checks
  output.py          # console, JSON, and CSV rendering
tests/                # unit and integration tests (uses loopback only)
```

## Licence

MIT. See `LICENSE`.
