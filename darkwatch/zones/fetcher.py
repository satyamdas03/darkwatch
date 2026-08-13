"""Fetch public maritime zone datasets for Darkwatch context.

Primary source: NOAA MPA Inventory 2023 via ArcGIS REST.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

NOAA_MPA_INVENTORY_URL = (
    "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/"
    "NOAA_MPA_Inventory_2023/FeatureServer/0/query"
)

DEFAULT_FIELDS = [
    "Site_ID",
    "Site_Name",
    "Gov_Level",
    "State",
    "Prot_Lvl",
    "Mgmt_Agen",
    "Cons_Focus",
    "Fish_Rstr",
    "Estab_Yr",
    "AreaKm",
    "AreaMar",
    "URL",
]


def _bbox_polygon(west: float, south: float, east: float, north: float) -> str:
    """Return an ArcGIS geometry envelope polygon string."""
    return f"{west},{south},{east},{north}"


def fetch_mpa_geojson(
    west: float,
    south: float,
    east: float,
    north: float,
    out_fields: list[str] | None = None,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Download MPA polygons intersecting a WGS84 bbox.

    Args:
        west, south, east, north: Bbox corners in decimal degrees.
        out_fields: Feature attributes to retrieve.
        timeout: HTTP timeout in seconds.

    Returns:
        GeoJSON FeatureCollection (may be empty).
    """
    out_fields = out_fields or DEFAULT_FIELDS
    params = {
        "where": "1=1",
        "outFields": ",".join(out_fields),
        "f": "geojson",
        "returnGeometry": "true",
        "inSR": "4326",
        "outSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "geometry": _bbox_polygon(west, south, east, north),
        "geometryType": "esriGeometryEnvelope",
    }
    resp = requests.get(NOAA_MPA_INVENTORY_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    if "features" not in data:
        raise ValueError(f"Unexpected ArcGIS response: {list(data.keys())}")
    return data


def save_mpa_geojson(
    data: dict[str, Any],
    path: str | Path,
) -> Path:
    """Write fetched GeoJSON to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path
