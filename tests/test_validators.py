import pytest

from scanner import ValidationError, is_private_target, parse_ports
from scanner.validators import validate_host


def test_parse_single_and_range_sorted_unique():
    assert parse_ports("80,22,20-22") == [20, 21, 22, 80]


@pytest.mark.parametrize("spec", ["", "0", "65536", "100-10", "abc"])
def test_parse_ports_rejects_bad_input(spec):
    with pytest.raises(ValidationError):
        parse_ports(spec)


@pytest.mark.parametrize("host", ["127.0.0.1", "10.0.0.5", "192.168.1.1", "localhost", "169.254.1.1"])
def test_private_targets(host):
    assert is_private_target(host)


@pytest.mark.parametrize("host", ["8.8.8.8", "example.com"])
def test_public_targets(host):
    assert not is_private_target(host)


def test_validate_host_accepts_ip_and_hostname():
    assert validate_host(" 127.0.0.1 ") == "127.0.0.1"
    assert validate_host("example.com") == "example.com"


@pytest.mark.parametrize("host", ["bad host", "-x", "a" * 300])
def test_validate_host_rejects_garbage(host):
    with pytest.raises(ValidationError):
        validate_host(host)
