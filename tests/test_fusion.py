"""Unit tests for the probabilistic SAR-to-AIS fusion module."""

from __future__ import annotations

import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from darkwatch.detect.contact import Contact
from darkwatch.fusion import (
    AISTrack,
    Verdict,
    associate_all_contacts,
    associate_contact,
    load_ais_csv,
)


def _make_ais_csv(rows: list[dict]) -> Path:
    df = pd.DataFrame(rows)
    path = Path(tempfile.mkdtemp()) / "ais.csv"
    df.to_csv(path, index=False)
    return path


def _contact_at(lon: float, lat: float, confidence: float = 0.8) -> Contact:
    return Contact(
        contact_id="c1",
        tile_id="t1",
        scene_name="s1",
        acquisition_time=datetime(2024, 7, 11, 14, 9, 10, tzinfo=timezone.utc),
        center_lon=lon,
        center_lat=lat,
        width_m=20.0,
        length_m=50.0,
        confidence=confidence,
        pixel_bbox=(10, 10, 20, 20),
        source="test",
    )


def test_load_ais_csv_filters_bbox_and_time():
    rows = [
        {
            "MMSI": 123456789,
            "BaseDateTime": "2024-07-11T14:08:00Z",
            "LAT": 34.61,
            "LON": -120.73,
            "SOG": 10.0,
        },
        {
            "MMSI": 123456789,
            "BaseDateTime": "2024-07-11T14:10:00Z",
            "LAT": 34.6101,
            "LON": -120.7301,
            "SOG": 10.0,
        },
        # Outside bbox
        {
            "MMSI": 987654321,
            "BaseDateTime": "2024-07-11T14:09:00Z",
            "LAT": 35.0,
            "LON": -121.5,
            "SOG": 10.0,
        },
        # Outside time
        {
            "MMSI": 123456789,
            "BaseDateTime": "2024-07-11T10:00:00Z",
            "LAT": 34.61,
            "LON": -120.73,
            "SOG": 10.0,
        },
    ]
    path = _make_ais_csv(rows)
    bbox = (-120.8, 34.3, -119.8, 34.7)
    time_window = (
        datetime(2024, 7, 11, 14, 0, 0, tzinfo=timezone.utc),
        datetime(2024, 7, 11, 14, 30, 0, tzinfo=timezone.utc),
    )
    tracks = load_ais_csv(path, bbox=bbox, time_window=time_window, min_messages=2)
    assert len(tracks) == 1
    assert tracks[0].mmsi == 123456789
    assert len(tracks[0].messages) == 2


def test_ais_track_interpolates_to_sar_time():
    df = pd.DataFrame(
        [
            {"BaseDateTime": "2024-07-11T14:08:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
            {"BaseDateTime": "2024-07-11T14:10:00Z", "LAT": 34.6101, "LON": -120.7301, "SOG": 10.0},
        ]
    )
    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], utc=True)
    track = AISTrack(mmsi=123456789, messages=df)
    t_sar = datetime(2024, 7, 11, 14, 9, 10, tzinfo=timezone.utc)
    lon, lat, sigma = track.interpolate(t_sar)
    assert 34.61 < lat < 34.6101
    assert -120.7301 < lon < -120.73
    assert sigma > 0


def test_associate_contact_clear_when_near_track():
    # AIS track runs straight through the contact location.
    df = pd.DataFrame(
        [
            {"BaseDateTime": "2024-07-11T14:08:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
            {"BaseDateTime": "2024-07-11T14:10:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
        ]
    )
    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], utc=True)
    track = AISTrack(mmsi=123456789, messages=df)
    contact = _contact_at(-120.73, 34.61, confidence=0.9)
    verdict = associate_contact(contact, [track])
    assert verdict.verdict == Verdict.CLEAR
    assert verdict.p_clear > verdict.p_dark


def test_associate_contact_dark_when_far_from_tracks():
    df = pd.DataFrame(
        [
            {"BaseDateTime": "2024-07-11T14:08:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
            {"BaseDateTime": "2024-07-11T14:10:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
        ]
    )
    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], utc=True)
    track = AISTrack(mmsi=123456789, messages=df)
    # Contact is 5 km away, outside the default 2 km gate.
    contact = _contact_at(-120.78, 34.61, confidence=0.9)
    verdict = associate_contact(contact, [track])
    assert verdict.verdict == Verdict.DARK
    assert verdict.p_dark > verdict.p_clear


def test_verdict_probabilities_sum_to_one():
    df = pd.DataFrame(
        [
            {"BaseDateTime": "2024-07-11T14:08:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
            {"BaseDateTime": "2024-07-11T14:10:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
        ]
    )
    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], utc=True)
    track = AISTrack(mmsi=123456789, messages=df)
    contact = _contact_at(-120.73, 34.61, confidence=0.5)
    verdict = associate_contact(contact, [track])
    total = verdict.p_artifact + verdict.p_clear + verdict.p_dark + verdict.p_review
    assert np.isclose(total, 1.0, atol=1e-3)


def test_real_vessel_mass_is_partitioned_between_clear_and_dark():
    """Regression: real-vessel mass (clear + dark + review) must be conserved.

    When a track lies inside the gate, review mass is zero and the original
    invariant (clear + dark = real mass) still holds. When no track is near,
    some dark mass is honestly moved to review, so clear + dark + review
    must equal real mass.
    """
    df = pd.DataFrame(
        [
            {"BaseDateTime": "2024-07-11T14:08:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
            {"BaseDateTime": "2024-07-11T14:10:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
        ]
    )
    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], utc=True)
    track = AISTrack(mmsi=123456789, messages=df)
    contact = _contact_at(-120.73, 34.61, confidence=0.5)
    verdict = associate_contact(contact, [track])
    real_mass = 1.0 - verdict.p_artifact
    assert np.isclose(verdict.p_clear + verdict.p_dark + verdict.p_review, real_mass, atol=1e-3)
    assert verdict.n_tracks_within_gate == 1


def test_associate_all_contacts_returns_one_per_contact():
    df = pd.DataFrame(
        [
            {"BaseDateTime": "2024-07-11T14:08:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
            {"BaseDateTime": "2024-07-11T14:10:00Z", "LAT": 34.61, "LON": -120.73, "SOG": 10.0},
        ]
    )
    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], utc=True)
    track = AISTrack(mmsi=123456789, messages=df)
    contacts = [_contact_at(-120.73, 34.61), _contact_at(-120.78, 34.61)]
    verdicts = associate_all_contacts(contacts, [track])
    assert len(verdicts) == 2
