"""YOLO-based vessel detector training and inference.

Designed for small consumer GPUs (RTX 5060 8 GB). Defaults to YOLOv8n
(nano) with small image size and batch size. Supports loading a custom
model path or a standard Ultralytics hub name.
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import rasterio
import shapely
from rasterio.control import GroundControlPoint
from scipy.interpolate import LinearNDInterpolator

from .contact import Contact


class VesselDetector:
    """Thin wrapper around an Ultralytics YOLO detector."""

    def __init__(self, model_path: str = "yolov8n.pt", device: str | None = None) -> None:
        """Initialize the detector.

        Args:
            model_path: Ultralytics hub name (e.g. 'yolov8n.pt') or path to a
                trained .pt/.onnx model.
            device: torch device; None lets Ultralytics auto-select (CUDA if available).
        """
        from ultralytics import YOLO

        self.model_path = model_path
        self.model = YOLO(model_path)
        self.device = device

    def train(
        self,
        data_yaml: Path | str,
        epochs: int = 50,
        imgsz: int = 640,
        batch: int = 4,
        patience: int = 10,
        name: str = "darkwatch_detector",
        project: Path | str = "models/detector_runs",
        **kwargs,
    ) -> Path:
        """Fine-tune the detector on a YOLO-format dataset.

        Returns the path to the best trained weights.
        """
        self.model.train(
            data=str(data_yaml),
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            patience=patience,
            name=name,
            project=str(project),
            device=self.device,
            **kwargs,
        )
        best = Path(project) / name / "weights" / "best.pt"
        return best

    def predict(
        self,
        image_paths: list[Path | str],
        conf: float = 0.25,
        iou: float = 0.45,
        imgsz: int = 640,
        **kwargs,
    ) -> list[list[dict]]:
        """Run inference on a list of image paths.

        Returns a list (per image) of detection dicts with keys:
          - image_id / tile_id
          - pixel_bbox: [xmin, ymin, xmax, ymax]
          - confidence
          - class_id
        """
        results = self.model.predict(
            source=[str(p) for p in image_paths],
            conf=conf,
            iou=iou,
            imgsz=imgsz,
            device=self.device,
            verbose=False,
            **kwargs,
        )

        detections_per_image = []
        for res in results:
            dets = []
            if res.boxes is None:
                detections_per_image.append(dets)
                continue
            boxes = res.boxes.xyxy.cpu().numpy()
            confs = res.boxes.conf.cpu().numpy()
            cls_ids = res.boxes.cls.cpu().numpy().astype(int)
            for box, conf, cls_id in zip(boxes, confs, cls_ids):
                dets.append(
                    {
                        "pixel_bbox": tuple(float(v) for v in box),
                        "confidence": float(conf),
                        "class_id": int(cls_id),
                    }
                )
            detections_per_image.append(dets)
        return detections_per_image


def _load_tile_georeference(img_path: Path) -> tuple[CRS, list[GroundControlPoint], tuple[int, int]]:
    """Read GCPs and CRS from a Darkwatch tile GeoTIFF."""
    from rasterio.crs import CRS

    with rasterio.open(img_path) as src:
        crs = src.crs
        gcps = src.gcps[0]
        shape = (src.height, src.width)
    return crs, gcps, shape


def _gcp_interpolator(gcps: list[GroundControlPoint], shape: tuple[int, int]) -> LinearNDInterpolator:
    """Build a barycentric (row, col) -> (lon, lat) interpolator from GCPs."""
    if len(gcps) < 3:
        raise ValueError(f"Need at least 3 GCPs, got {len(gcps)}")

    rows = np.array([g.row for g in gcps], dtype=np.float64)
    cols = np.array([g.col for g in gcps], dtype=np.float64)
    lons = np.array([g.x for g in gcps], dtype=np.float64)
    lats = np.array([g.y for g in gcps], dtype=np.float64)

    return LinearNDInterpolator(np.column_stack((rows, cols)), np.column_stack((lons, lats)))


def _pixel_size_meters(gcps: list[GroundControlPoint]) -> float:
    """Estimate pixel size in metres from corner GCPs (approximate at tile centre)."""
    # Use WGS84 Haversine between two adjacent corners.
    import math

    # Sort by (row, col) and pick two adjacent in column direction.
    gcps_sorted = sorted(gcps, key=lambda g: (g.row, g.col))
    if len(gcps_sorted) >= 4:
        a, b = gcps_sorted[0], gcps_sorted[1]
    else:
        a, b = gcps_sorted[0], gcps_sorted[-1]

    lat1, lon1 = math.radians(a.y), math.radians(a.x)
    lat2, lon2 = math.radians(b.y), math.radians(b.x)
    R = 6_371_000
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    dist = 2 * R * math.asin(math.sqrt(h))
    # Pixel column distance.
    pix_dist = math.hypot(b.col - a.col, b.row - a.row)
    if pix_dist == 0:
        return 10.0
    return dist / pix_dist


def detect_tiles(
    detector: VesselDetector,
    tile_manifest_path: Path | str,
    output_dir: Path | str,
    conf: float = 0.25,
    iou: float = 0.45,
    imgsz: int = 640,
) -> list[Contact]:
    """Run detector on all tiles in a Darkwatch manifest and geo-locate contacts.

    Args:
        detector: initialized VesselDetector.
        tile_manifest_path: path to manifest.json from `prep_scene`.
        output_dir: directory for detection outputs (images, labels, contacts.json).
        conf, iou, imgsz: inference parameters.

    Returns:
        List of Contact objects, one per detection.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    labels_dir = output_dir / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(Path(tile_manifest_path).read_text())
    image_paths = [Path(p) for p in manifest["tiles"]]
    tile_meta = [json.loads(Path(p).read_text()) for p in manifest["tile_meta"]]

    scene_name = manifest["scene_name"]
    acquisition_time = datetime.fromisoformat(manifest["acquisition_time"])

    detections_per_image = detector.predict(
        image_paths=image_paths,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
    )

    contacts: list[Contact] = []
    for img_path, meta, dets in zip(image_paths, tile_meta, detections_per_image):
        tile_id = meta["tile_id"]
        try:
            _, gcps, shape = _load_tile_georeference(img_path)
            interp = _gcp_interpolator(gcps, shape)
            pixel_size = _pixel_size_meters(gcps)
        except Exception as exc:
            print(f"WARN: cannot geo-reference {img_path}: {exc}")
            pixel_size = 10.0
            # Build a fallback identity-ish interpolator.
            interp = LinearNDInterpolator(
                np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
                np.column_stack(
                    [np.array([meta["corner_lons"][0]] * 4), np.array([meta["corner_lats"][0]] * 4)]
                ),
            )

        for i, det in enumerate(dets):
            xmin, ymin, xmax, ymax = det["pixel_bbox"]
            cx_pix = (xmin + xmax) / 2.0
            cy_pix = (ymin + ymax) / 2.0
            lonlat = interp([[cy_pix, cx_pix]])[0]
            if lonlat is None or not np.all(np.isfinite(lonlat)):
                continue
            center_lon, center_lat = float(lonlat[0]), float(lonlat[1])

            width_px = xmax - xmin
            height_px = ymax - ymin
            width_m = width_px * pixel_size
            length_m = height_px * pixel_size

            contact_id = f"{tile_id}_det{i:04d}"
            contacts.append(
                Contact(
                    contact_id=contact_id,
                    tile_id=tile_id,
                    scene_name=scene_name,
                    acquisition_time=acquisition_time,
                    center_lon=center_lon,
                    center_lat=center_lat,
                    width_m=width_m,
                    length_m=length_m,
                    confidence=det["confidence"],
                    pixel_bbox=(xmin, ymin, xmax, ymax),
                    source=f"{detector.model_path}",
                )
            )

    # Write YOLO-style detection labels and a JSON contact list.
    for contact in contacts:
        label_path = labels_dir / f"{contact.tile_id}.txt"
        # Append to existing labels if multiple contacts per tile.
        with open(label_path, "a") as f:
            # We don't know image dimensions here, so write absolute pixel bbox.
            f.write(f"ship {contact.pixel_bbox[0]:.2f} {contact.pixel_bbox[1]:.2f} "
                    f"{contact.pixel_bbox[2]:.2f} {contact.pixel_bbox[3]:.2f} "
                    f"{contact.confidence:.4f}\n")

    contacts_path = output_dir / "contacts.json"
    contacts_path.write_text(
        json.dumps(
            [
                {
                    "contact_id": c.contact_id,
                    "tile_id": c.tile_id,
                    "scene_name": c.scene_name,
                    "acquisition_time": c.acquisition_time.isoformat(),
                    "center_lon": c.center_lon,
                    "center_lat": c.center_lat,
                    "width_m": c.width_m,
                    "length_m": c.length_m,
                    "confidence": c.confidence,
                    "pixel_bbox": c.pixel_bbox,
                    "source": c.source,
                }
                for c in contacts
            ],
            indent=2,
        )
    )

    print(f"Detected {len(contacts)} contacts across {len(image_paths)} tiles")
    print(f"Contacts saved to {contacts_path}")
    return contacts
