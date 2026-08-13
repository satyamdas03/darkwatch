"""Maritime zone context for Darkwatch contacts.

Public sources:
- NOAA MPA Inventory (ArcGIS REST) for Marine Protected Areas.
- Future: US EEZ, VME closures, RFMO management zones.
"""

from __future__ import annotations

from .fetcher import fetch_mpa_geojson, save_mpa_geojson
from .zones import ZoneCatalog, context_for_contact, tag_contacts

__all__ = [
    "fetch_mpa_geojson",
    "save_mpa_geojson",
    "ZoneCatalog",
    "context_for_contact",
    "tag_contacts",
]
