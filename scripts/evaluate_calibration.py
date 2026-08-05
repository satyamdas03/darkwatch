"""Evaluate calibration of Darkwatch fusion probabilities against ground-truth labels.

Usage:
    python scripts/evaluate_calibration.py \
        --labels data/processed/calibration_labels.json \
        --output-dir notebooks/calibration
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.fusion.verdict import Verdict


def _load_labels(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    labels = {}
    for entry in data.get("labels", []):
        contact_id = entry["contact_id"]
        label = entry["label"].upper()
        if label not in {v.name for v in Verdict} | {"UNKNOWN"}:
            raise ValueError(f"Unknown label '{label}' for {contact_id}")
        labels[contact_id] = label
    return labels


def _load_verdicts_by_contact(path: Path) -> dict[str, dict]:
    verdicts = json.loads(path.read_text(encoding="utf-8"))
    return {v["contact_id"]: v for v in verdicts}


def _gather_predictions(labels: dict[str, str], verdict_paths: dict[str, Path]) -> dict:
    """Collect predicted probabilities and true labels across scenes."""
    records = []
    missing = []
    for contact_id, true_label in labels.items():
        found = False
        for scene, vpath in verdict_paths.items():
            verdicts = _load_verdicts_by_contact(vpath)
            if contact_id in verdicts:
                v = verdicts[contact_id]
                records.append(
                    {
                        "contact_id": contact_id,
                        "scene": scene,
                        "true_label": true_label,
                        "verdict": v["verdict"],
                        "p_artifact": v["p_artifact"],
                        "p_clear": v["p_clear"],
                        "p_dark": v["p_dark"],
                        "p_review": v["p_review"],
                        "n_tracks_within_gate": v["n_tracks_within_gate"],
                        "static_object": v.get("static_object"),
                        "nearest_dist_m": (
                            v.get("nearest_association", {}) or {}
                        ).get("distance_m"),
                    }
                )
                found = True
                break
        if not found:
            missing.append(contact_id)
    if missing:
        print(f"WARNING: {len(missing)} labeled contacts not found in verdicts:", file=sys.stderr)
        for cid in missing:
            print(f"  - {cid}", file=sys.stderr)
    return {"records": records}


def _brier_score(probs: np.ndarray, outcomes: np.ndarray) -> float:
    if len(probs) == 0:
        return float("nan")
    return float(np.mean((probs - outcomes) ** 2))


def _reliability_bins(probs: np.ndarray, outcomes: np.ndarray, n_bins: int = 5) -> tuple:
    """Return bin centers, observed fractions, counts, mean predicted per bin."""
    if len(probs) == 0:
        return np.array([]), np.array([]), np.array([]), np.array([])
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    observed = np.zeros(n_bins)
    counts = np.zeros(n_bins, dtype=int)
    mean_pred = np.zeros(n_bins)
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        if i == n_bins - 1:
            mask = (probs >= lo) & (probs <= hi)
        else:
            mask = (probs >= lo) & (probs < hi)
        counts[i] = int(np.count_nonzero(mask))
        if counts[i] > 0:
            observed[i] = float(np.mean(outcomes[mask]))
            mean_pred[i] = float(np.mean(probs[mask]))
        else:
            mean_pred[i] = centers[i]
    return centers, observed, counts, mean_pred


def _plot_reliability(
    probs: np.ndarray,
    outcomes: np.ndarray,
    class_name: str,
    n_bins: int,
    output_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    centers, observed, counts, mean_pred = _reliability_bins(probs, outcomes, n_bins)
    # Only plot bins with data
    valid = counts > 0
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect calibration")
    ax.scatter(mean_pred[valid], observed[valid], s=120, zorder=3, label="Observed fraction")
    for x, y, c in zip(mean_pred[valid], observed[valid], counts[valid]):
        ax.annotate(str(c), (x, y), textcoords="offset points", xytext=(6, 4), fontsize=9)
    ax.set_xlabel(f"Predicted p_{class_name.lower()}")
    ax.set_ylabel(f"Observed {class_name} fraction")
    ax.set_title(f"{class_name} calibration (n={len(probs)})")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def _plot_probability_distribution(records: list[dict], output_path: Path) -> None:
    """Stacked histogram of p_dark / p_clear / p_artifact by true label."""
    labels = sorted({r["true_label"] for r in records})
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    classes = [("p_dark", "DARK"), ("p_clear", "CLEAR"), ("p_artifact", "ARTIFACT")]
    for ax, (pkey, title) in zip(axes, classes):
        for label in labels:
            vals = [r[pkey] for r in records if r["true_label"] == label]
            if vals:
                ax.hist(vals, bins=np.linspace(0, 1, 11), alpha=0.5, label=label, edgecolor="black")
        ax.set_xlabel(f"Predicted {pkey}")
        ax.set_ylabel("Count")
        ax.set_title(title)
        ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def _build_report(data: dict, output_dir: Path, n_bins: int) -> str:
    records = data["records"]
    md = f"""# Darkwatch Calibration Report

**Generated:** {data['generated_at']}
**Labeled contacts:** {len(records)}
**Label source:** `data/processed/calibration_labels.json`

---

## 1. Label Counts

"""
    label_counts = defaultdict(int)
    for r in records:
        label_counts[r["true_label"]] += 1
    for label in sorted(label_counts):
        md += f"- **{label}:** {label_counts[label]}\n"

    md += "\n---\n\n## 2. Per-Class Calibration\n\n"

    # Per-class Brier and reliability
    class_metrics = {}
    for class_name in ["DARK", "CLEAR", "ARTIFACT"]:
        pkey = f"p_{class_name.lower()}"
        probs = np.array([r[pkey] for r in records])
        outcomes = np.array([1.0 if r["true_label"] == class_name else 0.0 for r in records])
        brier = _brier_score(probs, outcomes)
        mean_pred = float(np.mean(probs))
        class_metrics[class_name] = {"brier": brier, "mean_pred": mean_pred, "n": len(probs)}

        md += f"""### {class_name}

- Labeled positives: {int(np.sum(outcomes))}
- Mean predicted {pkey}: {mean_pred:.4f}
- Brier score: {brier:.4f}

| Predicted probability bin | Count | Observed {class_name} fraction | Mean predicted |
|---|---|---|---|
"""
        centers, observed, counts, mean_pred_bins = _reliability_bins(probs, outcomes, n_bins)
        for c, obs, cnt, mp in zip(centers, observed, counts, mean_pred_bins):
            if cnt > 0:
                md += f"| {c - 0.5 / n_bins:.2f} – {c + 0.5 / n_bins:.2f} | {cnt} | {obs:.3f} | {mp:.3f} |\n"
        md += "\n"

    md += "---\n\n## 3. Verdict-vs-Label Confusion\n\n"
    md += "| Verdict | Labels | Count |\n|---|---|---|\n"
    verdict_label_counts = defaultdict(int)
    for r in records:
        verdict_label_counts[(r["verdict"], r["true_label"])] += 1
    for (verdict, label), count in sorted(verdict_label_counts.items()):
        md += f"| {verdict} | {label} | {count} |\n"

    md += f"""
---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only {len(records)} labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
"""
    for r in records:
        static = r["static_object"]["name"] if r["static_object"] else "—"
        nearest = f"{r['nearest_dist_m']:.0f}" if r["nearest_dist_m"] is not None else "—"
        md += (
            f"| `{r['contact_id'][-40:]}` | {r['scene']} | {r['true_label']} | {r['verdict']} | "
            f"{r['p_artifact']:.4f} | {r['p_clear']:.4f} | {r['p_dark']:.4f} | {r['p_review']:.4f} | "
            f"{nearest} | {static} |\n"
        )

    md += f"""
---

*Generated by `scripts/evaluate_calibration.py`.*
"""
    return md


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Darkwatch fusion calibration")
    parser.add_argument("--labels", type=str, default=str(REPO_ROOT / "data" / "processed" / "calibration_labels.json"))
    parser.add_argument("--output-dir", type=str, default=str(REPO_ROOT / "notebooks" / "calibration"))
    parser.add_argument("--bins", type=int, default=5, help="Number of reliability bins")
    args = parser.parse_args()

    labels_path = Path(args.labels)
    output_dir = Path(args.output_dir)
    if not labels_path.exists():
        print(f"ERROR: labels file not found: {labels_path}", file=sys.stderr)
        return 1

    labels = _load_labels(labels_path)
    # Collect verdict file paths referenced in labels JSON
    labels_data = json.loads(labels_path.read_text(encoding="utf-8"))
    verdict_paths = {}
    for scene in labels_data.get("scenes", []):
        key = scene["name"]
        path = Path(scene["verdicts"])
        if not path.is_absolute():
            path = REPO_ROOT / path
        verdict_paths[key] = path

    data = _gather_predictions(labels, verdict_paths)
    if not data["records"]:
        print("ERROR: no labeled contacts matched any verdicts", file=sys.stderr)
        return 1

    from datetime import datetime, timezone

    data["generated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Plot reliability diagrams
    records = data["records"]
    for class_name in ["DARK", "CLEAR", "ARTIFACT"]:
        pkey = f"p_{class_name.lower()}"
        probs = np.array([r[pkey] for r in records])
        outcomes = np.array([1.0 if r["true_label"] == class_name else 0.0 for r in records])
        _plot_reliability(
            probs,
            outcomes,
            class_name,
            args.bins,
            output_dir / f"reliability_{class_name.lower()}.png",
        )

    # Plot probability distributions
    _plot_probability_distribution(records, output_dir / "probability_distribution.png")

    # Write report
    report_md = _build_report(data, output_dir, args.bins)
    (output_dir / "calibration_report.md").write_text(report_md, encoding="utf-8")
    print(f"Calibration report saved to {output_dir / 'calibration_report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
