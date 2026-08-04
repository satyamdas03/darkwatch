"""Convert SSDD COCO annotations to YOLO training format.

Usage:
    python scripts/prepare_ssdd.py --output-dir data/processed/ssdd_yolo --val-fraction 0.15
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.detect.dataset import coco_to_yolo_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert SSDD to YOLO format")
    parser.add_argument("--ssdd-dir", type=str, default=str(REPO_ROOT / "data" / "external" / "ssdd" / "Official-SSDD-OPEN" / "BBox_SSDD" / "coco_style"))
    parser.add_argument("--output-dir", type=str, default=str(REPO_ROOT / "data" / "processed" / "ssdd_yolo"))
    parser.add_argument("--val-fraction", type=float, default=0.15)
    args = parser.parse_args()

    ssdd_dir = Path(args.ssdd_dir)
    if not ssdd_dir.exists():
        print(f"ERROR: SSDD directory not found: {ssdd_dir}", file=sys.stderr)
        print("Download it first from https://github.com/TianwenZhang0825/Official-SSDD", file=sys.stderr)
        return 1

    result = coco_to_yolo_dataset(
        train_coco_path=ssdd_dir / "annotations" / "train.json",
        train_image_dir=ssdd_dir / "images" / "train",
        output_dir=args.output_dir,
        val_coco_path=ssdd_dir / "annotations" / "test.json",
        val_image_dir=ssdd_dir / "images" / "test",
    )

    print(f"YOLO dataset prepared at {result['output_dir']}")
    print(f"  train images: {result['train_count']}")
    print(f"  val images:   {result['val_count']}")
    print(f"  dataset.yaml: {result['yaml_path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
