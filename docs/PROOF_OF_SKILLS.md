# Proof of skills — Semi Truck Trip Planner

Maps each claimed Rework skill to concrete files, tests, and commands reviewers can run offline.

## Primary skills

### 1. Workflow Automation

**Claim:** Automates dispatcher/driver trip planning: destination (required) → geocode → HGV route → distance/ETA/steps/map card, with optional origin and vehicle constraints.

| Artifact | Path |
|----------|------|
| Orchestrator | `src/truckplan/planner.py` (`plan_trip`) |
| CLI workflow | `src/truckplan/cli.py` (`truckplan route`) |
| UI workflow | `src/truckplan/ui.py` (form submit + chat bot) |
| Evidence trip | `evidence/mock_trip_dallas_houston.json`, `evidence/trip-report.json` |
| Trip ROI card | `src/truckplan/roi.py` (assumptions + illustrative $ math) |

**Verify:**
```bash
make verify
TRUCKPLAN_FORCE_MOCK=1 truckplan route --to "Houston warehouse" --from "Dallas yard"
```

**Expected:** distance_m=`328500`, duration_s=`14100`, ETA `3h 55m`; ROI time saved `13` min, illustrative `~$7.58`/trip.

---

### 2. AI Integration & APIs

**Claim:** Integrates OpenRouteService geocoding + `driving-hgv` directions; passes vehicle restriction options; swaps to deterministic mock provider for CI.

| Artifact | Path |
|----------|------|
| ORS provider | `src/truckplan/providers/ors.py` |
| Mock provider | `src/truckplan/providers/mock.py` |
| Provider interface | `src/truckplan/providers/base.py` |
| Settings / key gate | `src/truckplan/config.py`, `.env.example` |
| Vehicle → ORS options | `src/truckplan/models.py` (`as_ors_options`) |

**Verify:**
```bash
pytest tests/test_mock_provider.py tests/test_planner.py -q
# Live (optional): set ORS_API_KEY and unset TRUCKPLAN_FORCE_MOCK
```

---

### 3. Python

**Claim:** Packaged Python 3.11+ app with typed models, CLI entrypoint, tests, Makefile, GitHub Actions.

| Artifact | Path |
|----------|------|
| Package | `src/truckplan/` |
| Build | `pyproject.toml` |
| Tests | `tests/` |
| CI | `.github/workflows/ci.yml` |
| Makefile | `Makefile` (`verify`, `ui`, `test`) |

**Verify:** `make verify` on Python 3.11+.

---

## Secondary skills

### 4. AI Agents & Assistants

**Claim:** Gradio “Trip bot” acts as a destination-first trip assistant; rule-based NL extracts destination/origin/hazmat from free text.

| Artifact | Path |
|----------|------|
| Bot UI | `src/truckplan/ui.py` (`plan_from_chat`, Trip bot tab) |
| NL parse | `src/truckplan/nlp.py` |
| CLI parse | `truckplan parse "..."` |

**Verify:**
```bash
pytest tests/test_nlp.py -q
truckplan parse "to Houston from Dallas, hazmat"
```

---

## Explicitly not claimed

| Skill | Why not |
|-------|---------|
| Prompt Engineering | NL layer is regex/rule-based; optional LLM polish is gated and unused in CI |
| Multimodal / RLHF / Fine-tuning / Document AI / AI Safety | Out of scope for this repo |

## Category suggestion

- **Primary category:** Workflow Automation  
- **Alt:** AI Integration & APIs  
- **Tags:** Workflow Automation, AI Integration & APIs, Python, AI Agents & Assistants
