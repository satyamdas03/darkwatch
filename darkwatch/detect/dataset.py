"""Convert public SAR ship detection datasets into Ultralytics YOLO training layout.

SSDD is distributed in COCO format. This module converts COCO [x, y, w, h]
annotations to YOLO normalized [x_center, y_center, w, h] text files and
creates the directory structure Ultralytics expects:

    output_dir/
      dataset.yaml
      images/
        train/
        val/
      labels/
        train/
        val/
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


CLASS_NAMES = ["ship"]


def _coco_bbox_to_yolo(bbox: list[float], img_w: int, img_h: int) -> tuple[float, float, float, float]:
    """Convert COCO bbox [x, y, w, h] to YOLO normalized [cx, cy, w, h]."""
    x, y, w, h = bbox
    cx = (x + w / 2.0) / img_w
    cy = (y + h / 2.0) / img_h
    nw = w / img_w
    nh = h / img_h
    return (
        max(0.0, min(1.0, cx)),
        max(0.0, min(1.0, cy)),
        max(0.0, min(1.0, nw)),
        max(0.0, min(1.0, nh)),
    )


def _split_train_val(image_ids: list[int], val_fraction: float = 0.15, seed: int = 42) -> tuple[set[int], set[int]]:
    """Deterministic train/val split by image id."""
    import random

    rng = random.Random(seed)
    shuffled = image_ids[:]
    rng.shuffle(shuffled)
    n_val = max(1, int(len(shuffled) * val_fraction))
    val_ids = set(shuffled[:n_val])
    train_ids = set(shuffled[n_val:])
    return train_ids, val_ids


def _write_split(
    coco: dict,
    image_dir: Path,
    output_dir: Path,
    split_ids: set[int],
    split_name: str,
) -> int:
    """Copy images and write YOLO labels for a split. Returns number of samples."""
    out_img_dir = output_dir / "images" / split_name
    out_lbl_dir = output_dir / "labels" / split_name
    out_img_dir.mkdir(parents=True, exist_ok=True)
    out_lbl_dir.mkdir(parents=True, exist_ok=True)

    # Index annotations by image id.
    anns_by_image: dict[int, list[dict]] = {}
    for ann in coco["annotations"]:
        anns_by_image.setdefault(ann["image_id"], []).append(ann)

    count = 0
    for img in coco["images"]:
        img_id = img["id"]
        if img_id not in split_ids:
            continue

        src_img = image_dir / img["file_name"]
        if not src_img.exists():
            continue

        dst_img = out_img_dir / src_img.name
        shutil.copy2(src_img, dst_img)

        # Verify size from disk; fall back to annotation if needed.
        try:
            with Image.open(dst_img) as im:
                img_w, img_h = im.size
        except Exception:
            img_w, img_h = img["width"], img["height"]

        lines = []
        for ann in anns_by_image.get(img_id, []):
            cx, cy, w, h = _coco_bbox_to_yolo(ann["bbox"], img_w, img_h)
            # SSDD categories use id 0 for ship.
            cls_id = ann.get("category_id", 0)
            lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

        label_name = src_img.stem + ".txt"
        (out_lbl_dir / label_name).write_text("\n".join(lines))
        count += 1

    return count


def coco_to_yolo_dataset(
    train_coco_path: Path | str,
    train_image_dir: Path | str,
    output_dir: Path | str,
    val_coco_path: Path | str | None = None,
    val_image_dir: Path | str | None = None,
    val_fraction: float = 0.15,
    seed: int = 42,
) -> dict:
    """Convert a COCO-format SSDD split into a YOLO dataset.

    Args:
        train_coco_path: path to COCO train annotations JSON.
        train_image_dir: directory containing train images.
        output_dir: where to write the YOLO dataset.
        val_coco_path: optional separate COCO validation annotations JSON.
        val_image_dir: directory for validation images (required if val_coco_path given).
        val_fraction: fraction of training images to hold out for validation when no
            separate val split is provided.
        seed: random seed for train/val split.

    Returns:
        Dict with split counts and path to dataset.yaml.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_coco = json.loads(Path(train_coco_path).read_text())

    if val_coco_path is not None:
        val_coco = json.loads(Path(val_coco_path).read_text())
        val_ids = {img["id"] for img in val_coco["images"]}
        train_ids = {img["id"] for img in train_coco["images"]}
        # Write both splits.
        train_count = _write_split(train_coco, Path(train_image_dir), output_dir, train_ids, "train")
        val_count = _write_split(val_coco, Path(val_image_dir), output_dir, val_ids, "val")
    else:
        image_ids = [img["id"] for img in train_coco["images"]]
        train_ids, val_ids = _split_train_val(image_ids, val_fraction, seed)
        train_count = _write_split(train_coco, Path(train_image_dir), output_dir, train_ids, "train")
        val_count = _write_split(train_coco, Path(train_image_dir), output_dir, val_ids, "val")

    yaml_path = output_dir / "dataset.yaml"
    yaml_path.write_text(
        f"""path: {output_dir.resolve().as_posix()}  # dataset root absolute path
train: images/train
val: images/val
nc: {len(CLASS_NAMES)}
names: {CLASS_NAMES}
"""
    )

    return {
        "output_dir": str(output_dir.resolve()),
        "yaml_path": str(yaml_path.resolve()),
        "train_count": train_count,
        "val_count": val_count,
    }
