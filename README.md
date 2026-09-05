# Semi Truck Trip Planner

[![CI](https://github.com/cmiedema25-rgb/semi-truck-trip-planner/actions/workflows/ci.yml/badge.svg)](https://github.com/cmiedema25-rgb/semi-truck-trip-planner/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)

**Destination-first HGV / truck routing for Class-8 semis** — CLI + Gradio trip-planner bot.  
Built as a [Rework Digital](https://reworkdigital.io) proof-of-work (Workflow Automation + AI Integration & APIs + Python).

> **Not a “100% legal routes” product.** Routes use an **HGV / truck routing profile** (`driving-hgv` via OpenRouteService when configured) that avoids many passenger-only paths when the provider supports it. Legality still depends on vehicle dimensions, permits, local restrictions, and provider data currency. See [Safety / disclaimer](#safety--disclaimer).

---

## Reviewer proof in 60 seconds

| Step | Command / link | Expected |
|------|----------------|----------|
| 1. Clone & verify offline | `make verify` | Tests green; mock Dallas→Houston **328500 m / 14100 s (~204.1 mi, 3h 55m)** |
| 2. Retained evidence | [`evidence/mock_trip_dallas_houston.json`](evidence/mock_trip_dallas_houston.json) | Same numbers + vehicle constraints |
| 3. Verification log | [`evidence/VERIFICATION.md`](evidence/VERIFICATION.md) | Exact `make verify` output notes |
| 4. Skills map | [`docs/PROOF_OF_SKILLS.md`](docs/PROOF_OF_SKILLS.md) | Skill → files → tests |
| 5. Demo video script | [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md) | ~2 min Loom script |
| 6. Paste-ready Rework fields | [`REWORK_SUBMISSION.md`](REWORK_SUBMISSION.md) | Title, category, skills, outcomes |
| 7. Live UI (optional) | `make ui` → http://127.0.0.1:7860 | Destination → route card + **Trip ROI** table |
| 8. ROI math | `evidence/trip-report.json` → `roi` | 15→2 min, $7.58/trip, ~$152/day @20 (illustrative) |

**Trip ROI card (illustrative scenario — not fake customers):** defaults assume **15 min** manual truck-aware check vs **2 min** in-app → **13 min (~87%)** saved; at **$35/hr** ≈ **$7.58/trip**; at **20 trips/day** ≈ **4.3 hours / ~$152** illustrative. Shown in Gradio + CLI after every successful route; fields retained in `evidence/trip-report.json`. All dollar figures are scenario math, not billed savings.

---

## Skills demonstrated

| Skill | Where it shows up |
|-------|-------------------|
| **Workflow Automation** | Destination-only → geocode → HGV route → ETA/steps/map card; CLI + Gradio bot for dispatch |
| **AI Integration & APIs** | OpenRouteService geocode + `driving-hgv`; mock+live provider swap; vehicle restrictions payload |
| **Python** | Typed package (`pydantic`), Typer CLI, Gradio UI, pytest, Makefile, GitHub Actions |
| **AI Agents & Assistants** | Gradio “Trip bot” tab + rule-based NL parse of free-text destinations |

**Not claimed:** Multimodal, RLHF, Fine-tuning, Document AI, AI Safety, Prompt Engineering (NL layer is rule-based, not prompt-tuned).

---

## Quick start

```bash
git clone https://github.com/cmiedema25-rgb/semi-truck-trip-planner.git
cd semi-truck-trip-planner
make verify          # offline — uses mock provider, no API key
make ui              # Gradio UI on :7860 (mock by default)
```

### CLI

```bash
# Destination only (origin = TRUCKPLAN_HOME_ORIGIN / Dallas default)
truckplan route --to "5600 Warehouse Blvd, Houston, TX"

truckplan route --to "Houston warehouse" --from "Dallas yard" --hazmat
truckplan route --to "Austin TX" --height-m 4.0 --weight-t 36 --preset dry_van --json

# Rule-based NL parse
truckplan parse "to Houston from Dallas, hazmat"
truckplan route --to "to Houston warehouse from Dallas yard" --parse-nl
```

### Live OpenRouteService (optional)

1. Free key: https://openrouteservice.org/dev/#/signup  
2. `cp .env.example .env` and set `ORS_API_KEY=...`  
3. Unset `TRUCKPLAN_FORCE_MOCK` (or set to `0`)  
4. Re-run `truckplan route --to "..."` or `make ui`

**What the ORS key enables:** live address geocoding + `driving-hgv` directions with optional height/width/length/weight/axle/hazmat restriction parameters. Without it, the offline mock provider still powers CI, demos, and `make verify`.

---

## Vehicle presets (Class-8)

Editable defaults (typical US interstate-oriented figures — **verify for your operation**):

| Preset | Height | Width | Length | Weight | Axles |
|--------|--------|-------|--------|--------|-------|
| `dry_van` (default) | 4.11 m (~13′6″) | 2.59 m (~8′6″) | 22.86 m (~75′ combo) | 36.29 t (~80,000 lb) | 5 |
| `reefer` | same baseline | | | | |
| `flatbed` | same baseline | | | | |

---

## Architecture

```
Destination (+ optional origin)
        │
        ▼
  NL parse (optional, rule-based)
        │
        ▼
  Provider: Mock (CI)  or  OpenRouteService (live)
        │   geocode → driving-hgv route
        ▼
  Route card: distance, ETA, steps, map link, disclaimer
```

| Path | Role |
|------|------|
| `src/truckplan/planner.py` | Orchestration |
| `src/truckplan/providers/ors.py` | Live ORS HGV API |
| `src/truckplan/providers/mock.py` | Offline Dallas→Houston fixture |
| `src/truckplan/nlp.py` | Destination/origin/hazmat parse |
| `src/truckplan/cli.py` | Typer CLI |
| `src/truckplan/ui.py` | Gradio form + trip bot |

---

## Safety / disclaimer

- Do **not** treat output as a guarantee of a fully legal truck route in every jurisdiction.  
- HGV profiles reduce use of many passenger-car-only paths **when the data provider supports it**.  
- Final compliance depends on **actual vehicle config**, **permits**, **local / temporal restrictions**, and **provider data freshness**.  
- Always follow your carrier’s routing and compliance process before dispatch.

---

## Demo video

- Script: [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md) (record real Gradio + terminal; show Trip ROI card)
- Silent product cut (real UI frames): [`demo/semi-truck-trip-planner-demo.mp4`](demo/semi-truck-trip-planner-demo.mp4) (~2 min)

## License

MIT © Charles Miedema
