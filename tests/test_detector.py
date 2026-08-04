"""Unit tests for detector helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from darkwatch.detect.contact import Contact
from darkwatch.detect.detector import _haversine_m, _deduplicate_contacts


def test_haversine_m_known_distance():
    """Haversine distance between two close points should be reasonable."""
    # ~1 degree of latitude is ~111 km.
    dist = _haversine_m(0.0, 0.0, 1.0, 0.0)
    assert 110_000 < dist < 112_000


def test_deduplicate_contacts_keeps_highest_confidence():
    """Contacts within the merge distance should keep the highest-confidence one."""
    base = dict(
        tile_id="t1",
        scene_name="scene",
        acquisition_time=datetime.now(timezone.utc),
        width_m=100.0,
        length_m=100.0,
        pixel_bbox=(0.0, 0.0, 10.0, 10.0),
        source="model.pt",
    )
    contacts = [
        Contact(contact_id="c1", center_lon=0.0, center_lat=0.0, confidence=0.5, **base),
        Contact(contact_id="c2", center_lon=0.0, center_lat=0.0001, confidence=0.9, **base),
        Contact(contact_id="c3", center_lon=10.0, center_lat=10.0, confidence=0.7, **base),
    ]
    kept = _deduplicate_contacts(contacts, distance_m=100.0)
    assert len(kept) == 2
    assert kept[0].contact_id == "c2"
    assert any(c.contact_id == "c3" for c in kept)


def test_deduplicate_contacts_different_objects():
    """Contacts far apart should not be merged."""
    base = dict(
        tile_id="t1",
        scene_name="scene",
        acquisition_time=datetime.now(timezone.utc),
        width_m=100.0,
        length_m=100.0,
        pixel_bbox=(0.0, 0.0, 10.0, 10.0),
        source="model.pt",
    )
    contacts = [
        Contact(contact_id="c1", center_lon=0.0, center_lat=0.0, confidence=0.5, **base),
        Contact(contact_id="c2", center_lon=1.0, center_lat=0.0, confidence=0.9, **base),
    ]
    kept = _deduplicate_contacts(contacts, distance_m=100.0)
    assert len(kept) == 2
