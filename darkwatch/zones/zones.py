"""In-memory zone catalog and contact tagging."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import geopandas as gpd
from shapely.geometry import Point


class ZoneCatalog:
    """Hold maritime zones and provide point-in-zone lookups."""

    def __init__(self, gdf: gpd.GeoDataFrame | None = None) -> None:
        self.gdf = gdf

    @classmethod
    def from_geojson(cls, path: str | Path) -> "ZoneCatalog":
        """Load zones from a GeoJSON file."""
        path = Path(path)
        if not path.exists():
            return cls(None)
        gdf = gpd.read_file(path)
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)
        return cls(gdf)

    def context(self, lon: float, lat: float) -> list[dict[str, Any]]:
        """Return all zones that contain the point."""
        if self.gdf is None or self.gdf.empty:
            return []
        point = Point(lon, lat)
        matches = self.gdf[self.gdf.geometry.contains(point)]
        records = []
        for _, row in matches.iterrows():
            records.append(
                {
                    "site_id": row.get("Site_ID"),
                    "name": row.get("Site_Name"),
                    "gov_level": row.get("Gov_Level"),
                    "state": row.get("State"),
                    "protection_level": row.get("Prot_Lvl"),
                    "management_agency": row.get("Mgmt_Agen"),
                    "conservation_focus": row.get("Cons_Focus"),
                    "fishing_restriction": row.get("Fish_Rstr"),
                    "established_year": row.get("Estab_Yr"),
                    "area_km2": row.get("AreaKm"),
                    "area_marine_km2": row.get("AreaMar"),
                    "url": row.get("URL"),
                }
            )
        return records


def context_for_contact(catalog: ZoneCatalog, contact: dict[str, Any]) -> list[dict[str, Any]]:
    """Return zone context for a single contact dict."""
    lon = contact.get("center_lon")
    lat = contact.get("center_lat")
    if lon is None or lat is None:
        return []
    return catalog.context(float(lon), float(lat))


def tag_contacts(catalog: ZoneCatalog, contacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return contacts augmented with ``zones`` context."""
    tagged = []
    for c in contacts:
        enriched = dict(c)
        enriched["zones"] = context_for_contact(catalog, c)
        tagged.append(enriched)
    return tagged
