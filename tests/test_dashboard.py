"""Tests for the Darkwatch analyst dashboard API."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from darkwatch.dashboard.api import create_app


@pytest.fixture
def mock_processed_dir(tmp_path: Path) -> Path:
    """Create a minimal processed scene with verdicts, summary, contacts."""
    scene_dir = tmp_path / "test_scene_20240101_v4_adaptive"
    scene_dir.mkdir()

    verdicts = [
        {
            "contact_id": "S1A_IW_GRDH_1SDV_20240101T000000_000000_000000_0000_vv_c100_r100_det0000",
            "verdict": "DARK",
            "p_artifact": 0.1,
            "p_clear": 0.05,
            "p_dark": 0.75,
            "p_review": 0.1,
            "n_tracks_within_gate": 0,
            "n_tracks_near_gate": 0,
            "best_association": None,
            "nearest_association": None,
            "static_object": None,
            "reasoning": "No AIS match within gate.",
        }
    ]
    summary = {
        "scene_time": "2024-01-01T00:00:00Z",
        "verdict_counts": {"DARK": 1, "CLEAR": 0, "ARTIFACT": 0, "REVIEW": 0},
        "contacts_fused": 1,
        "ais_tracks_loaded": 0,
    }
    contacts = [
        {
            "contact_id": "S1A_IW_GRDH_1SDV_20240101T000000_000000_000000_0000_vv_c100_r100_det0000",
            "center_lon": -118.0,
            "center_lat": 34.0,
            "width_m": 25.0,
            "length_m": 80.0,
            "confidence": 0.42,
        }
    ]

    (scene_dir / "verdicts.json").write_text(json.dumps(verdicts))
    (scene_dir / "summary.json").write_text(json.dumps(summary))
    (scene_dir / "contacts.json").write_text(json.dumps(contacts))
    return tmp_path


def test_health(mock_processed_dir: Path) -> None:
    app = create_app(data_dir=mock_processed_dir)
    client = TestClient(app)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_scenes(mock_processed_dir: Path) -> None:
    app = create_app(data_dir=mock_processed_dir)
    client = TestClient(app)
    resp = client.get("/api/scenes")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["scenes"]) == 1
    scene = data["scenes"][0]
    assert scene["scene_id"] == "test_scene_20240101_v4_adaptive"
    assert len(scene["verdicts"]) == 1
    assert scene["verdicts"][0]["verdict"] == "DARK"


def test_get_scene(mock_processed_dir: Path) -> None:
    app = create_app(data_dir=mock_processed_dir)
    client = TestClient(app)
    resp = client.get("/api/scenes/test_scene_20240101_v4_adaptive")
    assert resp.status_code == 200
    scene = resp.json()
    assert scene["scene_id"] == "test_scene_20240101_v4_adaptive"
    assert scene["summary"]["contacts_fused"] == 1


def test_get_scene_not_found(mock_processed_dir: Path) -> None:
    app = create_app(data_dir=mock_processed_dir)
    client = TestClient(app)
    resp = client.get("/api/scenes/missing_scene")
    assert resp.status_code == 404


def test_root_serves_dashboard(mock_processed_dir: Path) -> None:
    app = create_app(data_dir=mock_processed_dir)
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Darkwatch" in resp.text
