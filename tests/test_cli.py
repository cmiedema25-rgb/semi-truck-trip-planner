from typer.testing import CliRunner

from truckplan.cli import app

runner = CliRunner()


def test_version():
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0
    assert "truckplan" in r.stdout


def test_parse():
    r = runner.invoke(app, ["parse", "to Houston from Dallas, hazmat"])
    assert r.exit_code == 0
    assert "Houston" in r.stdout


def test_route_mock_json(monkeypatch):
    monkeypatch.setenv("TRUCKPLAN_FORCE_MOCK", "1")
    monkeypatch.delenv("ORS_API_KEY", raising=False)
    # Reload settings cache
    from truckplan.config import get_settings

    get_settings.cache_clear()
    r = runner.invoke(app, ["route", "--to", "Houston warehouse", "--from", "Dallas yard", "--json"])
    assert r.exit_code == 0
    assert "328500" in r.stdout or '"distance_m": 328500' in r.stdout
    get_settings.cache_clear()
