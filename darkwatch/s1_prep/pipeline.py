"""End-to-end S1 prep pipeline: read .SAFE → calibrate → land-mask → tile.

This is the Phase 1 automation layer. It is intentionally file-system-based and
provider-agnostic: give it a local .SAFE directory, get analysis-ready tiles.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import rasterio

from .calibrate import read_and_calibrate
from .geocode import S1Geocoder, build_geocoder
from .land_mask import apply_water_mask, compute_water_mask
from .reader import Polarization, read_safe_directory
from .tiler import S1Tile, make_tiles, save_tile


# Default theater for the first acquired scene (S1A pass 2024-07-01).
# The scene footprint is lat 34.18–36.08 N, lon -119.09 to -115.99 W.
# The Santa Barbara Channel proper is only partially covered by this pass;
# the western edge of the coverage is over open water near the channel islands.
DEFAULT_THEATER_BBOX = (-119.05, 34.55, -118.6, 34.75)


def prep_scene(
    safe_dir: Path,
    output_dir: Path,
    theater_bbox: tuple[float, float, float, float] = DEFAULT_THEATER_BBOX,
    tile_size: int = 512,
    overlap: int = 64,
    polarizations: Iterable[Polarization] = ("vv",),
    buffer_deg: float = 0.005,
    skip_existing: bool = True,
) -> dict:
    """Run the full S1 prep pipeline on one .SAFE scene.

    Args:
        safe_dir: path to extracted .SAFE directory.
        output_dir: where to write tiles and metadata.
        theater_bbox: WGS84 bbox (W, S, E, N) to crop before tiling.
        tile_size: pixel size of output tiles.
        overlap: pixel overlap between adjacent tiles.
        polarizations: which polarizations to process.
        buffer_deg: coastal buffer in degrees for land masking.
        skip_existing: if True, do not overwrite existing tiles.

    Returns:
        Dict with scene metadata, theater window, and tile paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scene = read_safe_directory(safe_dir)
    print(f"Processing {scene.product_name}")
    print(f"  acquisition: {scene.acquisition_time.isoformat()}")
    print(f"  polarizations: {scene.polarizations}")

    tiles_dir = output_dir / "tiles"
    viz_dir = output_dir / "viz"
    tiles_dir.mkdir(parents=True, exist_ok=True)
    viz_dir.mkdir(parents=True, exist_ok=True)

    all_tile_paths: list[tuple[Path, Path]] = []

    for pol in polarizations:
        if pol not in scene.polarizations:
            print(f"  skipping unavailable polarization: {pol}")
            continue

        asset = scene.asset(pol)
        with rasterio.open(asset.measurement_tiff) as src:
            full_shape = src.shape

        geocoder = build_geocoder(asset.annotation_xml, full_shape)
        col_off, row_off, width, height = geocoder.bbox_to_window(theater_bbox, padding=100)
        window = rasterio.windows.Window(col_off, row_off, width, height)

        print(f"  {pol.upper()}: theater window {window}")

        with rasterio.open(asset.measurement_tiff) as src:
            dn = src.read(1, window=window)

        sigma_db = read_and_calibrate(asset.calibration_xml, dn, to_decibels=True)
        water_mask = compute_water_mask(geocoder, (col_off, row_off, width, height), buffer_deg=buffer_deg)

        # Save a quick preview of the masked theater.
        preview_path = viz_dir / f"{scene.product_name}_{pol}_masked_preview.npy"
        np.save(preview_path, sigma_db)

        tile_count = 0
        for tile in make_tiles(
            sigma_db=sigma_db,
            water_mask=water_mask,
            geocoder=geocoder,
            scene_name=scene.product_name,
            polarization=pol,
            acquisition_time=scene.acquisition_time.isoformat(),
            tile_size=tile_size,
            overlap=overlap,
            window_offset=(col_off, row_off),
        ):
            img_path, meta_path = save_tile(tile, tiles_dir)
            all_tile_paths.append((img_path, meta_path))
            tile_count += 1

        print(f"  {pol.upper()}: wrote {tile_count} tiles")

    manifest = {
        "scene_name": scene.product_name,
        "safe_dir": str(safe_dir.resolve()),
        "acquisition_time": scene.acquisition_time.isoformat(),
        "theater_bbox": theater_bbox,
        "tile_size": tile_size,
        "overlap": overlap,
        "buffer_deg": buffer_deg,
        "tile_count": len(all_tile_paths),
        "tiles": [str(p[0]) for p in all_tile_paths],
        "tile_meta": [str(p[1]) for p in all_tile_paths],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest saved to {manifest_path}")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Darkwatch S1 prep pipeline")
    parser.add_argument("safe_dir", type=str, help="Path to .SAFE directory")
    parser.add_argument("--output-dir", type=str, default="data/processed", help="Output directory")
    parser.add_argument("--bbox", type=str, default=None, help="Theater bbox as W,S,E,N")
    parser.add_argument("--tile-size", type=int, default=512)
    parser.add_argument("--overlap", type=int, default=64)
    parser.add_argument("--pol", type=str, default="vv", help="Comma-separated polarizations (e.g. vv,vh)")
    parser.add_argument("--buffer-deg", type=float, default=0.005, help="Coastal buffer in degrees")
    args = parser.parse_args(argv)

    safe_dir = Path(args.safe_dir)
    if not safe_dir.exists():
        print(f"ERROR: SAFE directory not found: {safe_dir}", file=sys.stderr)
        return 1

    bbox = DEFAULT_THEATER_BBOX
    if args.bbox:
        parts = [float(x.strip()) for x in args.bbox.split(",")]
        if len(parts) != 4:
            raise ValueError("--bbox must be W,S,E,N")
        bbox = tuple(parts)

    polarizations = tuple(p.strip().lower() for p in args.pol.split(","))

    prep_scene(
        safe_dir=safe_dir,
        output_dir=Path(args.output_dir),
        theater_bbox=bbox,
        tile_size=args.tile_size,
        overlap=args.overlap,
        polarizations=polarizations,
        buffer_deg=args.buffer_deg,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
