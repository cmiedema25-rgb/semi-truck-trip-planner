from truckplan.models import VehicleProfile
from truckplan.providers.mock import DALLAS_YARD, HOUSTON_WH, MockProvider, sample_trip_dict


def test_geocode_known():
    p = MockProvider()
    d = p.geocode("Dallas yard")
    assert abs(d.lat - DALLAS_YARD.lat) < 0.01
    h = p.geocode("Houston warehouse")
    assert abs(h.lat - HOUSTON_WH.lat) < 0.01


def test_route_sample_numbers():
    p = MockProvider()
    r = p.route(DALLAS_YARD, HOUSTON_WH, VehicleProfile())
    assert r.provider == "mock"
    assert r.distance_m == 328500  # sum of sample steps
    assert r.duration_s == 14100
    assert abs(r.distance_mi - 204.1) < 0.2
    assert r.format_eta() == "3h 55m"
    assert len(r.steps) == 4
    assert "google.com/maps" in r.map_url


def test_sample_trip_dict():
    data = sample_trip_dict()
    assert data["distance_m"] == 328500
    assert data["provider"] == "mock"
