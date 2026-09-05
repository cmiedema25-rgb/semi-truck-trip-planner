# Rework Digital — paste-ready submission

**Repo URL:** https://github.com/cmiedema25-rgb/semi-truck-trip-planner  

**Title:** Semi Truck Trip Planner (HGV routing + dispatch ROI for Class-8)

**One-liner:** Destination-first Class-8 trip planner that returns HGV-oriented distance/ETA/steps plus an honest illustrative Trip ROI card (time saved vs manual truck-aware lookup).

**Description (short):**  
Drivers and dispatchers enter a destination (origin optional; defaults to home terminal). The app geocodes, requests an HGV / truck routing profile, and returns a route card: miles, ETA, turn-by-turn summary, map link, editable Class-8 constraints (height, width, length, weight, axles, hazmat), and a **Trip ROI** panel with transparent assumptions (manual ~15 min vs tool ~2 min → 13 min saved; illustrative labor math at $35/hr). Gradio trip-planner bot + Typer CLI + offline mock for `make verify`. Honest disclaimer — **no “100% legal route” claim**; all $ figures labeled illustrative/synthetic demo.

**Category:** Workflow Automation  

**Alt category:** AI Integration & APIs  

**Skills (select):**
- Workflow Automation
- AI Integration & APIs
- Python
- AI Agents & Assistants

**Do not select:** Multimodal, RLHF, Fine-tuning, Document AI, AI Safety, Prompt Engineering

**Demo video:** _(paste Loom/Unlisted URL after recording — follow VIDEO_SCRIPT.md; show real UI + ROI card)_

**Honest outcome / ROI numbers (synthetic scenario — not fake customers):**

| Metric | Value |
|--------|-------|
| Mock trip | Dallas yard → Houston warehouse |
| Route | **328500 m (~204.1 mi), 14100 s (3h 55m)** |
| Manual estimate | **15 min** |
| With this tool | **2 min** |
| Time saved / trip | **13 min (~87%)** |
| Illustrative labor / trip | **13/60 × $35 ≈ $7.58** |
| At 20 trips/day | **~4.3 hours / ~$152 illustrative** |
| pytest | **20+ passed** offline via mock |

Label in submission text: *“Illustrative scenario math from documented assumptions — not audited customer savings.”*

**Proof links:**
- Skills map: `docs/PROOF_OF_SKILLS.md`
- Evidence: `evidence/trip-report.json`, `evidence/mock_trip_dallas_houston.json`
- Verification: `evidence/VERIFICATION.md`
- Video script: `VIDEO_SCRIPT.md`
- Demo one-pager: `DEMO.md`
