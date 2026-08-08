"""Run the vessel detector on prepared Darkwatch tiles.

Usage:
    python scripts/detect_tiles.py \
        --manifest data/processed/s1a_20240711_channel/manifest.json \
        --model models/detector_runs/darkwatch_yolov8n_ssdd/weights/best.pt \
        --output-dir data/processed/detections_20240711 \
        --db-lo -25 --db-hi -5 --conf 0.25 --pol vv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.detect.detector import VesselDetector, detect_tiles


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect vessels in Darkwatch tiles")
    parser.add_argument("--manifest", type=str, required=True)
    parser.add_argument("--model", type=str, default="yolov8n.pt")
    parser.add_argument("--output-dir", type=str, default=str(REPO_ROOT / "data" / "processed" / "detections"))
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.45)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--db-lo", type=float, default=-25.0, help="Lower dB bound for contrast stretch")
    parser.add_argument("--db-hi", type=float, default=-5.0, help="Upper dB bound for contrast stretch")
    parser.add_argument("--no-stretch", action="store_true", help="Skip dB-to-uint8 contrast stretch")
    parser.add_argument("--adaptive-percentiles", type=str, default=None, help="Per-tile percentile stretch, e.g. '1,99'")
    parser.add_argument("--pol", type=str, default=None, help="Comma-separated polarizations to process (e.g. vv,vh); default = all in manifest")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    detector = VesselDetector(model_path=args.model, device=args.device)
    db_range = None if args.no_stretch else (args.db_lo, args.db_hi)
    polarizations = tuple(p.strip().lower() for p in args.pol.split(",")) if args.pol else None
    adaptive_percentiles = None
    if args.adaptive_percentiles:
        p_lo, p_hi = (float(v) for v in args.adaptive_percentiles.split(","))
        adaptive_percentiles = (p_lo, p_hi)
    detect_tiles(
        detector=detector,
        tile_manifest_path=manifest_path,
        output_dir=args.output_dir,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
        db_range=db_range,
        adaptive_percentiles=adaptive_percentiles,
        polarizations=polarizations,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
