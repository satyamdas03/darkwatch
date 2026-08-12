"""Unit tests for land/water masking."""

from __future__ import annotations

import numpy as np
import shapely
from scipy.interpolate import LinearNDInterpolator

from darkwatch.s1_prep.geocode import S1Geocoder
from darkwatch.s1_prep.land_mask import (
    LandMaskSource,
    apply_water_mask,
    compute_water_mask,
    water_fraction,
)


class _HalfLandSource(LandMaskSource):
    """Fake land source: land covers eastern half of the synthetic scene."""

    def get_land_union(self) -> shapely.Geometry:
        # Synthetic scene spans lon [-120, -119.5], lat [34, 34.5].
        return shapely.box(-119.8, 34.0, -119.5, 34.5)


def _synthetic_geocoder() -> S1Geocoder:
    """Build a geocoder where lon/lat are affine functions of line/pixel."""
    full_shape = (500, 500)
    lines = np.array([0, 0, 499, 499], dtype=np.float64)
    pixels = np.array([0, 499, 0, 499], dtype=np.float64)
    lats = 34.0 + lines * (0.5 / 499)
    lons = -120.0 + pixels * (0.5 / 499)

    grid = np.array(
        list(zip(lines.astype(int), pixels.astype(int), lats, lons, np.zeros_like(lats))),
        dtype=[("line", int), ("pixel", int), ("lat", float), ("lon", float), ("height", float)],
    )

    interp_line = LinearNDInterpolator(np.column_stack((lats, lons)), lines)
    interp_pixel = LinearNDInterpolator(np.column_stack((lats, lons)), pixels)
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


def test_compute_water_mask_excludes_land():
    geocoder = _synthetic_geocoder()
    land_source = _HalfLandSource()
    window = (0, 0, 500, 500)
    water_mask = compute_water_mask(geocoder, window, land_source, buffer_deg=0.0)

    assert water_mask.shape == (500, 500)
    assert water_mask.dtype == bool
    # Land box starts at lon=-119.8 (pixel ~200). Western 200 columns are fully
    # water; eastern 200 columns are fully land.
    assert water_mask[:, :200].mean() == 1.0
    assert water_mask[:, 300:].mean() < 0.05


def test_apply_water_mask_sets_land_to_nan():
    image = np.ones((10, 10), dtype=np.float32)
    mask = np.ones((10, 10), dtype=bool)
    mask[:, 5:] = False
    masked = apply_water_mask(image, mask)
    assert np.isnan(masked[:, 5:]).all()
    assert (masked[:, :5] == 1.0).all()


def test_water_fraction():
    mask = np.array([[True, True], [False, True]])
    assert water_fraction(mask) == 0.75
