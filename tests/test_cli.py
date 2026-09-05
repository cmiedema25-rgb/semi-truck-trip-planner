from typer.testing import CliRunner

from truckplan.cli import app

runner = CliRunner()


def test_version():
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0
    assert "truckplan" in r.stdout


def test_parse():
    r = runner.invoke(app, ["parse", "to Chicago from Ontario, hazmat"])
    assert r.exit_code == 0
    assert "Chicago" in r.stdout


def test_route_mock_json(monkeypatch):
    monkeypatch.setenv("TRUCKPLAN_FORCE_MOCK", "1")
    monkeypatch.delenv("ORS_API_KEY", raising=False)
    from truckplan.config import get_settings

    get_settings.cache_clear()
    r = runner.invoke(
        app,
        ["route", "--to", "Chicago warehouse", "--from", "Ontario CA terminal", "--json"],
    )
    assert r.exit_code == 0
    assert "3234781" in r.stdout
    get_settings.cache_clear()
