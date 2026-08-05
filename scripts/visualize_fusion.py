"""Generate an interactive Folium map of SAR contacts, AIS tracks, platforms, and verdicts.

Usage:
    python scripts/visualize_fusion.py \
        --contacts data/processed/detections_20240718/contacts.json \
        --ais data/external/ais/ais_2024-07-18_clipped.csv \
        --verdicts data/processed/fusion_20240718/verdicts.json \
        --output notebooks/fusion_20240718_map.html
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import folium
import folium.plugins
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.fusion.ais import _haversine_m, load_ais_csv
from darkwatch.fusion.static_objects import default_static_objects

VERDICT_COLORS = {
    "CLEAR": "#2ecc71",  # green
    "DARK": "#e74c3c",  # red
    "REVIEW": "#f1c40f",  # yellow
    "ARTIFACT": "#95a5a6",  # gray
}


def _load_contacts(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_verdicts(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {v["contact_id"]: v for v in data}


def _scene_time_from_verdicts(verdicts: dict[str, dict]) -> datetime:
    # Use the first contact acquisition time or fall back to now.
    for v in verdicts.values():
        cid = v["contact_id"]
        # Parse acquisition time from contact_id if possible: ..._YYYYmmddTHHMMSS_YYYYmmddTHHMMSS_...
        parts = cid.split("_")
        for part in parts:
            if len(part) == 15 and part[8] == "T":
                try:
                    return datetime.strptime(part, "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
                except ValueError:
                    pass
    return datetime.now(timezone.utc)


def _ais_tracks(ais_path: Path) -> dict[int, pd.DataFrame]:
    df = pd.read_csv(ais_path, parse_dates=["BaseDateTime"])
    tracks: dict[int, pd.DataFrame] = {}
    for mmsi, group in df.groupby("MMSI"):
        tracks[int(mmsi)] = group.sort_values("BaseDateTime").reset_index(drop=True)
    return tracks


def _interpolate_at_time(track: pd.DataFrame, t: datetime) -> tuple[float, float] | None:
    ts = track["BaseDateTime"]
    if t < ts.iloc[0] or t > ts.iloc[-1]:
        return None
    lons = track["LON"].values
    lats = track["LAT"].values
    t0 = ts.iloc[0]
    total = (ts.iloc[-1] - t0).total_seconds()
    target = (t - t0).total_seconds()
    if total == 0:
        return float(lons[0]), float(lats[0])
    frac = target / total
    # Simple linear interpolation (track is short; great-circle would be better but this is fine for display).
    lon = lons[0] + frac * (lons[-1] - lons[0])
    lat = lats[0] + frac * (lats[-1] - lats[0])
    return float(lon), float(lat)


def build_map(
    contacts: list[dict],
    verdicts: dict[str, dict],
    ais_path: Path,
    output_path: Path,
    gate_radius_m: float = 2000.0,
) -> None:
    t_sar = _scene_time_from_verdicts(verdicts)

    # Center on mean contact position.
    if contacts:
        center_lat = sum(c["center_lat"] for c in contacts) / len(contacts)
        center_lon = sum(c["center_lon"] for c in contacts) / len(contacts)
    else:
        center_lat, center_lon = 34.4, -120.5

    m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles="CartoDB dark_matter")

    # Layer groups.
    contact_layer = folium.FeatureGroup(name="SAR contacts", show=True)
    ais_layer = folium.FeatureGroup(name="AIS tracks", show=True)
    platform_layer = folium.FeatureGroup(name="Static objects (platforms)", show=True)
    gate_layer = folium.FeatureGroup(name="2 km gate circles", show=False)

    # Static objects.
    for obj in default_static_objects():
        folium.Marker(
            location=[obj.lat, obj.lon],
            icon=folium.Icon(color="lightgray", icon="wrench", prefix="fa"),
            popup=f"{obj.name} ({obj.category})",
            tooltip=obj.name,
        ).add_to(platform_layer)

    # AIS tracks.
    tracks = _ais_tracks(ais_path)
    for mmsi, track in tracks.items():
        points = [(float(lat), float(lon)) for lat, lon in zip(track["LAT"], track["LON"])]
        name = str(track["VesselName"].dropna().iloc[0]) if not track["VesselName"].dropna().empty else "Unknown"
        folium.PolyLine(
            locations=points,
            color="#3498db",
            weight=2,
            opacity=0.6,
            popup=f"MMSI {mmsi}: {name}",
        ).add_to(ais_layer)

        # Interpolated position at SAR time.
        interp = _interpolate_at_time(track, t_sar)
        if interp:
            ilon, ilat = interp
            folium.CircleMarker(
                location=[ilat, ilon],
                radius=5,
                color="#3498db",
                fill=True,
                fill_color="#3498db",
                popup=f"{name} (MMSI {mmsi}) at SAR time\n{t_sar.isoformat()}",
            ).add_to(ais_layer)

    # SAR contacts.
    for c in contacts:
        cid = c["contact_id"]
        v = verdicts.get(cid, {})
        verdict = v.get("verdict", "REVIEW")
        color = VERDICT_COLORS.get(verdict, "#f1c40f")
        p_clear = v.get("p_clear", 0.0)
        p_dark = v.get("p_dark", 0.0)
        p_artifact = v.get("p_artifact", 0.0)
        p_review = v.get("p_review", 0.0)

        best = v.get("best_association")
        nearest = v.get("nearest_association")
        assoc = best or nearest
        assoc_text = "No AIS association"
        if assoc:
            assoc_text = (
                f"Best/nearest: MMSI {assoc['mmsi']} — {assoc.get('vessel_name', 'Unknown')}\n"
                f"Distance: {assoc['distance_m']:.0f} m"
            )

        static = v.get("static_object")
        static_text = f"Static object: {static['name']} ({static['distance_m']:.0f} m)" if static else "No static object nearby"

        popup_html = f"""
        <b>{cid[-50:]}</b><br>
        Verdict: <b>{verdict}</b><br>
        p_clear={p_clear:.3f}, p_dark={p_dark:.3f}, p_artifact={p_artifact:.3f}, p_review={p_review:.3f}<br>
        Size: {c.get('width_m', 0):.0f} m × {c.get('length_m', 0):.0f} m<br>
        Detector confidence: {c.get('confidence', 0):.3f}<br>
        {assoc_text}<br>
        {static_text}
        """

        folium.CircleMarker(
            location=[c["center_lat"], c["center_lon"]],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=400),
            tooltip=f"{verdict} ({c['contact_id'][-20:]})",
        ).add_to(contact_layer)

        # 2 km gate circle (folium.Circle uses meters).
        folium.Circle(
            location=[c["center_lat"], c["center_lon"]],
            radius=gate_radius_m,
            color=color,
            weight=1,
            fill=False,
            opacity=0.4,
        ).add_to(gate_layer)

    contact_layer.add_to(m)
    ais_layer.add_to(m)
    platform_layer.add_to(m)
    gate_layer.add_to(m)

    folium.LayerControl().add_to(m)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(output_path)
    print(f"Map saved to {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Visualize fusion results on an interactive map")
    parser.add_argument("--contacts", type=str, required=True, help="Path to contacts.json")
    parser.add_argument("--ais", type=str, required=True, help="Path to clipped AIS CSV")
    parser.add_argument("--verdicts", type=str, required=True, help="Path to verdicts.json")
    parser.add_argument("--output", type=str, required=True, help="Path to output HTML map")
    parser.add_argument("--gate-radius-m", type=float, default=2000.0)
    args = parser.parse_args()

    contacts_path = Path(args.contacts)
    ais_path = Path(args.ais)
    verdicts_path = Path(args.verdicts)
    output_path = Path(args.output)

    for p in (contacts_path, ais_path, verdicts_path):
        if not p.exists():
            print(f"ERROR: file not found: {p}", file=sys.stderr)
            return 1

    contacts = _load_contacts(contacts_path)
    verdicts = _load_verdicts(verdicts_path)
    build_map(contacts, verdicts, ais_path, output_path, gate_radius_m=args.gate_radius_m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
