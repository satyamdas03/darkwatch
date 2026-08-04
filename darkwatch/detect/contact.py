"""Contact dataclass for detected vessels."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Contact:
    """A detected vessel-sized radar contact.

    Attributes:
        contact_id: unique identifier.
        tile_id: source tile identifier.
        scene_name: source Sentinel-1 product name.
        acquisition_time: UTC timestamp of the SAR image.
        center_lon: WGS84 longitude of the contact centre.
        center_lat: WGS84 latitude of the contact centre.
        width_m: approximate width in metres (from pixel size and bbox).
        length_m: approximate length in metres.
        confidence: detector confidence, 0–1.
        pixel_bbox: [x_min, y_min, x_max, y_max] in tile pixel coordinates.
        source: model name / version that produced the contact.
        meta: extra fields (e.g., number of detections merged).
    """

    contact_id: str
    tile_id: str
    scene_name: str
    acquisition_time: datetime
    center_lon: float
    center_lat: float
    width_m: float
    length_m: float
    confidence: float
    pixel_bbox: tuple[float, float, float, float]
    source: str = "darkwatch/detector"
    meta: dict = field(default_factory=dict)
