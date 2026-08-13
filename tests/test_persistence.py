"""Tests for Darkwatch persistence clustering."""

from __future__ import annotations

import pytest

from darkwatch.persistence.cluster import cluster_contacts, persistence_for_contact, tag_all_contacts


def test_cluster_finds_persistent_group() -> None:
    contacts = [
        # Cluster A: two scenes close together.
        {"contact_id": "a1", "center_lat": 34.0, "center_lon": -118.0, "scene_date": "20240711"},
        {"contact_id": "a2", "center_lat": 34.0005, "center_lon": -118.0005, "scene_date": "20240718"},
        # Noise: single isolated contact.
        {"contact_id": "b1", "center_lat": 35.0, "center_lon": -119.0, "scene_date": "20240711"},
    ]
    labels = cluster_contacts(contacts, eps_m=500.0, min_samples=2)
    assert labels[0] == labels[1]
    assert labels[2] == -1


def test_persistence_summary() -> None:
    contacts = [
        {"contact_id": "a1", "center_lat": 34.0, "center_lon": -118.0, "scene_date": "20240711"},
        {"contact_id": "a2", "center_lat": 34.0005, "center_lon": -118.0005, "scene_date": "20240718"},
        {"contact_id": "b1", "center_lat": 35.0, "center_lon": -119.0, "scene_date": "20240711"},
    ]
    labels = cluster_contacts(contacts, eps_m=500.0, min_samples=2)
    p0 = persistence_for_contact(contacts, 0, labels)
    assert p0["is_persistent"] is True
    assert p0["n_scenes"] == 2

    p2 = persistence_for_contact(contacts, 2, labels)
    assert p2["is_persistent"] is False


def test_tag_all_contacts() -> None:
    contacts = [
        {"contact_id": "a1", "center_lat": 34.0, "center_lon": -118.0, "scene_date": "20240711"},
        {"contact_id": "a2", "center_lat": 34.0005, "center_lon": -118.0005, "scene_date": "20240718"},
    ]
    tagged = tag_all_contacts(contacts, eps_m=500.0, min_samples=2)
    assert tagged[0]["persistence"]["is_persistent"] is True
