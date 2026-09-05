from truckplan.models import VehicleProfile
from truckplan.providers.mock import CHICAGO_WH, LA_TERMINAL, MockProvider, sample_trip_dict


def test_geocode_known():
    p = MockProvider()
    o = p.geocode("Ontario CA terminal")
    assert abs(o.lat - LA_TERMINAL.lat) < 0.01
    d = p.geocode("Chicago warehouse")
    assert abs(d.lat - CHICAGO_WH.lat) < 0.01


def test_route_long_haul_numbers():
    p = MockProvider()
    r = p.route(LA_TERMINAL, CHICAGO_WH, VehicleProfile())
    assert r.provider == "mock"
    assert r.distance_m == 3234781
    assert r.duration_s == 131564
    assert abs(r.distance_mi - 2010.0) < 0.5
    assert r.format_eta().startswith("36h")
    assert len(r.steps) == 5
    assert "google.com/maps" in r.map_url


def test_sample_trip_dict():
    data = sample_trip_dict()
    assert data["distance_m"] == 3234781
    assert data["provider"] == "mock"
