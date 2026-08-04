"""Phase 0 script: search and optionally download the first Sentinel-1 GRD scene
over the Santa Barbara Channel test theater.

Usage:
    python scripts/fetch_first_scene.py --download

Environment variables:
    DARKWATCH_CDSE_USERNAME
    DARKWATCH_CDSE_PASSWORD
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

# Add repo root to path so we can import darkwatch without installing.
REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.adapters.copernicus_adapter import CopernicusAdapter

# Santa Barbara Channel test theater.
SANTA_BARBARA_BBOX = (-120.5, 33.8, -119.0, 34.6)  # (min_lon, min_lat, max_lon, max_lat)


def main():
    parser = argparse.ArgumentParser(description="Fetch first Sentinel-1 scene over Santa Barbara Channel")
    parser.add_argument("--start", type=str, default=None, help="Start date ISO (e.g. 2024-07-01)")
    parser.add_argument("--end", type=str, default=None, help="End date ISO (e.g. 2024-08-01)")
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--index", type=int, default=0, help="Which search result to download (0 = first)")
    parser.add_argument("--download", action="store_true", help="Download the selected product")
    parser.add_argument("--output-dir", type=str, default=str(REPO_ROOT / "data" / "raw" / "s1"))
    args = parser.parse_args()

    username = os.environ.get("DARKWATCH_CDSE_USERNAME")
    password = os.environ.get("DARKWATCH_CDSE_PASSWORD")
    if not username or not password:
        print("ERROR: Set DARKWATCH_CDSE_USERNAME and DARKWATCH_CDSE_PASSWORD", file=sys.stderr)
        sys.exit(1)

    adapter = CopernicusAdapter(username=username, password=password)

    end = datetime.fromisoformat(args.end) if args.end else datetime.now(timezone.utc)
    start = datetime.fromisoformat(args.start) if args.start else end - timedelta(days=30)

    # Ensure naive datetimes are treated as UTC.
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)

    print(f"Searching CDSE for Sentinel-1 GRD over {SANTA_BARBARA_BBOX} from {start.date()} to {end.date()}...")
    products = adapter.search(
        bbox=SANTA_BARBARA_BBOX,
        start=start,
        end=end,
        product_type="IW_GRDH_1S",
        max_results=args.max_results,
    )

    if not products:
        print("No products found. Try widening the date range.")
        sys.exit(0)

    print(f"Found {len(products)} product(s):")
    for i, p in enumerate(products):
        print(f"  [{i}] {p.name}")
        print(f"       acquisition: {p.start_time.isoformat()}  size hint: {p.s3_path or 'N/A'}")

    # Save search results metadata.
    meta_path = Path(args.output_dir) / "search_results.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta = [
        {
            "id": p.product_id,
            "name": p.name,
            "product_type": p.product_type,
            "start": p.start_time.isoformat(),
            "end": p.end_time.isoformat(),
            "download_url": p.download_url,
            "zip_url": p.native_zip_url,
        }
        for p in products
    ]
    meta_path.write_text(json.dumps(meta, indent=2))
    print(f"Search metadata saved to {meta_path}")

    if args.download and products:
        idx = max(0, min(args.index, len(products) - 1))
        selected = products[idx]
        print(f"\nDownloading product [{idx}] {selected.name} ...")
        downloaded = adapter.download(selected, args.output_dir, extract=True)
        print(f"Extracted SAFE to: {downloaded}")


if __name__ == "__main__":
    main()
