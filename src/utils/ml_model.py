"""Optional scikit-learn model inference for machine health prediction."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = ROOT_DIR / "models" / "machine_health_model.joblib"


def _build_features(telemetry: dict[str, Any], feature_columns: list[str]) -> dict[str, Any]:
    return {
        column: telemetry.get(column, "OK" if column == "error_code" else 0)
        for column in feature_columns
    }


@lru_cache(maxsize=1)
def load_model_bundle(model_path: str = str(DEFAULT_MODEL_PATH)) -> dict[str, Any] | None:
    path = Path(model_path)
    if not path.exists():
        return None

    try:
        import joblib
    except ImportError:
        return {
            "load_error": "joblib package is not installed",
            "model_path": str(path),
        }

    try:
        return joblib.load(path)
    except Exception as exc:
        return {
            "load_error": str(exc),
            "model_path": str(path),
        }


def predict_machine_health(telemetry: dict[str, Any]) -> dict[str, Any]:
    """Return an ML prediction if the trained model is available."""

    bundle = load_model_bundle()
    if bundle is None:
        return {
            "status": "model_not_found",
            "model_path": str(DEFAULT_MODEL_PATH),
            "label": None,
            "confidence": None,
        }
    if "load_error" in bundle:
        return {
            "status": "load_failed",
            "model_path": bundle.get("model_path", str(DEFAULT_MODEL_PATH)),
            "error": bundle["load_error"],
            "label": None,
            "confidence": None,
        }

    try:
        import pandas as pd
    except ImportError:
        return {
            "status": "dependency_missing",
            "model_path": str(DEFAULT_MODEL_PATH),
            "error": "pandas package is not installed",
            "label": None,
            "confidence": None,
        }

    model = bundle["model"]
    feature_columns = bundle["feature_columns"]
    features = _build_features(telemetry, feature_columns)
    frame = pd.DataFrame([features], columns=feature_columns)

    label = str(model.predict(frame)[0])
    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(frame)[0]
        class_labels = list(model.classes_)
        confidence = float(probabilities[class_labels.index(label)])

    return {
        "status": "predicted",
        "model_path": str(DEFAULT_MODEL_PATH),
        "label": label,
        "confidence": round(confidence, 4) if confidence is not None else None,
        "model_accuracy": round(float(bundle.get("accuracy", 0)), 4),
        "features": features,
    }
