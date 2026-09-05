#!/usr/bin/env python3
"""Write retained ~2000-mile LA→Chicago trip JSON with HOS + ROI."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from truckplan.config import Settings
from truckplan.hos import LongHaulPlan
from truckplan.planner import plan_trip
from truckplan.providers.mock import MockProvider, sample_trip_dict
from truckplan.roi import DEFAULT_ASSUMPTIONS, compute_roi

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def main() -> None:
    EVIDENCE.mkdir(exist_ok=True)
    trip = sample_trip_dict()
    planned = plan_trip(
        destination="Chicago warehouse",
        origin="Ontario CA terminal",
        provider=MockProvider(),
        settings=Settings(ors_api_key=None, truckplan_force_mock=True),
    )
    roi = compute_roi(DEFAULT_ASSUMPTIONS)
    lh = LongHaulPlan.model_validate(planned.long_haul)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scenario": "Ontario CA (LA basin) → Chicago IL — ~2,010 mi Class-8 long-haul",
        "provider": "mock",
        "distance_m": planned.distance_m,
        "duration_s": planned.duration_s,
        "distance_mi": round(planned.distance_mi, 1),
        "driving_hours": round(planned.duration_s / 3600, 2),
        "eta": planned.format_eta(),
        "steps_count": len(planned.steps),
        "hos_days_required": lh.days_required,
        "vehicle": planned.vehicle.model_dump(),
        "map_url": planned.map_url,
        "summary": planned.summary,
        "long_haul": planned.long_haul,
        "roi": roi.model_dump(),
        "full_trip": {**trip, "long_haul": planned.long_haul, "roi": roi.model_dump()},
    }
    out_la = EVIDENCE / "mock_trip_la_chicago.json"
    out_la.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    report = EVIDENCE / "trip-report.json"
    report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    old = EVIDENCE / "mock_trip_dallas_houston.json"
    if old.exists():
        old.unlink()
    print(f"Wrote {out_la}")
    print(f"Wrote {report}")
    print(
        f"distance_m={planned.distance_m} duration_s={planned.duration_s} "
        f"mi={payload['distance_mi']} days={lh.days_required} "
        f"roi_saved_min={roi.time_saved_minutes} illustrative_usd={roi.illustrative_value_usd}"
    )


if __name__ == "__main__":
    main()
