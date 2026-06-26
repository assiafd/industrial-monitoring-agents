"""Send simulated industrial telemetry to the FastAPI workflow."""

from __future__ import annotations

import argparse
import random
from typing import Any

import requests


def generate_payload(critical: bool = False) -> dict[str, Any]:
    if critical:
        return {
            "machine_id": "PRESS-HYDRAULIQUE-02",
            "temperature_c": random.uniform(88, 110),
            "vibration_mm_s": random.uniform(8, 12),
            "pressure_bar": random.uniform(11, 15),
            "energy_kw": random.uniform(35, 52),
            "rotation_rpm": random.uniform(700, 2600),
            "error_code": random.choice(["E_TEMP", "E_VIB", "E_PRESSURE"]),
        }

    return {
        "machine_id": "CONVOYEUR-01",
        "temperature_c": random.uniform(45, 72),
        "vibration_mm_s": random.uniform(1, 4),
        "pressure_bar": random.uniform(6, 10),
        "energy_kw": random.uniform(15, 33),
        "rotation_rpm": random.uniform(900, 2500),
        "error_code": "OK",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000/analyze")
    parser.add_argument("--critical", action="store_true")
    args = parser.parse_args()

    payload = generate_payload(critical=args.critical)
    response = requests.post(args.url, json=payload, timeout=10)
    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()
