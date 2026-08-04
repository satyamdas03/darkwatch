"""Phase 0 manual walkthrough: open a Sentinel-1 GRD scene, calibrate, geocode,
crop to a test theater, and view the ship-sized bright returns.

This is intentionally low-automation — the goal is to understand the raw material
before building the S1 prep pipeline.

Usage:
    python scripts/inspect_scene.py data/raw/s1/S1A_...SAFE --output notebooks/inspect.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from defusedxml import ElementTree as ET

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import rasterio


# Santa Barbara Channel test theater (W, S, E, N).
SANTA_BARBARA_BBOX = (-120.5, 33.8, -119.0, 34.6)


def find_measurement_tiff(safe_dir: Path, polarization: str = "vv") -> Path:
    """Find a polarization measurement TIFF inside a SAFE directory."""
    pattern = f"s1*-iw-grd-{polarization}-*.tiff"
    candidates = list((safe_dir / "measurement").glob(pattern))
    if not candidates:
        raise FileNotFoundError(f"No {polarization} TIFF found in {safe_dir / 'measurement'}")
    return candidates[0]


def find_annotation_xml(safe_dir: Path, polarization: str) -> Path:
    """Find the main annotation XML for a given polarization."""
    pattern = f"s1*-iw-grd-{polarization}-*.xml"
    candidates = list((safe_dir / "annotation").glob(pattern))
    if not candidates:
        raise FileNotFoundError(f"No annotation XML for {polarization}")
    return candidates[0]


def find_calibration_xml(safe_dir: Path, polarization: str) -> Path:
    """Find the calibration XML for a given polarization."""
    pattern = f"calibration-s1*-iw-grd-{polarization}-*.xml"
    candidates = list((safe_dir / "annotation" / "calibration").glob(pattern))
    if not candidates:
        raise FileNotFoundError(f"No calibration XML for {polarization}")
    return candidates[0]


def read_calibration_vector(calib_xml: Path) -> tuple[np.ndarray, np.ndarray]:
    """Read the sigma-nought calibration samples from a Sentinel-1 calibration XML.

    Returns:
        (pixel_indices, sigma_nought_values) as 1-D arrays. The calibration is
        sampled at discrete range pixels; callers should interpolate to the full
        image width if needed.
    """
    tree = ET.parse(calib_xml)

    vector_list = tree.find(".//calibrationVectorList")
    if vector_list is None:
        # Namespaced fallback.
        vector_list = tree.find(
            ".//{http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-1/product/calibration}calibrationVectorList"
        )

    if vector_list is None:
        raise ValueError(f"Could not locate calibrationVectorList in {calib_xml}")

    # GRD products normally contain identical vectors for all azimuth lines.
    first_vector = vector_list.find("./calibrationVector")
    if first_vector is None:
        raise ValueError("No calibrationVector entries found")

    pixel_node = first_vector.find("./pixel")
    sigma_node = first_vector.find("./sigmaNought")
    if pixel_node is None or sigma_node is None:
        raise ValueError("No pixel/sigmaNought nodes found in calibrationVector")

    pixel_indices = np.fromstring(pixel_node.text, sep=" ")
    sigma_values = np.fromstring(sigma_node.text, sep=" ")
    return pixel_indices, sigma_values


def build_range_calibration(width: int, pixel_indices: np.ndarray, sigma_values: np.ndarray) -> np.ndarray:
    """Interpolate sampled sigma-nought calibration to every range column."""
    if pixel_indices.shape[0] != sigma_values.shape[0]:
        raise ValueError("pixel_indices and sigma_values length mismatch")
    full_columns = np.arange(width)
    return np.interp(full_columns, pixel_indices, sigma_values)


def calibrate_to_sigma_nought(dn_array: np.ndarray, calib_vector: np.ndarray) -> np.ndarray:
    """Convert digital numbers to sigma-nought (linear backscatter).

    Sentinel-1 GRD: sigma0 = DN^2 / calibration_vector^2
    """
    sigma0 = (dn_array.astype(np.float32) ** 2) / (calib_vector.astype(np.float32) ** 2)
    return sigma0


def to_db(sigma0: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """Linear sigma-nought to decibel."""
    return 10.0 * np.log10(np.maximum(sigma0, eps))


def read_geolocation_grid(annotation_xml: Path) -> np.ndarray:
    """Read the Sentinel-1 geolocation grid as a structured array.

    Columns: line, pixel, latitude, longitude, height.
    """
    tree = ET.parse(annotation_xml)
    grid_list = tree.find(".//geolocationGridPointList")
    if grid_list is None:
        raise ValueError(f"No geolocationGridPointList in {annotation_xml}")

    records = []
    for pt in grid_list.findall("./geolocationGridPoint"):
        records.append(
            (
                int(pt.find("./line").text),
                int(pt.find("./pixel").text),
                float(pt.find("./latitude").text),
                float(pt.find("./longitude").text),
                float(pt.find("./height").text),
            )
        )
    return np.array(records, dtype=[("line", int), ("pixel", int), ("lat", float), ("lon", float), ("height", float)])


def bbox_to_pixel_window(
    geolocation_grid: np.ndarray,
    bbox: tuple[float, float, float, float],
    full_shape: tuple[int, int],
    padding: int = 50,
) -> rasterio.windows.Window:
    """Convert a WGS84 bbox (W, S, E, N) into a pixel-window inside the SAR image.

    Uses barycentric interpolation within the Sentinel-1 geolocation grid
    (scipy LinearNDInterpolator). Returns a rasterio Window in full-resolution
    pixel coordinates.
    """
    from scipy.interpolate import LinearNDInterpolator

    min_lon, min_lat, max_lon, max_lat = bbox

    lats = geolocation_grid["lat"]
    lons = geolocation_grid["lon"]
    lines = geolocation_grid["line"].astype(float)
    pixels = geolocation_grid["pixel"].astype(float)

    # Build direct (lat, lon) -> (line, pixel) interpolators.
    interp_line = LinearNDInterpolator(np.column_stack((lats, lons)), lines)
    interp_pixel = LinearNDInterpolator(np.column_stack((lats, lons)), pixels)

    corners_latlon = np.array([
        [min_lat, min_lon],
        [min_lat, max_lon],
        [max_lat, min_lon],
        [max_lat, max_lon],
    ])
    ys = interp_line(corners_latlon)
    xs = interp_pixel(corners_latlon)

    # If NaN, some corners fall outside the grid; clip to image bounds later.
    valid = np.isfinite(xs) & np.isfinite(ys)
    if not valid.any():
        raise ValueError(f"Bbox {bbox} is outside the geolocation grid coverage.")

    xs = xs[valid]
    ys = ys[valid]

    min_x = int(np.clip(np.floor(xs.min()) - padding, 0, full_shape[1] - 1))
    max_x = int(np.clip(np.ceil(xs.max()) + padding, 0, full_shape[1]))
    min_y = int(np.clip(np.floor(ys.min()) - padding, 0, full_shape[0] - 1))
    max_y = int(np.clip(np.ceil(ys.max()) + padding, 0, full_shape[0]))

    width = max(1, max_x - min_x)
    height = max(1, max_y - min_y)
    return rasterio.windows.Window(min_x, min_y, width, height)


def main():
    parser = argparse.ArgumentParser(description="Inspect a Sentinel-1 GRD scene")
    parser.add_argument("safe_dir", type=str, help="Path to extracted .SAFE directory")
    parser.add_argument("--pol", type=str, default="vv", choices=["vv", "vh"])
    parser.add_argument("--output", type=str, default=None, help="PNG output path")
    parser.add_argument("--max-lines", type=int, default=12000, help="Max downsampled height for full-scene view")
    parser.add_argument("--bbox", type=str, default=None, help="Custom bbox as W,S,E,N (default: Santa Barbara Channel)")
    args = parser.parse_args()

    safe_dir = Path(args.safe_dir)
    if not safe_dir.exists():
        print(f"ERROR: SAFE directory not found: {safe_dir}", file=sys.stderr)
        sys.exit(1)

    bbox = SANTA_BARBARA_BBOX
    if args.bbox:
        bbox = tuple(float(x) for x in args.bbox.split(","))
        if len(bbox) != 4:
            raise ValueError("--bbox must be W,S,E,N")

    tiff_path = find_measurement_tiff(safe_dir, args.pol)
    annotation_xml = find_annotation_xml(safe_dir, args.pol)
    calib_xml = find_calibration_xml(safe_dir, args.pol)

    print(f"Opening {tiff_path.name} ...")
    with rasterio.open(tiff_path) as src:
        full_shape = src.shape
        print(f"  full shape: {full_shape}")
        print(f"  dtype: {src.dtypes[0]}")

        geo_grid = read_geolocation_grid(annotation_xml)
        print(f"  geolocation grid points: {len(geo_grid)}")
        print(f"  geolocation lat range: {geo_grid['lat'].min():.4f} to {geo_grid['lat'].max():.4f}")
        print(f"  geolocation lon range: {geo_grid['lon'].min():.4f} to {geo_grid['lon'].max():.4f}")

        window = bbox_to_pixel_window(geo_grid, bbox, full_shape, padding=200)
        print(f"  theater pixel window: {window}")

        # Read the cropped theater region at full resolution for inspection.
        dn_cropped = src.read(1, window=window)
        print(f"  cropped shape: {dn_cropped.shape}")

        # Also read a downsampled full-scene overview.
        if full_shape[0] > args.max_lines:
            dn_overview = src.read(
                1,
                out_shape=(args.max_lines, full_shape[1]),
                resampling=rasterio.enums.Resampling.average,
            )
        else:
            dn_overview = src.read(1)

    print(f"Reading calibration from {calib_xml.name} ...")
    pixel_indices, sigma_values = read_calibration_vector(calib_xml)
    calib_full = build_range_calibration(full_shape[1], pixel_indices, sigma_values)

    # Calibrate overview (need same width as overview; use nearest interpolation).
    calib_overview = calib_full  # same width since overview keeps full width
    sigma0_overview = calibrate_to_sigma_nought(dn_overview, calib_overview)
    sigma_db_overview = to_db(sigma0_overview)

    # Calibrate cropped region.
    col_off, row_off = int(window.col_off), int(window.row_off)
    calib_cropped = calib_full[col_off : col_off + dn_cropped.shape[1]]
    sigma0_cropped = calibrate_to_sigma_nought(dn_cropped, calib_cropped)
    sigma_db_cropped = to_db(sigma0_cropped)

    print(f"  cropped sigma0 dB range: {sigma_db_cropped.min():.2f} to {sigma_db_cropped.max():.2f}")
    print(f"  cropped sigma0 dB mean: {sigma_db_cropped.mean():.2f}, std: {sigma_db_cropped.std():.2f}")

    # Detect very bright targets as a crude first-pass "what might be a ship" hint.
    bright_threshold = sigma_db_cropped.mean() + 3.0 * sigma_db_cropped.std()
    bright_mask = sigma_db_cropped > bright_threshold
    num_bright = int(bright_mask.sum())
    print(f"  bright pixels above {bright_threshold:.1f} dB: {num_bright}")

    # Visualize.
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Full scene overview.
    ax = axes[0]
    im = ax.imshow(sigma_db_overview, cmap="gray", vmin=-25, vmax=5, aspect="auto")
    # Overlay theater window.
    # Window is in full coords; overview is downsampled in rows only.
    if full_shape[0] > args.max_lines:
        scale_y = args.max_lines / full_shape[0]
    else:
        scale_y = 1.0
    rect = patches.Rectangle(
        (window.col_off, window.row_off * scale_y),
        window.width,
        window.height * scale_y,
        linewidth=2,
        edgecolor="r",
        facecolor="none",
    )
    ax.add_patch(rect)
    ax.set_title("Full scene overview (red box = theater)")
    plt.colorbar(im, ax=ax, fraction=0.046)

    # Cropped theater.
    ax = axes[1]
    im = ax.imshow(sigma_db_cropped, cmap="gray", vmin=-25, vmax=5, aspect="auto")
    ax.set_title(f"Santa Barbara Channel theater ({bbox})")
    plt.colorbar(im, ax=ax, fraction=0.046)

    # Bright target hint.
    ax = axes[2]
    ax.imshow(sigma_db_cropped, cmap="gray", vmin=-25, vmax=5, aspect="auto")
    ys, xs = np.where(bright_mask)
    if len(xs) > 0:
        # Downsample bright pixels if there are too many for clarity.
        step = max(1, len(xs) // 2000)
        ax.scatter(xs[::step], ys[::step], c="red", s=2, alpha=0.6, label="bright pixels")
        ax.legend()
    ax.set_title(f"Bright-pixel hint (threshold {bright_threshold:.1f} dB)")

    fig.suptitle(f"Darkwatch Phase 0 — {safe_dir.name}", fontsize=13)
    plt.tight_layout()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"Saved figure to {out_path}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
