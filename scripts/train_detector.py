"""Fine-tune a YOLO detector on the SSDD YOLO dataset.

Usage:
    python scripts/train_detector.py --data data/processed/ssdd_yolo/dataset.yaml \
        --model yolov8n.pt --epochs 50 --imgsz 640 --batch 4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.detect.detector import VesselDetector


def main() -> int:
    parser = argparse.ArgumentParser(description="Train Darkwatch vessel detector")
    parser.add_argument("--data", type=str, default=str(REPO_ROOT / "data" / "processed" / "ssdd_yolo" / "dataset.yaml"))
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Ultralytics hub name or model path")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=4, help="Batch size; reduce to 2 if OOM on 8 GB")
    parser.add_argument("--patience", type=int, default=10)
    parser.add_argument("--project", type=str, default=str(REPO_ROOT / "models" / "detector_runs"))
    parser.add_argument("--name", type=str, default="darkwatch_yolov8n_ssdd")
    parser.add_argument("--device", type=str, default=None, help="torch device (e.g. cuda:0)")
    args = parser.parse_args()

    data_yaml = Path(args.data)
    if not data_yaml.exists():
        print(f"ERROR: dataset.yaml not found: {data_yaml}", file=sys.stderr)
        print("Run scripts/prepare_ssdd.py first.", file=sys.stderr)
        return 1

    detector = VesselDetector(model_path=args.model, device=args.device)
    best_weights = detector.train(
        data_yaml=data_yaml,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        patience=args.patience,
        name=args.name,
        project=args.project,
    )

    print(f"Training complete. Best weights: {best_weights}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
