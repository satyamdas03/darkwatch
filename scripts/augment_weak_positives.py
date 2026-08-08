"""Photometric augmentation for weak positive GRD chips.

Generates N augmented copies of each positive chip in a source YOLO directory.
Only photometric / speckle transforms are used so bounding boxes remain valid.
Output chips are saved to a new YOLO-format directory alongside a manifest.

Usage:
    python scripts/augment_weak_positives.py \
        --input data/processed/grd_chips_jul23_loose \
        --output data/processed/grd_chips_20240723_weak_aug \
        --num-augs 50 --seed 42
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import cv2
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def _photometric_aug(img: np.ndarray, rng: random.Random) -> np.ndarray:
    """Apply a random photometric augmentation to a uint8 RGB chip.

    Keeps geometry fixed, so YOLO bboxes stay valid.
    """
    out = img.astype(np.float32)

    # Random brightness / contrast shift (linear: out = (out - 127.5) * scale + 127.5 + shift)
    scale = rng.uniform(0.7, 1.4)
    shift = rng.uniform(-25.0, 25.0)
    out = (out - 127.5) * scale + 127.5 + shift

    # Speckle-like multiplicative noise (SAR coherent speckle model)
    if rng.random() < 0.7:
        speckle_std = rng.uniform(0.03, 0.12)
        noise = np.random.normal(0.0, speckle_std, out.shape).astype(np.float32)
        out = out * (1.0 + noise)

    # Additive Gaussian noise
    if rng.random() < 0.5:
        gauss_std = rng.uniform(2.0, 8.0)
        out = out + np.random.normal(0.0, gauss_std, out.shape).astype(np.float32)

    # Mild blur
    if rng.random() < 0.3:
        k = rng.choice([3, 5])
        out = cv2.GaussianBlur(out, (k, k), 0)

    # Gamma / power-law (simulate different dB-to-uint8 mappings)
    if rng.random() < 0.4:
        gamma = rng.uniform(0.6, 1.5)
        out = np.sign(out) * np.power(np.abs(out) / 255.0, gamma) * 255.0

    # Salt-and-pepper (impulse noise from SAR processing / bright pixels)
    if rng.random() < 0.2:
        salt_prob = rng.uniform(0.001, 0.005)
        pepper_prob = rng.uniform(0.001, 0.005)
        mask_salt = np.random.random(out.shape[:2]) < salt_prob
        mask_pepper = np.random.random(out.shape[:2]) < pepper_prob
        for c in range(out.shape[2]):
            out[:, :, c][mask_salt] = 255.0
            out[:, :, c][mask_pepper] = 0.0

    out = np.clip(out, 0.0, 255.0).astype(np.uint8)
    return out


def _collect_positives(input_dir: Path) -> list[tuple[Path, Path]]:
    """Return (image_path, label_path) for chips with non-empty YOLO labels."""
    image_dir = input_dir / "images"
    label_dir = input_dir / "labels"
    samples: list[tuple[Path, Path]] = []
    for img_path in sorted(image_dir.glob("*.png")):
        lbl_path = label_dir / f"{img_path.stem}.txt"
        if lbl_path.exists() and lbl_path.read_text().strip():
            samples.append((img_path, lbl_path))
    return samples


def augment_weak_positives(
    input_dir: Path,
    output_dir: Path,
    num_augs: int,
    seed: int,
) -> dict:
    """Generate photometric augmentations of weak positive chips."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "images").mkdir(exist_ok=True)
    (output_dir / "labels").mkdir(exist_ok=True)

    rng = random.Random(seed)
    positives = _collect_positives(input_dir)

    generated = 0
    for img_path, lbl_path in positives:
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"WARN: could not read {img_path}")
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        label_text = lbl_path.read_text()

        for i in range(num_augs):
            aug_img = _photometric_aug(img, rng)
            sample_name = f"{img_path.stem}_aug{i:03d}"
            out_img = output_dir / "images" / f"{sample_name}.png"
            out_lbl = output_dir / "labels" / f"{sample_name}.txt"
            cv2.imwrite(str(out_img), cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))
            out_lbl.write_text(label_text)
            generated += 1

    manifest = {
        "input_dir": str(input_dir.resolve()),
        "output_dir": str(output_dir.resolve()),
        "num_augs": num_augs,
        "seed": seed,
        "source_positives": len(positives),
        "generated": generated,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Photometric augmentation for weak-positive GRD chips"
    )
    parser.add_argument("--input", type=str, required=True, help="source YOLO chip directory")
    parser.add_argument("--output", type=str, required=True, help="output YOLO chip directory")
    parser.add_argument("--num-augs", type=int, default=50, help="augmented copies per positive")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    manifest = augment_weak_positives(
        input_dir=Path(args.input),
        output_dir=Path(args.output),
        num_augs=args.num_augs,
        seed=args.seed,
    )

    print(f"Weak-positive augmentation complete: {manifest['output_dir']}")
    print(f"  source positives: {manifest['source_positives']}")
    print(f"  generated chips:  {manifest['generated']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
