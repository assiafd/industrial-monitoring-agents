"""Train the machine-health classification model.

Usage:
    python scripts/train_model.py
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT_DIR / "data" / "telemetry_training.csv"
MODEL_PATH = ROOT_DIR / "models" / "machine_health_model.joblib"

FEATURE_COLUMNS = [
    "temperature_c",
    "vibration_mm_s",
    "pressure_bar",
    "energy_kw",
    "rotation_rpm",
    "error_code",
]
TARGET_COLUMN = "label"


def build_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "error_code",
                OneHotEncoder(handle_unknown="ignore"),
                ["error_code"],
            )
        ],
        remainder="passthrough",
    )
    classifier = RandomForestClassifier(
        n_estimators=120,
        random_state=42,
        class_weight="balanced",
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def main() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset introuvable: {DATASET_PATH}")

    dataset = pd.read_csv(DATASET_PATH)
    missing_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN]) - set(dataset.columns)
    if missing_columns:
        raise ValueError(f"Colonnes manquantes dans le dataset: {sorted(missing_columns)}")

    x = dataset[FEATURE_COLUMNS]
    y = dataset[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = build_pipeline()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "feature_columns": FEATURE_COLUMNS,
            "target_column": TARGET_COLUMN,
            "accuracy": accuracy,
        },
        MODEL_PATH,
    )

    print(f"Modèle sauvegardé: {MODEL_PATH}")
    print(f"Accuracy test: {accuracy:.3f}")
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    main()
