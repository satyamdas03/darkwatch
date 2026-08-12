"""Theater-aware default calibration model registry.

Fusion probabilities are trained (Platt-scaled) on labeled contacts. A model
fit on Santa Barbara + Gulf of Mexico scenes does not transfer perfectly to the
Southern California Bight, so each supported operational theater can have its
own default calibration model. Explicit ``--calibration-model`` paths always
override these defaults.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[2]

_DEFAULT_CALIBRATION_DIR = REPO_ROOT / "data" / "processed"

# Maps static-object / operational theater names to default calibration models.
# Paths are stored relative to the repository root so the registry remains
# portable across machines.
DEFAULT_CALIBRATION_MODELS: dict[str, str] = {
    "santa_barbara": "data/processed/fusion_calibration_v4_adaptive_combined.json",
    "gulf": "data/processed/fusion_calibration_v4_adaptive_combined.json",
    "southern_california": "data/processed/fusion_calibration_v4_adaptive_socal.json",
}

# Optional alias lookup for user-facing theater names.
_THEATER_ALIASES: dict[str, str] = {
    "sb": "santa_barbara",
    "socal": "southern_california",
    "scb": "southern_california",
    "gom": "gulf",
    "gulf_of_mexico": "gulf",
}


def resolve_theater_name(theater: str | None) -> str | None:
    """Normalize a theater string to the canonical registry key."""
    if theater is None:
        return None
    key = theater.lower().strip().replace(" ", "_")
    return _THEATER_ALIASES.get(key, key)


def default_calibration_model(
    theater: str | None,
    *,
    root: Path = REPO_ROOT,
    explicit_path: str | Path | None = None,
    path_exists: Callable[[Path], bool] = Path.exists,
) -> Path | None:
    """Return the calibration model path for a theater.

    If ``explicit_path`` is provided, it wins. Otherwise the theater is
    resolved to a default path from ``DEFAULT_CALIBRATION_MODELS``. Missing
    model files are logged via a raised ``FileNotFoundError`` so callers can
    fail gracefully.
    """
    if explicit_path is not None:
        path = Path(explicit_path)
        if not path.is_absolute():
            path = root / path
        if not path_exists(path):
            raise FileNotFoundError(f"Explicit calibration model not found: {path}")
        return path

    key = resolve_theater_name(theater)
    if key is None or key not in DEFAULT_CALIBRATION_MODELS:
        return None

    rel = DEFAULT_CALIBRATION_MODELS[key]
    path = root / rel
    if not path_exists(path):
        raise FileNotFoundError(
            f"Default calibration model for theater '{key}' not found: {path}"
        )
    return path
