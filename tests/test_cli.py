from main import main


def test_presets_lists_common(capsys):
    assert main(["presets"]) == 0
    assert "common" in capsys.readouterr().out


def test_refuses_public_target_without_authorization(capsys):
    assert main(["scan", "8.8.8.8", "--ports", "53"]) == 2
    assert "--authorized" in capsys.readouterr().err


def test_bad_port_spec_is_reported(capsys):
    assert main(["scan", "127.0.0.1", "--ports", "99999"]) == 2
    assert "out of range" in capsys.readouterr().err
