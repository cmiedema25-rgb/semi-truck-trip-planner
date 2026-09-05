"""Honest, transparent trip ROI estimates for dispatch workflows.

All dollar figures are **illustrative scenario math** — not billed customer savings.
Assumptions are editable constants documented for Rework reviewers.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class RoiAssumptions(BaseModel):
    """Editable dispatch-time assumptions (minutes / loaded hourly rate)."""

    manual_minutes: float = Field(
        default=15.0,
        description="Typical manual truck-aware route check (PC*MILER / tribal knowledge / Maps trial).",
    )
    tool_minutes: float = Field(
        default=2.0,
        description="Time to enter destination + vehicle preset and read the route card.",
    )
    dispatcher_rate_usd_per_hour: float = Field(
        default=35.0,
        description="Illustrative loaded dispatcher labor rate ($/hr) for scenario math only.",
    )
    trips_per_day: int = Field(
        default=20,
        ge=1,
        description="Scenario volume for daily rollup (synthetic demo default).",
    )


DEFAULT_ASSUMPTIONS = RoiAssumptions()


class TripRoi(BaseModel):
    """Per-trip and daily rollup ROI card."""

    assumptions: RoiAssumptions
    time_saved_minutes: float
    time_saved_pct: float
    illustrative_value_usd: float
    daily_hours_saved: float
    daily_illustrative_value_usd: float
    label: str = (
        "Illustrative scenario / synthetic demo — not audited customer savings. "
        "No customer logos or billed ROI claimed."
    )
    operational_levers: list[str] = Field(default_factory=list)

    def as_table_rows(self) -> list[tuple[str, str]]:
        a = self.assumptions
        return [
            ("Manual estimate", f"{a.manual_minutes:.0f} min"),
            ("With Semi Truck Trip Planner", f"{a.tool_minutes:.0f} min"),
            ("Time saved", f"{self.time_saved_minutes:.0f} min (~{self.time_saved_pct:.0f}%)"),
            (
                "Illustrative labor value (this trip)",
                f"${self.illustrative_value_usd:.2f}  [{self.time_saved_minutes:.0f}/60 × ${a.dispatcher_rate_usd_per_hour:.0f}/hr]",
            ),
            (
                f"At {a.trips_per_day} trips/day (scenario)",
                f"~{self.daily_hours_saved:.1f} hours / ~${self.daily_illustrative_value_usd:.0f} illustrative",
            ),
        ]


def compute_roi(assumptions: RoiAssumptions | None = None) -> TripRoi:
    a = assumptions or DEFAULT_ASSUMPTIONS
    saved = max(0.0, a.manual_minutes - a.tool_minutes)
    pct = (saved / a.manual_minutes * 100.0) if a.manual_minutes else 0.0
    value = (saved / 60.0) * a.dispatcher_rate_usd_per_hour
    daily_hours = (saved * a.trips_per_day) / 60.0
    daily_value = daily_hours * a.dispatcher_rate_usd_per_hour
    levers = [
        "HGV profile applies height/weight/hazmat constraints when the provider supports it — fewer passenger-route mistakes.",
        "Repeatable Class-8 vehicle presets reduce re-entry error across shifts.",
        "Retained trip JSON supports audit, dispatcher handoff, and compliance review.",
    ]
    return TripRoi(
        assumptions=a,
        time_saved_minutes=round(saved, 2),
        time_saved_pct=round(pct, 1),
        illustrative_value_usd=round(value, 2),
        daily_hours_saved=round(daily_hours, 2),
        daily_illustrative_value_usd=round(daily_value, 2),
        operational_levers=levers,
    )


def format_roi_markdown(roi: TripRoi) -> str:
    rows = roi.as_table_rows()
    lines = [
        "### Trip ROI (illustrative scenario)",
        "",
        "| Metric | Value |",
        "| --- | --- |",
    ]
    for k, v in rows:
        lines.append(f"| {k} | {v} |")
    lines.extend(["", f"_{roi.label}_", "", "**Operational levers**"])
    for item in roi.operational_levers:
        lines.append(f"- {item}")
    return "\n".join(lines)


def format_roi_plain(roi: TripRoi) -> str:
    parts = ["Trip ROI (illustrative scenario / synthetic demo):"]
    for k, v in roi.as_table_rows():
        parts.append(f"  {k}: {v}")
    parts.append(f"  Note: {roi.label}")
    return "\n".join(parts)
