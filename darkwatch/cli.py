"""Unified `darkwatch` command-line interface.

This module wraps the scattered `scripts/` tools into a single, discoverable
CLI. Long-term the subcommands should call library functions directly; for now
they invoke the existing scripts as subprocesses to avoid a large refactor.
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import typer

REPO_ROOT = Path(__file__).resolve().parents[1]

app = typer.Typer(
    help="Darkwatch — maritime dark-vessel detection from Sentinel-1 SAR + AIS.",
    rich_markup_mode="markdown",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _run_script(name: str, args: list[str]) -> None:
    """Invoke a script from the ``scripts/`` directory and stream output."""
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / name), *args]
    typer.echo(f"[darkwatch] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


@app.command()
def search_scenes(
    start: Annotated[str, typer.Option(help="Start date ISO (YYYY-MM-DD)")],
    end: Annotated[str, typer.Option(help="End date ISO (YYYY-MM-DD)")],
    operational_bbox: Annotated[
        str,
        typer.Option(help="Target theater bbox as W,S,E,N"),
    ] = "-120.8,34.3,-119.8,34.7",
    search_bbox: Annotated[
        str,
        typer.Option(help="CDSE search bbox as W,S,E,N"),
    ] = "-120.5,33.8,-119.0,34.6",
    max_results: Annotated[int, typer.Option(help="Maximum CDSE products to score")] = 50,
    min_overlap: Annotated[float, typer.Option(help="Minimum operational-bbox overlap (0-1)")] = 0.75,
    output: Annotated[Path, typer.Option(help="Path for scores JSON")] = REPO_ROOT / "data" / "raw" / "s1" / "scene_scores.json",
    theater_name: Annotated[str | None, typer.Option(help="Tag for the theater being scored")] = None,
) -> None:
    """Search CDSE and rank candidate Sentinel-1 scenes by ocean coverage."""
    args = [
        "--start", start,
        "--end", end,
        "--operational-bbox", operational_bbox,
        "--search-bbox", search_bbox,
        "--max-results", str(max_results),
        "--min-overlap", str(min_overlap),
        "--output", str(output),
    ]
    if theater_name:
        args.extend(["--theater-name", theater_name])
    _run_script("pick_ocean_scene.py", args)


@app.command()
def process_scene(
    product_id: Annotated[str, typer.Option(help="CDSE product UUID")],
    product_name: Annotated[str, typer.Option(help="SAFE product name")],
    date: Annotated[str, typer.Option(help="Acquisition date YYYY-MM-DD")],
    bbox: Annotated[str, typer.Option(help="Theater bbox W,S,E,N")],
    tile_size: Annotated[int, typer.Option(help="Tile size in pixels")] = 1024,
    overlap: Annotated[int, typer.Option(help="Tile overlap in pixels")] = 128,
    pol: Annotated[str, typer.Option(help="Comma-separated polarizations (vv,vh)")] = "vv,vh",
    model: Annotated[
        Path,
        typer.Option(help="Path to YOLO detector weights"),
    ] = REPO_ROOT / "models" / "detector_runs" / "darkwatch_yolov8n_ssdd_grd_v4" / "weights" / "best.pt",
    adaptive_percentiles: Annotated[str, typer.Option(help="Adaptive stretch percentiles (lo,hi)")] = "1,99",
    conf: Annotated[float, typer.Option(help="Detector confidence threshold")] = 0.05,
    ais_time_window: Annotated[int, typer.Option(help="AIS window +/- minutes around SAR time")] = 120,
    output_base: Annotated[str, typer.Option(help="Base output directory")] = "data/processed",
    theater: Annotated[str | None, typer.Option(help="Static-object catalog theater (santa_barbara, gulf, southern_california)")] = None,
    skip_download: Annotated[bool, typer.Option(help="Skip SAR download if already present")] = False,
    skip_ais: Annotated[bool, typer.Option(help="Skip NOAA AIS fetch")] = False,
    skip_fuse: Annotated[bool, typer.Option(help="Skip fusion step")] = False,
) -> None:
    """Download, prep, detect, fetch AIS, and fuse a single Sentinel-1 scene."""
    args = [
        "--product-id", product_id,
        "--product-name", product_name,
        "--date", date,
        "--bbox", bbox,
        "--tile-size", str(tile_size),
        "--overlap", str(overlap),
        "--pol", pol,
        "--model", str(model),
        "--adaptive-percentiles", adaptive_percentiles,
        "--conf", str(conf),
        "--ais-time-window-minutes", str(ais_time_window),
        "--output-base", output_base,
    ]
    if theater:
        args.extend(["--theater", theater])
    if skip_download:
        args.append("--skip-download")
    if skip_ais:
        args.append("--skip-ais")
    if skip_fuse:
        args.append("--skip-fuse")
    _run_script("process_scene.py", args)


@app.command()
def build_labels(
    scenes: Annotated[str, typer.Option(help="Scene group: santa_barbara, gulf, or southern_california")] = "santa_barbara",
    output: Annotated[
        Path,
        typer.Option(help="Output labels JSON path"),
    ] = REPO_ROOT / "data" / "processed" / "calibration_labels_v4_adaptive.json",
    base_labels: Annotated[Path | None, typer.Option(help="Existing authoritative labels JSON to preserve")] = None,
    theater_bbox: Annotated[
        str | None,
        typer.Option(help="Operational theater bbox W,S,E,N (default from script)"),
    ] = None,
) -> None:
    """Build ground-truth calibration labels from contacts + verdicts."""
    args = ["--scenes", scenes, "--output", str(output)]
    if base_labels:
        args.extend(["--base-labels", str(base_labels)])
    if theater_bbox:
        args.extend(["--theater", *theater_bbox.split(",")])
    _run_script("build_v4_calibration_labels.py", args)


@app.command()
def fit_calibration(
    labels: Annotated[
        Path,
        typer.Option(help="Labels JSON path"),
    ] = REPO_ROOT / "data" / "processed" / "calibration_labels_v4_adaptive_recal3.json",
    output: Annotated[
        Path,
        typer.Option(help="Output calibration model JSON path"),
    ] = REPO_ROOT / "data" / "processed" / "fusion_calibration_v4_adaptive_recal3.json",
    l2_penalty: Annotated[float, typer.Option(help="L2 regularization toward identity")] = 0.01,
) -> None:
    """Fit a learned calibration model on labeled contacts."""
    _run_script(
        "fit_calibration.py",
        ["--labels", str(labels), "--output", str(output), "--l2-penalty", str(l2_penalty)],
    )


@app.command()
def evaluate(
    labels: Annotated[
        Path,
        typer.Option(help="Labels JSON path"),
    ] = REPO_ROOT / "data" / "processed" / "calibration_labels.json",
    output_dir: Annotated[
        Path,
        typer.Option(help="Directory for calibration plots and report"),
    ] = REPO_ROOT / "notebooks" / "calibration",
    calibration_model: Annotated[Path | None, typer.Option(help="Optional calibration model JSON to apply")] = None,
    bins: Annotated[int, typer.Option(help="Number of reliability bins")] = 5,
) -> None:
    """Evaluate fusion calibration against ground-truth labels."""
    args = ["--labels", str(labels), "--output-dir", str(output_dir), "--bins", str(bins)]
    if calibration_model:
        args.extend(["--calibration-model", str(calibration_model)])
    _run_script("evaluate_calibration.py", args)


@app.command()
def serve(
    host: Annotated[str, typer.Option(help="Bind address")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Bind port")] = 8050,
    data_dir: Annotated[
        Path,
        typer.Option(help="Root directory containing processed scenes"),
    ] = REPO_ROOT / "data" / "processed",
) -> None:
    """Launch the analyst web dashboard (placeholder — backend under construction)."""
    typer.echo(f"Dashboard server not yet implemented; would serve from {data_dir} on {host}:{port}")
    raise typer.Exit(code=1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
