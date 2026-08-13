"""Tests for the Darkwatch maritime zones module."""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Point, Polygon

from darkwatch.zones.zones import ZoneCatalog, context_for_contact, tag_contacts


@pytest.fixture
def sample_zone_geojson(tmp_path: Path) -> Path:
    """Create a tiny GeoJSON with one polygon zone."""
    path = tmp_path / "test_zones.geojson"
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "Site_ID": "TEST-001",
                    "Site_Name": "Test Sanctuary",
                    "Gov_Level": "Federal",
                    "Prot_Lvl": "No Take",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-118.5, 33.3],
                            [-117.5, 33.3],
                            [-117.5, 34.0],
                            [-118.5, 34.0],
                            [-118.5, 33.3],
                        ]
                    ],
                },
            }
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_zone_catalog_from_geojson(sample_zone_geojson: Path) -> None:
    catalog = ZoneCatalog.from_geojson(sample_zone_geojson)
    assert catalog.gdf is not None
    assert len(catalog.gdf) == 1


def test_context_inside_zone(sample_zone_geojson: Path) -> None:
    catalog = ZoneCatalog.from_geojson(sample_zone_geojson)
    ctx = catalog.context(-118.0, 33.5)
    assert len(ctx) == 1
    assert ctx[0]["name"] == "Test Sanctuary"
    assert ctx[0]["protection_level"] == "No Take"


def test_context_outside_zone(sample_zone_geojson: Path) -> None:
    catalog = ZoneCatalog.from_geojson(sample_zone_geojson)
    ctx = catalog.context(-100.0, 25.0)
    assert ctx == []


def test_tag_contacts(sample_zone_geojson: Path) -> None:
    catalog = ZoneCatalog.from_geojson(sample_zone_geojson)
    contacts = [
        {"contact_id": "inside", "center_lon": -118.0, "center_lat": 33.5},
        {"contact_id": "outside", "center_lon": -100.0, "center_lat": 25.0},
    ]
    tagged = tag_contacts(catalog, contacts)
    assert len(tagged[0]["zones"]) == 1
    assert tagged[1]["zones"] == []


def test_context_for_contact_missing_coords(sample_zone_geojson: Path) -> None:
    catalog = ZoneCatalog.from_geojson(sample_zone_geojson)
    assert context_for_contact(catalog, {"contact_id": "no-coords"}) == []
