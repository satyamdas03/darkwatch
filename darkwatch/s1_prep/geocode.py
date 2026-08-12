"""Geocoding helpers for Sentinel-1 GRD products.

Sentinel-1 GRD measurement TIFFs are stored in radar geometry (line/pixel).
The annotation XML contains a sparse geolocation grid mapping a subset of
(line, pixel) → (lat, lon, height). We use scipy to interpolate between those
control points.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np
import shapely
from scipy.interpolate import LinearNDInterpolator

from .reader import read_geolocation_grid


def _bbox_to_polygon(bbox: tuple[float, float, float, float]) -> shapely.Geometry:
    """Turn W,S,E,N bbox into a shapely polygon."""
    minx, miny, maxx, maxy = bbox
    return shapely.geometry.Polygon(
        [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)]
    )


@dataclass(frozen=True)
class S1Geocoder:
    """Interpolators mapping (lat, lon) ↔ (line, pixel)."""

    interp_line: LinearNDInterpolator
    interp_pixel: LinearNDInterpolator
    interp_lat: LinearNDInterpolator
    interp_lon: LinearNDInterpolator
    full_shape: tuple[int, int]
    grid: np.ndarray
    _image_extent_poly: shapely.Geometry | None = field(default=None, init=False, repr=False)

    def lonlat_to_pixel(self, lon: float, lat: float) -> tuple[float, float]:
        """Convert a single WGS84 coordinate to (line, pixel)."""
        line = self.interp_line([[lat, lon]])[0]
        pixel = self.interp_pixel([[lat, lon]])[0]
        return float(line), float(pixel)

    def pixel_to_lonlat(self, line: float, pixel: float) -> tuple[float, float]:
        """Convert a single (line, pixel) coordinate to (lon, lat)."""
        lon = self.interp_lon([[line, pixel]])[0]
        lat = self.interp_lat([[line, pixel]])[0]
        return float(lon), float(lat)

    def image_extent_polygon(self) -> shapely.Geometry:
        """Return the geographic extent of the full image as a shapely polygon.

        This uses the convex hull of the sparse geolocation grid points, which
        is guaranteed to be a valid polygon and safely bounds the image.
        """
        if self._image_extent_poly is None:
            lons = self.grid["lon"].astype(float)
            lats = self.grid["lat"].astype(float)
            pts = shapely.multipoints(np.column_stack((lons, lats)))
            hull = shapely.convex_hull(pts)
            object.__setattr__(self, "_image_extent_poly", hull)
        return self._image_extent_poly  # type: ignore[return-value]

    def bbox_to_window(
        self,
        bbox: tuple[float, float, float, float],
        padding: int = 50,
    ) -> tuple[int, int, int, int]:
        """Convert WGS84 bbox (W, S, E, N) to pixel window (min_x, min_y, width, height).

        If the requested bbox extends outside the scene footprint, the returned
        window is clipped to the covered portion so the caller still gets the
        largest usable sub-image instead of a collapsed single-pixel window.
        """
        min_lon, min_lat, max_lon, max_lat = bbox
        bbox_poly = _bbox_to_polygon(bbox)
        extent_poly = self.image_extent_polygon()

        inter = bbox_poly.intersection(extent_poly)
        if inter.is_empty:
            raise ValueError(f"Bbox {bbox} does not intersect the scene footprint.")

        # Collect all vertices of the covered portion. For a polygon/polygon
        # intersection this may be a polygon or multi-polygon.
        xy = []
        for geom in getattr(inter, "geoms", [inter]):
            if hasattr(geom, "exterior"):
                xy.extend(geom.exterior.coords[:-1])  # omit duplicate closing point

        if not xy:
            raise ValueError(f"Bbox {bbox} intersection with scene footprint is degenerate.")

        pts = np.array(xy, dtype=np.float64)
        lats = pts[:, 1]
        lons = pts[:, 0]
        corners = np.column_stack((lats, lons))
        lines = self.interp_line(corners)
        pixels = self.interp_pixel(corners)

        valid = np.isfinite(lines) & np.isfinite(pixels)
        if not valid.any():
            raise ValueError(f"Bbox {bbox} is outside the geolocation grid coverage.")

        lines = lines[valid]
        pixels = pixels[valid]
        height, width = self.full_shape

        min_x = max(0, int(np.floor(pixels.min()) - padding))
        max_x = min(width, int(np.ceil(pixels.max()) + padding))
        min_y = max(0, int(np.floor(lines.min()) - padding))
        max_y = min(height, int(np.ceil(lines.max()) + padding))

        out_width = max(1, max_x - min_x)
        out_height = max(1, max_y - min_y)
        return min_x, min_y, out_width, out_height

    def window_to_lonlat_grid(
        self,
        window: tuple[int, int, int, int],
    ) -> tuple[np.ndarray, np.ndarray]:
        """Build lon/lat grids for every pixel in a pixel window.

        Args:
            window: (col_off, row_off, width, height) in full-resolution pixels.

        Returns:
            (lon_grid, lat_grid), each shape (height, width).
        """
        col_off, row_off, width, height = window
        cols = np.arange(col_off, col_off + width)
        rows = np.arange(row_off, row_off + height)
        col_grid, row_grid = np.meshgrid(cols, rows)

        points = np.column_stack((row_grid.ravel(), col_grid.ravel()))
        lons = self.interp_lon(points).reshape(height, width)
        lats = self.interp_lat(points).reshape(height, width)
        return lons, lats


def build_geocoder(annotation_xml: Path, full_shape: tuple[int, int]) -> S1Geocoder:
    """Build a geocoder from an annotation XML and the measurement image shape."""
    grid = read_geolocation_grid(annotation_xml)

    lats = grid["lat"].astype(np.float64)
    lons = grid["lon"].astype(np.float64)
    lines = grid["line"].astype(np.float64)
    pixels = grid["pixel"].astype(np.float64)

    # (lat, lon) -> (line, pixel)
    interp_line = LinearNDInterpolator(np.column_stack((lats, lons)), lines)
    interp_pixel = LinearNDInterpolator(np.column_stack((lats, lons)), pixels)

    # (line, pixel) -> (lat, lon)
    interp_lat = LinearNDInterpolator(np.column_stack((lines, pixels)), lats)
    interp_lon = LinearNDInterpolator(np.column_stack((lines, pixels)), lons)

    return S1Geocoder(
        interp_line=interp_line,
        interp_pixel=interp_pixel,
        interp_lat=interp_lat,
        interp_lon=interp_lon,
        full_shape=full_shape,
        grid=grid,
    )
