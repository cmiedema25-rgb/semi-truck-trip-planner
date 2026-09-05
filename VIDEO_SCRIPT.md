# Demo video script — Long-Haul Semi Truck Trip Planner (~100–120 seconds)

**Suggested title:** `Long-Haul Semi Truck Trip Planner — LA→Chicago ~2010 mi + HOS/ROI`

**Record:** real Gradio UI + terminal. 1280×720 or 1920×1080. Neutral desktop. No neon captions, no fake logos, no “100% legal” claims.

### Before record
```bash
make verify
TRUCKPLAN_FORCE_MOCK=1 make ui   # http://127.0.0.1:7860
```

---

## Spoken script

### 0:00–0:20 — Problem
“Long-haul dispatch still burns a lot of time sketching a two-thousand-mile truck-aware route — legal path, fuel, and HOS — by hand. This is a destination-first Class-8 long-haul planner. Demo lane: Ontario California terminal to Chicago — about two thousand ten miles. HGV profile when available. Not a one-hundred-percent legal guarantee, and HOS here is a planning aid only.”

### 0:20–0:55 — Plan the OTR load
**Type:** Destination `4400 S Pulaski Rd, Chicago, IL 60632` · Origin `1200 Commerce Dr, Ontario, CA 91761` · preset dry van · **Plan long-haul truck route**.

**Say:** “Submit once. We get distance about two thousand ten miles, roughly thirty-six and a half driving hours, corridor steps, and a map link.”

### 0:55–1:25 — HOS multi-day + ROI (critical)
Scroll to **Long-haul / HOS plan** then **Trip ROI**.

**Say:** “Under illustrative eleven-hour driving limits this breaks into four days — eleven, eleven, eleven, and a short day-four block — plus thirty-minute breaks after eight driving hours, fuel about every six hundred miles, and overnight offs. ROI assumptions: manual long-haul plan about thirty-two minutes versus four minutes here — twenty-eight minutes saved, about sixteen dollars thirty-three illustrative labor at thirty-five an hour. At eight long-haul dispatches a day, about three point seven hours, roughly one hundred thirty-one dollars — labeled synthetic demo, not customer savings.”

### 1:25–1:45 — Offline proof
Show `make verify` or `evidence/trip-report.json` (`distance_mi` 2010, `hos_days_required` 4, `roi`).

### 1:45–2:00 — Close
“Reproduce with make verify. Optional OpenRouteService key for live driving-HGV. Repo: semi-truck-trip-planner.”

## Don’t
Cartoon cards, emoji spam, stock truck montages, fake $ banners, “100% legal.”
