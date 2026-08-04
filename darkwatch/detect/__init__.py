"""Vessel detection in SAR imagery (S2).

Public exports:
  - VesselDetector: thin wrapper around an Ultralytics YOLO model.
  - coco_to_yolo_dataset: convert SSDD COCO annotations to YOLO training layout.
  - detect_tiles: run inference on Darkwatch tiles and emit geo-located contacts.
"""

from __future__ import annotations

from .contact import Contact
from .dataset import coco_to_yolo_dataset
from .detector import VesselDetector, detect_tiles

__all__ = [
    "Contact",
    "coco_to_yolo_dataset",
    "VesselDetector",
    "detect_tiles",
]
