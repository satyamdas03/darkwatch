"""Build a mixed YOLO dataset from a base dataset plus GRD chip directories.

Usage:
    python scripts/build_mixed_dataset.py \
        --base data/processed/ssdd_yolo \
        --grd data/processed/grd_chips_20240711 \
        --grd data/processed/grd_chips_20240718 \
        --grd data/processed/grd_chips_20240723_loose \
        --output data/processed/mixed_ssdd_grd_v2 \
        --val-fraction 0.15 --seed 42
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def _collect_yolo_samples(source_dir: Path) -> list[tuple[Path, Path]]:
    """Return (image_path, label_path) pairs for a YOLO-format source directory.

    Recursively scans ``images/`` for ``*.png``, ``*.jpg``, ``*.jpeg`` and pairs
    each with the corresponding ``labels/`` ``.txt`` file at the same relative
    path. This handles both flat datasets and datasets already split into
    ``train`` / ``val`` subdirectories.
    """
    image_dir = source_dir / "images"
    label_dir = source_dir / "labels"
    samples: list[tuple[Path, Path]] = []
    for ext in ("**/*.png", "**/*.jpg", "**/*.jpeg"):
        for img_path in sorted(image_dir.glob(ext)):
            rel = img_path.relative_to(image_dir)
            lbl_path = label_dir / rel.with_suffix(".txt")
            if lbl_path.exists():
                samples.append((img_path, lbl_path))
    return samples


def build_mixed_dataset(
    base_dir: Path,
    grd_dirs: list[Path],
    output_dir: Path,
    val_fraction: float = 0.15,
    seed: int = 42,
) -> dict:
    """Merge a base YOLO dataset and GRD chip dirs into a single YOLO dataset.

    Splits all samples into train/val using a fixed seed. Image and label files
    are copied into ``images/train``, ``images/val``, ``labels/train``,
    ``labels/val``. Empty label files are preserved as background samples.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(seed)

    all_samples: list[tuple[Path, Path, str]] = []
    for img_path, lbl_path in _collect_yolo_samples(base_dir):
        all_samples.append((img_path, lbl_path, "base"))
    for grd_dir in grd_dirs:
        for img_path, lbl_path in _collect_yolo_samples(grd_dir):
            all_samples.append((img_path, lbl_path, grd_dir.name))

    rng.shuffle(all_samples)
    n_val = max(1, int(round(len(all_samples) * val_fraction)))
    val_samples = all_samples[:n_val]
    train_samples = all_samples[n_val:]

    splits = {"train": train_samples, "val": val_samples}
    stats: dict[str, dict] = {}
    for split_name, samples in splits.items():
        split_img_dir = output_dir / "images" / split_name
        split_lbl_dir = output_dir / "labels" / split_name
        split_img_dir.mkdir(parents=True, exist_ok=True)
        split_lbl_dir.mkdir(parents=True, exist_ok=True)

        source_counts: dict[str, int] = {}
        positives = 0
        negatives = 0
        for img_path, lbl_path, source in samples:
            source_counts[source] = source_counts.get(source, 0) + 1
            dst_img = split_img_dir / img_path.name
            dst_lbl = split_lbl_dir / f"{img_path.stem}.txt"
            shutil.copy2(img_path, dst_img)
            shutil.copy2(lbl_path, dst_lbl)
            lbl_text = lbl_path.read_text().strip()
            if lbl_text:
                positives += 1
            else:
                negatives += 1

        stats[split_name] = {
            "total": len(samples),
            "positives": positives,
            "negatives": negatives,
            "sources": source_counts,
        }

    yaml_path = output_dir / "dataset.yaml"
    yaml_path.write_text(
        f"path: {output_dir.resolve()}\n"
        f"train: images/train\n"
        f"val: images/val\n"
        f"nc: 1\n"
        f"names: ['ship']\n"
    )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "base_dir": str(base_dir.resolve()),
                "grd_dirs": [str(d.resolve()) for d in grd_dirs],
                "val_fraction": val_fraction,
                "seed": seed,
                "stats": stats,
            },
            indent=2,
        )
    )

    return {
        "output_dir": str(output_dir.resolve()),
        "yaml_path": str(yaml_path.resolve()),
        "train": stats["train"],
        "val": stats["val"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a mixed SSDD + GRD YOLO dataset")
    parser.add_argument("--base", type=str, required=True, help="base YOLO dataset directory")
    parser.add_argument("--grd", type=str, action="append", default=[], help="GRD chip directory (repeatable)")
    parser.add_argument("--output", type=str, required=True, help="output dataset directory")
    parser.add_argument("--val-fraction", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    result = build_mixed_dataset(
        base_dir=Path(args.base),
        grd_dirs=[Path(d) for d in args.grd],
        output_dir=Path(args.output),
        val_fraction=args.val_fraction,
        seed=args.seed,
    )

    print(f"Mixed dataset built at {result['output_dir']}")
    print(f"  train: {result['train']['total']} ({result['train']['positives']} pos, {result['train']['negatives']} neg)")
    print(f"  val:   {result['val']['total']} ({result['val']['positives']} pos, {result['val']['negatives']} neg)")
    print(f"  yaml:  {result['yaml_path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
