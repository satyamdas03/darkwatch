"""Land / coastline masking for Sentinel-1 GRD imagery.

Design: a swappable land-mask source. The default provider fetches Natural Earth
public-domain land polygons. Other adapters can plug in later (GSHHG, ESA
WorldCover, OpenStreetMap, etc.).

Masking is performed in WGS84 lat/lon space. For each pixel in the SAR image we
compute its lon/lat via the geocoder, then check whether it falls inside a land
polygon. The output is a boolean water mask (True = water / keep,
False = land / discard).
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

import numpy as np
import shapely
from shapely.geometry import box

from .geocode import S1Geocoder


class LandMaskSource(Protocol):
    """Pluggable source of land polygons."""

    def get_land_union(self) -> shapely.Geometry:
        """Return a single (possibly multi) polygon covering all land."""
        ...


class NaturalEarthLand:
    """Default public-domain land-mask source.

    Uses Natural Earth `ne_50m_land` polygons (public domain). Land polygons are
    exact enough for first-pass coastal masking and correctly exclude inland
    land, not just a buffered strip around the coastline.
    """

    resolution: str = "50m"
    cache_dir: Path | None = None

    def get_land_union(self) -> shapely.Geometry:
        import zipfile

        import geopandas as gpd
        import requests

        cache = self.cache_dir or Path.home() / ".cache" / "darkwatch" / "natural_earth"
        cache.mkdir(parents=True, exist_ok=True)

        res = self.resolution
        zip_path = cache / f"ne_{res}_land.zip"
        extract_dir = cache / f"ne_{res}_land"
        shp_path = extract_dir / f"ne_{res}_land.shp"

        # Natural Earth direct download URLs. The first is the AWS mirror;
        # the second is the canonical naturalearthdata.com URL (note the
        # literal `http//` segment in their path).
        urls = [
            f"https://naturalearth.s3.amazonaws.com/{res}_physical/ne_{res}_land.zip",
            f"https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/{res}/physical/ne_{res}_land.zip",
        ]

        if not shp_path.exists():
            if not zip_path.exists():
                last_exc: Exception | None = None
                for url in urls:
                    try:
                        resp = requests.get(url, timeout=180)
                        resp.raise_for_status()
                        zip_path.write_bytes(resp.content)
                        break
                    except Exception as exc:
                        last_exc = exc
                else:
                    raise last_exc or RuntimeError(f"Failed to download Natural Earth {res} land polygons")
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

        gdf = gpd.read_file(shp_path)
        # Keep only land polygons; drop small dependency islands if they
        # overlap the scene bbox?  For now use full union.
        return gdf.geometry.unary_union


class ShapefileLand:
    """Land mask from a user-supplied shapefile (e.g., GSHHG, ESA WorldCover)."""

    path: Path

    def get_land_union(self) -> shapely.Geometry:
        import geopandas as gpd

        gdf = gpd.read_file(self.path)
        return gdf.geometry.unary_union


# Backwards-compatible alias for code/config that still references the old name.
NaturalEarthCoastline = NaturalEarthLand
ShapefileCoastline = ShapefileLand


def compute_water_mask(
    geocoder: S1Geocoder,
    window: tuple[int, int, int, int],
    land_source: LandMaskSource | None = None,
    buffer_deg: float = 0.0,
) -> np.ndarray:
    """Compute a water mask for a pixel window.

    Args:
        geocoder: S1Geocoder for the scene.
        window: (col_off, row_off, width, height).
        land_source: LandMaskSource to use; default NaturalEarthLand.
        buffer_deg: Extra coastal buffer in degrees (approximate; ~0.01 deg ~ 1 km).
            Positive values expand land, negative shrink it.

    Returns:
        Boolean mask, shape (height, width). True = water / keep.
    """
    if land_source is None:
        land_source = NaturalEarthLand()

    land_union = land_source.get_land_union()
    if buffer_deg:
        land_union = land_union.buffer(buffer_deg)

    lon_grid, lat_grid = geocoder.window_to_lonlat_grid(window)
    # shapely.contains_xy is vectorised and faster than the deprecated
    # shapely.vectorized.contains module.
    try:
        contains = shapely.contains_xy(land_union, lon_grid.ravel(), lat_grid.ravel())
    except Exception as exc:  # pragma: no cover - defensive fallback
        import warnings

        warnings.warn(f"shapely.contains_xy failed ({exc}), falling back to vectorized.contains")
        contains = shapely.vectorized.contains(land_union, lon_grid, lat_grid).ravel()

    water_mask = ~contains.reshape(lat_grid.shape)
    return water_mask


def water_fraction(water_mask: np.ndarray) -> float:
    """Return fraction of window that is water (valid)."""
    if water_mask.size == 0:
        return 0.0
    return float(np.count_nonzero(water_mask) / water_mask.size)


def apply_water_mask(image: np.ndarray, water_mask: np.ndarray, fill_value: float = np.nan) -> np.ndarray:
    """Apply a water mask to a 2-D image, setting land pixels to fill_value."""
    masked = image.copy()
    masked[~water_mask] = fill_value
    return masked


def mask_safe_directory(
    safe_dir: Path,
    geocoder: S1Geocoder,
    window: tuple[int, int, int, int],
    pol: str = "vv",
    land_source: LandMaskSource | None = None,
    buffer_deg: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Read, calibrate, and mask a region of a .SAFE scene.

    Returns (sigma_db, lon_grid, lat_grid, water_mask).
    """
    from .calibrate import read_and_calibrate
    from .reader import read_safe_directory

    scene = read_safe_directory(safe_dir)
    asset = scene.asset(pol)

    import rasterio

    with rasterio.open(asset.measurement_tiff) as src:
        dn = src.read(1, window=rasterio.windows.Window(*window))

    sigma_db = read_and_calibrate(asset.calibration_xml, dn, to_decibels=True)
    water_mask = compute_water_mask(geocoder, window, land_source, buffer_deg)
    sigma_db_masked = apply_water_mask(sigma_db, water_mask)
    lon_grid, lat_grid = geocoder.window_to_lonlat_grid(window)
    return sigma_db_masked, lon_grid, lat_grid, water_mask
