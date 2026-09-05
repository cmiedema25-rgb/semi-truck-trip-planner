# Demo one-pager (Rework paste)

## What it is
Destination-first **semi-truck trip planner**: enter a delivery address (origin optional), get an **HGV-oriented** route card — distance, ETA, steps, map link, Class-8 vehicle constraints.

## How to run (60 seconds)
```bash
git clone https://github.com/cmiedema25-rgb/semi-truck-trip-planner.git
cd semi-truck-trip-planner && make verify && make ui
```
Open http://127.0.0.1:7860 → Destination `Houston warehouse` → Plan truck route.

## Offline proof numbers (mock)
| Metric | Value |
|--------|-------|
| Scenario | Dallas yard → Houston warehouse |
| distance_m | **328500** |
| duration_s | **14100** |
| Distance | **~204.1 mi** |
| ETA | **3h 55m** |
| Steps | 4 |

## Live routing
Set `ORS_API_KEY` from https://openrouteservice.org/dev/#/signup → geocode + `driving-hgv`.

## Disclaimer
Uses HGV / truck profile when supported. **Not** a guarantee of fully legal routes for every vehicle/jurisdiction. Verify dimensions, permits, and local restrictions.


## Trip ROI (illustrative scenario)

| Metric | Value |
|--------|-------|
| Manual estimate | 15 min |
| With Semi Truck Trip Planner | 2 min |
| Time saved | 13 min (~87%) |
| Illustrative labor value | 13/60 × $35 ≈ **$7.58** this trip |
| At 20 trips/day | ~**4.3 hours** / ~**$152** illustrative |

Assumptions are editable in `src/truckplan/roi.py`. Dollar figures are **not** customer savings.
