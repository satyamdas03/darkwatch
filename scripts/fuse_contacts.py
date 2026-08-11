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
from darkwatch.fusion.associate import (
    DEFAULT_PLAUSIBILITY_ABSOLUTE_MARGIN_M,
    DEFAULT_PLAUSIBILITY_LENGTH_TOLERANCE,
)
from darkwatch.fusion.calibration import CalibrationModel
from darkwatch.fusion.static_objects import default_static_objects


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
    parser.add_argument("--static-confidence-scale", type=float, default=1.5, help="Multiplier for raw static-object confidence")
    parser.add_argument("--static-confidence-floor", type=float, default=0.3, help="Minimum static-object confidence for any hit")
    parser.add_argument("--size-max-dim-soft-m", type=float, default=500.0, help="Soft size threshold for artifact evidence")
    parser.add_argument("--size-max-dim-hard-m", type=float, default=1_000.0, help="Hard size threshold for artifact evidence")
    parser.add_argument("--size-tile-edge-min-size-m", type=float, default=80.0, help="Minimum contact size (m) for tile-edge artifact penalty to apply")
    parser.add_argument("--size-tile-edge-min-tile-ratio", type=float, default=0.0, help="Minimum contact max-dim / min-tile-dim ratio for tile-edge penalty (0 disables)")
    parser.add_argument("--artifact-conf-ais-discount-power", type=float, default=1.0, help="Power for (1 - p_matched_given_real) artifact discount for strong AIS matches")
    parser.add_argument("--dark-artifact-coupling", type=float, default=0.6, help="How strongly artifact evidence competes with dark-vessel residual")
    parser.add_argument("--disable-physical-plausibility", action="store_true", help="Disable the AIS size-compatibility gate")
    parser.add_argument("--plausibility-length-tolerance", type=float, default=DEFAULT_PLAUSIBILITY_LENGTH_TOLERANCE, help="Multiplier on AIS vessel length allowed for SAR contact max dimension")
    parser.add_argument("--plausibility-absolute-margin-m", type=float, default=DEFAULT_PLAUSIBILITY_ABSOLUTE_MARGIN_M, help="Absolute margin (m) added to allowed SAR contact size")
    parser.add_argument("--calibration-model", type=str, default=None, help="Optional JSON calibration model to apply to raw probabilities")
    parser.add_argument("--theater", type=str, default=None, choices=["santa_barbara", "gulf"], help="Static-object catalog theater (santa_barbara or gulf)")
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

    static_objects = None
    if args.theater:
        static_objects = default_static_objects(args.theater)
        print(f"Loaded static-object catalog for theater: {args.theater}")

    print(f"Fusing {len(contacts)} contacts ...")
    verdicts = associate_all_contacts(
        contacts,
        tracks,
        t_sar=t_sar,
        gate_radius_m=args.gate_m,
        static_objects=static_objects,
        static_confidence_scale=args.static_confidence_scale,
        static_confidence_floor=args.static_confidence_floor,
        size_max_dim_soft_m=args.size_max_dim_soft_m,
        size_max_dim_hard_m=args.size_max_dim_hard_m,
        size_tile_edge_min_size_m=args.size_tile_edge_min_size_m,
        size_tile_edge_min_tile_ratio=args.size_tile_edge_min_tile_ratio,
        artifact_conf_ais_discount_power=args.artifact_conf_ais_discount_power,
        dark_artifact_coupling=args.dark_artifact_coupling,
        enable_physical_plausibility=not args.disable_physical_plausibility,
        plausibility_length_tolerance=args.plausibility_length_tolerance,
        plausibility_absolute_margin_m=args.plausibility_absolute_margin_m,
    )

    calibration_model = None
    if args.calibration_model:
        calibration_model = CalibrationModel.load(args.calibration_model)
        print(f"Loaded calibration model from {args.calibration_model}")

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

    if calibration_model is not None:
        from darkwatch.fusion.verdict import Verdict

        for r in results:
            cal = calibration_model.transform(
                r["p_artifact"], r["p_clear"], r["p_dark"], r["p_review"]
            )
            r["p_artifact"] = round(cal["p_artifact"], 4)
            r["p_clear"] = round(cal["p_clear"], 4)
            r["p_dark"] = round(cal["p_dark"], 4)
            r["p_review"] = round(cal["p_review"], 4)
            if cal["p_artifact"] > 0.5:
                r["verdict"] = Verdict.ARTIFACT.value
            elif cal["p_clear"] > 0.6:
                r["verdict"] = Verdict.CLEAR.value
            elif cal["p_dark"] > 0.6:
                r["verdict"] = Verdict.DARK.value
            else:
                r["verdict"] = Verdict.REVIEW.value

    output_path = output_dir / "verdicts.json"
    output_path.write_text(json.dumps(results, indent=2))
    print(f"Verdicts saved to {output_path}")

    # Summary
    counts: dict[str, int] = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    calibration_model_rel = None
    if args.calibration_model:
        model_path = Path(args.calibration_model)
        if not model_path.is_absolute():
            model_path = REPO_ROOT / model_path
        try:
            calibration_model_rel = str(model_path.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            calibration_model_rel = str(model_path).replace("\\", "/")

    summary = {
        "scene_time": t_sar.isoformat() if t_sar else None,
        "gate_radius_m": args.gate_m,
        "contacts_fused": len(contacts),
        "ais_tracks_loaded": len(tracks),
        "verdict_counts": counts,
        "calibration_model": calibration_model_rel,
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print("Verdict summary:", counts)
    print(f"Summary saved to {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
