"""Optional Gemini LLM client used by the agents."""

from __future__ import annotations

import os
from time import perf_counter
from typing import Any


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_INPUT_COST_PER_1M_TOKENS = 0.30
DEFAULT_OUTPUT_COST_PER_1M_TOKENS = 2.50


def get_llm_metadata() -> dict[str, Any]:
    """Return the configured LLM metadata without exposing secrets."""

    return {
        "provider": "google_gemini",
        "model": os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL,
        "enabled": bool((os.getenv("GOOGLE_API_KEY") or "").strip()),
    }


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def _extract_usage_metadata(response: Any) -> dict[str, int]:
    usage = getattr(response, "usage_metadata", None)
    if usage is None:
        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    prompt_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
    completion_tokens = int(getattr(usage, "candidates_token_count", 0) or 0)
    total_tokens = int(getattr(usage, "total_token_count", 0) or 0)

    if total_tokens == 0:
        total_tokens = prompt_tokens + completion_tokens

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


def _estimate_tokens_from_text(prompt: str, output: str | None = None) -> dict[str, int]:
    # Rough fallback used only when Gemini does not return usage metadata.
    prompt_tokens = max(1, round(len(prompt.split()) * 1.3))
    completion_tokens = round(len((output or "").split()) * 1.3)
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }


def _estimate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    input_cost = _float_env("GEMINI_INPUT_COST_PER_1M_TOKENS", DEFAULT_INPUT_COST_PER_1M_TOKENS)
    output_cost = _float_env("GEMINI_OUTPUT_COST_PER_1M_TOKENS", DEFAULT_OUTPUT_COST_PER_1M_TOKENS)
    estimated = (prompt_tokens / 1_000_000) * input_cost
    estimated += (completion_tokens / 1_000_000) * output_cost
    return round(estimated, 8)


def _metrics(
    *,
    started_at: float,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    total_tokens: int = 0,
) -> dict[str, Any]:
    return {
        "latency_seconds": round(perf_counter() - started_at, 4),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": _estimate_cost(prompt_tokens, completion_tokens),
    }


def generate_with_gemini(prompt: str) -> dict[str, Any]:
    """Generate a response with Gemini when GOOGLE_API_KEY is configured.

    The project stays fully testable without network or API credentials. When the
    key or SDK is missing, agents receive an explicit skipped status and use their
    deterministic fallback logic.
    """

    started_at = perf_counter()
    api_key = (os.getenv("GOOGLE_API_KEY") or "").strip()
    model_name = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL

    if not api_key:
        return {
            "status": "skipped",
            "reason": "GOOGLE_API_KEY is not configured",
            "provider": "google_gemini",
            "model": model_name,
            "text": None,
            **_metrics(started_at=started_at),
        }

    try:
        import google.generativeai as genai
    except ImportError:
        return {
            "status": "skipped",
            "reason": "google-generativeai package is not installed",
            "provider": "google_gemini",
            "model": model_name,
            "text": None,
            **_metrics(started_at=started_at),
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 512,
            },
        )
        text = getattr(response, "text", None) or ""
        usage = _extract_usage_metadata(response)
        if usage["total_tokens"] == 0:
            usage = _estimate_tokens_from_text(prompt, text)
        return {
            "status": "generated",
            "provider": "google_gemini",
            "model": model_name,
            "text": text,
            **_metrics(
                started_at=started_at,
                prompt_tokens=usage["prompt_tokens"],
                completion_tokens=usage["completion_tokens"],
                total_tokens=usage["total_tokens"],
            ),
        }
    except Exception as exc:
        return {
            "status": "failed",
            "provider": "google_gemini",
            "model": model_name,
            "error": str(exc),
            "text": None,
            **_metrics(started_at=started_at),
        }
