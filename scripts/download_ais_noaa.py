"""Fast NOAA AIS daily zip downloader with resume support using Python requests.

Usage:
    python scripts/download_ais_noaa.py 2024-08-11 --output-dir data/external/ais
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{year}"


def download(date_str: str, output_dir: Path, chunk_size: int = 1024 * 1024) -> Path:
    date = datetime.strptime(date_str, "%Y-%m-%d")
    url = f"{BASE_URL.format(year=date.year)}/AIS_{date.strftime('%Y_%m_%d')}.zip"
    zip_path = output_dir / f"AIS_{date.strftime('%Y_%m_%d')}.zip"
    output_dir.mkdir(parents=True, exist_ok=True)

    existing_size = zip_path.stat().st_size if zip_path.exists() else 0
    headers = {"Range": f"bytes={existing_size}-"} if existing_size else {}

    print(f"Downloading {url} to {zip_path}")
    if existing_size:
        print(f"Resuming from {existing_size} bytes")

    with requests.get(url, headers=headers, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        total = existing_size + int(resp.headers.get("content-length", 0))
        mode = "ab" if existing_size else "wb"
        downloaded = existing_size
        with open(zip_path, mode) as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if downloaded % (10 * chunk_size) == 0:
                        pct = downloaded / total * 100 if total else 0
                        print(f"  {downloaded / 1e6:.1f} MB / {total / 1e6:.1f} MB ({pct:.1f}%)")

    print(f"Done. Saved {downloaded} bytes to {zip_path}")
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="YYYY-MM-DD")
    parser.add_argument("--output-dir", type=str, default="data/external/ais")
    args = parser.parse_args()
    try:
        download(args.date, Path(args.output_dir))
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
