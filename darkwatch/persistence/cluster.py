"""Density-based persistence clustering across Darkwatch scenes.

Clusters contacts by great-circle distance. A contact is considered persistent
if it belongs to a cluster that spans at least two distinct acquisition dates.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

R_EARTH_M = 6_371_000.0


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres between two WGS84 points."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R_EARTH_M * math.asin(math.sqrt(h))


def _neighbors(contacts: list[dict[str, Any]], index: int, eps_m: float) -> list[int]:
    """Return indices of contacts within *eps_m* of contact *index*."""
    c0 = contacts[index]
    lat0, lon0 = c0["center_lat"], c0["center_lon"]
    result = []
    for i, c in enumerate(contacts):
        if _haversine_m(lat0, lon0, c["center_lat"], c["center_lon"]) <= eps_m:
            result.append(i)
    return result


def cluster_contacts(
    contacts: list[dict[str, Any]],
    eps_m: float = 500.0,
    min_samples: int = 2,
) -> dict[int, int]:
    """Run DBSCAN-style clustering and return index -> cluster_id mapping.

    Contacts without coordinates are assigned cluster_id -1 (noise).
    Cluster ids start at 0.
    """
    n = len(contacts)
    labels = [-1] * n
    core = [False] * n

    # Precompute neighbor lists to avoid repeated haversine calculations.
    neighbor_lists = [[] for _ in range(n)]
    for i in range(n):
        c = contacts[i]
        if c.get("center_lat") is None or c.get("center_lon") is None:
            continue
        neighbor_lists[i] = _neighbors(contacts, i, eps_m)
        # DBSCAN: core if at least min_samples points in eps-neighborhood.
        core[i] = len(neighbor_lists[i]) >= min_samples

    cluster_id = 0
    for i in range(n):
        if not core[i] or labels[i] != -1:
            continue
        # BFS/DFS from core point i.
        labels[i] = cluster_id
        queue = list(neighbor_lists[i])
        for j in queue:
            if labels[j] == -1:
                labels[j] = cluster_id
                if core[j]:
                    for k in neighbor_lists[j]:
                        if labels[k] == -1 and k not in queue:
                            queue.append(k)
        cluster_id += 1

    return {i: labels[i] for i in range(n)}


def persistence_for_contact(
    contacts: list[dict[str, Any]],
    contact_index: int,
    cluster_labels: dict[int, int],
) -> dict[str, Any]:
    """Return persistence summary for a single contact index."""
    label = cluster_labels.get(contact_index, -1)
    if label == -1:
        return {"cluster_id": None, "n_scenes": 1, "is_persistent": False}

    scene_dates: set[str] = set()
    cluster_size = 0
    for i, c in enumerate(contacts):
        if cluster_labels.get(i) == label:
            cluster_size += 1
            date = c.get("scene_date")
            if date:
                scene_dates.add(str(date))

    return {
        "cluster_id": int(label),
        "n_scenes": len(scene_dates),
        "cluster_size": cluster_size,
        "is_persistent": len(scene_dates) >= 2,
    }


def tag_all_contacts(
    contacts: list[dict[str, Any]],
    eps_m: float = 500.0,
    min_samples: int = 2,
) -> list[dict[str, Any]]:
    """Return contacts augmented with ``persistence`` metadata."""
    labels = cluster_contacts(contacts, eps_m=eps_m, min_samples=min_samples)
    tagged = []
    for i, c in enumerate(contacts):
        enriched = dict(c)
        enriched["persistence"] = persistence_for_contact(contacts, i, labels)
        tagged.append(enriched)
    return tagged
