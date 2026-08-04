"""Build a quick mosaic from a tile manifest for visual validation.

Usage:
    python scripts/mosaic_tiles.py data/processed/s1a_20240711_channel/manifest.json --output notebooks/phase1_mosaic.png
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import Normalize


def load_tile(path: Path) -> np.ndarray:
    with rasterio.open(path) as src:
        img = src.read(1)
    return img


def build_mosaic(manifest_path: Path) -> np.ndarray:
    manifest = json.loads(manifest_path.read_text())
    tiles = [(Path(p), json.loads(Path(meta).read_text())) for p, meta in zip(manifest["tiles"], manifest["tile_meta"])]
    # Sort by row_off then col_off.
    tiles.sort(key=lambda x: (x[1]["row_off"], x[1]["col_off"]))

    # Determine canvas size from tile offsets.
    max_row = max(t[1]["row_off"] + t[1]["height"] for t in tiles)
    max_col = max(t[1]["col_off"] + t[1]["width"] for t in tiles)
    canvas = np.full((max_row, max_col), np.nan, dtype=np.float32)

    for img_path, meta in tiles:
        img = load_tile(img_path)
        r, c = meta["row_off"], meta["col_off"]
        h, w = img.shape
        # Use average in overlap regions.
        existing = canvas[r : r + h, c : c + w]
        mask = ~np.isnan(existing) & ~np.isnan(img)
        merged = np.where(mask, (existing + img) / 2.0, np.where(np.isnan(existing), img, existing))
        canvas[r : r + h, c : c + w] = merged

    return canvas


def main() -> int:
    parser = argparse.ArgumentParser(description="Mosaic Darkwatch tiles")
    parser.add_argument("manifest", type=str)
    parser.add_argument("--output", type=str, default="notebooks/phase1_mosaic.png")
    parser.add_argument("--vmin", type=float, default=-30)
    parser.add_argument("--vmax", type=float, default=0)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    canvas = build_mosaic(manifest_path)
    valid = canvas[~np.isnan(canvas)]
    print(f"Mosaic shape: {canvas.shape}")
    print(f"Valid pixels: {len(valid)} ({len(valid)/canvas.size:.2%})")
    print(f"Intensity dB: min={valid.min():.2f} max={valid.max():.2f} mean={valid.mean():.2f}")

    # Crop to the valid-data bounding box so the image is not dominated by
    # empty margins outside the theater window.
    valid_mask = ~np.isnan(canvas)
    rows = np.any(valid_mask, axis=1)
    cols = np.any(valid_mask, axis=0)
    if np.any(rows) and np.any(cols):
        r0, r1 = np.where(rows)[0][[0, -1]]
        c0, c1 = np.where(cols)[0][[0, -1]]
        canvas = canvas[r0 : r1 + 1, c0 : c1 + 1]

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(
        canvas,
        norm=Normalize(vmin=args.vmin, vmax=args.vmax),
        cmap="gray",
        aspect="auto",
    )
    ax.set_title(Path(args.manifest).parent.name)
    plt.colorbar(ax.images[0], ax=ax, fraction=0.02, label="sigma0 [dB]")
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Mosaic saved to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
