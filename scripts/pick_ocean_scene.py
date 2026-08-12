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
OPERATIONAL_BBOX = (-120.8, 34.3, -119.8, 34.7)  # western Santa Barbara Channel


def _bbox_to_polygon(bbox: tuple[float, float, float, float]) -> shapely.Geometry:
    minx, miny, maxx, maxy = bbox
    return shapely.geometry.Polygon(
        [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)]
    )


def _operational_overlap(footprint_geojson: dict, operational_bbox: tuple[float, float, float, float]) -> float:
    """Fraction of the operational bbox that is covered by the scene footprint."""
    geom = shapely.geometry.shape(footprint_geojson)
    op_poly = _bbox_to_polygon(operational_bbox)
    inter = geom.intersection(op_poly)
    if op_poly.area == 0:
        return 0.0
    return inter.area / op_poly.area


def _footprint_water_fraction(
    footprint_geojson: dict,
    land: shapely.Geometry,
    samples: int = 200,
    clip_bbox: tuple[float, float, float, float] | None = None,
) -> float:
    """Estimate water fraction inside a footprint (optionally clipped to a bbox).

    If ``clip_bbox`` is supplied, samples are restricted to the intersection of
    the footprint and the bbox, so the returned fraction reflects the usable
    operational area rather than the whole swath.
    """
    geom = shapely.geometry.shape(footprint_geojson)
    if clip_bbox is not None:
        geom = geom.intersection(_bbox_to_polygon(clip_bbox))
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
    parser.add_argument(
        "--min-overlap",
        type=float,
        default=0.75,
        help="Minimum fraction of the operational bbox that must be covered (default 0.75)",
    )
    parser.add_argument(
        "--operational-bbox",
        type=str,
        default=None,
        help="Target theater bbox as W,S,E,N; scenes are scored by overlap with this bbox",
    )
    parser.add_argument(
        "--search-bbox",
        type=str,
        default=None,
        help="CDSE search bbox as W,S,E,N; defaults to the Santa Barbara search region",
    )
    parser.add_argument(
        "--theater-name",
        type=str,
        default=None,
        help="Optional tag added to the output JSON for the theater being scored",
    )
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

    search_bbox = SANTA_BARBARA_BBOX
    if args.search_bbox:
        parts = [float(x.strip()) for x in args.search_bbox.split(",")]
        if len(parts) != 4:
            raise ValueError("--search-bbox must be W,S,E,N")
        search_bbox = tuple(parts)

    adapter = CopernicusAdapter(username=username, password=password)
    theater_tag = f" ({args.theater_name})" if args.theater_name else ""
    print(f"Searching CDSE{theater_tag} over {search_bbox} from {start.date()} to {end.date()} ...")
    products = adapter.search(
        bbox=search_bbox,
        start=start,
        end=end,
        product_type="IW_GRDH_1S",
        max_results=args.max_results,
    )
    if not products:
        print("No products found.")
        return 0

    operational_bbox = OPERATIONAL_BBOX
    if args.operational_bbox:
        parts = [float(x.strip()) for x in args.operational_bbox.split(",")]
        if len(parts) != 4:
            raise ValueError("--operational-bbox must be W,S,E,N")
        operational_bbox = tuple(parts)

    print(f"Scoring {len(products)} products for ocean coverage and operational overlap ...")
    print(f"  operational bbox: {operational_bbox}")
    land = NaturalEarthLand().get_land_union()

    scores = []
    skipped = 0
    for p in products:
        op_overlap = _operational_overlap(p.footprint, operational_bbox)
        if op_overlap < args.min_overlap:
            skipped += 1
            continue
        # Water fraction within the part of the operational bbox actually covered.
        water_frac = _footprint_water_fraction(
            p.footprint, land, samples=400, clip_bbox=operational_bbox
        )
        # Combined score: fraction of the operational bbox that is covered by water.
        score = water_frac * op_overlap
        scores.append({
            "id": p.product_id,
            "name": p.name,
            "start": p.start_time.isoformat(),
            "water_fraction": round(water_frac, 4),
            "operational_overlap": round(op_overlap, 4),
            "combined_score": round(score, 4),
            "footprint": p.footprint,
            "download_url": p.download_url,
            "theater_name": args.theater_name,
            "search_bbox": search_bbox,
            "operational_bbox": operational_bbox,
        })
        print(f"  {score:.2%} combined  {water_frac:.2%} water  {op_overlap:.2%} overlap  {p.name}")

    if skipped:
        print(f"  (skipped {skipped} scenes with overlap < {args.min_overlap:.0%})")

    if not scores:
        print("No scenes meet the minimum overlap requirement.", file=sys.stderr)
        return 1

    scores.sort(key=lambda x: x["combined_score"], reverse=True)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(scores, indent=2))
    print(f"Saved scores to {out_path}")
    top = scores[0]
    print(
        f"Top candidate: {top['name']} ("
        f"water={top['water_fraction']:.2%}, "
        f"overlap={top['operational_overlap']:.2%}, "
        f"score={top['combined_score']:.2%})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
