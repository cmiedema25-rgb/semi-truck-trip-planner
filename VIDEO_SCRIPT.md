# Demo video script — Semi Truck Trip Planner (~100–120 seconds)

**Purpose:** Loom / Unlisted YouTube for Rework Digital. Record the **real Gradio UI and terminal** — not a slideshow, not CapCut hype.

**Suggested title:** `Semi Truck Trip Planner — HGV route + dispatch ROI (Dallas→Houston demo)`

**Technical:** 1280×720 or 1920×1080 MP4 · steady framing · dark/neutral desktop · no meme fonts · no neon caption bars · no fake customer logos or “$ saved” banners.

---

## Before you hit record

```bash
cd semi-truck-trip-planner
make verify          # confirm 20 passed; evidence JSON present
TRUCKPLAN_FORCE_MOCK=1 make ui   # http://127.0.0.1:7860
```

Open: (1) Gradio in the browser, (2) a terminal with the repo root. Cursor large enough to follow.

---

## Spoken script (dispatcher / engineer tone)

### 0:00–0:18 — Problem

“Dispatch still spends a long time on each load just to get a truck-aware route — bouncing between PC*MILER, tribal knowledge, and passenger Maps. I’m showing a destination-first trip planner for Class-8 semis. It uses an HGV routing profile when available. It does **not** claim one-hundred-percent legal routes — that still depends on your vehicle, permits, and local data.”

**On screen:** Gradio title + disclaimer visible; do not overlay marketing text.

### 0:18–0:55 — Plan a real-looking trip

**Actions (slow, readable):**
1. Destination: `5600 Warehouse Blvd, Houston, TX 77092`
2. Origin: `1234 Trucking Way, Dallas, TX 75201`
3. Preset: `dry_van` (Class-8 defaults). Optionally open the constraints accordion so height/weight/axles are visible.
4. Click **Plan truck route**.

**Say:**  
“Origin is optional — it can default to the home terminal — but for this demo I’m using Dallas yard to Houston warehouse. Class-8 dry van preset: about thirteen-six height, eighty-thousand pounds, five axles.”

**After render, point to:** distance **~204.1 mi**, ETA **3h 55m**, steps, map link.  
*(Mock numbers are fixed for offline CI; live ORS will differ.)*

### 0:55–1:25 — Trip ROI card (critical for Rework)

Scroll to the **Trip ROI** table on the same results panel.

**Say:**  
“Here’s the ROI card with transparent assumptions — not customer revenue. Manual truck-aware check: fifteen minutes. This tool: about two minutes. Time saved: thirteen minutes, roughly eighty-seven percent. Illustrative labor value at thirty-five dollars an hour is about seven fifty-eight **for this trip**. At twenty trips a day, that’s about four point three hours, around one hundred fifty-one dollars — again, **illustrative scenario math**, synthetic demo, not billed savings. Operationally you also get HGV constraints, reusable presets, and a retained trip JSON for handoff.”

**Do not** show fake dashboards, emoji, or customer logos.

### 1:25–1:45 — Offline proof

**On screen:** Terminal → `make verify` summary or open `evidence/trip-report.json` / `evidence/mock_trip_dallas_houston.json` and scroll `roi`.

**Say:**  
“Reviewers can reproduce offline: make verify — twenty tests, same distance and the same ROI fields in evidence. No API key required for the mock path.”

### 1:45–2:00 — Close

**Say:**  
“Repo is public on GitHub under semi-truck-trip-planner. Optional OpenRouteService key turns on live geocoding and driving-HGV. Thanks for reviewing.”

**On screen:** README “Reviewer proof in 60 seconds” or the GitHub URL — plain browser, no title-card animation.

---

## Burnt-in labels (optional only)

If you must caption a silent cut: small sans-serif, bottom third, e.g. `Dallas → Houston · mock HGV · illustrative ROI`. Prefer the UI table itself.

## Don’t

- Cartoon title cards, emoji spam, neon bars, rapid zooms  
- “100% legal” on screen or in VO  
- Fake customer logos or “Customer saved $X”  
- Stock truck montage (prefer pure product screen recording)

## Deliverable paths

- Script: this file  
- Preferred MP4: `demo/semi-truck-trip-planner-demo.mp4` (also copy under `/workspace/rework-demos/recordings/` when recording in this workspace)
