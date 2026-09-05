# Verification log

## Environment
- Date: **2026-09-04 18:49 PDT**
- Python: Python 3.13.5
- Mode: `TRUCKPLAN_FORCE_MOCK=1`

## Command
```bash
make verify
```

## Results
| Check | Result |
|-------|--------|
| pytest | **25 passed** |
| Scenario | Ontario CA → Chicago IL (~2000 mi long-haul) |
| distance_m | **3234781** |
| duration_s | **131564** |
| distance_mi | **2010.0** |
| Driving hours | **~36.5** |
| ETA | **36h 32m** |
| HOS days (illustrative 11-hr) | **4** |
| ROI saved | **28 min** (32→4) |
| Illustrative $/trip | **$16.33** |
| @ 8 long-haul/day | **~3.7 h / ~$131** |
| Evidence | `evidence/mock_trip_la_chicago.json`, `evidence/trip-report.json` |

## Labels
- No "100% legal routes" claim.
- HOS = planning aid, not compliance certification.
- Dollar figures = illustrative scenario / synthetic demo.
