#!/usr/bin/env python3
"""Write retained mock trip JSON + trip-report with ROI fields."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from truckplan.config import Settings
from truckplan.planner import plan_trip
from truckplan.providers.mock import MockProvider, sample_trip_dict
from truckplan.roi import DEFAULT_ASSUMPTIONS, compute_roi

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def main() -> None:
    EVIDENCE.mkdir(exist_ok=True)
    trip = sample_trip_dict()
    planned = plan_trip(
        destination="Houston warehouse",
        origin="Dallas yard",
        provider=MockProvider(),
        settings=Settings(ors_api_key=None, truckplan_force_mock=True),
    )
    roi = compute_roi(DEFAULT_ASSUMPTIONS)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scenario": "Dallas yard → Houston warehouse (Class-8 dry van)",
        "provider": "mock",
        "distance_m": planned.distance_m,
        "duration_s": planned.duration_s,
        "distance_mi": round(planned.distance_mi, 1),
        "eta": planned.format_eta(),
        "steps_count": len(planned.steps),
        "vehicle": planned.vehicle.model_dump(),
        "map_url": planned.map_url,
        "summary": planned.summary,
        "roi": roi.model_dump(),
        "full_trip": {**trip, "roi": roi.model_dump()},
    }
    out = EVIDENCE / "mock_trip_dallas_houston.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    report = EVIDENCE / "trip-report.json"
    report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Wrote {report}")
    print(
        f"distance_m={planned.distance_m} duration_s={planned.duration_s} "
        f"eta={planned.format_eta()} roi_saved_min={roi.time_saved_minutes} "
        f"illustrative_usd={roi.illustrative_value_usd}"
    )


if __name__ == "__main__":
    main()
