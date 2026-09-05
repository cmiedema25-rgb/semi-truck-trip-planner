"""Offline mock provider with a fixed Dallas → Houston sample route."""

from __future__ import annotations

from truckplan.models import GeoPoint, RouteResult, RouteStep, VehicleProfile

# Approximate coords for demo addresses
DALLAS_YARD = GeoPoint(lat=32.7767, lon=-96.7970, label="1234 Trucking Way, Dallas, TX 75201")
HOUSTON_WH = GeoPoint(lat=29.7604, lon=-95.3698, label="5600 Warehouse Blvd, Houston, TX 77092")

# Known address fragments → mock points (case-insensitive contains)
_KNOWN: list[tuple[str, GeoPoint]] = [
    ("dallas", DALLAS_YARD),
    ("trucking way", DALLAS_YARD),
    ("houston", HOUSTON_WH),
    ("warehouse", HOUSTON_WH),
]

_SAMPLE_STEPS = [
    RouteStep(
        instruction="Head south on I-45 toward Houston",
        distance_m=180000,
        duration_s=7200,
        name="I-45 S",
    ),
    RouteStep(
        instruction="Continue on I-45 South through Huntsville",
        distance_m=120000,
        duration_s=4500,
        name="I-45 S",
    ),
    RouteStep(
        instruction="Take exit toward US-290 / Warehouse district",
        distance_m=25000,
        duration_s=1800,
        name="US-290",
    ),
    RouteStep(
        instruction="Arrive at destination on Warehouse Blvd",
        distance_m=3500,
        duration_s=600,
        name="Warehouse Blvd",
    ),
]


class MockProvider:
    """Deterministic provider for CI / offline demos — no network calls."""

    name = "mock"

    def geocode(self, address: str) -> GeoPoint:
        text = address.lower().strip()
        for key, point in _KNOWN:
            if key in text:
                return GeoPoint(lat=point.lat, lon=point.lon, label=address)
        # Default: treat unknown as near Houston (destination-only demos)
        if "origin" in text or "yard" in text or "terminal" in text:
            return GeoPoint(lat=DALLAS_YARD.lat, lon=DALLAS_YARD.lon, label=address)
        return GeoPoint(lat=HOUSTON_WH.lat, lon=HOUSTON_WH.lon, label=address)

    def route(
        self,
        origin: GeoPoint,
        destination: GeoPoint,
        vehicle: VehicleProfile,
    ) -> RouteResult:
        distance_m = sum(s.distance_m for s in _SAMPLE_STEPS)
        duration_s = sum(s.duration_s for s in _SAMPLE_STEPS)
        map_url = (
            f"https://www.openstreetmap.org/directions?"
            f"engine=fossgis_osrm_car&route={origin.lat}%2C{origin.lon}"
            f"%3B{destination.lat}%2C{destination.lon}"
        )
        google_url = (
            f"https://www.google.com/maps/dir/{origin.lat},{origin.lon}/"
            f"{destination.lat},{destination.lon}"
        )
        summary = (
            f"Mock HGV route from {origin.label or 'origin'} to "
            f"{destination.label or 'destination'}: "
            f"{distance_m / 1609.344:.1f} mi, ~{int(duration_s // 3600)}h "
            f"{int((duration_s % 3600) // 60)}m "
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
                [-96.5, 31.5],
                [-95.8, 30.5],
                [destination.lon, destination.lat],
            ],
        )


def sample_trip_dict() -> dict:
    """Serialize the canonical mock trip for evidence/examples."""
    provider = MockProvider()
    origin = DALLAS_YARD
    dest = HOUSTON_WH
    vehicle = VehicleProfile()
    result = provider.route(origin, dest, vehicle)
    return result.model_dump()
