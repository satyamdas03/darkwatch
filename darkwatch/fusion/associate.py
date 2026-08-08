"""Probabilistic SAR-contact-to-AIS-track association.

The core question answered here: for each SAR contact, what is the probability
that it is explained by a cooperative AIS track versus being a dark vessel or
a non-vessel artifact?
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable

import numpy as np

from ..detect.contact import Contact
from .ais import AISTrack, _haversine_m
from .static_objects import DEFAULT_PLATFORM_BUFFER_M, StaticObjectHit, check_contact
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

# Size/shape artifact evidence defaults.
DEFAULT_SIZE_MAX_DIM_SOFT_M = 500.0
DEFAULT_SIZE_MAX_DIM_HARD_M = 1_000.0
DEFAULT_SIZE_MIN_ASPECT_SOFT = 5.0
DEFAULT_SIZE_MIN_ASPECT_HARD = 10.0
DEFAULT_SIZE_TILE_EDGE_BUFFER_PX = 4.0
DEFAULT_SIZE_TILE_EDGE_CONFIDENCE = 0.7

# Static-object penalty scaling defaults.
DEFAULT_STATIC_CONFIDENCE_SCALE = 1.5
DEFAULT_STATIC_CONFIDENCE_FLOOR = 0.3

# Coupling between artifact evidence and the dark-vessel residual. A contact
# that looks like an artifact is more likely to be an artifact than a dark
# vessel, but dark vessels are still possible.
DEFAULT_DARK_ARTIFACT_COUPLING = 0.6


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
    nearest_association: TrackAssociation | None = None
    n_tracks_within_gate: int = 0
    n_tracks_near_gate: int = 0  # within 2x gate but outside
    static_object_hit: StaticObjectHit | None = None
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


def size_artifact_confidence(
    contact: Contact,
    max_dim_soft_threshold_m: float = DEFAULT_SIZE_MAX_DIM_SOFT_M,
    max_dim_hard_threshold_m: float = DEFAULT_SIZE_MAX_DIM_HARD_M,
    min_aspect_soft: float = DEFAULT_SIZE_MIN_ASPECT_SOFT,
    min_aspect_hard: float = DEFAULT_SIZE_MIN_ASPECT_HARD,
    tile_edge_buffer_px: float = DEFAULT_SIZE_TILE_EDGE_BUFFER_PX,
    tile_edge_confidence: float = DEFAULT_SIZE_TILE_EDGE_CONFIDENCE,
    tile_shape_px: tuple[int, int] | None = None,
) -> float:
    """Return 0..1 probability that a SAR contact is a non-vessel size/shape artifact.

    Combines three evidence channels:
      * Oversize: real vessels rarely exceed ~500 m; contacts >1000 m are almost
        certainly azimuth-ambiguity or wind-streak artifacts.
      * Extreme aspect ratio: azimuth smearing produces very elongated boxes.
      * Tile-edge truncation: detections touching a tile border are often partial
        or duplicated artifacts.
    """
    conf = 0.0
    if (
        contact.width_m
        and contact.length_m
        and contact.width_m > 0
        and contact.length_m > 0
    ):
        max_dim = max(contact.width_m, contact.length_m)
        min_dim = min(contact.width_m, contact.length_m)
        aspect = max_dim / min_dim if min_dim > 0 else float("inf")

        # Oversize ramp: linear from soft to hard threshold, capped at 1.0.
        if max_dim >= max_dim_hard_threshold_m:
            conf = 1.0
        elif max_dim > max_dim_soft_threshold_m:
            conf = max(
                conf,
                (max_dim - max_dim_soft_threshold_m)
                / (max_dim_hard_threshold_m - max_dim_soft_threshold_m),
            )

        # Elongation ramp: azimuth/wind artifacts are often very long and thin.
        if aspect >= min_aspect_hard:
            conf = 1.0
        elif aspect > min_aspect_soft:
            conf = max(
                conf,
                (aspect - min_aspect_soft) / (min_aspect_hard - min_aspect_soft),
            )

    # Tile-edge truncation: partial/crowded detections at image borders.
    if contact.pixel_bbox is not None:
        xmin, ymin, xmax, ymax = contact.pixel_bbox
        near_zero = xmin < tile_edge_buffer_px or ymin < tile_edge_buffer_px
        near_far = False
        if tile_shape_px is not None:
            h, w = tile_shape_px
            near_far = (
                xmax > w - tile_edge_buffer_px
                or ymax > h - tile_edge_buffer_px
            )
        if near_zero or near_far:
            conf = max(conf, tile_edge_confidence)

    return float(min(conf, 1.0))


def associate_contact(
    contact: Contact,
    tracks: Iterable[AISTrack],
    t_sar: datetime | None = None,
    gate_radius_m: float = DEFAULT_GATE_RADIUS_M,
    max_extrapolate_s: float = 600.0,
    check_static_objects: bool = True,
    artifact_prior: float = DEFAULT_ARTIFACT_PRIOR,
    static_buffer_m: float = DEFAULT_PLATFORM_BUFFER_M,
    static_confidence_scale: float = DEFAULT_STATIC_CONFIDENCE_SCALE,
    static_confidence_floor: float = DEFAULT_STATIC_CONFIDENCE_FLOOR,
    size_max_dim_soft_m: float = DEFAULT_SIZE_MAX_DIM_SOFT_M,
    size_max_dim_hard_m: float = DEFAULT_SIZE_MAX_DIM_HARD_M,
    size_min_aspect_soft: float = DEFAULT_SIZE_MIN_ASPECT_SOFT,
    size_min_aspect_hard: float = DEFAULT_SIZE_MIN_ASPECT_HARD,
    size_tile_edge_buffer_px: float = DEFAULT_SIZE_TILE_EDGE_BUFFER_PX,
    size_tile_edge_confidence: float = DEFAULT_SIZE_TILE_EDGE_CONFIDENCE,
    dark_artifact_coupling: float = DEFAULT_DARK_ARTIFACT_COUPLING,
    image_shape_px: tuple[int, int] | None = None,
) -> ContactVerdict:
    """Compute the fusion verdict for a single SAR contact.

    Args:
        contact: SAR contact to attribute.
        tracks: iterable of ``AISTrack`` objects in the neighborhood.
        t_sar: SAR acquisition time; defaults to ``contact.acquisition_time``.
        gate_radius_m: maximum distance for an AIS track to explain the contact.
        max_extrapolate_s: maximum seconds to extrapolate an AIS track to t_sar.
        check_static_objects: whether to check known fixed objects.
        artifact_prior: base prior that a contact is a non-vessel artifact.
        static_buffer_m: radius for static-object hits.
        static_confidence_scale: multiplier for raw static-object confidence.
        static_confidence_floor: minimum static-object confidence for any hit.
        size_max_dim_soft_m: soft threshold above which size artifact evidence
            starts to accumulate.
        size_max_dim_hard_m: hard threshold above which size artifact evidence
            saturates at 1.0.
        size_min_aspect_soft: soft minimum aspect ratio for artifact evidence.
        size_min_aspect_hard: hard minimum aspect ratio for artifact evidence.
        size_tile_edge_buffer_px: pixel distance from a tile border treated as
            an edge-truncated detection.
        size_tile_edge_confidence: artifact confidence boost for edge contacts.
        dark_artifact_coupling: how strongly artifact evidence also competes
            with the dark-vessel residual.
        image_shape_px: optional (height, width) of the source tile, used for
            far-edge truncation checks.

    Returns:
        ``ContactVerdict`` with component probabilities and evidence trail.
    """
    if t_sar is None:
        t_sar = contact.acquisition_time
    if isinstance(t_sar, datetime) and t_sar.tzinfo is None:
        t_sar = t_sar.replace(tzinfo=timezone.utc)

    reasoning: list[str] = []
    sar_sigma = _sar_sigma_m(contact)
    associations: list[TrackAssociation] = []
    nearest_candidates: list[TrackAssociation] = []

    for track in tracks:
        interp = track.interpolate(t_sar, max_extrapolate_s=max_extrapolate_s)
        if interp is None:
            continue
        lon_i, lat_i, sigma_ais = interp
        d = _haversine_m(contact.center_lat, contact.center_lon, lat_i, lon_i)

        sigma_total = math.hypot(sigma_ais, sar_sigma)
        likelihood = _gaussian_likelihood(d, sigma_total)
        assoc = TrackAssociation(
            mmsi=track.mmsi,
            distance_m=d,
            sigma_m=sigma_total,
            likelihood=likelihood,
            interpolated_lon=lon_i,
            interpolated_lat=lat_i,
            vessel_name=track.vessel_name,
        )
        nearest_candidates.append(assoc)
        if d <= gate_radius_m:
            associations.append(assoc)

    nearest_candidates.sort(key=lambda a: a.distance_m)
    nearest_association = nearest_candidates[0] if nearest_candidates else None
    n_tracks_within_gate = len(associations)
    n_tracks_near_gate = len(
        [a for a in nearest_candidates if gate_radius_m < a.distance_m <= 2 * gate_radius_m]
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
    # Low-confidence detections keep some artifact probability; high-confidence
    # detections are treated as real vessels unless AIS geometry contradicts it.
    p_real_vessel = float(contact.confidence)
    p_artifact = (1.0 - p_real_vessel) * artifact_prior

    # Static-object exclusion: if the contact sits on a known fixed object
    # (oil platform, rig, small island), shift real-vessel mass to artifact.
    static_hit = (
        check_contact(contact, buffer_m=static_buffer_m)
        if check_static_objects
        else StaticObjectHit(False, None, float("inf"), 0.0)
    )
    static_conf = 0.0
    if static_hit.hit and static_hit.confidence > 0.0:
        static_conf = min(
            1.0,
            static_hit.confidence * static_confidence_scale + static_confidence_floor,
        )
        reasoning.append(
            f"Static object nearby: {static_hit.object.name} "
            f"({static_hit.distance_m:.0f} m away); "
            f"scaled static confidence {static_conf:.3f}."
        )

    # Size/shape artifact evidence.
    size_conf = size_artifact_confidence(
        contact,
        max_dim_soft_threshold_m=size_max_dim_soft_m,
        max_dim_hard_threshold_m=size_max_dim_hard_m,
        min_aspect_soft=size_min_aspect_soft,
        min_aspect_hard=size_min_aspect_hard,
        tile_edge_buffer_px=size_tile_edge_buffer_px,
        tile_edge_confidence=size_tile_edge_confidence,
        tile_shape_px=image_shape_px,
    )
    if size_conf > 0.0:
        max_dim = max(contact.width_m or 0.0, contact.length_m or 0.0)
        min_dim = min(contact.width_m or 1.0, contact.length_m or 1.0)
        aspect = max_dim / min_dim if min_dim > 0 else float("inf")
        reasoning.append(
            f"Size/shape artifact evidence: max_dim={max_dim:.0f} m, "
            f"aspect={aspect:.1f}, confidence={size_conf:.3f}."
        )

    # Combine independent artifact evidence channels.
    artifact_conf = 1.0 - (1.0 - size_conf) * (1.0 - static_conf)

    # Apply artifact evidence to real-vessel mass.
    if artifact_conf > 0.0:
        artifact_boost = p_real_vessel * artifact_conf
        p_artifact += artifact_boost
        p_real_vessel *= (1.0 - artifact_conf)
        reasoning.append(
            f"Artifact evidence ({artifact_conf:.3f}) shifted "
            f"{artifact_boost:.3f} real-vessel probability to artifact."
        )

    # Remaining real-vessel mass is split between clear and dark according to
    # the AIS evidence. Capture the AIS-derived match probability first so it
    # is not corrupted by the rescaling on the next line.
    real_mass = max(0.0, 1.0 - p_artifact)
    p_matched_given_real = p_clear
    p_clear = real_mass * p_matched_given_real
    p_dark = real_mass * (1.0 - p_matched_given_real)
    p_review = 0.0

    # Artifact evidence also competes with the dark-vessel residual.
    if artifact_conf > 0.0 and p_dark > 0.0:
        coupled_artifact_conf = artifact_conf * dark_artifact_coupling
        dark_artifact_boost = p_dark * coupled_artifact_conf
        p_artifact += dark_artifact_boost
        p_dark *= (1.0 - coupled_artifact_conf)
        reasoning.append(
            f"Artifact evidence also shifted {dark_artifact_boost:.3f} "
            f"dark-vessel probability to artifact."
        )

    # Innocent AIS dropout / coverage-gap adjustment.
    # If a track is just outside the gate we cannot confidently call the vessel
    # dark. If no tracks are anywhere nearby we may be in an AIS coverage gap.
    # Shift some mass from dark to review proportionally to the gap evidence.
    if p_dark > 0 and n_tracks_near_gate > 0 and nearest_association is not None:
        gap_ratio = max(0.0, 1.0 - nearest_association.distance_m / (2 * gate_radius_m))
        if gap_ratio > 0.0:
            shift = p_dark * gap_ratio * 0.5
            p_review += shift
            p_dark -= shift
            reasoning.append(
                f"Nearest AIS track MMSI {nearest_association.mmsi} is "
                f"{nearest_association.distance_m:.0f} m from contact (outside gate); "
                f"shifting {shift:.3f} probability from dark to review."
            )
    elif p_dark > 0 and n_tracks_within_gate == 0 and n_tracks_near_gate == 0:
        # No tracks anywhere nearby: high uncertainty about deliberate switch-off.
        shift = p_dark * 0.25
        p_review += shift
        p_dark -= shift
        reasoning.append("No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.")

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
        nearest_association=nearest_association,
        n_tracks_within_gate=n_tracks_within_gate,
        n_tracks_near_gate=n_tracks_near_gate,
        static_object_hit=static_hit,
        reasoning=reasoning,
    )


def associate_all_contacts(
    contacts: Iterable[Contact],
    tracks: Iterable[AISTrack],
    t_sar: datetime | None = None,
    gate_radius_m: float = DEFAULT_GATE_RADIUS_M,
    max_extrapolate_s: float = 600.0,
    check_static_objects: bool = True,
    artifact_prior: float = DEFAULT_ARTIFACT_PRIOR,
    static_buffer_m: float = DEFAULT_PLATFORM_BUFFER_M,
    static_confidence_scale: float = DEFAULT_STATIC_CONFIDENCE_SCALE,
    static_confidence_floor: float = DEFAULT_STATIC_CONFIDENCE_FLOOR,
    size_max_dim_soft_m: float = DEFAULT_SIZE_MAX_DIM_SOFT_M,
    size_max_dim_hard_m: float = DEFAULT_SIZE_MAX_DIM_HARD_M,
    size_min_aspect_soft: float = DEFAULT_SIZE_MIN_ASPECT_SOFT,
    size_min_aspect_hard: float = DEFAULT_SIZE_MIN_ASPECT_HARD,
    size_tile_edge_buffer_px: float = DEFAULT_SIZE_TILE_EDGE_BUFFER_PX,
    size_tile_edge_confidence: float = DEFAULT_SIZE_TILE_EDGE_CONFIDENCE,
    dark_artifact_coupling: float = DEFAULT_DARK_ARTIFACT_COUPLING,
    image_shape_px: tuple[int, int] | None = None,
) -> list[ContactVerdict]:
    """Run association for every contact using the same track collection."""
    return [
        associate_contact(
            c,
            tracks,
            t_sar,
            gate_radius_m,
            max_extrapolate_s,
            check_static_objects,
            artifact_prior,
            static_buffer_m,
            static_confidence_scale,
            static_confidence_floor,
            size_max_dim_soft_m,
            size_max_dim_hard_m,
            size_min_aspect_soft,
            size_min_aspect_hard,
            size_tile_edge_buffer_px,
            size_tile_edge_confidence,
            dark_artifact_coupling,
            image_shape_px,
        )
        for c in contacts
    ]
