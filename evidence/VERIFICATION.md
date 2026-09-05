# Verification log

Captured locally before publish. Reviewers can reproduce with `make verify` (no API key).

## Environment

- Date: **2026-09-04 18:42 PDT**
- Python: Python 3.13.5
- Mode: `TRUCKPLAN_FORCE_MOCK=1` (offline mock provider)

## Command

```bash
make verify
```

## Results

| Check | Result |
|-------|--------|
| pytest | **23 passed** |
| distance_m | **328500** |
| duration_s | **14100** |
| distance_mi | **204.1** |
| ETA | **3h 55m** |
| steps | **4** |
| ROI time saved | **13 min (~86.7%)** |
| Illustrative labor / trip | **$7.58** (13/60 × $35/hr) |
| Daily @ 20 trips | **~4.3 hours / ~$152 illustrative** |
| Evidence | `evidence/trip-report.json`, `evidence/mock_trip_dallas_houston.json` |

## Disclaimer / ROI labeling

- No "100% legal routes" marketing claim.
- All dollar figures labeled **illustrative scenario / synthetic demo** — not audited customer savings.
