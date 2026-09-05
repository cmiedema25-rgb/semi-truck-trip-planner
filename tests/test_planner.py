import os

import pytest

from truckplan.config import Settings
from truckplan.planner import build_vehicle, get_provider, plan_trip
from truckplan.providers.mock import MockProvider


def test_get_provider_defaults_to_mock(monkeypatch):
    monkeypatch.delenv("ORS_API_KEY", raising=False)
    settings = Settings(ors_api_key=None, truckplan_force_mock=False)
    assert isinstance(get_provider(settings), MockProvider)


def test_force_mock_even_with_key():
    settings = Settings(ors_api_key="fake", truckplan_force_mock=True)
    assert isinstance(get_provider(settings), MockProvider)


def test_plan_destination_only_offline():
    result = plan_trip(
        destination="Houston warehouse",
        provider=MockProvider(),
        settings=Settings(ors_api_key=None, truckplan_home_origin="Dallas yard"),
    )
    assert result.distance_m == 328500
    assert "Houston" in result.destination.label or result.destination.lat
    assert result.summary
    assert "decision support" in result.summary.lower() or "HGV" in result.summary or "mock" in result.summary.lower()


def test_plan_with_nl_hazmat():
    result = plan_trip(
        destination="to Houston warehouse from Dallas, hazmat",
        parse_nl=True,
        provider=MockProvider(),
        settings=Settings(ors_api_key=None),
    )
    assert result.vehicle.hazmat is True


def test_build_vehicle_overrides():
    v = build_vehicle(preset="dry_van", height_m=4.0, hazmat=True)
    assert v.height_m == 4.0
    assert v.hazmat is True


def test_missing_destination():
    with pytest.raises(ValueError, match="Destination"):
        plan_trip(destination="  ", provider=MockProvider())
