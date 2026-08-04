"""Verdict taxonomy for dark-vessel attribution."""

from __future__ import annotations

from enum import Enum


class Verdict(str, Enum):
    """Discrete verdict labels for a SAR contact."""

    CLEAR = "CLEAR"
    DARK = "DARK"
    ARTIFACT = "ARTIFACT"
    REVIEW = "REVIEW"
