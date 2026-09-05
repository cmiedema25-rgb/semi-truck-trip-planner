"""Offline mock provider — retained long-haul lane: LA → Chicago (~2,010 mi)."""

from __future__ import annotations

from truckplan.models import GeoPoint, RouteResult, RouteStep, VehicleProfile

# Ontario / LA basin terminal → Chicago warehouse (canonical ~2000-mile demo)
LA_TERMINAL = GeoPoint(
    lat=34.0633,
    lon=-117.6509,
    label="1200 Commerce Dr, Ontario, CA 91761",
)
CHICAGO_WH = GeoPoint(
    lat=41.8369,
    lon=-87.6847,
    label="4400 S Pulaski Rd, Chicago, IL 60632",
)

_SAMPLE_STEPS = [
    RouteStep(
        instruction="Depart Ontario CA terminal; merge onto I-15 N toward Barstow / Las Vegas",
        distance_m=450000,
        duration_s=18316,
        name="I-15 N",
    ),
    RouteStep(
        instruction="Continue I-15 N through Utah; join I-70 E toward Denver corridor",
        distance_m=820000,
        duration_s=33341,
        name="I-15 N / I-70 E",
    ),
    RouteStep(
        instruction="I-70 E / I-76 E into Nebraska; I-80 E toward Omaha / Des Moines",
        distance_m=980000,
        duration_s=39860,
        name="I-70 E / I-80 E",
    ),
    RouteStep(
        instruction="I-80 E across Iowa; I-55 N / I-294 toward Chicago metro",
        distance_m=900000,
        duration_s=36632,
        name="I-80 E / I-55 N",
    ),
    RouteStep(
        instruction="Local approaches to Pulaski Rd warehouse — arrive destination",
        distance_m=84781,
        duration_s=3415,
        name="Chicago local",
    ),
]
# 450+820+980+900+84.781 = 3234.781 km? meters: 3,234,781 ≈ 2010.0 mi


_KNOWN: list[tuple[str, GeoPoint]] = [
    ("ontario", LA_TERMINAL),
    ("los angeles", LA_TERMINAL),
    ("la ", LA_TERMINAL),
    ("california", LA_TERMINAL),
    ("commerce dr", LA_TERMINAL),
    ("chicago", CHICAGO_WH),
    ("pulaski", CHICAGO_WH),
    ("illinois", CHICAGO_WH),
]


class MockProvider:
    """Deterministic long-haul provider for CI / offline demos — no network."""

    name = "mock"

    def geocode(self, address: str) -> GeoPoint:
        text = address.lower().strip()
        for key, point in _KNOWN:
            if key in text:
                return GeoPoint(lat=point.lat, lon=point.lon, label=address)
        if any(k in text for k in ("origin", "yard", "terminal", "home")):
            return GeoPoint(lat=LA_TERMINAL.lat, lon=LA_TERMINAL.lon, label=address)
        # Default unknown destinations toward Chicago for destination-only demos
        return GeoPoint(lat=CHICAGO_WH.lat, lon=CHICAGO_WH.lon, label=address)

    def route(
        self,
        origin: GeoPoint,
        destination: GeoPoint,
        vehicle: VehicleProfile,
    ) -> RouteResult:
        distance_m = float(sum(s.distance_m for s in _SAMPLE_STEPS))
        duration_s = float(sum(s.duration_s for s in _SAMPLE_STEPS))
        google_url = (
            f"https://www.google.com/maps/dir/{origin.lat},{origin.lon}/"
            f"{destination.lat},{destination.lon}"
        )
        summary = (
            f"Mock long-haul HGV route from {origin.label or 'origin'} to "
            f"{destination.label or 'destination'}: "
            f"{distance_m / 1609.344:.0f} mi, ~{duration_s / 3600:.1f} driving hours "
            f"(vehicle: {vehicle.name}, hazmat={vehicle.hazmat})."
        )
        return RouteResult(
            origin=origin,
            destination=destination,
            distance_m=distance_m,
            duration_s=duration_s,
            steps=list(_SAMPLE_STEPS),
            vehicle=vehicle,
            provider=self.name,
            profile="driving-hgv (mock)",
            summary=summary,
            map_url=google_url,
            geometry=[
                [origin.lon, origin.lat],
                [-115.1, 36.1],
                [-105.0, 39.7],
                [-96.0, 41.3],
                [destination.lon, destination.lat],
            ],
        )


def sample_trip_dict() -> dict:
    provider = MockProvider()
    result = provider.route(LA_TERMINAL, CHICAGO_WH, VehicleProfile())
    return result.model_dump()
