"""Select a Sentinel-1 scene whose footprint contains the most open ocean.

Usage:
    python scripts/pick_ocean_scene.py --start 2024-07-01 --end 2024-07-31 --max-results 50
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import shapely
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.adapters.copernicus_adapter import CopernicusAdapter
from darkwatch.s1_prep.land_mask import NaturalEarthLand

SANTA_BARBARA_BBOX = (-120.5, 33.8, -119.0, 34.6)


def _footprint_water_fraction(footprint_geojson: dict, land: shapely.Geometry, samples: int = 200) -> float:
    """Estimate water fraction inside a footprint by sampling points."""
    geom = shapely.geometry.shape(footprint_geojson)
    bounds = geom.bounds
    if not bounds or bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
        return 0.0
    minx, miny, maxx, maxy = bounds
    rng = np.random.default_rng(0)
    pts_lon = rng.uniform(minx, maxx, size=samples)
    pts_lat = rng.uniform(miny, maxy, size=samples)
    points = shapely.points(pts_lon, pts_lat)
    inside = shapely.within(points, geom)
    land_mask = shapely.contains_xy(land, pts_lon[inside], pts_lat[inside])
    water = np.count_nonzero(~land_mask)
    total_inside = np.count_nonzero(inside)
    if total_inside == 0:
        return 0.0
    return water / total_inside


def main() -> int:
    parser = argparse.ArgumentParser(description="Score S1 scenes by ocean coverage")
    parser.add_argument("--start", type=str, default=None)
    parser.add_argument("--end", type=str, default=None)
    parser.add_argument("--max-results", type=int, default=50)
    parser.add_argument("--output", type=str, default=str(REPO_ROOT / "data" / "raw" / "s1" / "scene_scores.json"))
    args = parser.parse_args()

    username = os.environ.get("DARKWATCH_CDSE_USERNAME")
    password = os.environ.get("DARKWATCH_CDSE_PASSWORD")
    if not username or not password:
        print("ERROR: Set DARKWATCH_CDSE_USERNAME and DARKWATCH_CDSE_PASSWORD", file=sys.stderr)
        return 1

    end = datetime.fromisoformat(args.end) if args.end else datetime.now(timezone.utc)
    start = datetime.fromisoformat(args.start) if args.start else end - timedelta(days=60)
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)

    adapter = CopernicusAdapter(username=username, password=password)
    print(f"Searching CDSE over {SANTA_BARBARA_BBOX} from {start.date()} to {end.date()} ...")
    products = adapter.search(
        bbox=SANTA_BARBARA_BBOX,
        start=start,
        end=end,
        product_type="IW_GRDH_1S",
        max_results=args.max_results,
    )
    if not products:
        print("No products found.")
        return 0

    print(f"Scoring {len(products)} products for ocean coverage ...")
    land = NaturalEarthLand().get_land_union()

    scores = []
    for p in products:
        water_frac = _footprint_water_fraction(p.footprint, land, samples=400)
        scores.append({
            "id": p.product_id,
            "name": p.name,
            "start": p.start_time.isoformat(),
            "water_fraction": round(water_frac, 4),
            "footprint": p.footprint,
            "download_url": p.download_url,
        })
        print(f"  {water_frac:.2%} water  {p.name}")

    scores.sort(key=lambda x: x["water_fraction"], reverse=True)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(scores, indent=2))
    print(f"Saved scores to {out_path}")
    print(f"Top candidate: {scores[0]['name']} ({scores[0]['water_fraction']:.2%} water)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
