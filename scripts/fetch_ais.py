"""Download and clip NOAA Marine Cadastre AIS broadcast data.

Usage:
    python scripts/fetch_ais.py \
        --date 2024-07-11 \
        --bbox "-120.8,34.3,-119.8,34.7" \
        --time-window-minutes 60 \
        --output-dir data/external/ais
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

NOAA_AIS_BASE_URL = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{year}"


def _parse_bbox(value: str) -> tuple[float, float, float, float]:
    parts = [float(v.strip()) for v in value.split(",")]
    if len(parts) != 4:
        raise ValueError("bbox must be min_lon,min_lat,max_lon,max_lat")
    return tuple(parts)  # type: ignore[return-value]


def _daily_csv_url(date: datetime) -> str:
    year = date.year
    date_str = date.strftime("%Y_%m_%d")
    return f"{NOAA_AIS_BASE_URL.format(year=year)}/AIS_{date_str}.zip"


def download_file(url: str, dest: Path) -> None:
    """Download ``url`` to ``dest`` using curl (available in Git Bash on Windows)."""
    import subprocess

    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url} ...")
    result = subprocess.run(
        ["curl", "-L", "-o", str(dest), url],
        check=True,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Download failed: {result.stderr}")
    print(f"Saved to {dest}")


def unzip_daily(zip_path: Path, extract_dir: Path) -> Path:
    """Extract the daily zip; return path to the extracted CSV directory."""
    extract_dir.mkdir(parents=True, exist_ok=True)
    print(f"Extracting {zip_path} ...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    # The zip typically contains one or more CSVs at the root.
    csvs = list(extract_dir.glob("*.csv"))
    if not csvs:
        raise FileNotFoundError(f"No CSV found in {extract_dir}")
    print(f"Extracted {len(csvs)} CSV file(s)")
    return extract_dir


def filter_ais_csv(
    csv_dir: Path,
    bbox: tuple[float, float, float, float],
    time_window: tuple[datetime, datetime],
    output_path: Path,
) -> int:
    """Filter all CSVs in ``csv_dir`` and write a single clipped CSV.

    Returns the number of rows written.
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    chunk_size = 500_000
    rows_written = 0
    first = True

    for csv_path in sorted(csv_dir.glob("*.csv")):
        print(f"Filtering {csv_path.name} ...")
        for chunk in pd.read_csv(
            csv_path,
            parse_dates=["BaseDateTime"],
            chunksize=chunk_size,
            low_memory=False,
        ):
            chunk["BaseDateTime"] = pd.to_datetime(chunk["BaseDateTime"], utc=True)
            chunk = chunk[
                (chunk["LON"] >= min_lon)
                & (chunk["LON"] <= max_lon)
                & (chunk["LAT"] >= min_lat)
                & (chunk["LAT"] <= max_lat)
                & (chunk["BaseDateTime"] >= time_window[0])
                & (chunk["BaseDateTime"] <= time_window[1])
            ]
            if len(chunk):
                chunk.to_csv(output_path, mode="w" if first else "a", index=False, header=first)
                rows_written += len(chunk)
                first = False

    print(f"Wrote {rows_written} clipped rows to {output_path}")
    return rows_written


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch and clip NOAA AIS data")
    parser.add_argument("--date", type=str, required=True, help="Date to fetch (YYYY-MM-DD)")
    parser.add_argument("--bbox", type=str, required=True, help="min_lon,min_lat,max_lon,max_lat")
    parser.add_argument(
        "--time-window-minutes",
        type=int,
        default=60,
        help="Keep AIS messages within +/- this many minutes of local noon (or use --center-time)",
    )
    parser.add_argument("--center-time", type=str, default=None, help="UTC center time ISO (overrides noon)")
    parser.add_argument("--output-dir", type=str, default=str(REPO_ROOT / "data" / "external" / "ais"))
    parser.add_argument("--keep-zip", action="store_true", help="Keep the downloaded daily zip")
    args = parser.parse_args()

    date = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    bbox = _parse_bbox(args.bbox)

    if args.center_time:
        center = datetime.fromisoformat(args.center_time).replace(tzinfo=timezone.utc)
    else:
        # Default: local noon if not provided, but safer to require it.
        center = date.replace(hour=12, minute=0, second=0)
    half = timedelta(minutes=args.time_window_minutes)
    time_window = (center - half, center + half)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = date.strftime("%Y-%m-%d")
    zip_path = output_dir / f"AIS_{date.strftime('%Y_%m_%d')}.zip"
    extract_dir = output_dir / f"AIS_{date.strftime('%Y_%m_%d')}_extracted"
    clipped_path = output_dir / f"ais_{date_str}_clipped.csv"

    if not zip_path.exists():
        url = _daily_csv_url(date)
        download_file(url, zip_path)

    if not any(extract_dir.glob("*.csv")):
        unzip_daily(zip_path, extract_dir)

    rows = filter_ais_csv(extract_dir, bbox, time_window, clipped_path)
    print(f"Done. {rows} clipped AIS rows available at {clipped_path}")

    if not args.keep_zip:
        zip_path.unlink(missing_ok=True)
        print(f"Removed {zip_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
