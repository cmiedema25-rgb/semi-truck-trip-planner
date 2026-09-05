"""Trip planning orchestration: geocode → HGV route → long-haul HOS → ROI."""

from __future__ import annotations

from typing import Optional

from truckplan.config import Settings, get_settings
from truckplan.hos import DEFAULT_HOS, plan_long_haul
from truckplan.models import PRESETS, RouteResult, VehicleProfile
from truckplan.nlp import maybe_llm_polish, parse_trip_text, template_summary
from truckplan.providers.base import Provider
from truckplan.providers.mock import MockProvider
from truckplan.providers.ors import OpenRouteServiceProvider
from truckplan.roi import RoiAssumptions, compute_roi


def get_provider(settings: Optional[Settings] = None) -> Provider:
    settings = settings or get_settings()
    if settings.use_live_ors:
        return OpenRouteServiceProvider(settings.ors_api_key)  # type: ignore[arg-type]
    return MockProvider()


def build_vehicle(
    preset: str = "dry_van",
    height_m: Optional[float] = None,
    width_m: Optional[float] = None,
    length_m: Optional[float] = None,
    weight_t: Optional[float] = None,
    axles: Optional[int] = None,
    hazmat: bool = False,
) -> VehicleProfile:
    base = PRESETS.get(preset, PRESETS["dry_van"]).model_copy(deep=True)
    if height_m is not None:
        base.height_m = height_m
    if width_m is not None:
        base.width_m = width_m
    if length_m is not None:
        base.length_m = length_m
    if weight_t is not None:
        base.weight_t = weight_t
    if axles is not None:
        base.axles = axles
    base.hazmat = hazmat or base.hazmat
    return base


def plan_trip(
    destination: str,
    origin: Optional[str] = None,
    *,
    preset: str = "dry_van",
    height_m: Optional[float] = None,
    width_m: Optional[float] = None,
    length_m: Optional[float] = None,
    weight_t: Optional[float] = None,
    axles: Optional[int] = None,
    hazmat: bool = False,
    provider: Optional[Provider] = None,
    settings: Optional[Settings] = None,
    parse_nl: bool = False,
) -> RouteResult:
    """Plan an HGV-oriented long-haul route. Destination required; origin defaults to home terminal."""
    settings = settings or get_settings()
    provider = provider or get_provider(settings)

    dest_text = destination
    origin_text = origin
    if parse_nl:
        parsed = parse_trip_text(destination if not origin else f"from {origin} to {destination}")
        if parsed.destination:
            dest_text = parsed.destination
        if parsed.origin and not origin_text:
            origin_text = parsed.origin
        hazmat = hazmat or parsed.hazmat

    if not dest_text or not str(dest_text).strip():
        raise ValueError("Destination address is required")

    origin_text = (origin_text or settings.truckplan_home_origin).strip()
    vehicle = build_vehicle(
        preset=preset,
        height_m=height_m,
        width_m=width_m,
        length_m=length_m,
        weight_t=weight_t,
        axles=axles,
        hazmat=hazmat,
    )

    origin_pt = provider.geocode(origin_text)
    dest_pt = provider.geocode(dest_text)
    result = provider.route(origin_pt, dest_pt, vehicle)

    summary = template_summary(
        origin_label=origin_pt.label or origin_text,
        dest_label=dest_pt.label or dest_text,
        distance_mi=result.distance_mi,
        eta=result.format_eta(),
        vehicle_name=vehicle.name,
        provider=result.provider,
        hazmat=vehicle.hazmat,
    )
    result.summary = maybe_llm_polish(
        summary,
        openai_key=settings.openai_api_key,
        anthropic_key=settings.anthropic_api_key,
    )
    lh = plan_long_haul(result.distance_mi, result.duration_s, DEFAULT_HOS)
    result.long_haul = lh.model_dump()
    result.roi = compute_roi(RoiAssumptions()).model_dump()
    return result
