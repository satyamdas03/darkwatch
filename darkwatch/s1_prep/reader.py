"""Sentinel-1 .SAFE reader — locate and parse GRD product files.

This module is intentionally low-level and provider-agnostic at the file level:
it reads a local .SAFE directory and exposes the measurement TIFFs,
calibration XMLs, annotation XMLs, and the geolocation grid.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from defusedxml import ElementTree as ET

Polarization = Literal["vv", "vh"]


@dataclass(frozen=True)
class S1PolarizationAssets:
    """Files for one polarization of a GRD product."""

    pol: Polarization
    measurement_tiff: Path
    annotation_xml: Path
    calibration_xml: Path
    noise_xml: Path | None = None


@dataclass(frozen=True)
class S1Scene:
    """A parsed Sentinel-1 GRD .SAFE directory."""

    safe_dir: Path
    product_name: str
    platform: str  # e.g. "S1A"
    mode: str  # e.g. "IW"
    product_type: str  # e.g. "GRDH"
    polarizations: list[Polarization]
    start_time: datetime
    end_time: datetime
    assets: dict[Polarization, S1PolarizationAssets]

    def asset(self, pol: Polarization) -> S1PolarizationAssets:
        if pol not in self.assets:
            raise ValueError(f"Polarization {pol} not available in {self.product_name}")
        return self.assets[pol]

    @property
    def acquisition_time(self) -> datetime:
        """Best single timestamp for the scene (midpoint)."""
        return self.start_time + (self.end_time - self.start_time) / 2


def _parse_timestamp(ts: str | None) -> datetime:
    if ts is None:
        return datetime.now(timezone.utc)
    ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def read_safe_directory(safe_dir: Path | str) -> S1Scene:
    """Parse a Sentinel-1 .SAFE directory."""
    safe_dir = Path(safe_dir)
    if not safe_dir.is_dir():
        raise NotADirectoryError(f"SAFE directory not found: {safe_dir}")

    # Product name is the directory stem without .SAFE.
    product_name = safe_dir.stem
    parts = product_name.split("_")
    if len(parts) < 5:
        raise ValueError(f"Unexpected SAFE product name: {product_name}")

    platform = parts[0]
    mode = parts[1]
    product_type = parts[2]

    measurement_dir = safe_dir / "measurement"
    annotation_dir = safe_dir / "annotation"
    calibration_dir = annotation_dir / "calibration"
    if not measurement_dir.is_dir() or not annotation_dir.is_dir():
        raise ValueError(f"Invalid SAFE structure: missing measurement or annotation dirs in {safe_dir}")

    # Identify polarizations by TIFF names.
    tiff_files = sorted(measurement_dir.glob("*.tiff"))
    polarizations: list[Polarization] = []
    assets: dict[Polarization, S1PolarizationAssets] = {}

    for tiff in tiff_files:
        name_lower = tiff.stem.lower()
        if "-vv-" in name_lower:
            pol: Polarization = "vv"
        elif "-vh-" in name_lower:
            pol = "vh"
        else:
            continue

        annotation_xml = annotation_dir / f"{tiff.stem}.xml"
        if not annotation_xml.exists():
            # Some products name annotation XML with uppercase polarization.
            annotation_xml = annotation_dir / f"{tiff.stem.upper()}.xml"

        calibration_xml = calibration_dir / f"calibration-{tiff.stem}.xml"
        noise_xml = calibration_dir / f"noise-{tiff.stem}.xml"
        if not calibration_xml.exists():
            calibration_xml = calibration_dir / f"calibration-{tiff.stem.upper()}.xml"
        if not noise_xml.exists():
            noise_xml = calibration_dir / f"noise-{tiff.stem.upper()}.xml"
        if not noise_xml.exists():
            noise_xml = None

        polarizations.append(pol)
        assets[pol] = S1PolarizationAssets(
            pol=pol,
            measurement_tiff=tiff,
            annotation_xml=annotation_xml,
            calibration_xml=calibration_xml,
            noise_xml=noise_xml,
        )

    if not polarizations:
        raise ValueError(f"No VV/VH measurement TIFFs found in {measurement_dir}")

    # Parse start/end times from the first annotation XML.
    first_annotation = assets[polarizations[0]].annotation_xml
    tree = ET.parse(first_annotation)
    root = tree.getroot()

    ads_header = root.find(".//adsHeader")
    if ads_header is None:
        # Some files have no namespace prefix.
        ads_header = root.find(
            ".//{http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-1/product}adsHeader"
        )

    start_time = _parse_timestamp(
        ads_header.findtext("startTime") if ads_header is not None else None
    )
    end_time = _parse_timestamp(
        ads_header.findtext("stopTime") if ads_header is not None else None
    )

    return S1Scene(
        safe_dir=safe_dir,
        product_name=product_name,
        platform=platform,
        mode=mode,
        product_type=product_type,
        polarizations=polarizations,
        start_time=start_time,
        end_time=end_time,
        assets=assets,
    )


def read_geolocation_grid(annotation_xml: Path) -> "np.ndarray":
    """Read the Sentinel-1 geolocation grid from an annotation XML.

    Returns a structured numpy array with fields: line, pixel, lat, lon, height.
    """
    import numpy as np

    tree = ET.parse(annotation_xml)
    grid_list = tree.find(".//geolocationGridPointList")
    if grid_list is None:
        grid_list = tree.find(
            ".//{http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-1/product}geolocationGridPointList"
        )
    if grid_list is None:
        raise ValueError(f"No geolocationGridPointList in {annotation_xml}")

    records = []
    for pt in grid_list.findall("./geolocationGridPoint"):
        records.append(
            (
                int(pt.findtext("line") or 0),
                int(pt.findtext("pixel") or 0),
                float(pt.findtext("latitude") or 0.0),
                float(pt.findtext("longitude") or 0.0),
                float(pt.findtext("height") or 0.0),
            )
        )
    return np.array(
        records,
        dtype=[("line", int), ("pixel", int), ("lat", float), ("lon", float), ("height", float)],
    )
