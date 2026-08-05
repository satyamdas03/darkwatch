"""Run probabilistic SAR-to-AIS fusion on detected contacts.

Usage:
    python scripts/fuse_contacts.py \
        --contacts data/processed/detections_20240711/contacts.json \
        --ais data/external/ais/ais_2024-07-11_clipped.csv \
        --output-dir data/processed/fusion_20240711
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.detect.contact import Contact
from darkwatch.fusion import associate_all_contacts, load_ais_csv


def _parse_bbox(value: str) -> tuple[float, float, float, float]:
    parts = [float(v.strip()) for v in value.split(",")]
    if len(parts) != 4:
        raise ValueError("bbox must be min_lon,min_lat,max_lon,max_lat")
    return tuple(parts)  # type: ignore[return-value]


def load_contacts(path: Path) -> list[Contact]:
    data = json.loads(path.read_text())
    contacts: list[Contact] = []
    for item in data:
        contacts.append(
            Contact(
                contact_id=item["contact_id"],
                tile_id=item["tile_id"],
                scene_name=item["scene_name"],
                acquisition_time=datetime.fromisoformat(item["acquisition_time"]),
                center_lon=item["center_lon"],
                center_lat=item["center_lat"],
                width_m=item.get("width_m"),
                length_m=item.get("length_m"),
                confidence=item["confidence"],
                pixel_bbox=tuple(item["pixel_bbox"]),
                source=item["source"],
            )
        )
    return contacts


def main() -> int:
    parser = argparse.ArgumentParser(description="Fuse SAR contacts with AIS tracks")
    parser.add_argument("--contacts", type=str, required=True, help="Path to contacts.json")
    parser.add_argument("--ais", type=str, required=True, help="Path to clipped AIS CSV")
    parser.add_argument("--output-dir", type=str, default=str(REPO_ROOT / "data" / "processed" / "fusion"))
    parser.add_argument("--gate-m", type=float, default=2_000.0, help="Association gate radius in metres")
    parser.add_argument("--time-window-minutes", type=int, default=60, help="AIS interpolation window around SAR time")
    parser.add_argument("--bbox", type=str, default=None, help="Optional AIS bbox filter")
    args = parser.parse_args()

    contacts_path = Path(args.contacts)
    ais_path = Path(args.ais)
    if not contacts_path.exists():
        print(f"ERROR: contacts not found: {contacts_path}", file=sys.stderr)
        return 1
    if not ais_path.exists():
        print(f"ERROR: AIS CSV not found: {ais_path}", file=sys.stderr)
        return 1

    contacts = load_contacts(contacts_path)
    if not contacts:
        print("ERROR: no contacts to fuse", file=sys.stderr)
        return 1

    t_sar = contacts[0].acquisition_time
    half = timedelta(minutes=args.time_window_minutes)
    time_window = (t_sar - half, t_sar + half)

    bbox = None
    if args.bbox:
        bbox = _parse_bbox(args.bbox)

    print(f"Loading AIS tracks from {ais_path} ...")
    tracks = load_ais_csv(ais_path, bbox=bbox, time_window=time_window, min_messages=2)
    print(f"Loaded {len(tracks)} AIS tracks")

    print(f"Fusing {len(contacts)} contacts ...")
    verdicts = associate_all_contacts(contacts, tracks, t_sar=t_sar, gate_radius_m=args.gate_m)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    def _assoc_dict(a):
        if a is None:
            return None
        return {
            "mmsi": a.mmsi,
            "vessel_name": a.vessel_name,
            "distance_m": round(a.distance_m, 1),
            "sigma_m": round(a.sigma_m, 1),
            "interpolated_lon": a.interpolated_lon,
            "interpolated_lat": a.interpolated_lat,
            "p_match": round(a.likelihood, 4),
        }

    def _static_dict(s):
        if s is None or not s.hit:
            return None
        return {
            "name": s.object.name if s.object else None,
            "distance_m": round(s.distance_m, 1),
            "confidence": round(s.confidence, 4),
        }

    results = []
    for v in verdicts:
        results.append(
            {
                "contact_id": v.contact_id,
                "verdict": v.verdict.value,
                "p_artifact": round(v.p_artifact, 4),
                "p_clear": round(v.p_clear, 4),
                "p_dark": round(v.p_dark, 4),
                "p_review": round(v.p_review, 4),
                "n_tracks_within_gate": v.n_tracks_within_gate,
                "n_tracks_near_gate": v.n_tracks_near_gate,
                "best_association": _assoc_dict(v.best_association),
                "nearest_association": _assoc_dict(v.nearest_association),
                "static_object": _static_dict(v.static_object_hit),
                "reasoning": v.reasoning,
            }
        )

    output_path = output_dir / "verdicts.json"
    output_path.write_text(json.dumps(results, indent=2))
    print(f"Verdicts saved to {output_path}")

    # Summary
    counts: dict[str, int] = {}
    for v in verdicts:
        counts[v.verdict.value] = counts.get(v.verdict.value, 0) + 1
    summary = {
        "scene_time": t_sar.isoformat() if t_sar else None,
        "gate_radius_m": args.gate_m,
        "contacts_fused": len(contacts),
        "ais_tracks_loaded": len(tracks),
        "verdict_counts": counts,
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print("Verdict summary:", counts)
    print(f"Summary saved to {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
