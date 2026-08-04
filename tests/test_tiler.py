"""Unit tests for SAR tiling."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import LinearNDInterpolator

from darkwatch.s1_prep.geocode import S1Geocoder
from darkwatch.s1_prep.tiler import S1Tile, make_tiles


def _synthetic_geocoder() -> S1Geocoder:
    full_shape = (2048, 2048)
    lines = np.array([0, 0, 2047, 2047], dtype=np.float64)
    pixels = np.array([0, 2047, 0, 2047], dtype=np.float64)
    lats = 34.0 + lines * (1.0 / 2047)
    lons = -120.0 + pixels * (1.0 / 2047)

    return S1Geocoder(
        interp_line=LinearNDInterpolator(np.column_stack((lats, lons)), lines),
        interp_pixel=LinearNDInterpolator(np.column_stack((lats, lons)), pixels),
        interp_lat=LinearNDInterpolator(np.column_stack((lines, pixels)), lats),
        interp_lon=LinearNDInterpolator(np.column_stack((lines, pixels)), lons),
        full_shape=full_shape,
    )


def test_make_tiles_skips_all_land_and_preserves_water_fraction():
    geocoder = _synthetic_geocoder()
    sigma_db = np.full((2200, 2200), -15.0, dtype=np.float32)
    water_mask = np.zeros((2200, 2200), dtype=bool)
    water_mask[:, :1500] = True  # western 1500 columns are water

    tiles = list(
        make_tiles(
            sigma_db=sigma_db,
            water_mask=water_mask,
            geocoder=geocoder,
            scene_name="SYNTH",
            polarization="vv",
            acquisition_time="2024-01-01T00:00:00Z",
            tile_size=1024,
            overlap=128,
            window_offset=(0, 0),
        )
    )

    # With width 2200, tile_size 1024, overlap 128:
    # step = 896; columns: 0, 896, 1792 -> widths 1024, 1024, 408.
    # Height 2200: rows 0, 896, 1792 -> heights 1024, 1024, 408.
    # Eastern all-land tiles (col >= 1500) should be skipped.
    assert len(tiles) > 0
    for tile in tiles:
        assert isinstance(tile, S1Tile)
        assert tile.water_mask is not None
        assert tile.spec.water_fraction > 0.0
        # Synthetic scene spans lon -120 to -119.5; every tile centre is in that range.
        assert -120.5 < tile.spec.center_lon < -119.0
