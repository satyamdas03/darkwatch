"""Extract real Sentinel-1 GRD training chips from Darkwatch contacts.

Creates a YOLO-format dataset of positive (vessel) chips from labeled contacts
and negative (empty ocean) chips from water-only tiles. Each chip is converted
from float dB to uint8 RGB using a configurable or adaptive contrast stretch.

Usage:
    python scripts/extract_grd_chips.py \
        --contacts data/processed/detections_20240718/contacts.json \
        --manifest data/processed/s1a_20240718_channel/manifest.json \
        --labels data/processed/calibration_labels.json \
        --output-dir data/processed/grd_chips \
        --chip-size 256 --negatives-per-scene 20
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.detect.contact import Contact


def _db_to_uint8(arr: np.ndarray, db_range: tuple[float, float] | None = None) -> np.ndarray:
    """Convert a dB chip to uint8 RGB.

    If ``db_range`` is None, an adaptive percentile stretch is used
    (1st and 99th percentile of the chip mapped to 0 and 255).
    """
    if db_range is None:
        finite = arr[np.isfinite(arr)]
        if len(finite) == 0:
            lo, hi = -30.0, -10.0
        else:
            lo, hi = float(np.percentile(finite, 1)), float(np.percentile(finite, 99))
            if lo == hi:
                hi = lo + 1.0
    else:
        lo, hi = db_range

    arr = np.nan_to_num(arr, nan=lo, posinf=hi, neginf=lo)
    stretched = np.clip((arr - lo) / (hi - lo), 0.0, 1.0)
    uint8 = (stretched * 255.0).astype(np.uint8)
    return np.stack([uint8, uint8, uint8], axis=-1)


def _load_tile_by_id(tile_id: str, manifest: dict) -> Path:
    """Find the GeoTIFF path for a tile_id in a manifest."""
    for img_path, meta_path in zip(manifest["tiles"], manifest["tile_meta"]):
        meta = json.loads(Path(meta_path).read_text())
        if meta["tile_id"] == tile_id:
            return Path(img_path)
    raise ValueError(f"tile_id {tile_id} not found in manifest")


def _chip_window(
    tile_meta: dict,
    center_px: tuple[float, float],
    chip_size: int,
) -> tuple[int, int, int, int]:
    """Compute a clipped chip window around a pixel center."""
    cx, cy = center_px
    width = tile_meta["width"]
    height = tile_meta["height"]
    x1 = max(0, min(width - chip_size, int(round(cx - chip_size / 2))))
    y1 = max(0, min(height - chip_size, int(round(cy - chip_size / 2))))
    w = min(chip_size, width - x1)
    h = min(chip_size, height - y1)
    return x1, y1, w, h


def _center_from_bbox(bbox: tuple[float, float, float, float]) -> tuple[float, float]:
    xmin, ymin, xmax, ymax = bbox
    return (xmin + xmax) / 2.0, (ymin + ymax) / 2.0


def _bbox_from_window(
    tile_bbox: tuple[float, float, float, float],
    window: tuple[int, int, int, int],
    chip_size: int,
) -> tuple[float, float, float, float]:
    """Convert a pixel bbox in the full tile to a chip-normalized YOLO bbox.

    Returns [cx, cy, w, h] in chip-normalized coordinates (0..1).
    """
    xmin, ymin, xmax, ymax = tile_bbox
    wx, wy, ww, wh = window

    # Clamp contact bbox to the chip window.
    cx_min = max(0.0, xmin - wx)
    cy_min = max(0.0, ymin - wy)
    cx_max = min(float(ww), xmax - wx)
    cy_max = min(float(wh), ymax - wy)

    cx = (cx_min + cx_max) / 2.0 / ww
    cy = (cy_min + cy_max) / 2.0 / wh
    w = max(0.0, cx_max - cx_min) / ww
    h = max(0.0, cy_max - cy_min) / wh
    return cx, cy, w, h


def _extract_chip(
    tile_path: Path,
    window: tuple[int, int, int, int],
    db_range: tuple[float, float] | None,
) -> tuple[np.ndarray, int, int]:
    """Read a chip from a tile and convert to uint8 RGB. Returns (rgb, w, h)."""
    with rasterio.open(tile_path) as ds:
        win = rasterio.windows.Window(*window)
        chip = ds.read(1, window=win)
    rgb = _db_to_uint8(chip, db_range)
    h, w = rgb.shape[:2]
    return rgb, w, h


def _contact_to_chip(
    contact: Contact,
    manifest: dict,
    output_dir: Path,
    chip_size: int,
    db_range: tuple[float, float] | None,
    sample_name: str,
) -> dict:
    """Extract one positive chip from a contact and write image + YOLO label."""
    tile_path = _load_tile_by_id(contact.tile_id, manifest)
    tile_meta = json.loads(tile_path.with_suffix(".json").read_text())
    cx, cy = _center_from_bbox(contact.pixel_bbox)
    window = _chip_window(tile_meta, (cx, cy), chip_size)

    rgb, w, h = _extract_chip(tile_path, window, db_range)
    if w < 32 or h < 32:
        raise ValueError(f"chip too small: {w}x{h}")

    img_path = output_dir / "images" / f"{sample_name}.png"
    lbl_path = output_dir / "labels" / f"{sample_name}.txt"
    img_path.parent.mkdir(parents=True, exist_ok=True)
    lbl_path.parent.mkdir(parents=True, exist_ok=True)

    Image.fromarray(rgb).save(img_path)

    yolo_bbox = _bbox_from_window(contact.pixel_bbox, window, chip_size)
    lbl_path.write_text(f"0 {yolo_bbox[0]:.6f} {yolo_bbox[1]:.6f} {yolo_bbox[2]:.6f} {yolo_bbox[3]:.6f}")

    return {
        "sample": sample_name,
        "contact_id": contact.contact_id,
        "tile_id": contact.tile_id,
        "window": window,
        "label": "positive",
    }


def _extract_negatives(
    manifest: dict,
    contacts: list[Contact],
    output_dir: Path,
    chip_size: int,
    db_range: tuple[float, float] | None,
    negatives_per_scene: int,
    rng: random.Random,
) -> list[dict]:
    """Extract empty-ocean negative chips avoiding existing contact centers."""
    # Build a set of protected pixel centers per tile.
    protected: dict[str, list[tuple[float, float]]] = {}
    for c in contacts:
        protected.setdefault(c.tile_id, []).append(_center_from_bbox(c.pixel_bbox))

    records = []
    img_dir = output_dir / "images"
    lbl_dir = output_dir / "labels"
    img_dir.mkdir(parents=True, exist_ok=True)
    lbl_dir.mkdir(parents=True, exist_ok=True)

    for img_path, meta_path in zip(manifest["tiles"], manifest["tile_meta"]):
        meta = json.loads(Path(meta_path).read_text())
        tile_id = meta["tile_id"]
        width = meta["width"]
        height = meta["height"]
        if width < chip_size or height < chip_size:
            continue

        tile_path = Path(img_path)
        guards = protected.get(tile_id, [])

        attempts = 0
        extracted = 0
        while extracted < negatives_per_scene and attempts < negatives_per_scene * 50:
            attempts += 1
            x1 = rng.randint(0, width - chip_size)
            y1 = rng.randint(0, height - chip_size)
            cx = x1 + chip_size / 2
            cy = y1 + chip_size / 2

            # Reject if too close to an existing contact center.
            if any(
                abs(cx - gx) < chip_size and abs(cy - gy) < chip_size
                for gx, gy in guards
            ):
                continue

            window = (x1, y1, chip_size, chip_size)
            try:
                rgb, w, h = _extract_chip(tile_path, window, db_range)
            except Exception:
                continue
            if w < chip_size or h < chip_size:
                continue

            sample_name = f"neg_{tile_id}_x{x1}_y{y1}"
            img_path_out = img_dir / f"{sample_name}.png"
            lbl_path_out = lbl_dir / f"{sample_name}.txt"
            Image.fromarray(rgb).save(img_path_out)
            lbl_path_out.write_text("")  # empty label = background
            records.append(
                {
                    "sample": sample_name,
                    "tile_id": tile_id,
                    "window": window,
                    "label": "negative",
                }
            )
            extracted += 1

    return records


def build_grd_dataset(
    contacts_json: Path,
    manifest_json: Path,
    labels_json: Path,
    output_dir: Path,
    chip_size: int = 256,
    db_range: tuple[float, float] | None = None,
    negatives_per_scene: int = 20,
    seed: int = 42,
) -> dict:
    """Build a YOLO-format dataset from labeled GRD contacts and negative ocean chips."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    contacts_raw = json.loads(contacts_json.read_text())
    contacts = [Contact(**c) for c in contacts_raw]
    manifest = json.loads(manifest_json.read_text())
    labels = json.loads(labels_json.read_text())

    label_by_id = {lb["contact_id"]: lb["label"] for lb in labels["labels"]}

    records = []
    positives = 0
    for contact in contacts:
        label = label_by_id.get(contact.contact_id)
        if label is None:
            continue
        if label in ("UNKNOWN",):
            continue
        sample_name = f"grd_{contact.contact_id}"
        try:
            rec = _contact_to_chip(
                contact, manifest, output_dir, chip_size, db_range, sample_name
            )
            rec["ground_truth"] = label
            records.append(rec)
            positives += 1
        except Exception as exc:
            print(f"WARN: failed to extract chip for {contact.contact_id}: {exc}")

    negative_records = _extract_negatives(
        manifest, contacts, output_dir, chip_size, db_range, negatives_per_scene, rng
    )
    records.extend(negative_records)

    return {
        "output_dir": str(output_dir.resolve()),
        "positives": positives,
        "negatives": len(negative_records),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract GRD training chips from Darkwatch contacts")
    parser.add_argument("--contacts", type=str, required=True, help="contacts.json from detect_tiles")
    parser.add_argument("--manifest", type=str, required=True, help="tile manifest.json")
    parser.add_argument("--labels", type=str, required=True, help="calibration_labels.json")
    parser.add_argument("--output-dir", type=str, required=True)
    parser.add_argument("--chip-size", type=int, default=256)
    parser.add_argument("--db-lo", type=float, default=None, help="lower dB bound; omit for adaptive stretch")
    parser.add_argument("--db-hi", type=float, default=None, help="upper dB bound; omit for adaptive stretch")
    parser.add_argument("--negatives-per-scene", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    db_range = (args.db_lo, args.db_hi) if args.db_lo is not None and args.db_hi is not None else None

    result = build_grd_dataset(
        contacts_json=Path(args.contacts),
        manifest_json=Path(args.manifest),
        labels_json=Path(args.labels),
        output_dir=Path(args.output_dir),
        chip_size=args.chip_size,
        db_range=db_range,
        negatives_per_scene=args.negatives_per_scene,
        seed=args.seed,
    )

    print(f"GRD chip dataset: {result['output_dir']}")
    print(f"  positives: {result['positives']}")
    print(f"  negatives: {result['negatives']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
