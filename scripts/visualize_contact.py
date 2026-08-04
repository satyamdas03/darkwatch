"""Visualize SAR contacts on their source tiles.

Usage:
    python scripts/visualize_contact.py \
        --contacts data/processed/detections_20240711/contacts.json \
        --manifest data/processed/s1a_20240711_channel/manifest.json \
        --output-dir notebooks/contact_viz
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import rasterio

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.detect.detector import _db_to_uint8


def _render_tile(
    rgb: np.ndarray,
    contact: dict,
    title: str,
    crop: tuple[int, int, int, int] | None = None,
) -> plt.Figure:
    """Render a tile (optionally cropped) with a detection bounding box.

    Args:
        rgb: uint8 RGB array (H, W, 3).
        contact: detection dict with pixel_bbox and metadata.
        title: figure title.
        crop: optional (xmin, ymin, xmax, ymax) crop in pixel coords.

    Returns:
        Matplotlib figure.
    """
    xmin, ymin, xmax, ymax = contact["pixel_bbox"]

    if crop is not None:
        cxmin, cymin, cxmax, cymax = crop
        rgb = rgb[cymin:cymax, cxmin:cxmax]
        xmin -= cxmin
        xmax -= cxmin
        ymin -= cymin
        ymax -= cymin
        figsize = (6, 6)
    else:
        figsize = (8, 8)

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(rgb)
    rect = patches.Rectangle(
        (xmin, ymin),
        xmax - xmin,
        ymax - ymin,
        linewidth=2,
        edgecolor="red",
        facecolor="none",
    )
    ax.add_patch(rect)
    ax.plot((xmin + xmax) / 2, (ymin + ymax) / 2, "ro", markersize=6)
    ax.set_title(title, fontsize=9)
    ax.axis("off")
    return fig


def visualize_contact(
    contact: dict,
    tile_path: Path,
    output_dir: Path,
    db_range: tuple[float, float] = (-25.0, -5.0),
    zoom_margin_px: int = 100,
) -> list[Path]:
    """Render full-tile and zoomed views of one contact.

    Returns:
        List of saved PNG paths.
    """
    with rasterio.open(tile_path) as src:
        arr = src.read(1)

    rgb = _db_to_uint8(arr, db_range=db_range)
    h, w = rgb.shape[:2]
    xmin, ymin, xmax, ymax = [int(round(v)) for v in contact["pixel_bbox"]]

    title = (
        f"{contact['contact_id']}\n"
        f"lon {contact['center_lon']:.5f}, lat {contact['center_lat']:.5f} | "
        f"conf {contact['confidence']:.2f} | "
        f"size {contact['width_m']:.0f}m x {contact['length_m']:.0f}m"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    # Full-tile context view.
    fig = _render_tile(rgb, contact, f"Context view\n{title}")
    full_path = output_dir / f"{contact['contact_id']}.png"
    fig.savefig(full_path, dpi=150, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    saved.append(full_path)
    print(f"Saved {full_path}")

    # Zoomed crop around the detection.
    cxmin = max(0, xmin - zoom_margin_px)
    cymin = max(0, ymin - zoom_margin_px)
    cxmax = min(w, xmax + zoom_margin_px)
    cymax = min(h, ymax + zoom_margin_px)
    if cxmax - cxmin > 20 and cymax - cymin > 20:
        fig = _render_tile(rgb, contact, f"Zoomed view\n{title}", crop=(cxmin, cymin, cxmax, cymax))
        zoom_path = output_dir / f"{contact['contact_id']}_zoom.png"
        fig.savefig(zoom_path, dpi=150, bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)
        saved.append(zoom_path)
        print(f"Saved {zoom_path}")

    return saved


def main() -> int:
    parser = argparse.ArgumentParser(description="Visualize SAR contacts on source tiles")
    parser.add_argument("--contacts", type=str, required=True, help="Path to contacts.json")
    parser.add_argument("--manifest", type=str, required=True, help="Path to tile manifest.json")
    parser.add_argument("--output-dir", type=str, default="notebooks/contact_viz")
    parser.add_argument("--db-lo", type=float, default=-25.0)
    parser.add_argument("--db-hi", type=float, default=-5.0)
    parser.add_argument("--zoom-margin", type=int, default=100, help="Pixels around bbox for zoomed crop")
    args = parser.parse_args()

    contacts_path = Path(args.contacts)
    manifest_path = Path(args.manifest)
    output_dir = Path(args.output_dir)

    if not contacts_path.exists():
        print(f"ERROR: contacts file not found: {contacts_path}", file=sys.stderr)
        return 1
    if not manifest_path.exists():
        print(f"ERROR: manifest file not found: {manifest_path}", file=sys.stderr)
        return 1

    contacts = json.loads(contacts_path.read_text())
    manifest = json.loads(manifest_path.read_text())

    # Build a map from tile_id to image path.
    tile_by_id: dict[str, Path] = {}
    for tile_path in manifest["tiles"]:
        tile_path = Path(tile_path)
        meta_path = tile_path.with_suffix(".json")
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
            tile_by_id[meta["tile_id"]] = tile_path

    db_range = (args.db_lo, args.db_hi)
    for contact in contacts:
        tile_id = contact["tile_id"]
        tile_path = tile_by_id.get(tile_id)
        if tile_path is None or not tile_path.exists():
            print(f"WARN: source tile not found for {tile_id}", file=sys.stderr)
            continue
        visualize_contact(contact, tile_path, output_dir, db_range=db_range, zoom_margin_px=args.zoom_margin)

    return 0


if __name__ == "__main__":
    sys.exit(main())
