"""Gradio long-haul trip-planner bot — destination-first UX for OTR dispatch."""

from __future__ import annotations

import gradio as gr

from truckplan.hos import LongHaulPlan, format_long_haul_markdown
from truckplan.models import PRESETS
from truckplan.nlp import parse_trip_text
from truckplan.planner import plan_trip
from truckplan.roi import TripRoi, format_roi_markdown

DISCLAIMER = (
    "**Safety / disclaimer:** Routes use an **HGV / truck routing profile** that avoids many "
    "passenger-only paths when the provider supports it. Legality still depends on vehicle "
    "dimensions, permits, local restrictions, and provider data currency. "
    "This tool does **not** guarantee a fully legal route for every jurisdiction or load. "
    "**HOS / multi-day helpers are planning aids only — not compliance certification.** "
    "Verify with your ELD, carrier policy, and current FMCSA rules before dispatch."
)


def _format_card(result) -> str:
    lines = [
        "### Long-haul route card",
        f"**From:** {result.origin.label}",
        f"**To:** {result.destination.label}",
        f"**Distance:** {result.distance_mi:.0f} mi",
        f"**Driving time:** {result.format_eta()} ({result.duration_s / 3600:.1f} h)",
        f"**Provider:** `{result.provider}` / `{result.profile}`",
        f"**Vehicle:** {result.vehicle.name} "
        f"(H={result.vehicle.height_m}m, W={result.vehicle.width_m}m, "
        f"L={result.vehicle.length_m}m, {result.vehicle.weight_t}t, "
        f"{result.vehicle.axles} axles, hazmat={result.vehicle.hazmat})",
        f"**Map:** [{result.map_url}]({result.map_url})",
        "",
        f"**Summary:** {result.summary}",
        "",
        "#### Steps (corridor summary)",
    ]
    for i, step in enumerate(result.steps[:30], 1):
        lines.append(f"{i}. {step.instruction} ({step.distance_m / 1609.344:.0f} mi)")
    if getattr(result, "long_haul", None):
        lines.extend(["", format_long_haul_markdown(LongHaulPlan.model_validate(result.long_haul))])
    if getattr(result, "roi", None):
        lines.extend(["", format_roi_markdown(TripRoi.model_validate(result.roi))])
    lines.extend(["", "---", DISCLAIMER])
    return "\n".join(lines)


def plan_from_form(
    destination: str,
    origin: str,
    preset: str,
    height_m: float,
    width_m: float,
    length_m: float,
    weight_t: float,
    axles: int,
    hazmat: bool,
    use_nl: bool,
) -> str:
    if not (destination or "").strip():
        return "⚠️ Destination is required (destination-only UX supported — origin defaults to home terminal)."
    try:
        result = plan_trip(
            destination=destination.strip(),
            origin=origin.strip() or None,
            preset=preset,
            height_m=height_m,
            width_m=width_m,
            length_m=length_m,
            weight_t=weight_t,
            axles=axles,
            hazmat=hazmat,
            parse_nl=use_nl,
        )
        return _format_card(result)
    except Exception as exc:  # noqa: BLE001
        return f"**Error:** {exc}"


def plan_from_chat(message: str, history: list) -> str:
    parsed = parse_trip_text(message)
    if not parsed.destination:
        return (
            "Tell me the long-haul destination — e.g. `Chicago IL` or "
            "`to Chicago from Ontario CA terminal, hazmat`."
        )
    try:
        result = plan_trip(
            destination=parsed.destination,
            origin=parsed.origin,
            hazmat=parsed.hazmat,
            parse_nl=False,
        )
        return _format_card(result)
    except Exception as exc:  # noqa: BLE001
        return f"**Error:** {exc}"


def build_app() -> gr.Blocks:
    presets = list(PRESETS.keys())
    default = PRESETS["dry_van"]
    with gr.Blocks(title="Long-Haul Semi Truck Trip Planner") as demo:
        gr.Markdown(
            "# 🚛 Long-Haul Semi Truck Trip Planner\n"
            "Plan **~2,000-mile Class-8 OTR** trips: destination-first HGV routing, "
            "multi-day / HOS sketch, fuel & rest cadence, and an honest dispatch ROI card.\n\n"
            "Demo lane: **Ontario, CA → Chicago, IL (~2,010 mi)**.\n\n"
            + DISCLAIMER
        )
        with gr.Tab("Route form"):
            with gr.Row():
                destination = gr.Textbox(
                    label="Destination (required)",
                    placeholder="4400 S Pulaski Rd, Chicago, IL 60632",
                    value="4400 S Pulaski Rd, Chicago, IL 60632",
                )
                origin = gr.Textbox(
                    label="Origin (optional — default home terminal)",
                    placeholder="1200 Commerce Dr, Ontario, CA 91761",
                    value="1200 Commerce Dr, Ontario, CA 91761",
                )
            with gr.Row():
                preset = gr.Dropdown(presets, value="dry_van", label="Vehicle preset (53' long-haul)")
                hazmat = gr.Checkbox(label="Hazmat", value=False)
                use_nl = gr.Checkbox(label="Parse destination as NL", value=False)
            with gr.Accordion("Vehicle constraints (editable Class-8 long-haul defaults)", open=False):
                height_m = gr.Number(value=default.height_m, label="Height (m) ~13'6\"")
                width_m = gr.Number(value=default.width_m, label="Width (m) ~8'6\"")
                length_m = gr.Number(value=default.length_m, label="Length (m) ~75' combo")
                weight_t = gr.Number(value=default.weight_t, label="Weight (metric tons) ~80k lb")
                axles = gr.Number(value=default.axles, label="Axles", precision=0)
            submit = gr.Button("Plan long-haul truck route", variant="primary")
            out = gr.Markdown()
            submit.click(
                plan_from_form,
                inputs=[
                    destination, origin, preset, height_m, width_m,
                    length_m, weight_t, axles, hazmat, use_nl,
                ],
                outputs=out,
            )
        with gr.Tab("Trip bot"):
            gr.Markdown("Chat-style assistant for long-haul destinations / short trip sentences.")
            chatbot = gr.Chatbot(type="messages")
            msg = gr.Textbox(
                label="Message",
                placeholder="to Chicago IL from Ontario CA, hazmat",
            )
            clear = gr.Button("Clear")

            def respond(message: str, history: list):
                reply = plan_from_chat(message, history)
                history = history + [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": reply},
                ]
                return history, ""

            msg.submit(respond, [msg, chatbot], [chatbot, msg])
            clear.click(lambda: ([], ""), None, [chatbot, msg])
    return demo


def launch_ui(host: str = "127.0.0.1", port: int = 7860, share: bool = False) -> None:
    demo = build_app()
    demo.launch(server_name=host, server_port=port, share=share)


if __name__ == "__main__":
    launch_ui()
