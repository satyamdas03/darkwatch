"""Darkwatch analyst web dashboard.

A lightweight FastAPI backend that scans ``data/processed`` for completed
scenes and serves verdicts, contacts, summaries, and generated maps to a
single-page frontend.
"""

from __future__ import annotations

from .api import create_app

__all__ = ["create_app"]
