"""End-to-end pipeline for a new Sentinel-1 scene: download -> prep -> detect -> AIS -> fuse -> report.

Usage:
    python scripts/process_scene.py \
        --product-id cf535cd8-7b21-47f5-a3fc-7fc3e20af328 \
        --product-name S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3 \
        --date 2024-08-11 \
        --bbox "-120.8,34.3,-119.8,34.7" \
        --tile-size 1024 \
        --overlap 128 \
        --pol "vv,vh" \
        --model models/detector_runs/darkwatch_yolov8n_ssdd_grd_v4/weights/best.pt \
        --adaptive-percentiles "1,99" \
        --conf 0.05 \
        --output-base data/processed
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.adapters.copernicus_adapter import CopernicusAdapter


def _load_env(path: Path = REPO_ROOT / ".env") -> None:
    """Load key=value pairs from .env into process environment."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _run(cmd: list[str], cwd: Path = REPO_ROOT) -> None:
    """Run a subprocess command, streaming output, raising on failure."""
    print(f"\n[RUN] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Process a new Sentinel-1 scene end-to-end")
    parser.add_argument("--product-id", type=str, required=True, help="CDSE product UUID")
    parser.add_argument("--product-name", type=str, required=True, help="SAFE product name")
    parser.add_argument("--date", type=str, required=True, help="Acquisition date YYYY-MM-DD")
    parser.add_argument("--bbox", type=str, required=True, help="Theater bbox W,S,E,N")
    parser.add_argument("--tile-size", type=int, default=1024)
    parser.add_argument("--overlap", type=int, default=128)
    parser.add_argument("--pol", type=str, default="vv,vh")
    parser.add_argument("--model", type=str, default="models/detector_runs/darkwatch_yolov8n_ssdd_grd_v4/weights/best.pt")
    parser.add_argument("--adaptive-percentiles", type=str, default="1,99")
    parser.add_argument("--conf", type=float, default=0.05)
    parser.add_argument("--output-base", type=str, default="data/processed")
    parser.add_argument("--ais-time-window-minutes", type=int, default=120, help="AIS window +/- around SAR acquisition time")
    parser.add_argument("--theater", type=str, default=None, choices=["santa_barbara", "gulf"], help="Static-object catalog theater")
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--skip-prep", action="store_true")
    parser.add_argument("--skip-detect", action="store_true")
    parser.add_argument("--skip-ais", action="store_true")
    parser.add_argument("--skip-fuse", action="store_true")
    args = parser.parse_args()

    _load_env()

    safe_name = args.product_name.removesuffix(".SAFE")
    scene_dir_name = safe_name.lower().replace(".", "_")
    raw_dir = REPO_ROOT / "data" / "raw" / "s1"
    safe_dir = raw_dir / f"{safe_name}.SAFE"
    output_dir = REPO_ROOT / args.output_base / scene_dir_name
    detections_dir = REPO_ROOT / args.output_base / f"detections_{args.date.replace('-', '')}_v4_adaptive"
    fusion_dir = REPO_ROOT / args.output_base / f"fusion_{args.date.replace('-', '')}_v4_adaptive"
    ais_csv = REPO_ROOT / "data" / "external" / "ais" / f"ais_{args.date}_clipped.csv"

    state = {
        "product_id": args.product_id,
        "product_name": args.product_name,
        "date": args.date,
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "steps": [],
    }
    state_path = output_dir / "processing_state.json"
    output_dir.mkdir(parents=True, exist_ok=True)

    def _record(step: str, status: str, **extra) -> None:
        entry = {"step": step, "status": status, "at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
        entry.update(extra)
        state["steps"].append(entry)
        state_path.write_text(json.dumps(state, indent=2))
        print(f"[STATE] {step}: {status}")

    try:
        if not args.skip_download:
            _record("download", "started")
            adapter = CopernicusAdapter()
            safe_path = adapter.download_by_id(args.product_id, raw_dir, extract=True)
            print(f"[DONE] Downloaded and extracted to {safe_path}")
            _record("download", "completed", safe_dir=str(safe_path))
        else:
            print("[SKIP] download")
            _record("download", "skipped")

        if not args.skip_prep:
            _record("prep", "started")
            _run([
                sys.executable, "scripts/prep_s1.py", str(safe_dir),
                "--output-dir", str(output_dir),
                "--bbox", args.bbox,
                "--tile-size", str(args.tile_size),
                "--overlap", str(args.overlap),
                "--pol", args.pol,
            ])
            _record("prep", "completed", manifest=str(output_dir / "manifest.json"))
        else:
            print("[SKIP] prep")
            _record("prep", "skipped")

        manifest_path = output_dir / "manifest.json"
        if not args.skip_detect:
            _record("detect", "started")
            _run([
                sys.executable, "scripts/detect_tiles.py",
                "--manifest", str(manifest_path),
                "--model", args.model,
                "--output-dir", str(detections_dir),
                "--adaptive-percentiles", args.adaptive_percentiles,
                "--conf", str(args.conf),
                "--pol", args.pol,
            ])
            _record("detect", "completed", contacts=str(detections_dir / "contacts.json"))
        else:
            print("[SKIP] detect")
            _record("detect", "skipped")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        acquisition_time = manifest["acquisition_time"]

        if not args.skip_ais:
            _record("ais", "started")
            _run([
                sys.executable, "scripts/fetch_ais.py",
                "--date", args.date,
                "--bbox", args.bbox,
                "--center-time", acquisition_time,
                "--time-window-minutes", str(args.ais_time_window_minutes),
                "--output-dir", str(REPO_ROOT / "data" / "external" / "ais"),
            ])
            _record("ais", "completed", csv=str(ais_csv))
        else:
            print("[SKIP] ais")
            _record("ais", "skipped")

        contacts_path = detections_dir / "contacts.json"
        if not args.skip_fuse and contacts_path.exists() and ais_csv.exists():
            _record("fuse", "started")
            fuse_cmd = [
                sys.executable, "scripts/fuse_contacts.py",
                "--contacts", str(contacts_path),
                "--ais", str(ais_csv),
                "--output-dir", str(fusion_dir),
            ]
            if args.theater:
                fuse_cmd.extend(["--theater", args.theater])
            _run(fuse_cmd)
            _record("fuse", "completed", verdicts=str(fusion_dir / "verdicts.json"))
        else:
            print("[SKIP] fuse")
            _record("fuse", "skipped")

        # Optional report + map.
        verdicts_path = fusion_dir / "verdicts.json"
        summary_path = fusion_dir / "summary.json"
        if verdicts_path.exists() and summary_path.exists() and ais_csv.exists():
            _record("report", "started")
            _run([
                sys.executable, "scripts/fusion_report.py",
                "--contacts", str(contacts_path),
                "--ais", str(ais_csv),
                "--verdicts", str(verdicts_path),
                "--summary", str(summary_path),
                "--output", str(REPO_ROOT / "notebooks" / f"fusion_{args.date.replace('-', '')}_report.md"),
            ])
            _record("report", "completed")

            _record("map", "started")
            _run([
                sys.executable, "scripts/visualize_fusion.py",
                "--contacts", str(contacts_path),
                "--ais", str(ais_csv),
                "--verdicts", str(verdicts_path),
                "--output", str(REPO_ROOT / "notebooks" / f"fusion_{args.date.replace('-', '')}_map.html"),
            ])
            _record("map", "completed")

        state["finished_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        state["status"] = "completed"
        state_path.write_text(json.dumps(state, indent=2))
        print("\n[ALL DONE]")
        return 0

    except Exception as exc:
        state["status"] = "failed"
        state["error"] = str(exc)
        state["finished_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        state_path.write_text(json.dumps(state, indent=2))
        print(f"\n[FAILED] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
