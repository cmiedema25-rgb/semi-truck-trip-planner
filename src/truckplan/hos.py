"""Illustrative HOS / multi-day long-haul planning aids (US property-carrying sketch).

NOT legal advice or compliance certification. Rules encoded here are simplified
planning defaults commonly referenced for property-carrying CDL operations:
  - 11 hours driving within a 14-hour on-duty window after 10 consecutive hours off
  - 30-minute break required after 8 cumulative hours of driving
Actual carrier policy, ELD data, adverse conditions, and current FMCSA rules govern.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class HosAssumptions(BaseModel):
    max_drive_hours_per_day: float = Field(default=11.0, description="11-hour driving limit")
    duty_window_hours: float = Field(default=14.0, description="14-hour on-duty window")
    break_after_drive_hours: float = Field(default=8.0, description="30-min break after 8 driving hours")
    break_minutes: float = Field(default=30.0)
    average_speed_mph: float = Field(
        default=55.0,
        description="Planning speed for interval estimates when live traffic unused",
    )
    fuel_stop_every_miles: float = Field(default=600.0, description="Typical long-haul fuel cadence")
    rest_stop_every_miles: float = Field(default=250.0, description="Rest / stretch cadence along route")


DEFAULT_HOS = HosAssumptions()


class DriveBlock(BaseModel):
    day: int
    label: str
    drive_hours: float
    distance_mi: float
    notes: str = ""


class PlannedStop(BaseModel):
    kind: str  # break | fuel | rest | overnight
    after_miles: float
    after_drive_hours: float
    description: str


class LongHaulPlan(BaseModel):
    total_distance_mi: float
    total_drive_hours: float
    days_required: int
    drive_blocks: list[DriveBlock]
    stops: list[PlannedStop]
    hos_summary: str
    disclaimer: str = (
        "HOS helpers are planning aids only — not compliance certification or legal advice. "
        "Verify with your ELD, carrier policy, and current FMCSA rules before dispatch."
    )


def plan_long_haul(
    distance_mi: float,
    duration_s: float | None = None,
    assumptions: HosAssumptions | None = None,
) -> LongHaulPlan:
    """Build multi-day drive blocks + break/fuel/rest cadence from distance/duration."""
    a = assumptions or DEFAULT_HOS
    if duration_s and duration_s > 0:
        drive_hours = duration_s / 3600.0
    else:
        drive_hours = distance_mi / a.average_speed_mph if a.average_speed_mph else 0.0

    drive_hours = max(drive_hours, 0.0)
    distance_mi = max(distance_mi, 0.0)

    blocks: list[DriveBlock] = []
    remaining_h = drive_hours
    remaining_mi = distance_mi
    day = 1
    while remaining_h > 0.05 or remaining_mi > 1:
        block_h = min(a.max_drive_hours_per_day, remaining_h if remaining_h > 0 else a.max_drive_hours_per_day)
        if drive_hours <= 0:
            break
        # Pro-rate miles by hours when we have a duration; else by max day miles
        if drive_hours > 0:
            block_mi = distance_mi * (block_h / drive_hours) if remaining_h == drive_hours and day == 1 and remaining_mi == distance_mi else min(
                remaining_mi, distance_mi * (block_h / drive_hours)
            )
            # simpler: allocate by remaining proportion
            block_mi = remaining_mi if remaining_h <= a.max_drive_hours_per_day + 1e-6 else remaining_mi * (block_h / remaining_h)
        else:
            block_mi = min(remaining_mi, a.average_speed_mph * a.max_drive_hours_per_day)

        block_mi = round(min(block_mi, remaining_mi), 1)
        block_h = round(min(block_h, remaining_h), 2)
        notes = "Within illustrative 11-hr drive / 14-hr window."
        if block_h >= a.break_after_drive_hours:
            notes += f" Include {a.break_minutes:.0f}-min break after {a.break_after_drive_hours:.0f} driving hours."
        blocks.append(
            DriveBlock(
                day=day,
                label=f"Day {day} drive block",
                drive_hours=block_h,
                distance_mi=block_mi,
                notes=notes,
            )
        )
        remaining_h = round(remaining_h - block_h, 3)
        remaining_mi = round(remaining_mi - block_mi, 3)
        day += 1
        if day > 14:  # safety
            break

    stops: list[PlannedStop] = []
    # Driving-hour based mandatory break(s)
    hours_cursor = a.break_after_drive_hours
    while hours_cursor < drive_hours - 0.1:
        miles_at = round(distance_mi * (hours_cursor / drive_hours), 1) if drive_hours else 0.0
        stops.append(
            PlannedStop(
                kind="break",
                after_miles=miles_at,
                after_drive_hours=hours_cursor,
                description=f"30-min break after {hours_cursor:.0f} hrs driving (illustrative HOS)",
            )
        )
        hours_cursor += a.break_after_drive_hours

    # Rest cadence by miles
    m = a.rest_stop_every_miles
    while m < distance_mi - 10:
        hrs = round((m / distance_mi) * drive_hours, 2) if distance_mi else 0.0
        stops.append(
            PlannedStop(
                kind="rest",
                after_miles=round(m, 1),
                after_drive_hours=hrs,
                description=f"Suggested rest / stretch stop near mile {m:.0f}",
            )
        )
        m += a.rest_stop_every_miles

    # Fuel cadence
    m = a.fuel_stop_every_miles
    while m < distance_mi - 10:
        hrs = round((m / distance_mi) * drive_hours, 2) if distance_mi else 0.0
        stops.append(
            PlannedStop(
                kind="fuel",
                after_miles=round(m, 1),
                after_drive_hours=hrs,
                description=f"Suggested fuel stop near mile {m:.0f} (~{a.fuel_stop_every_miles:.0f}-mi cadence)",
            )
        )
        m += a.fuel_stop_every_miles

    # Overnight between days
    for b in blocks[:-1]:
        stops.append(
            PlannedStop(
                kind="overnight",
                after_miles=round(sum(x.distance_mi for x in blocks if x.day <= b.day), 1),
                after_drive_hours=round(sum(x.drive_hours for x in blocks if x.day <= b.day), 2),
                description=f"End Day {b.day} — 10 consecutive hours off before Day {b.day + 1} (illustrative)",
            )
        )

    stops.sort(key=lambda s: (s.after_miles, s.kind))

    days_required = max(1, len(blocks))
    hos_summary = (
        f"Long-haul plan: {distance_mi:.0f} mi, ~{drive_hours:.1f} driving hours across "
        f"{days_required} day(s) using illustrative 11/14 HOS limits "
        f"(30-min break after {a.break_after_drive_hours:.0f} hrs driving)."
    )
    return LongHaulPlan(
        total_distance_mi=round(distance_mi, 1),
        total_drive_hours=round(drive_hours, 2),
        days_required=days_required,
        drive_blocks=blocks,
        stops=stops,
        hos_summary=hos_summary,
    )


def format_long_haul_markdown(plan: LongHaulPlan) -> str:
    lines = [
        "### Long-haul / HOS plan (planning aid)",
        "",
        plan.hos_summary,
        "",
        "| Day | Drive hours | Distance | Notes |",
        "| --- | ---: | ---: | --- |",
    ]
    for b in plan.drive_blocks:
        lines.append(f"| Day {b.day} | {b.drive_hours:.1f} h | {b.distance_mi:.0f} mi | {b.notes} |")
    lines.extend(["", "**Suggested stops (approximate cadence)**", ""])
    for s in plan.stops[:12]:
        lines.append(f"- **{s.kind}** @ ~{s.after_miles:.0f} mi ({s.after_drive_hours:.1f} h): {s.description}")
    if len(plan.stops) > 12:
        lines.append(f"- … {len(plan.stops) - 12} more scheduled stops in full JSON report")
    lines.extend(["", f"_{plan.disclaimer}_"])
    return "\n".join(lines)


def format_long_haul_plain(plan: LongHaulPlan) -> str:
    parts = [plan.hos_summary]
    for b in plan.drive_blocks:
        parts.append(f"  Day {b.day}: {b.drive_hours:.1f} h / {b.distance_mi:.0f} mi — {b.notes}")
    parts.append("  Stops:")
    for s in plan.stops[:10]:
        parts.append(f"    [{s.kind}] ~{s.after_miles:.0f} mi — {s.description}")
    parts.append(f"  Note: {plan.disclaimer}")
    return "\n".join(parts)
