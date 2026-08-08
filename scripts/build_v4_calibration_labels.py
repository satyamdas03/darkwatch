"""Build ground-truth labels for the v4 adaptive-stretch calibration dataset.

Rules (applied in order; first match wins):
1. Manual overrides for well-documented ambiguous cases.
2. AIS association inside the gate -> CLEAR.
3. Static object (oil platform) within 200 m -> ARTIFACT.
4. Contact dimension > 500 m -> ARTIFACT (azimuth-ambiguity / wind streak).
5. Bounding box touches the tile edge (<= 1 px) -> ARTIFACT.
6. Contact center outside the default Santa Barbara theater -> ARTIFACT.
7. Otherwise -> DARK (no cooperative AIS, no platform, plausible vessel size).

The script reads the v4 adaptive detection contacts and fusion verdicts, emits
`data/processed/calibration_labels_v4_adaptive.json`, and prints a summary.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.fusion.verdict import Verdict

DEFAULT_THEATER = (-119.05, 34.55, -118.6, 34.75)  # (min_lon, min_lat, max_lon, max_lat)

# Manual overrides keyed by contact_id.
OVERRIDES: dict[str, tuple[str, str]] = {
    # July 11: low-confidence contact far outside the Channel Islands theater.
    "S1A_IW_GRDH_1SDV_20240711T140858_20240711T140923_054714_06A94E_9466_vh_c4210_r14398_det0000": (
        "ARTIFACT",
        "Low-confidence detection far outside operational theater; likely false positive",
    ),
    # July 18: plausible-looking VV contact in the Santa Barbara east lane but no AIS
    # within the gate; large dimensions and proximity to KNOX T's corridor make it
    # an azimuth-ambiguity or duplicate-detection candidate rather than a confident dark vessel.
    "S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c9548_r7947_det0000": (
        "UNKNOWN",
        "No AIS within gate, no platform nearby, but 244x375 m and near KNOX T corridor; ambiguous",
    ),
    # July 23: tile-edge detection in the crowded northern cluster; treat as artifact.
    "S1A_IW_GRDH_1SDV_20240723T020701_20240723T020726_054882_06AF26_69FC_vh_c21010_r14232_det0002": (
        "ARTIFACT",
        "Tile-edge detection (xmin~0, ymin~0) within crowded cluster; likely truncation artifact",
    ),
}


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _touches_edge(pixel_bbox: list[float], image_size: tuple[float, float] = (1024.0, 1024.0)) -> bool:
    xmin, ymin, xmax, ymax = pixel_bbox
    w, h = image_size
    margin = 1.0
    return xmin <= margin or ymin <= margin or xmax >= (w - margin) or ymax >= (h - margin)


def _inside_theater(lon: float, lat: float) -> bool:
    min_lon, min_lat, max_lon, max_lat = DEFAULT_THEATER
    return min_lon <= lon <= max_lon and min_lat <= lat <= max_lat


def _label_contact(contact: dict, verdict: dict) -> tuple[str, str]:
    cid = contact["contact_id"]
    if cid in OVERRIDES:
        return OVERRIDES[cid]

    width_m = contact.get("width_m", 0.0)
    length_m = contact.get("length_m", 0.0)
    pixel_bbox = contact.get("pixel_bbox", [0.0, 0.0, 0.0, 0.0])
    center_lon = contact.get("center_lon", 0.0)
    center_lat = contact.get("center_lat", 0.0)

    n_tracks = verdict.get("n_tracks_within_gate", 0)
    static = verdict.get("static_object")
    static_dist = static["distance_m"] if static else float("inf")

    if n_tracks > 0:
        assoc = verdict.get("best_association") or verdict.get("nearest_association")
        name = assoc.get("vessel_name", assoc.get("mmsi", "unknown")) if assoc else "unknown"
        dist = assoc.get("distance_m", float("nan")) if assoc else float("nan")
        return (
            "CLEAR",
            f"AIS association inside gate: {name} at {dist:.0f} m",
        )

    # Use the same 250 m buffer as the fusion static-object check.
    if static_dist < 250.0:
        return (
            "ARTIFACT",
            f"Static object {static['name']} at {static_dist:.0f} m",
        )

    if max(width_m, length_m) > 500.0:
        return (
            "ARTIFACT",
            f"Oversized detection ({width_m:.0f} m x {length_m:.0f} m); likely azimuth ambiguity or wind streak",
        )

    if _touches_edge(pixel_bbox):
        return (
            "ARTIFACT",
            "Detection bounding box touches tile edge; likely truncation artifact",
        )

    return (
        "DARK",
        "No AIS within gate, no platform within 200 m, plausible vessel dimensions",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v4 adaptive calibration labels")
    parser.add_argument(
        "--output",
        type=str,
        default=str(REPO_ROOT / "data" / "processed" / "calibration_labels_v4_adaptive.json"),
    )
    args = parser.parse_args()

    scenes = [
        {
            "name": "2024-07-11",
            "contacts": REPO_ROOT / "data" / "processed" / "detections_20240711_v4_adaptive" / "contacts.json",
            "verdicts": REPO_ROOT / "data" / "processed" / "fusion_20240711_v4_adaptive" / "verdicts.json",
        },
        {
            "name": "2024-07-18",
            "contacts": REPO_ROOT / "data" / "processed" / "detections_20240718_v4_adaptive" / "contacts.json",
            "verdicts": REPO_ROOT / "data" / "processed" / "fusion_20240718_v4_adaptive" / "verdicts.json",
        },
        {
            "name": "2024-07-23",
            "contacts": REPO_ROOT / "data" / "processed" / "detections_20240723_v4_adaptive" / "contacts.json",
            "verdicts": REPO_ROOT / "data" / "processed" / "fusion_20240723_v4_adaptive" / "verdicts.json",
        },
    ]

    labels: list[dict] = []
    label_counts: dict[str, int] = {}
    for scene in scenes:
        contacts = json.loads(scene["contacts"].read_text(encoding="utf-8"))
        verdicts = {v["contact_id"]: v for v in json.loads(scene["verdicts"].read_text(encoding="utf-8"))}
        for contact in contacts:
            cid = contact["contact_id"]
            verdict = verdicts.get(cid)
            if verdict is None:
                print(f"WARN: no verdict for {cid}", file=sys.stderr)
                continue
            label, note = _label_contact(contact, verdict)
            labels.append(
                {
                    "contact_id": cid,
                    "label": label,
                    "note": note,
                }
            )
            label_counts[label] = label_counts.get(label, 0) + 1

    output_data = {
        "scenes": [
            {
                "name": s["name"],
                "verdicts": str(s["verdicts"].relative_to(REPO_ROOT)).replace("\\", "/"),
            }
            for s in scenes
        ],
        "labels": labels,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")

    print(f"Wrote {len(labels)} labels to {output_path}")
    for label, count in sorted(label_counts.items()):
        print(f"  {label}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
