"""Persistence tracking for Darkwatch contacts across repeat SAR passes.

Clusters contacts by location across multiple scenes and flags vessels that
appear in the same place on different acquisition dates — a strong signal for
stationary or repeatedly active dark vessels.
"""

from __future__ import annotations

from .cluster import cluster_contacts, persistence_for_contact

__all__ = ["cluster_contacts", "persistence_for_contact"]
