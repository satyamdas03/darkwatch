"""Run the vessel detector on prepared Darkwatch tiles.

Usage:
    python scripts/detect_tiles.py \
        --manifest data/processed/s1a_20240711_channel/manifest.json \
        --model yolov8n.pt \
        --output-dir data/processed/detections_20240711
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
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    detector = VesselDetector(model_path=args.model, device=args.device)
    detect_tiles(
        detector=detector,
        tile_manifest_path=manifest_path,
        output_dir=args.output_dir,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
