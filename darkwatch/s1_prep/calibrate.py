"""Sentinel-1 GRD radiometric calibration: raw DN → sigma-nought (dB).

Reference: Sentinel-1 Product Specification. For GRD products:
    sigma0 = DN^2 / K^2
where K is the per-pixel sigma-nought calibration factor sampled along range.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
from defusedxml import ElementTree as ET


CalibrationKind = Literal["sigma", "beta", "gamma", "dn"]


def _read_calibration_samples(calib_xml: Path, kind: CalibrationKind = "sigma") -> tuple[np.ndarray, np.ndarray]:
    """Read (pixel_indices, calibration_values) for the requested kind.

    `kind` maps to the XML tag names:
        sigma -> sigmaNought
        beta  -> betaNought
        gamma -> gamma
        dn    -> dn
    """
    tag_map = {
        "sigma": "sigmaNought",
        "beta": "betaNought",
        "gamma": "gamma",
        "dn": "dn",
    }
    tag_name = tag_map[kind]

    tree = ET.parse(calib_xml)

    vector_list = tree.find(".//calibrationVectorList")
    if vector_list is None:
        vector_list = tree.find(
            ".//{http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-1/product/calibration}calibrationVectorList"
        )
    if vector_list is None:
        raise ValueError(f"Could not locate calibrationVectorList in {calib_xml}")

    first_vector = vector_list.find("./calibrationVector")
    if first_vector is None:
        raise ValueError("No calibrationVector entries found")

    pixel_node = first_vector.find("./pixel")
    value_node = first_vector.find(f"./{tag_name}")
    if pixel_node is None or value_node is None:
        raise ValueError(f"No pixel/{tag_name} nodes found in calibrationVector")

    pixel_indices = np.fromstring(pixel_node.text, sep=" ", dtype=np.int64)
    values = np.fromstring(value_node.text, sep=" ", dtype=np.float32)
    if pixel_indices.shape[0] != values.shape[0]:
        raise ValueError("pixel and calibration value length mismatch")
    return pixel_indices, values


def build_range_calibration_vector(width: int, pixel_indices: np.ndarray, values: np.ndarray) -> np.ndarray:
    """Interpolate sampled calibration values to every range column."""
    full_columns = np.arange(width, dtype=np.float32)
    return np.interp(full_columns, pixel_indices.astype(np.float32), values).astype(np.float32)


def calibrate_dn_to_sigma0(dn_array: np.ndarray, calib_vector: np.ndarray) -> np.ndarray:
    """Convert raw digital numbers to linear sigma-nought.

    Args:
        dn_array: raw DN image, shape (height, width).
        calib_vector: per-column calibration factor, shape (width,).

    Returns:
        Linear sigma-nought array, same shape as dn_array, float32.
    """
    if calib_vector.shape[0] != dn_array.shape[1]:
        raise ValueError(
            f"Calibration vector width ({calib_vector.shape[0]}) does not match "
            f"image width ({dn_array.shape[1]})"
        )
    dn = dn_array.astype(np.float32)
    calib = calib_vector.astype(np.float32)
    # Broadcast calibration across rows.
    sigma0 = (dn ** 2) / (calib ** 2)
    return sigma0


def sigma0_to_db(sigma0: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """Linear sigma-nought to decibel."""
    return 10.0 * np.log10(np.maximum(sigma0, eps))


def db_to_sigma0(sigma_db: np.ndarray) -> np.ndarray:
    """Decibel to linear sigma-nought."""
    return 10.0 ** (sigma_db / 10.0)


def read_and_calibrate(
    calib_xml: Path,
    dn_array: np.ndarray,
    to_decibels: bool = True,
    kind: CalibrationKind = "sigma",
) -> np.ndarray:
    """Convenience: read calibration XML and apply it to a DN array."""
    pixel_indices, values = _read_calibration_samples(calib_xml, kind=kind)
    calib_vector = build_range_calibration_vector(dn_array.shape[1], pixel_indices, values)
    sigma0 = calibrate_dn_to_sigma0(dn_array, calib_vector)
    if to_decibels:
        return sigma0_to_db(sigma0)
    return sigma0
