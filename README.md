# Long-Haul Semi Truck Trip Planner

[![CI](https://github.com/cmiedema25-rgb/semi-truck-trip-planner/actions/workflows/ci.yml/badge.svg)](https://github.com/cmiedema25-rgb/semi-truck-trip-planner/actions/workflows/ci.yml)

Class-8 OTR trip planner for ~2,000-mile lanes: HGV routing, multi-day HOS sketches, fuel/rest cadence, Gradio UI, and a simple dispatch time-savings estimate.

**Not a legality or compliance product.** HGV profiles help when the provider has data; HOS helpers are planning aids only — not ELD certification.

Canonical offline demo: Ontario, CA → Chicago, IL (~2,010 mi).

## Quick start

```bash
git clone https://github.com/cmiedema25-rgb/semi-truck-trip-planner.git
cd semi-truck-trip-planner
make verify          # offline mock — no API key
make ui              # Gradio on :7860
```

### CLI

```bash
truckplan route --to "4400 S Pulaski Rd, Chicago, IL 60632"
truckplan route --to "Chicago IL" --from "Ontario CA" --hazmat --json
truckplan parse "to Chicago from Ontario CA terminal, hazmat"
```

### Live OpenRouteService (optional)

1. Key from https://openrouteservice.org/dev/#/signup
2. `cp .env.example .env` → set `ORS_API_KEY=`
3. Unset `TRUCKPLAN_FORCE_MOCK`
4. Re-run CLI or `make ui`

Without a key, the mock ~2010 mi lane powers CI and demos.

## Features

- `driving-hgv` route when live ORS is configured
- Distance / driving hours + multi-day HOS break sketch
- Fuel / rest cadence estimates
- Editable Class-8 presets (dry van / reefer / flatbed)
- Gradio trip bot with simple NL destination parse

## Disclaimer

No guarantee of a fully legal truck route. Follow carrier routing and compliance before dispatch.

## License

MIT © Charles Miedema
