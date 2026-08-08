"""YOLO-based vessel detector training and inference.

Designed for small consumer GPUs (RTX 5060 8 GB). Defaults to YOLOv8n
(nano) with small image size and batch size. Supports loading a custom
model path or a standard Ultralytics hub name.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import math

import numpy as np
import rasterio
import shapely
from rasterio.control import GroundControlPoint
from scipy.interpolate import LinearNDInterpolator

from .contact import Contact


def _db_to_uint8(
    arr: np.ndarray,
    db_range: tuple[float, float] = (-25.0, -5.0),
    adaptive_percentiles: tuple[float, float] | None = None,
) -> np.ndarray:
    """Convert a SAR dB image to an 8-bit RGB array suitable for SSDD-trained YOLO.

    The default stretch maps -25 dB -> 0 and -5 dB -> 255. NaN/Inf values are
    clamped to the range limits before stretching.

    If ``adaptive_percentiles`` is provided (e.g. ``(1.0, 99.0)``), the stretch
    bounds are computed per-image from those percentiles of the finite dB values,
    but clamped to ``db_range`` to avoid extreme outliers. This helps bring out
    faint, low-backscatter vessels in heterogeneous tiles.
    """
    lo, hi = db_range
    finite = arr[np.isfinite(arr)]
    if adaptive_percentiles is not None and len(finite) > 0:
        p_lo, p_hi = adaptive_percentiles
        lo = max(lo, float(np.percentile(finite, p_lo)))
        hi = min(hi, float(np.percentile(finite, p_hi)))
        if lo >= hi:
            hi = lo + 1.0

    arr = np.nan_to_num(arr, nan=lo, posinf=hi, neginf=lo)
    stretched = np.clip((arr - lo) / (hi - lo), 0.0, 1.0)
    uint8 = (stretched * 255.0).astype(np.uint8)

    if uint8.ndim == 2:
        # Grayscale -> RGB by duplicating the single band.
        uint8 = np.stack([uint8, uint8, uint8], axis=-1)
    elif uint8.ndim == 3:
        # Channel-first (C, H, W) as returned by rasterio.read() with indexes=None.
        if uint8.shape[0] == 1:
            uint8 = np.stack([uint8[0], uint8[0], uint8[0]], axis=-1)
        elif uint8.shape[0] == 3:
            uint8 = np.transpose(uint8, (1, 2, 0))
        elif uint8.shape[-1] == 1:
            uint8 = np.stack([uint8[..., 0], uint8[..., 0], uint8[..., 0]], axis=-1)
        # If shape[-1] == 3 we already have RGB.

    return uint8


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
        train_kwargs = dict(kwargs)
        if self.device is not None:
            train_kwargs.setdefault("device", self.device)
        self.model.train(
            data=str(data_yaml),
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            patience=patience,
            name=name,
            project=str(project),
            **train_kwargs,
        )
        best = Path(project) / name / "weights" / "best.pt"
        return best

    def predict(
        self,
        image_paths: list[Path | str | np.ndarray],
        conf: float = 0.25,
        iou: float = 0.45,
        imgsz: int = 640,
        db_range: tuple[float, float] | None = (-25.0, -5.0),
        adaptive_percentiles: tuple[float, float] | None = None,
        **kwargs,
    ) -> list[list[dict]]:
        """Run inference on a list of image paths or arrays.

        GeoTIFF paths are loaded with rasterio and converted from float dB to
        uint8 RGB using ``db_range``. Existing uint8 arrays are passed through
        (duplicated to 3 channels if grayscale). Plain image paths are passed to
        YOLO unchanged.

        If ``adaptive_percentiles`` is given (e.g. ``(1.0, 99.0)``), the dB
        stretch limits are computed per-image from those percentiles, clamped
        to ``db_range``. This can reveal faint targets in tiles with highly
        variable backscatter.

        Returns a list (per image) of detection dicts with keys:
          - image_id / tile_id
          - pixel_bbox: [xmin, ymin, xmax, ymax]
          - confidence
          - class_id
        """
        sources: list[np.ndarray | str] = []
        for src in image_paths:
            if isinstance(src, np.ndarray):
                arr = src
                if arr.dtype != np.uint8 and db_range is not None:
                    arr = _db_to_uint8(arr, db_range, adaptive_percentiles=adaptive_percentiles)
                elif arr.ndim == 2:
                    arr = np.stack([arr, arr, arr], axis=-1)
                sources.append(arr)
                continue

            path = Path(src)
            if path.suffix.lower() in {".tif", ".tiff"}:
                with rasterio.open(path) as ds:
                    arr = ds.read(1)
                if db_range is not None:
                    arr = _db_to_uint8(arr, db_range, adaptive_percentiles=adaptive_percentiles)
                elif arr.ndim == 2:
                    arr = np.stack([arr, arr, arr], axis=-1)
                sources.append(arr)
            else:
                sources.append(str(path))

        results = self.model.predict(
            source=sources,
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


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres between two WGS84 points."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _deduplicate_contacts(contacts: list[Contact], distance_m: float = 100.0) -> list[Contact]:
    """Merge contacts that are likely the same physical vessel.

    Keeps the highest-confidence contact from each spatial cluster.
    """
    sorted_contacts = sorted(contacts, key=lambda c: c.confidence, reverse=True)
    kept: list[Contact] = []
    for candidate in sorted_contacts:
        if not any(_haversine_m(candidate.center_lat, candidate.center_lon, k.center_lat, k.center_lon) < distance_m for k in kept):
            kept.append(candidate)
    return kept


def detect_tiles(
    detector: VesselDetector,
    tile_manifest_path: Path | str,
    output_dir: Path | str,
    conf: float = 0.25,
    iou: float = 0.45,
    imgsz: int = 640,
    db_range: tuple[float, float] | None = (-25.0, -5.0),
    adaptive_percentiles: tuple[float, float] | None = None,
    polarizations: Iterable[str] | None = None,
) -> list[Contact]:
    """Run detector on all tiles in a Darkwatch manifest and geo-locate contacts.

    Args:
        detector: initialized VesselDetector.
        adaptive_percentiles: if given, per-tile percentile stretch is applied
            to GeoTIFF dB data (e.g. ``(1.0, 99.0)``).
        tile_manifest_path: path to manifest.json from `prep_scene`.
        output_dir: directory for detection outputs (images, labels, contacts.json).
        conf, iou, imgsz: inference parameters.
        db_range: dB contrast-stretch range for float GeoTIFF tiles; set to
            ``None`` to skip stretching.
        polarizations: if provided, only process tiles whose metadata
            ``polarization`` field is in this set (e.g. {"vv"} or {"vv", "vh"}).

    Returns:
        List of Contact objects, one per detection.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    labels_dir = output_dir / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(Path(tile_manifest_path).read_text())
    all_image_paths = [Path(p) for p in manifest["tiles"]]
    all_tile_meta = [json.loads(Path(p).read_text()) for p in manifest["tile_meta"]]

    if polarizations is not None:
        pol_set = {p.lower() for p in polarizations}
        image_paths = []
        tile_meta = []
        for img_path, meta in zip(all_image_paths, all_tile_meta):
            if meta.get("polarization", "").lower() in pol_set:
                image_paths.append(img_path)
                tile_meta.append(meta)
    else:
        image_paths = all_image_paths
        tile_meta = all_tile_meta

    scene_name = manifest["scene_name"]
    acquisition_time = datetime.fromisoformat(manifest["acquisition_time"])

    detections_per_image = detector.predict(
        image_paths=image_paths,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        db_range=db_range,
        adaptive_percentiles=adaptive_percentiles,
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

    # Merge contacts from overlapping tiles that describe the same physical vessel.
    contacts = _deduplicate_contacts(contacts, distance_m=100.0)

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
