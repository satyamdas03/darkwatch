"""Debug script for Southern California Bight geocoder window collapse."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import rasterio

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.s1_prep.geocode import build_geocoder
from darkwatch.s1_prep.reader import read_safe_directory

SAFE_DIR = REPO_ROOT / "data" / "raw" / "s1" / "S1A_IW_GRDH_1SDV_20240706T015825_20240706T015854_054634_06A693_4441.SAFE"
SCB_BBOX = (-118.5, 33.3, -117.5, 34.0)  # W, S, E, N

scene = read_safe_directory(SAFE_DIR)
print(f"Scene: {scene.product_name}")
print(f"Polarizations: {scene.polarizations}")

for pol in scene.polarizations:
    asset = scene.asset(pol)
    with rasterio.open(asset.measurement_tiff) as src:
        full_shape = src.shape
        print(f"\n{pol.upper()}: full shape = {full_shape}")

    geocoder = build_geocoder(asset.annotation_xml, full_shape)

    # Inspect the geolocation grid.
    from darkwatch.s1_prep.reader import read_geolocation_grid
    grid = read_geolocation_grid(asset.annotation_xml)
    print(f"Geolocation grid shape: {grid.shape}")
    print(f"  line range: {grid['line'].min()} - {grid['line'].max()}")
    print(f"  pixel range: {grid['pixel'].min()} - {grid['pixel'].max()}")
    print(f"  lat range: {grid['lat'].min():.4f} - {grid['lat'].max():.4f}")
    print(f"  lon range: {grid['lon'].min():.4f} - {grid['lon'].max():.4f}")

    # Convert SCB bbox corners to pixel coordinates.
    min_lon, min_lat, max_lon, max_lat = SCB_BBOX
    corners = [
        ("SW", min_lat, min_lon),
        ("SE", min_lat, max_lon),
        ("NW", max_lat, min_lon),
        ("NE", max_lat, max_lon),
    ]
    print(f"\nSCB bbox corners -> (line, pixel):")
    for name, lat, lon in corners:
        line, pixel = geocoder.lonlat_to_pixel(lon, lat)
        valid = np.isfinite(line) and np.isfinite(pixel)
        print(f"  {name} ({lat:.3f}, {lon:.3f}) -> line={line:.1f}, pixel={pixel:.1f} valid={valid}")

    # Show computed window with different paddings.
    for padding in [0, 50, 100, 200, 500]:
        try:
            min_x, min_y, width, height = geocoder.bbox_to_window(SCB_BBOX, padding=padding)
            print(f"  padding={padding}: Window(col_off={min_x}, row_off={min_y}, width={width}, height={height})")
        except Exception as exc:
            print(f"  padding={padding}: ERROR {exc}")
