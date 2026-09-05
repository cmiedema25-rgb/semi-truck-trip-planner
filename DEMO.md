# Demo one-pager — Long-Haul Semi Truck Trip Planner

## What it is
Destination-first **~2,000-mile Class-8 OTR** planner: HGV route card, multi-day HOS sketch, fuel/rest cadence, illustrative dispatch ROI.

## Run (60 seconds)
```bash
git clone https://github.com/cmiedema25-rgb/semi-truck-trip-planner.git
cd semi-truck-trip-planner && make verify && make ui
```
Open http://127.0.0.1:7860 → Destination Chicago / Origin Ontario CA → Plan.

## Offline proof (mock)
| Metric | Value |
|--------|-------|
| Lane | Ontario CA → Chicago IL |
| distance_m | **3234781** (~2010 mi) |
| duration_s | **131564** (~36.5 h) |
| HOS days | **4** |
| ROI | 32→4 min; **$16.33**/trip; **~$131**/day @8 |

## Disclaimer
HGV profile when supported. HOS = planning aid only. Not “100% legal.” $ = illustrative.
