"""Learned calibration layer for Darkwatch fusion probabilities.

The fusion engine emits marginal probabilities for each verdict class. Those
probabilities are principled but not empirically calibrated: a contact with
``p_clear = 0.7`` may not actually be matched to AIS 70% of the time. This
module fits a small post-processing model on hand-labeled contacts so that the
reported probabilities better match observed frequencies.

The model is intentionally simple: per-class Platt (logistic) scaling,

    logit(p_cal) = scale * logit(p_raw) + shift

fitted by minimizing the Brier score. With only a few dozen labels the model
stays well regularized and interpretable. It can be saved to JSON and loaded
at inference time.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize

from darkwatch.fusion.verdict import Verdict


@dataclass
class CalibrationModel:
    """Per-class Platt calibration parameters."""

    params: dict[str, tuple[float, float]] = field(default_factory=dict)
    classes: tuple[str, ...] = ("p_artifact", "p_clear", "p_dark", "p_review")

    EPS: float = 1e-6

    def fit(self, records: list[dict[str, Any]], l2_penalty: float = 0.01) -> "CalibrationModel":
        """Fit Platt scaling on a list of records.

        Each record must contain the raw probability keys used by
        ``ContactVerdict`` (``p_artifact``, ``p_clear``, ``p_dark``,
        ``p_review``) and a ``true_label`` field (a ``Verdict`` name or
        ``UNKNOWN``).
        """
        for pkey in self.classes:
            probs = np.array([r[pkey] for r in records])
            outcomes = np.array(
                [1.0 if r["true_label"] == self._verdict_from_key(pkey) else 0.0 for r in records]
            )
            scale, shift = self._fit_class(probs, outcomes, l2_penalty)
            self.params[pkey] = (float(scale), float(shift))
        return self

    def transform(self, p_artifact: float, p_clear: float, p_dark: float, p_review: float) -> dict[str, float]:
        """Return calibrated probabilities for a single contact."""
        raw = {
            "p_artifact": p_artifact,
            "p_clear": p_clear,
            "p_dark": p_dark,
            "p_review": p_review,
        }
        calibrated: dict[str, float] = {}
        for pkey, p_raw in raw.items():
            scale, shift = self.params.get(pkey, (1.0, 0.0))
            logit_raw = math.log((max(p_raw, self.EPS)) / max(1.0 - p_raw, self.EPS))
            logit_cal = scale * logit_raw + shift
            calibrated[pkey] = self._sigmoid(logit_cal)
        total = sum(calibrated.values())
        if total > 0.0:
            calibrated = {k: v / total for k, v in calibrated.items()}
        return calibrated

    def transform_records(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return a new list of records with calibrated probabilities and verdicts."""
        out: list[dict[str, Any]] = []
        for r in records:
            cal = self.transform(
                r["p_artifact"], r["p_clear"], r["p_dark"], r["p_review"]
            )
            rec = dict(r)
            rec["p_artifact"] = cal["p_artifact"]
            rec["p_clear"] = cal["p_clear"]
            rec["p_dark"] = cal["p_dark"]
            rec["p_review"] = cal["p_review"]
            rec["verdict"] = self._verdict_from_probs(cal)
            out.append(rec)
        return out

    def save(self, path: str | Path) -> None:
        """Serialize to JSON."""
        payload = {
            "classes": list(self.classes),
            "params": {k: list(v) for k, v in self.params.items()},
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "CalibrationModel":
        """Load a previously saved model."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        model = cls(classes=tuple(payload.get("classes", cls.classes)))
        model.params = {k: tuple(v) for k, v in payload["params"].items()}
        return model

    @staticmethod
    def _verdict_from_key(pkey: str) -> str:
        return pkey.replace("p_", "").upper()

    @staticmethod
    def _verdict_from_probs(probs: dict[str, float]) -> str:
        if probs["p_artifact"] > 0.5:
            return Verdict.ARTIFACT.name
        if probs["p_clear"] > 0.6:
            return Verdict.CLEAR.name
        if probs["p_dark"] > 0.6:
            return Verdict.DARK.name
        return Verdict.REVIEW.name

    @staticmethod
    def _sigmoid(x: float) -> float:
        if x >= 0:
            z = math.exp(-x)
            return 1.0 / (1.0 + z)
        z = math.exp(x)
        return z / (1.0 + z)

    def _fit_class(
        self, probs: np.ndarray, outcomes: np.ndarray, l2_penalty: float
    ) -> tuple[float, float]:
        """Fit (scale, shift) by minimizing Brier + L2 penalty on parameters."""

        def objective(theta: np.ndarray) -> float:
            scale, shift = float(theta[0]), float(theta[1])
            logit_raw = np.log(np.maximum(probs, self.EPS) / np.maximum(1.0 - probs, self.EPS))
            logit_cal = scale * logit_raw + shift
            cal = 1.0 / (1.0 + np.exp(-logit_cal))
            brier = float(np.mean((cal - outcomes) ** 2))
            penalty = l2_penalty * ((scale - 1.0) ** 2 + shift ** 2)
            return brier + penalty

        result = minimize(objective, np.array([1.0, 0.0]), method="Nelder-Mead")
        return float(result.x[0]), float(result.x[1])


def brier_score(probs: np.ndarray, outcomes: np.ndarray) -> float:
    if len(probs) == 0:
        return float("nan")
    return float(np.mean((probs - outcomes) ** 2))
