"""Domain models for vehicle constraints and route results."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from truckplan.roi import TripRoi


class VehicleProfile(BaseModel):
    """Physical / regulatory constraints for a heavy goods vehicle."""

    name: str = "Class-8 53' dry van"
    height_m: float = Field(default=4.11, description="Overall height in meters (~13'6\")")
    width_m: float = Field(default=2.59, description="Overall width in meters (~8'6\")")
    length_m: float = Field(default=22.86, description="Overall length in meters (~75' combo)")
    weight_t: float = Field(default=36.29, description="Gross weight in metric tons (~80,000 lb)")
    axles: int = Field(default=5, ge=2, le=12)
    hazmat: bool = False

    def as_ors_options(self) -> dict:
        """Map to OpenRouteService HGV profile options."""
        opts: dict = {
            "profile_params": {
                "restrictions": {
                    "height": self.height_m,
                    "width": self.width_m,
                    "length": self.length_m,
                    "weight": self.weight_t,
                    "axlecount": self.axles,
                }
            }
        }
        if self.hazmat:
            opts["profile_params"]["restrictions"]["hazmat"] = True
        return opts


# Typical Class-8 dry-van defaults (US interstate limits; verify locally).
CLASS8_DRY_VAN = VehicleProfile()

CLASS8_REEFER = VehicleProfile(
    name="Class-8 53' reefer",
    height_m=4.11,
    width_m=2.59,
    length_m=22.86,
    weight_t=36.29,
    axles=5,
)

FLATBED = VehicleProfile(
    name="Class-8 flatbed",
    height_m=4.11,
    width_m=2.59,
    length_m=22.86,
    weight_t=36.29,
    axles=5,
)

PRESETS: dict[str, VehicleProfile] = {
    "dry_van": CLASS8_DRY_VAN,
    "reefer": CLASS8_REEFER,
    "flatbed": FLATBED,
}


class GeoPoint(BaseModel):
    lat: float
    lon: float
    label: str = ""


class RouteStep(BaseModel):
    instruction: str
    distance_m: float
    duration_s: float
    name: str = ""


class RouteResult(BaseModel):
    """Normalized route payload returned by any provider."""

    origin: GeoPoint
    destination: GeoPoint
    distance_m: float
    duration_s: float
    steps: list[RouteStep] = Field(default_factory=list)
    vehicle: VehicleProfile
    provider: str
    profile: str = "driving-hgv"
    summary: str = ""
    map_url: str = ""
    geometry: Optional[list[list[float]]] = None  # [[lon, lat], ...]
    roi: Optional[dict] = None  # TripRoi.model_dump() — illustrative scenario math

    @property
    def distance_mi(self) -> float:
        return self.distance_m / 1609.344

    @property
    def duration_hours(self) -> float:
        return self.duration_s / 3600.0

    def format_eta(self) -> str:
        hours = int(self.duration_s // 3600)
        mins = int((self.duration_s % 3600) // 60)
        if hours:
            return f"{hours}h {mins}m"
        return f"{mins}m"
