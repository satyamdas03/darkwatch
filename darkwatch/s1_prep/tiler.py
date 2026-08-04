"""Tile a masked, calibrated SAR image into GPU-sized chips with geo-coordinates.

Each tile is saved as a small GeoTIFF or numpy array plus sidecar JSON with:
  - source scene
  - tile pixel window
  - acquisition time
  - corner/centre coordinates
  - polarization
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np
import rasterio
from rasterio.control import GroundControlPoint
from rasterio.crs import CRS
from rasterio.transform import Affine

from .geocode import S1Geocoder


@dataclass
class TileSpec:
    """Description of one SAR tile."""

    tile_id: str
    scene_name: str
    polarization: str
    col_off: int
    row_off: int
    width: int
    height: int
    acquisition_time: str
    center_lon: float
    center_lat: float
    corner_lons: list[float]
    corner_lats: list[float]
    water_fraction: float = 0.0
    extra: dict = field(default_factory=dict)


@dataclass
class S1Tile:
    """A single SAR tile with data and metadata."""

    data: np.ndarray  # 2-D image chip
    water_mask: np.ndarray | None
    spec: TileSpec
    transform: Affine | None = None


def _generate_tile_windows(
    full_shape: tuple[int, int],
    tile_size: int,
    overlap: int = 0,
) -> Iterable[tuple[int, int, int, int]]:
    """Yield (col_off, row_off, width, height) windows covering an image."""
    height, width = full_shape
    step = tile_size - overlap
    for row in range(0, height, step):
        for col in range(0, width, step):
            w = min(tile_size, width - col)
            h = min(tile_size, height - row)
            if w <= 0 or h <= 0:
                continue
            yield col, row, w, h


def make_tiles(
    sigma_db: np.ndarray,
    water_mask: np.ndarray,
    geocoder: S1Geocoder,
    scene_name: str,
    polarization: str,
    acquisition_time: str,
    tile_size: int = 512,
    overlap: int = 64,
    window_offset: tuple[int, int] = (0, 0),
) -> Iterable[S1Tile]:
    """Create overlapping tiles from a masked SAR image region.

    Args:
        sigma_db: calibrated dB image, shape (height, width).
        water_mask: boolean water mask, same shape.
        geocoder: scene geocoder.
        scene_name: source product name.
        polarization: "vv" or "vh".
        acquisition_time: ISO timestamp string.
        tile_size: chip side length in pixels.
        overlap: overlap between tiles in pixels.
        window_offset: (col_off, row_off) of this region within the full scene.

    Yields:
        S1Tile objects.
    """
    region_height, region_width = sigma_db.shape
    base_col_off, base_row_off = window_offset

    for col, row, w, h in _generate_tile_windows((region_height, region_width), tile_size, overlap):
        chip = sigma_db[row : row + h, col : col + w]
        mask_chip = water_mask[row : row + h, col : col + w]

        # Skip tiles that are entirely land.
        if not mask_chip.any():
            continue

        full_col = base_col_off + col
        full_row = base_row_off + row
        tile_id = f"{scene_name}_{polarization}_c{full_col}_r{full_row}"

        # Geo-coordinates for corners and center.
        corners_full = np.array(
            [
                [full_row, full_col],
                [full_row, full_col + w],
                [full_row + h, full_col + w],
                [full_row + h, full_col],
            ],
            dtype=np.float64,
        )
        corner_lons = geocoder.interp_lon(corners_full).tolist()
        corner_lats = geocoder.interp_lat(corners_full).tolist()

        center_full = np.array([[full_row + h / 2, full_col + w / 2]], dtype=np.float64)
        center_lon = float(geocoder.interp_lon(center_full)[0])
        center_lat = float(geocoder.interp_lat(center_full)[0])

        water_frac = float(np.count_nonzero(mask_chip) / mask_chip.size) if mask_chip.size else 0.0

        spec = TileSpec(
            tile_id=tile_id,
            scene_name=scene_name,
            polarization=polarization,
            col_off=full_col,
            row_off=full_row,
            width=w,
            height=h,
            acquisition_time=acquisition_time,
            center_lon=center_lon,
            center_lat=center_lat,
            corner_lons=corner_lons,
            corner_lats=corner_lats,
            water_fraction=water_frac,
            extra={"valid_pixels": int(np.count_nonzero(mask_chip))},
        )

        yield S1Tile(data=chip, water_mask=mask_chip, spec=spec)


def save_tile(
    tile: S1Tile,
    output_dir: Path,
    dtype: np.dtype = np.float32,
) -> tuple[Path, Path]:
    """Save a tile as GeoTIFF + JSON sidecar.

    The GeoTIFF is written in pixel coordinates; the JSON carries geo metadata.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    img_path = output_dir / f"{tile.spec.tile_id}.tif"
    meta_path = output_dir / f"{tile.spec.tile_id}.json"

    h, w = tile.data.shape
    spec = tile.spec

    # Build ground-control points from the four tile corners so the GeoTIFF
    # carries a proper WGS84 geo-reference even though the SAR grid is only
    # approximately affine in lat/lon.
    gcp_crs = CRS.from_epsg(4326)
    corner_rows = [0, 0, h, h]
    corner_cols = [0, w, w, 0]
    gcps = [
        GroundControlPoint(r, c, lon, lat)
        for r, c, lon, lat in zip(
            corner_rows, corner_cols, spec.corner_lons, spec.corner_lats
        )
    ]

    with rasterio.open(
        img_path,
        "w",
        driver="GTiff",
        height=h,
        width=w,
        count=1,
        dtype=dtype,
        crs=gcp_crs,
        transform=Affine.identity(),
        gcps=gcps,
        compress="lzw",
    ) as dst:
        dst.write(tile.data.astype(dtype), 1)

    meta = asdict(spec)
    meta_path.write_text(json.dumps(meta, indent=2))

    return img_path, meta_path
