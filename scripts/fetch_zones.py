"""Fetch maritime zone context for a theater bbox.

Usage:
    python scripts/fetch_zones.py \
        --bbox "-120.8,34.3,-119.8,34.7" \
        --output data/external/zones/santa_barbara_mpa.geojson
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.zones.fetcher import fetch_mpa_geojson, save_mpa_geojson


def _parse_bbox(value: str) -> tuple[float, float, float, float]:
    parts = [float(v.strip()) for v in value.split(",")]
    if len(parts) != 4:
        raise ValueError("bbox must be west,south,east,north")
    return tuple(parts)  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch maritime zones for a bbox")
    parser.add_argument("--bbox", type=str, required=True, help="W,S,E,N bbox in decimal degrees")
    parser.add_argument(
        "--output",
        type=str,
        default=str(REPO_ROOT / "data" / "external" / "zones" / "mpa.geojson"),
    )
    args = parser.parse_args()

    west, south, east, north = _parse_bbox(args.bbox)
    print(f"Fetching NOAA MPA Inventory for bbox ({west},{south},{east},{north}) ...")
    try:
        data = fetch_mpa_geojson(west, south, east, north)
        path = save_mpa_geojson(data, args.output)
        print(f"Saved {len(data.get('features', []))} MPA features to {path}")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
