"""Fit a learned calibration model for Darkwatch fusion probabilities.

Usage:
    python scripts/fit_calibration.py \
        --labels data/processed/calibration_labels_v4_adaptive_recal3.json \
        --output data/processed/fusion_calibration_v4_adaptive_recal3.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.fusion.calibration import CalibrationModel, brier_score


def _load_records(labels_path: Path) -> list[dict]:
    labels_data = json.loads(labels_path.read_text(encoding="utf-8"))
    labels = {entry["contact_id"]: entry["label"].upper() for entry in labels_data.get("labels", [])}

    records: list[dict] = []
    for scene in labels_data.get("scenes", []):
        verdicts_path = Path(scene["verdicts"])
        if not verdicts_path.is_absolute():
            verdicts_path = REPO_ROOT / verdicts_path
        verdicts = json.loads(verdicts_path.read_text(encoding="utf-8"))
        for v in verdicts:
            cid = v["contact_id"]
            if cid not in labels:
                continue
            records.append(
                {
                    "contact_id": cid,
                    "scene": scene["name"],
                    "true_label": labels[cid],
                    "p_artifact": v["p_artifact"],
                    "p_clear": v["p_clear"],
                    "p_dark": v["p_dark"],
                    "p_review": v["p_review"],
                }
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit Darkwatch fusion calibration model")
    parser.add_argument(
        "--labels",
        type=str,
        default=str(REPO_ROOT / "data" / "processed" / "calibration_labels_v4_adaptive_recal3.json"),
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(REPO_ROOT / "data" / "processed" / "fusion_calibration_v4_adaptive_recal3.json"),
    )
    parser.add_argument(
        "--l2-penalty",
        type=float,
        default=0.01,
        help="L2 regularization encouraging identity mapping",
    )
    args = parser.parse_args()

    labels_path = Path(args.labels)
    output_path = Path(args.output)
    if not labels_path.exists():
        print(f"ERROR: labels file not found: {labels_path}", file=sys.stderr)
        return 1

    records = _load_records(labels_path)
    if not records:
        print("ERROR: no labeled contacts found", file=sys.stderr)
        return 1

    model = CalibrationModel().fit(records, l2_penalty=args.l2_penalty)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(output_path)

    print(f"Fitted calibration model on {len(records)} contacts")
    print(f"Saved to {output_path}")
    print("Parameters:")
    for pkey, (scale, shift) in sorted(model.params.items()):
        print(f"  {pkey}: scale={scale:.4f}, shift={shift:.4f}")

    print("\nPer-class Brier (raw -> calibrated):")
    calibrated = model.transform_records(records)
    for pkey in model.classes:
        class_name = model._verdict_from_key(pkey)
        raw_probs = np.array([r[pkey] for r in records])
        cal_probs = np.array([r[pkey] for r in calibrated])
        outcomes = np.array([1.0 if r["true_label"] == class_name else 0.0 for r in records])
        raw_brier = brier_score(raw_probs, outcomes)
        cal_brier = brier_score(cal_probs, outcomes)
        n_pos = int(np.sum(outcomes))
        print(f"  {class_name}: {raw_brier:.4f} -> {cal_brier:.4f}  (positives={n_pos})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
