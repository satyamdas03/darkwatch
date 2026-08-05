"""Static-object exclusion for maritime SAR contacts.

A SAR contact with no AIS match is still not a dark vessel if it sits on a
known fixed object (oil platform, rig, small island/rock, navigation marker).
This module holds authoritative point/polygon datasets for the Santa Barbara
Channel theater and computes a static-object proximity score that the
fusion layer can use to shift probability from DARK to ARTIFACT.

Data sources are all public domain / US government:
- Oil platforms: California OSPR ds357 via ArcGIS REST service.
- Islands/rocks: Natural Earth 10m coastline / OpenStreetMap (future).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

from ..detect.contact import Contact


# Radius within which a contact is considered to sit on a static object.
DEFAULT_PLATFORM_BUFFER_M = 250.0


@dataclass(frozen=True)
class StaticObject:
    """A known fixed object on the water."""

    name: str
    lon: float
    lat: float
    category: str
    source: str
    buffer_m: float = DEFAULT_PLATFORM_BUFFER_M


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres between two WGS84 points."""
    R = 6_371_000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(h))


def _platforms_santa_barbara_channel() -> list[StaticObject]:
    """Return the authoritative set of oil platforms in the Santa Barbara Channel.

    Coordinates are from the California OSPR ds357 dataset (public domain),
    queried from the ArcGIS REST service on 2026-08-04.
    """
    return [
        StaticObject("Platform Irene", -120.730435, 34.610403, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Hidalgo", -120.703295, 34.495000, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Harvest", -120.681822, 34.469123, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Hermosa", -120.647392, 34.455070, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Hondo", -120.121508, 34.390723, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Harmony", -120.168503, 34.376667, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Heritage", -120.280166, 34.350383, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Holly", -119.906444, 34.389773, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Rincon Island", -119.445385, 34.347293, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Hogan", -119.542443, 34.337672, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Houchin", -119.553074, 34.334989, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Hillhouse", -119.604207, 34.331341, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Henry", -119.561355, 34.333253, "oil_platform", "OSPR ds357"),
        StaticObject("Platform A", -119.613430, 34.331884, "oil_platform", "OSPR ds357"),
        StaticObject("Platform B", -119.622497, 34.332340, "oil_platform", "OSPR ds357"),
        StaticObject("Platform C", -119.631729, 34.332923, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Gail", -119.401166, 34.125083, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Gilda", -119.419514, 34.182343, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Grace", -119.468780, 34.179572, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Habitat", -119.589052, 34.286615, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Gina", -119.277202, 34.117502, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Eureka", -118.117392, 33.563804, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Ellen", -118.129120, 33.582389, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Elly", -118.127987, 33.583425, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Edith", -118.141585, 33.595808, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Grissom", -118.181739, 33.759480, "oil_platform", "OSPR ds357"),
        StaticObject("Platform White", -118.159395, 33.752693, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Chaffee", -118.139121, 33.739849, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Freeman", -118.162439, 33.741455, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Esther", -118.114158, 33.718998, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Eva", -118.061976, 33.661740, "oil_platform", "OSPR ds357"),
        StaticObject("Platform Emmy", -118.044565, 33.662179, "oil_platform", "OSPR ds357"),
    ]


def default_static_objects() -> list[StaticObject]:
    """Return the default static-object catalog for the current theater."""
    return _platforms_santa_barbara_channel()


@dataclass
class StaticObjectHit:
    """Result of checking a contact against the static-object catalog."""

    hit: bool
    object: StaticObject | None
    distance_m: float
    confidence: float  # 0..1 probability that the contact is the object


def check_contact(
    contact: Contact,
    objects: Iterable[StaticObject] | None = None,
    buffer_m: float = DEFAULT_PLATFORM_BUFFER_M,
) -> StaticObjectHit:
    """Check whether a contact sits on or very near a known static object.

    Returns the nearest object and a confidence that the contact is that object.
    Confidence is a smooth falloff from 1.0 at the object location to 0.0 at
    ``buffer_m`` metres away.
    """
    if objects is None:
        objects = default_static_objects()

    best: StaticObject | None = None
    best_distance = float("inf")
    for obj in objects:
        d = _haversine_m(
            contact.center_lat, contact.center_lon, obj.lat, obj.lon
        )
        if d < best_distance:
            best_distance = d
            best = obj

    if best is None or best_distance > buffer_m:
        return StaticObjectHit(False, best, best_distance, 0.0)

    confidence = max(0.0, 1.0 - (best_distance / buffer_m))
    return StaticObjectHit(True, best, best_distance, confidence)
