# Long-Haul Semi Truck Trip Planner

[![CI](https://github.com/cmiedema25-rgb/semi-truck-trip-planner/actions/workflows/ci.yml/badge.svg)](https://github.com/cmiedema25-rgb/semi-truck-trip-planner/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

**~2,000-mile Class-8 OTR trip planner** — destination-first HGV routing, multi-day / HOS sketch, fuel & rest cadence, and an honest dispatch ROI card.  
Built as a [Rework Digital](https://reworkdigital.io) proof-of-work (Workflow Automation + AI Integration & APIs + Python + AI Agents).

> **Not a “100% legal routes” product.** Routes use an **HGV / truck routing profile** (`driving-hgv` via OpenRouteService when configured). Legality still depends on vehicle dimensions, permits, local restrictions, and provider data currency. **HOS helpers are planning aids only — not compliance certification.**

**Canonical demo lane:** Ontario, CA (LA basin terminal) → Chicago, IL — **~2,010 miles**, ~36.5 driving hours, **4 illustrative HOS days**.

---

## Reviewer proof in 60 seconds

| Step | Command / link | Expected |
|------|----------------|----------|
| 1. Clone & verify offline | `make verify` | Tests green; mock **LA→Chicago 3234781 m / 131564 s (~2010 mi, 36h 32m, 4 HOS days)** |
| 2. Retained evidence | [`evidence/mock_trip_la_chicago.json`](evidence/mock_trip_la_chicago.json) | Distance + `long_haul` blocks + `roi` |
| 3. Trip report | [`evidence/trip-report.json`](evidence/trip-report.json) | Same payload for paste fields |
| 4. Verification log | [`evidence/VERIFICATION.md`](evidence/VERIFICATION.md) | Exact `make verify` notes |
| 5. Skills map | [`docs/PROOF_OF_SKILLS.md`](docs/PROOF_OF_SKILLS.md) | Skill → files → tests |
| 6. Demo video script | [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md) | ~2 min Loom over real UI |
| 7. Paste-ready Rework | [`REWORK_SUBMISSION.md`](REWORK_SUBMISSION.md) | Title, category, ROI |
| 8. Live UI | `make ui` → http://127.0.0.1:7860 | Chicago destination → route + HOS + ROI |

**Trip ROI (illustrative — not fake customers):** manual long-haul plan **~32 min** (route + fuel/HOS sketch) vs **~4 min** in-app → **28 min (~87.5%)** saved; at **$35/hr** ≈ **$16.33/trip**; at **8 long-haul dispatches/day** ≈ **3.7 hours / ~$131 illustrative**.

---

## Skills demonstrated

| Skill | Where it shows up |
|-------|-------------------|
| **Workflow Automation** | Destination → geocode → HGV route → multi-day HOS + fuel/rest → ROI card |
| **AI Integration & APIs** | OpenRouteService geocode + `driving-hgv`; mock+live providers; vehicle restrictions |
| **Python** | Typed package, Typer CLI, Gradio UI, pytest, Makefile, GitHub Actions |
| **AI Agents & Assistants** | Gradio Trip bot + rule-based NL parse for OTR destinations |

**Not claimed:** Multimodal, RLHF, Fine-tuning, Document AI, AI Safety, Prompt Engineering.

---

## Quick start

```bash
git clone https://github.com/cmiedema25-rgb/semi-truck-trip-planner.git
cd semi-truck-trip-planner
make verify          # offline mock — no API key
make ui              # Gradio on :7860
```

### CLI

```bash
# Destination only (origin = Ontario CA home terminal by default)
truckplan route --to "4400 S Pulaski Rd, Chicago, IL 60632"

truckplan route --to "Chicago IL" --from "Ontario CA" --hazmat --json
truckplan parse "to Chicago from Ontario CA terminal, hazmat"
```

### Live OpenRouteService (optional)

1. Free key: https://openrouteservice.org/dev/#/signup  
2. `cp .env.example .env` → set `ORS_API_KEY=`  
3. Unset `TRUCKPLAN_FORCE_MOCK`  
4. Re-run CLI or `make ui`

**ORS key enables:** live geocoding + `driving-hgv` with height/width/length/weight/axle/hazmat options. Without it, the ~2010 mi mock lane powers CI and demos.

---

## Long-haul features

1. **HGV truck-profile route** (`driving-hgv` when live)  
2. **Trip distance / driving hours**  
3. **HOS-aware break schedule** (illustrative 11-hr drive / 14-hr window / 30-min after 8 driving) — planning aid only  
4. **Fuel / rest stop cadence** (~600 mi fuel, ~250 mi rest intervals when POI data absent)  
5. **53' dry van long-haul presets** (editable height/weight/hazmat)  
6. **Multi-day summary** (Day 1…Day N drive blocks)

---

## Vehicle presets (Class-8 long-haul)

| Preset | Height | Width | Length | Weight | Axles |
|--------|--------|-------|--------|--------|-------|
| `dry_van` (default) | 4.11 m (~13′6″) | 2.59 m (~8′6″) | 22.86 m (~75′ combo) | 36.29 t (~80,000 lb) | 5 |
| `reefer` / `flatbed` | same editable baseline | | | | |

---

## Architecture

```
Destination (+ optional origin / home terminal)
        │
        ▼
  NL parse (optional) → Provider (Mock CI | ORS live)
        │
        ▼
  Route + LongHaulPlan (HOS days/stops) + Trip ROI
```

---

## Safety / disclaimer

- No guarantee of a fully legal truck route in every jurisdiction.  
- HGV profiles help when provider data supports them.  
- **HOS / break / fuel sketches are planning aids — not ELD compliance or legal advice.**  
- Follow carrier routing and compliance process before dispatch.

---

## Demo video

- Script: [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md)  
- Silent product cut: [`demo/semi-truck-trip-planner-demo.mp4`](demo/semi-truck-trip-planner-demo.mp4) (regenerate after UI changes)

## License

MIT © Charles Miedema
