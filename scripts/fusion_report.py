"""Generate a human-readable Markdown report from a fusion run.

Usage:
    python scripts/fusion_report.py \
        --contacts data/processed/detections_20240711/contacts.json \
        --ais data/external/ais/ais_2024-07-11_clipped.csv \
        --verdicts data/processed/fusion_20240711/verdicts.json \
        --summary data/processed/fusion_20240711/summary.json \
        --output notebooks/fusion_20240711_report.md
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.detect.contact import Contact
from darkwatch.fusion.ais import _haversine_m


def _load_contacts(path: Path) -> list[Contact]:
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


def _load_verdicts(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def _load_summary(path: Path) -> dict:
    return json.loads(path.read_text())


def _contact_by_id(contacts: list[Contact], contact_id: str) -> Contact | None:
    for c in contacts:
        if c.contact_id == contact_id:
            return c
    return None


def _format_ais_table(ais_path: Path, contacts: list[Contact]) -> str:
    df = pd.read_csv(ais_path, parse_dates=["BaseDateTime"])
    rows: list[str] = []
    for mmsi, group in df.groupby("MMSI"):
        group = group.sort_values("BaseDateTime").reset_index(drop=True)
        name = (
            group["VesselName"].dropna().iloc[0]
            if not group["VesselName"].dropna().empty
            else None
        )
        # Approximate distance to the first contact (theater is small enough).
        first = contacts[0]
        mid_idx = len(group) // 2
        d = _haversine_m(
            first.center_lat,
            first.center_lon,
            float(group.iloc[mid_idx]["LAT"]),
            float(group.iloc[mid_idx]["LON"]),
        )
        status_vals = group["Status"].dropna().unique()
        status = ", ".join(str(int(s)) for s in status_vals) if len(status_vals) else "n/a"
        sog_vals = group["SOG"].dropna()
        speed = f"{sog_vals.mean():.1f}" if len(sog_vals) else "n/a"
        rows.append(
            f"| {mmsi} | {name or 'n/a'} | {len(group)} | {speed} | {status} | ~{d:,.0f} |"
        )
    header = "| MMSI | Name | Messages | Avg SOG (kn) | Status(es) | Distance to contact (m) |\n|---|---|---|---|---|---|"
    return header + "\n" + "\n".join(rows)


def _format_verdict_table(verdicts: list[dict]) -> str:
    lines: list[str] = []
    lines.append("| Contact | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest MMSI | Nearest dist (m) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for v in verdicts:
        nearest = v.get("nearest_association") or {}
        nearest_mmsi = nearest.get("mmsi", "n/a")
        nearest_dist = nearest.get("distance_m", "n/a")
        lines.append(
            f"| `{v['contact_id']}` | {v['verdict']} | {v['p_artifact']} | "
            f"{v['p_clear']} | {v['p_dark']} | {v['p_review']} | {nearest_mmsi} | {nearest_dist} |"
        )
    return "\n".join(lines)


def _format_reasoning(verdict: dict) -> str:
    lines = [f"- {r}" for r in verdict.get("reasoning", [])]
    return "\n".join(lines) if lines else "_No reasoning recorded._"


def generate_report(
    contacts_path: Path,
    ais_path: Path,
    verdicts_path: Path,
    summary_path: Path,
) -> str:
    contacts = _load_contacts(contacts_path)
    verdicts = _load_verdicts(verdicts_path)
    summary = _load_summary(summary_path)

    scene_time = summary.get("scene_time", "unknown")
    gate_radius_m = summary.get("gate_radius_m", 2000)
    contacts_fused = summary.get("contacts_fused", len(verdicts))
    ais_tracks_loaded = summary.get("ais_tracks_loaded", "unknown")
    counts = summary.get("verdict_counts", {})

    md = f"""# Darkwatch Fusion Report

**Scene time:** {scene_time}
**AIS file:** `{ais_path}`
**Association gate:** {gate_radius_m} m
**Contacts fused:** {contacts_fused}
**AIS tracks loaded:** {ais_tracks_loaded}
**Verdict counts:** {counts}

---

## 1. SAR Contacts

"""
    for v in verdicts:
        c = _contact_by_id(contacts, v["contact_id"])
        if c is None:
            continue
        md += f"""### `{v['contact_id']}`

| Field | Value |
|---|---|
| Center | `{c.center_lon:.5f}, {c.center_lat:.5f}` |
| Estimated size | {c.width_m:.0f} m × {c.length_m:.0f} m |
| Detector confidence | {c.confidence:.3f} |
| **Verdict** | **{v['verdict']}** |
| p_artifact | {v['p_artifact']} |
| p_clear | {v['p_clear']} |
| p_dark | {v['p_dark']} |
| p_review | {v['p_review']} |
| Tracks within gate | {v['n_tracks_within_gate']} |
| Tracks near gate (1×–2×) | {v['n_tracks_near_gate']} |

**Reasoning:**
{_format_reasoning(v)}

"""

    md += f"""---

## 2. Verdict Summary Table

{_format_verdict_table(verdicts)}

---

## 3. AIS Tracks in Theater

{_format_ais_table(ais_path, contacts)}

---

## 4. Interpretation Notes

- A SAR contact with no AIS track inside the gate is **not automatically dark**. It may be:
  - a genuine dark vessel,
  - a transponding vessel with a temporary AIS outage,
  - a radar artifact (wave clutter, azimuth ambiguity, wind streak),
  - a fixed object (oil platform, small island, navigation marker).
- `p_review` is raised when no AIS track exists within 2× the gate radius, reflecting the possibility of an innocent coverage gap.
- The **nearest association** column shows the closest cooperative track even when it lies outside the gate, so a human can judge whether the contact is plausibly explained by nearby traffic.

---

*Generated by `scripts/fusion_report.py` on {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}.*
"""
    return md


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Markdown fusion report")
    parser.add_argument("--contacts", type=str, required=True, help="Path to contacts.json")
    parser.add_argument("--ais", type=str, required=True, help="Path to clipped AIS CSV")
    parser.add_argument("--verdicts", type=str, required=True, help="Path to verdicts.json")
    parser.add_argument("--summary", type=str, required=True, help="Path to summary.json")
    parser.add_argument("--output", type=str, required=True, help="Path to output Markdown file")
    args = parser.parse_args()

    contacts_path = Path(args.contacts)
    ais_path = Path(args.ais)
    verdicts_path = Path(args.verdicts)
    summary_path = Path(args.summary)
    output_path = Path(args.output)

    for p in (contacts_path, ais_path, verdicts_path, summary_path):
        if not p.exists():
            print(f"ERROR: file not found: {p}", file=sys.stderr)
            return 1

    report = generate_report(contacts_path, ais_path, verdicts_path, summary_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report saved to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
