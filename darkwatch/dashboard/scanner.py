"""Scan ``data/processed`` for completed Darkwatch scenes.

A scene is considered dashboard-ready when it contains at least a
``verdicts.json`` and ``summary.json`` file. Contacts and generated maps are
attached opportunistically.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = REPO_ROOT / "data" / "processed"


@dataclass
class Scene:
    """Dashboard representation of one processed scene."""

    scene_id: str
    path: Path
    verdicts: list[dict[str, Any]] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    contacts: list[dict[str, Any]] = field(default_factory=list)
    map_html: str | None = None
    processing_state: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        try:
            rel_path = str(self.path.relative_to(REPO_ROOT))
        except ValueError:
            rel_path = str(self.path)
        return {
            "scene_id": self.scene_id,
            "path": rel_path,
            "verdicts": self.verdicts,
            "summary": self.summary,
            "contacts": self.contacts,
            "map_html": self.map_html,
            "processing_state": self.processing_state,
        }


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _find_map_html(scene_path: Path, scene_id: str) -> Path | None:
    """Look for a generated Folium map near the scene or in notebooks/."""
    candidates = [
        scene_path / "map.html",
        scene_path / f"{scene_id}_map.html",
    ]
    # Standard report maps are notebooks/fusion_YYYYMMDD_map.html. Try to pull
    # an 8-digit date out of the scene id (e.g. fusion_20240706_v4_adaptive).
    m = re.search(r"(\d{8})", scene_id)
    if m:
        date_part = m.group(1)
        candidates.append(REPO_ROOT / "notebooks" / f"fusion_{date_part}_map.html")
        candidates.append(REPO_ROOT / "notebooks" / f"fusion_{date_part}_socal_cal_map.html")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _contact_date(contact_id: str) -> str | None:
    """Extract YYYYMMDD acquisition date from a Sentinel-1 contact id."""
    import re

    m = re.search(r"_(\d{8})T\d{6}_", contact_id)
    if m:
        return m.group(1)
    return None


def find_contact_thumbnail(contact_id: str) -> Path | None:
    """Return the zoom review-grid PNG path for a contact, if available."""
    date = _contact_date(contact_id)
    if not date:
        return None
    thumb_dir = REPO_ROOT / "notebooks" / f"contact_viz_{date}_v4_adaptive"
    if not thumb_dir.exists():
        return None
    # Zoomed chip is the analyst-friendly view.
    zoom_candidate = thumb_dir / f"{contact_id}_zoom.png"
    if zoom_candidate.exists():
        return zoom_candidate
    full_candidate = thumb_dir / f"{contact_id}.png"
    if full_candidate.exists():
        return full_candidate
    return None


def scan_scenes(data_dir: Path = DEFAULT_DATA_DIR) -> list[Scene]:
    """Return dashboard-ready scenes under *data_dir*."""
    scenes: list[Scene] = []
    if not data_dir.exists():
        return scenes

    for entry in sorted(data_dir.iterdir()):
        if not entry.is_dir():
            continue
        verdicts_path = entry / "verdicts.json"
        summary_path = entry / "summary.json"
        if not verdicts_path.exists() or not summary_path.exists():
            continue

        scene = Scene(scene_id=entry.name, path=entry)
        scene.verdicts = _load_json(verdicts_path) or []
        scene.summary = _load_json(summary_path) or {}
        scene.contacts = _load_json(entry / "contacts.json") or []
        if not scene.contacts:
            # Contacts are usually stored in the detections_YYYYMMDD directory.
            m = re.search(r"(\d{8})", entry.name)
            if m:
                detections_dir = (
                    REPO_ROOT / "data" / "processed" / f"detections_{m.group(1)}_v4_adaptive"
                )
                if detections_dir.exists():
                    scene.contacts = _load_json(detections_dir / "contacts.json") or []

        map_path = _find_map_html(entry, entry.name)
        if map_path:
            scene.map_html = map_path.read_text(encoding="utf-8")

        scene.processing_state = _load_json(entry / "processing_state.json")
        scenes.append(scene)

    return scenes


def find_scene(scene_id: str, data_dir: Path = DEFAULT_DATA_DIR) -> Scene | None:
    """Return a single scene by id, or None if not found."""
    for scene in scan_scenes(data_dir):
        if scene.scene_id == scene_id:
            return scene
    return None
