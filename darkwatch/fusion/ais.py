"""AIS track loading and interpolation for SAR-to-AIS fusion.

Works with NOAA Marine Cadastre CSV broadcast-point files. The module filters
large daily CSVs by geographic bounding box and time window, groups messages by
MMSI into tracks, and interpolates each track to a requested SAR capture time.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

# NOAA AIS default position uncertainty (m). AIS GPS is typically 10-100 m;
# 50 m is a conservative mean for Class A transponders.
DEFAULT_AIS_POSITION_SIGMA_M = 50.0

# Default vessel speed to assume when AIS SOG is missing/unusable (knots).
DEFAULT_SPEED_KNOTS = 5.0

# Multiplier applied to the time-gap × speed product to obtain interpolation
# uncertainty. A value < 1 reflects that the vessel is unlikely to turn sharply.
INTERP_UNCERTAINTY_FACTOR = 0.5

# Minimum allowed association uncertainty (m).
MIN_SIGMA_M = 20.0


@dataclass
class AISTrack:
    """A single vessel track: MMSI + sorted messages + interpolation state."""

    mmsi: int
    messages: pd.DataFrame = field(repr=False)
    vessel_name: str | None = None
    vessel_type: int | None = None
    length_m: float | None = None
    width_m: float | None = None

    def __post_init__(self) -> None:
        # Ensure chronological order and build interpolators lazily.
        self.messages = self.messages.sort_values("BaseDateTime").reset_index(drop=True)
        self._lon_interp: interp1d | None = None
        self._lat_interp: interp1d | None = None
        self._build_interpolators()

    def _build_interpolators(self) -> None:
        if len(self.messages) < 2:
            self._lon_interp = None
            self._lat_interp = None
            return
        times = self.messages["BaseDateTime"].astype("int64")  # ns since epoch
        lons = self.messages["LON"].to_numpy(dtype=np.float64)
        lats = self.messages["LAT"].to_numpy(dtype=np.float64)
        self._lon_interp = interp1d(
            times, lons, kind="linear", bounds_error=False, fill_value="extrapolate"
        )
        self._lat_interp = interp1d(
            times, lats, kind="linear", bounds_error=False, fill_value="extrapolate"
        )

    @property
    def time_min(self) -> datetime:
        return self.messages["BaseDateTime"].min()

    @property
    def time_max(self) -> datetime:
        return self.messages["BaseDateTime"].max()

    def interpolate(
        self, t: datetime, max_extrapolate_s: float = 600.0
    ) -> tuple[float, float, float] | None:
        """Return (lon, lat, sigma_m) for this track at time ``t``.

        ``sigma_m`` combines the AIS GPS uncertainty with an interpolation
        uncertainty that grows with the time gap to the nearest AIS message.

        Returns ``None`` if the requested time is outside the track's time
        span by more than ``max_extrapolate_s`` seconds.
        """
        t_ns = pd.Timestamp(t).value
        t_min_ns = pd.Timestamp(self.time_min).value
        t_max_ns = pd.Timestamp(self.time_max).value

        before_gap_s = max(0.0, (t_min_ns - t_ns) / 1e9)
        after_gap_s = max(0.0, (t_ns - t_max_ns) / 1e9)
        if before_gap_s > max_extrapolate_s or after_gap_s > max_extrapolate_s:
            return None

        gap_s = max(before_gap_s, after_gap_s)

        # Find nearest messages for speed estimate.
        df = self.messages
        idx_after = df["BaseDateTime"].searchsorted(t)
        if idx_after == 0:
            speed_knots = _sog_or_default(df.iloc[0])
        elif idx_after >= len(df):
            speed_knots = _sog_or_default(df.iloc[-1])
        else:
            row_before = df.iloc[idx_after - 1]
            row_after = df.iloc[idx_after]
            dt_s = max(1.0, (row_after["BaseDateTime"] - row_before["BaseDateTime"]).total_seconds())
            speed_knots = max(_sog_or_default(row_before), _sog_or_default(row_after))
            # Cap speed to avoid absurd outliers corrupting uncertainty.
            speed_knots = min(speed_knots, 60.0)

        speed_mps = speed_knots * 0.514444
        sigma_interp_m = gap_s * speed_mps * INTERP_UNCERTAINTY_FACTOR
        sigma_m = math.hypot(DEFAULT_AIS_POSITION_SIGMA_M, sigma_interp_m)
        sigma_m = max(sigma_m, MIN_SIGMA_M)

        if self._lon_interp is None or self._lat_interp is None:
            # Single message: return it with large extrapolation uncertainty.
            return float(df.iloc[0]["LON"]), float(df.iloc[0]["LAT"]), sigma_m

        lon = float(self._lon_interp(t_ns))
        lat = float(self._lat_interp(t_ns))
        return lon, lat, sigma_m


def _sog_or_default(row: pd.Series) -> float:
    sog = row.get("SOG")
    if sog is None or pd.isna(sog) or sog <= 0 or sog > 100:
        return DEFAULT_SPEED_KNOTS
    return float(sog)


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres between two WGS84 points."""
    R = 6_371_000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def parse_ais_datetime(value) -> datetime:
    """Parse NOAA Marine Cadastre ``BaseDateTime`` strings to timezone-aware UTC."""
    if isinstance(value, datetime):
        dt = value
    else:
        dt = pd.to_datetime(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_ais_csv(
    csv_path: Path | str,
    bbox: tuple[float, float, float, float] | None = None,
    time_window: tuple[datetime, datetime] | None = None,
    min_messages: int = 2,
) -> list[AISTrack]:
    """Load NOAA Marine Cadastre CSV and return ``AISTrack`` objects.

    Args:
        csv_path: path to the CSV file (may be large; filtered in chunks).
        bbox: optional (min_lon, min_lat, max_lon, max_lat) filter.
        time_window: optional (t_start, t_end) UTC filter.
        min_messages: minimum messages required to keep a track.

    Returns:
        List of ``AISTrack`` instances, one per MMSI that passed filters.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    # NOAA daily files can be several GB uncompressed. Read in chunks and
    # filter early so memory stays bounded.
    chunk_rows: list[pd.DataFrame] = []
    chunk_size = 500_000

    usecols = [
        "MMSI",
        "BaseDateTime",
        "LAT",
        "LON",
        "SOG",
        "COG",
        "Heading",
        "VesselName",
        "IMO",
        "VesselType",
        "Status",
        "Length",
        "Width",
        "Draft",
        "Cargo",
        "TransceiverClass",
    ]
    # Only use columns that exist in the file.
    available_cols = set(pd.read_csv(csv_path, nrows=1).columns)
    usecols = [c for c in usecols if c in available_cols]

    for chunk in pd.read_csv(
        csv_path,
        usecols=usecols,
        parse_dates=["BaseDateTime"] if "BaseDateTime" in usecols else False,
        chunksize=chunk_size,
        low_memory=False,
    ):
        if "BaseDateTime" in chunk.columns:
            chunk["BaseDateTime"] = pd.to_datetime(chunk["BaseDateTime"], utc=True)
        else:
            raise ValueError("CSV missing required BaseDateTime column")

        # Geographic filter.
        if bbox is not None:
            min_lon, min_lat, max_lon, max_lat = bbox
            chunk = chunk[
                (chunk["LON"] >= min_lon)
                & (chunk["LON"] <= max_lon)
                & (chunk["LAT"] >= min_lat)
                & (chunk["LAT"] <= max_lat)
            ]

        # Temporal filter.
        if time_window is not None:
            t_start, t_end = time_window
            chunk = chunk[(chunk["BaseDateTime"] >= t_start) & (chunk["BaseDateTime"] <= t_end)]

        if len(chunk):
            chunk_rows.append(chunk)

    if not chunk_rows:
        return []

    df = pd.concat(chunk_rows, ignore_index=True)
    df = df.sort_values(["MMSI", "BaseDateTime"]).reset_index(drop=True)

    tracks: list[AISTrack] = []
    for mmsi, group in df.groupby("MMSI"):
        if len(group) < min_messages:
            continue
        group = group.reset_index(drop=True)
        meta = group.iloc[0]
        tracks.append(
            AISTrack(
                mmsi=int(mmsi),
                messages=group,
                vessel_name=_safe_str(meta.get("VesselName")),
                vessel_type=_safe_int(meta.get("VesselType")),
                length_m=_safe_float(meta.get("Length")),
                width_m=_safe_float(meta.get("Width")),
            )
        )

    return tracks


def _safe_str(value) -> str | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    s = str(value).strip()
    return s or None


def _safe_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def _safe_float(value) -> float | None:
    if value is None:
        return None
    try:
        f = float(value)
        if math.isnan(f):
            return None
        return f
    except (ValueError, TypeError):
        return None
