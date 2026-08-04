"""Probabilistic SAR-contact-to-AIS-track association.

The core question answered here: for each SAR contact, what is the probability
that it is explained by a cooperative AIS track versus being a dark vessel or
a non-vessel artifact?
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable

import numpy as np

from ..detect.contact import Contact
from .ais import AISTrack, _haversine_m
from .verdict import Verdict

# Default gate radius (m). AIS tracks farther than this from a contact cannot
# explain it.
DEFAULT_GATE_RADIUS_M = 2_000.0

# Default SAR geolocation uncertainty per pixel.
SAR_PIXEL_SIGMA_FACTOR = 1.5

# Prior probability that a SAR contact is an artifact rather than a real vessel.
DEFAULT_ARTIFACT_PRIOR = 0.15

# Prior probability that a real vessel contact is dark (no AIS match) before
# seeing the AIS geometry. This is intentionally conservative.
DEFAULT_DARK_PRIOR = 0.10


@dataclass
class TrackAssociation:
    """Association between one SAR contact and one interpolated AIS track."""

    mmsi: int
    distance_m: float
    sigma_m: float
    likelihood: float
    interpolated_lon: float
    interpolated_lat: float
    vessel_name: str | None = None


@dataclass
class ContactVerdict:
    """Fusion result for a single SAR contact."""

    contact_id: str
    # Component probabilities
    p_artifact: float
    p_clear: float  # matched to an AIS track
    p_dark: float  # real vessel, no AIS match
    p_review: float  # uncertain — needs human review

    # Evidence trail
    associations: list[TrackAssociation] = field(default_factory=list)
    best_association: TrackAssociation | None = None
    reasoning: list[str] = field(default_factory=list)

    @property
    def verdict(self) -> Verdict:
        """Return the discrete verdict label."""
        if self.p_artifact > 0.5:
            return Verdict.ARTIFACT
        if self.p_clear > 0.6:
            return Verdict.CLEAR
        if self.p_dark > 0.6:
            return Verdict.DARK
        return Verdict.REVIEW


def _gaussian_likelihood(distance_m: float, sigma_m: float) -> float:
    """Un-normalized 2-D Gaussian likelihood at distance ``distance_m``."""
    if sigma_m <= 0:
        sigma_m = 1.0
    return math.exp(-(distance_m ** 2) / (2.0 * sigma_m ** 2))


def _sar_sigma_m(contact: Contact) -> float:
    """Estimate SAR contact geolocation uncertainty in metres."""
    # Pixel size estimate from contact size if width/length are reasonable.
    if contact.width_m and contact.length_m and contact.width_m > 0:
        pixel_size = min(contact.width_m, contact.length_m)
    else:
        pixel_size = 10.0
    return pixel_size * SAR_PIXEL_SIGMA_FACTOR


def associate_contact(
    contact: Contact,
    tracks: Iterable[AISTrack],
    t_sar: datetime | None = None,
    gate_radius_m: float = DEFAULT_GATE_RADIUS_M,
    max_extrapolate_s: float = 600.0,
) -> ContactVerdict:
    """Compute the fusion verdict for a single SAR contact.

    Args:
        contact: SAR contact to attribute.
        tracks: iterable of ``AISTrack`` objects in the neighborhood.
        t_sar: SAR acquisition time; defaults to ``contact.acquisition_time``.
        gate_radius_m: maximum distance for an AIS track to explain the contact.
        max_extrapolate_s: maximum seconds to extrapolate an AIS track to t_sar.

    Returns:
        ``ContactVerdict`` with component probabilities and evidence trail.
    """
    if t_sar is None:
        t_sar = contact.acquisition_time

    reasoning: list[str] = []
    associations: list[TrackAssociation] = []

    sar_sigma = _sar_sigma_m(contact)

    for track in tracks:
        interp = track.interpolate(t_sar, max_extrapolate_s=max_extrapolate_s)
        if interp is None:
            continue
        lon_i, lat_i, sigma_ais = interp
        d = _haversine_m(contact.center_lat, contact.center_lon, lat_i, lon_i)
        if d > gate_radius_m:
            continue

        sigma_total = math.hypot(sigma_ais, sar_sigma)
        likelihood = _gaussian_likelihood(d, sigma_total)
        associations.append(
            TrackAssociation(
                mmsi=track.mmsi,
                distance_m=d,
                sigma_m=sigma_total,
                likelihood=likelihood,
                interpolated_lon=lon_i,
                interpolated_lat=lat_i,
                vessel_name=track.vessel_name,
            )
        )

    # Sort by likelihood descending.
    associations.sort(key=lambda a: a.likelihood, reverse=True)
    best_association = associations[0] if associations else None

    # Convert likelihoods to a total "explained by AIS" probability.
    # Use a softmax-like normalization with a no-match alternative.
    # The no-match score is the dark prior scaled so that very low likelihoods
    # do not over-explain contacts.
    if associations:
        # Scale likelihoods so that a 1-sigma hit has moderate evidence.
        scores = np.array([a.likelihood for a in associations], dtype=np.float64)
        # Softmax temperature keeps the math numerically stable.
        scores = np.exp(scores - np.max(scores))
        no_match_score = math.exp(1.0) * DEFAULT_DARK_PRIOR  # baseline alternative
        denom = no_match_score + scores.sum()
        p_match_each = scores / denom
        for a, p in zip(associations, p_match_each):
            a.likelihood = float(p)  # re-use likelihood field as posterior prob
        p_clear = float(scores.sum() / denom)
    else:
        p_clear = 0.0
        reasoning.append("No AIS track within gate radius.")

    # Detection confidence feeds into real-vessel probability.
    p_real_vessel = contact.confidence
    p_artifact = (1.0 - p_real_vessel) * DEFAULT_ARTIFACT_PRIOR

    # Remaining real-vessel mass is split between clear and dark.
    real_mass = max(0.0, 1.0 - p_artifact)
    # Dark probability = real vessels not explained by AIS.
    p_dark = real_mass * (1.0 - p_clear) * (1.0 - DEFAULT_ARTIFACT_PRIOR)
    # Review = leftover uncertainty where no single explanation dominates.
    p_review = max(0.0, 1.0 - (p_artifact + p_clear + p_dark))

    if best_association:
        reasoning.append(
            f"Best AIS match: MMSI {best_association.mmsi} "
            f"at {best_association.distance_m:.0f} m "
            f"(σ={best_association.sigma_m:.0f} m), "
            f"P(match)={best_association.likelihood:.3f}."
        )
    else:
        reasoning.append("No AIS match within gate; contact is candidate dark vessel if real.")

    # Ensure probabilities sum to 1 (within rounding).
    total = p_artifact + p_clear + p_dark + p_review
    if total > 0 and abs(total - 1.0) > 1e-6:
        p_artifact /= total
        p_clear /= total
        p_dark /= total
        p_review /= total

    return ContactVerdict(
        contact_id=contact.contact_id,
        p_artifact=p_artifact,
        p_clear=p_clear,
        p_dark=p_dark,
        p_review=p_review,
        associations=associations,
        best_association=best_association,
        reasoning=reasoning,
    )


def associate_all_contacts(
    contacts: Iterable[Contact],
    tracks: Iterable[AISTrack],
    t_sar: datetime | None = None,
    gate_radius_m: float = DEFAULT_GATE_RADIUS_M,
    max_extrapolate_s: float = 600.0,
) -> list[ContactVerdict]:
    """Run association for every contact using the same track collection."""
    return [
        associate_contact(c, tracks, t_sar, gate_radius_m, max_extrapolate_s)
        for c in contacts
    ]
