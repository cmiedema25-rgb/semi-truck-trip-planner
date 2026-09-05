"""OpenRouteService live geocoding + driving-hgv routing."""

from __future__ import annotations

import httpx

from truckplan.models import GeoPoint, RouteResult, RouteStep, VehicleProfile

ORS_GEOCODE = "https://api.openrouteservice.org/geocode/search"
ORS_DIRECTIONS = "https://api.openrouteservice.org/v2/directions/{profile}/json"


class OpenRouteServiceError(RuntimeError):
    pass


class OpenRouteServiceProvider:
    name = "openrouteservice"
    profile = "driving-hgv"

    def __init__(self, api_key: str, timeout: float = 30.0):
        if not api_key or not api_key.strip():
            raise ValueError("ORS API key is required for live routing")
        self.api_key = api_key.strip()
        self.timeout = timeout

    def _headers(self) -> dict:
        return {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def geocode(self, address: str) -> GeoPoint:
        params = {
            "api_key": self.api_key,
            "text": address,
            "size": 1,
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.get(ORS_GEOCODE, params=params)
            if resp.status_code >= 400:
                raise OpenRouteServiceError(
                    f"Geocode failed ({resp.status_code}): {resp.text[:300]}"
                )
            data = resp.json()
        features = data.get("features") or []
        if not features:
            raise OpenRouteServiceError(f"No geocode results for: {address!r}")
        feat = features[0]
        lon, lat = feat["geometry"]["coordinates"]
        props = feat.get("properties") or {}
        label = props.get("label") or address
        return GeoPoint(lat=float(lat), lon=float(lon), label=label)

    def route(
        self,
        origin: GeoPoint,
        destination: GeoPoint,
        vehicle: VehicleProfile,
    ) -> RouteResult:
        url = ORS_DIRECTIONS.format(profile=self.profile)
        body: dict = {
            "coordinates": [
                [origin.lon, origin.lat],
                [destination.lon, destination.lat],
            ],
            "instructions": True,
            "units": "m",
            "geometry": True,
            "options": vehicle.as_ors_options(),
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, headers=self._headers(), json=body)
            if resp.status_code >= 400:
                # Retry without strict vehicle restrictions if ORS rejects options
                body.pop("options", None)
                resp = client.post(url, headers=self._headers(), json=body)
                if resp.status_code >= 400:
                    raise OpenRouteServiceError(
                        f"Directions failed ({resp.status_code}): {resp.text[:400]}"
                    )
            data = resp.json()

        routes = data.get("routes") or []
        if not routes:
            raise OpenRouteServiceError("ORS returned no routes")
        route = routes[0]
        summary = route.get("summary") or {}
        distance_m = float(summary.get("distance") or 0)
        duration_s = float(summary.get("duration") or 0)

        steps: list[RouteStep] = []
        for segment in route.get("segments") or []:
            for step in segment.get("steps") or []:
                steps.append(
                    RouteStep(
                        instruction=step.get("instruction") or "",
                        distance_m=float(step.get("distance") or 0),
                        duration_s=float(step.get("duration") or 0),
                        name=step.get("name") or "",
                    )
                )

        google_url = (
            f"https://www.google.com/maps/dir/{origin.lat},{origin.lon}/"
            f"{destination.lat},{destination.lon}"
        )
        text_summary = (
            f"HGV route ({self.profile}) from {origin.label} to {destination.label}: "
            f"{distance_m / 1609.344:.1f} mi, ETA {int(duration_s // 3600)}h "
            f"{int((duration_s % 3600) // 60)}m. "
            f"Vehicle: {vehicle.name} "
            f"(H={vehicle.height_m}m W={vehicle.width_m}m L={vehicle.length_m}m "
            f"Wgt={vehicle.weight_t}t axles={vehicle.axles} hazmat={vehicle.hazmat})."
        )
        return RouteResult(
            origin=origin,
            destination=destination,
            distance_m=distance_m,
            duration_s=duration_s,
            steps=steps,
            vehicle=vehicle,
            provider=self.name,
            profile=self.profile,
            summary=text_summary,
            map_url=google_url,
            geometry=None,
        )
