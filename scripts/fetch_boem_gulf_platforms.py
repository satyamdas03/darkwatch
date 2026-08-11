"""Fetch and cache the BOEM/BSEE Gulf of Mexico platform dataset.

Usage:
    python scripts/fetch_boem_gulf_platforms.py \
        --output data/external/boem_gulf_platforms.geojson
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

BOEM_GULF_QUERY_URL = (
    "https://gis.boem.gov/arcgis/rest/services/BOEM_BSEE/GOA_Layers/MapServer/0/query"
)


def fetch_geojson(url: str) -> dict:
    """Query the BOEM REST endpoint and return the GeoJSON payload."""
    params = {
        "where": "1=1",
        "outFields": "*",
        "f": "geojson",
        "outSR": "4326",
    }
    response = requests.get(url, params=params, timeout=120)
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch BOEM Gulf of Mexico platform GeoJSON")
    parser.add_argument(
        "--output",
        type=str,
        default=str(REPO_ROOT / "data" / "external" / "boem_gulf_platforms.geojson"),
        help="Output GeoJSON path",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Fetching BOEM Gulf of Mexico platforms ...")
    data = fetch_geojson(BOEM_GULF_QUERY_URL)
    features = data.get("features", [])
    print(f"Retrieved {len(features)} platform features")

    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Saved to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
