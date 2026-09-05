# Proof of skills — Long-Haul Semi Truck Trip Planner

## Primary

### Workflow Automation
Destination-first OTR planning: geocode → HGV route → multi-day HOS + fuel/rest → ROI.
- `src/truckplan/planner.py`, `cli.py`, `ui.py`, `hos.py`, `roi.py`
- Evidence: `evidence/mock_trip_la_chicago.json` (~2010 mi, 4 HOS days)
- Verify: `make verify` → distance_m=`3234781`, duration_s=`131564`, days=`4`, ROI saved=`28` min

### AI Integration & APIs
- `providers/ors.py` (`driving-hgv`), `providers/mock.py`, `models.py` (`as_ors_options`), `.env.example`

### Python
- `src/truckplan/`, `pyproject.toml`, `tests/`, `.github/workflows/ci.yml`, `Makefile`

## Secondary

### AI Agents & Assistants
- Gradio Trip bot (`ui.py`) + rule-based NL (`nlp.py`)

## Not claimed
Prompt Engineering, Multimodal, RLHF, Fine-tuning, Document AI, AI Safety

## Category
Workflow Automation (alt: AI Integration & APIs)  
Tags: Workflow Automation, AI Integration & APIs, Python, AI Agents & Assistants
