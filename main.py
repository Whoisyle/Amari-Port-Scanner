#!/usr/bin/env python3
"""Command-line interface for the Amari Port Scanner.

Only scan systems you own or have written permission to test. Scanning public
(non-private) addresses requires the explicit --authorized flag.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scanner import PRESETS, ValidationError, is_private_target, parse_ports
from scanner.output import to_console, to_csv, to_json
from scanner.scanner import scan_host
from scanner.validators import validate_host


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="amari-portscan", description="Authorized TCP connect port scanner.")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Scan a host for open TCP ports")
    scan.add_argument("host", help="IP address or hostname")
    group = scan.add_mutually_exclusive_group()
    group.add_argument("--ports", help="Ports, e.g. 22,80,8000-8100 (default: common preset)")
    group.add_argument("--preset", choices=sorted(PRESETS), help="Use a named port preset")
    group.add_argument("--common", action="store_true", help="Shortcut for --preset common")
    scan.add_argument("--timeout", type=float, default=1.0, help="Per-port timeout in seconds (default 1.0)")
    scan.add_argument("--threads", type=int, default=50, help="Concurrent connections (default 50)")
    scan.add_argument("--show-closed", action="store_true", help="Include closed and filtered ports in console output")
    scan.add_argument("--authorized", action="store_true", help="Confirm you have permission to scan a non-private target")
    scan.add_argument("--json", metavar="FILE", help="Write results as JSON")
    scan.add_argument("--csv", metavar="FILE", help="Write results as CSV")

    sub.add_parser("presets", help="List port presets")
    return parser


def _resolve_ports(args: argparse.Namespace) -> list[int]:
    if args.ports:
        return parse_ports(args.ports)
    name = args.preset or "common"
    return list(PRESETS[name])


def cmd_scan(args: argparse.Namespace) -> int:
    host = validate_host(args.host)
    if not is_private_target(host) and not args.authorized:
        print(
            f"Refusing to scan {host}: it is not a private or loopback address.\n"
            "If you have written permission to test it, re-run with --authorized.",
            file=sys.stderr,
        )
        return 2

    ports = _resolve_ports(args)
    report = scan_host(host, ports, timeout=args.timeout, threads=args.threads)
    print(to_console(report, show_closed=args.show_closed))

    if args.json:
        Path(args.json).write_text(to_json(report), encoding="utf-8")
        print(f"JSON written to {args.json}")
    if args.csv:
        Path(args.csv).write_text(to_csv(report), encoding="utf-8")
        print(f"CSV written to {args.csv}")
    return 0


def cmd_presets(_: argparse.Namespace) -> int:
    for name, ports in sorted(PRESETS.items()):
        print(f"{name:<10} {', '.join(str(p) for p in ports)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "scan":
            return cmd_scan(args)
        return cmd_presets(args)
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
