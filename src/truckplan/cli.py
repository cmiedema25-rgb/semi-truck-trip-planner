"""CLI: truckplan route / truckplan ui / truckplan parse."""

from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from truckplan import __version__
from truckplan.nlp import parse_trip_text
from truckplan.planner import plan_trip
from truckplan.roi import TripRoi, format_roi_plain

app = typer.Typer(
    name="truckplan",
    help="Semi-truck trip planner — HGV routing for Class-8 vehicles.",
    add_completion=False,
)
console = Console()

DISCLAIMER = (
    "Routes use an HGV / truck routing profile that avoids many passenger-only paths "
    "when the provider supports it. Legality still depends on vehicle dimensions, "
    "permits, local restrictions, and provider data currency. Not legal advice."
)


@app.callback()
def main() -> None:
    """Semi-truck trip planner CLI."""


@app.command("version")
def version_cmd() -> None:
    """Print package version."""
    console.print(f"truckplan {__version__}")


@app.command("parse")
def parse_cmd(
    text: str = typer.Argument(..., help="Free-text trip request"),
) -> None:
    """Parse natural-language trip text (rule-based, offline)."""
    parsed = parse_trip_text(text)
    console.print_json(data={
        "destination": parsed.destination,
        "origin": parsed.origin,
        "hazmat": parsed.hazmat,
        "notes": parsed.notes,
    })


@app.command("route")
def route_cmd(
    to_addr: str = typer.Option(..., "--to", help="Destination address (required)"),
    from_addr: Optional[str] = typer.Option(
        None, "--from", help="Origin address (default: home terminal from env)"
    ),
    height_m: Optional[float] = typer.Option(None, "--height-m", help="Vehicle height meters"),
    width_m: Optional[float] = typer.Option(None, "--width-m", help="Vehicle width meters"),
    length_m: Optional[float] = typer.Option(None, "--length-m", help="Vehicle length meters"),
    weight_t: Optional[float] = typer.Option(None, "--weight-t", help="Gross weight metric tons"),
    axles: Optional[int] = typer.Option(None, "--axles", help="Axle count"),
    hazmat: bool = typer.Option(False, "--hazmat", help="Flag hazardous materials"),
    preset: str = typer.Option("dry_van", "--preset", help="dry_van | reefer | flatbed"),
    parse_nl: bool = typer.Option(False, "--parse-nl", help="Parse --to as free-text NL"),
    as_json: bool = typer.Option(False, "--json", help="Emit JSON"),
) -> None:
    """Plan an HGV-oriented truck route to a destination."""
    try:
        result = plan_trip(
            destination=to_addr,
            origin=from_addr,
            preset=preset,
            height_m=height_m,
            width_m=width_m,
            length_m=length_m,
            weight_t=weight_t,
            axles=axles,
            hazmat=hazmat,
            parse_nl=parse_nl,
        )
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    if as_json:
        console.print(json.dumps(result.model_dump(), indent=2))
        return

    table = Table(title="Truck route", show_header=True)
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Origin", result.origin.label)
    table.add_row("Destination", result.destination.label)
    table.add_row("Distance", f"{result.distance_mi:.1f} mi ({result.distance_m:.0f} m)")
    table.add_row("ETA", result.format_eta())
    table.add_row("Provider", f"{result.provider} / {result.profile}")
    table.add_row("Vehicle", result.vehicle.name)
    table.add_row(
        "Constraints",
        f"H={result.vehicle.height_m}m W={result.vehicle.width_m}m "
        f"L={result.vehicle.length_m}m Wgt={result.vehicle.weight_t}t "
        f"axles={result.vehicle.axles} hazmat={result.vehicle.hazmat}",
    )
    table.add_row("Map", result.map_url)
    console.print(table)
    console.print(Panel(result.summary, title="Summary"))
    if result.steps:
        steps = Table(title="Turn-by-turn (summary)", show_header=True)
        steps.add_column("#", style="dim")
        steps.add_column("Instruction")
        steps.add_column("Dist")
        for i, step in enumerate(result.steps[:25], 1):
            steps.add_row(str(i), step.instruction, f"{step.distance_m / 1609.344:.1f} mi")
        console.print(steps)
    if result.roi:
        console.print(Panel(format_roi_plain(TripRoi.model_validate(result.roi)), title="Trip ROI"))
    console.print(f"[yellow]{DISCLAIMER}[/yellow]")


@app.command("ui")
def ui_cmd(
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(7860, "--port"),
    share: bool = typer.Option(False, "--share"),
) -> None:
    """Launch the Gradio trip-planner bot UI."""
    from truckplan.ui import launch_ui

    launch_ui(host=host, port=port, share=share)


if __name__ == "__main__":
    app()
