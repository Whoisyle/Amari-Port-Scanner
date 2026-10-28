import socket

from scanner import scan_host, scan_port
from scanner.models import CLOSED, FILTERED, OPEN
from scanner.output import to_csv, to_json


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_open_port_detected():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        port = listener.getsockname()[1]
        assert scan_port("127.0.0.1", port, timeout=1.0).state == OPEN


def test_closed_port_detected():
    assert scan_port("127.0.0.1", _free_port(), timeout=1.0).state == CLOSED


def test_unroutable_host_is_filtered_not_crash():
    result = scan_port("256.256.256.256", 80, timeout=0.2)
    assert result.state == FILTERED


def test_scan_host_returns_sorted_results_and_open_list():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        open_port = listener.getsockname()[1]
        closed_port = _free_port()
        report = scan_host("127.0.0.1", sorted([open_port, closed_port]), timeout=1.0, threads=4)
    assert [r.port for r in report.results] == sorted([open_port, closed_port])
    assert open_port in [r.port for r in report.open_ports]


def test_json_and_csv_output_shape():
    report = scan_host("127.0.0.1", [_free_port()], timeout=0.5, threads=1)
    assert '"host": "127.0.0.1"' in to_json(report)
    assert to_csv(report).splitlines()[0] == "host,port,state,service"
