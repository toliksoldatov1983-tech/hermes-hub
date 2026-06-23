"""Provider-neutral Vision placeholder.

This file is kept for compatibility with the first Vision scaffold. It does
not import provider SDKs and never calls an external API.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from malyarka_vision.config import VisionConfig, check_vision_ready


def recognize_order_photo(
    photo_input: str | bytes | Path | None = None,
    *,
    config: VisionConfig | None = None,
    prompt: str | None = None,
) -> dict[str, Any]:
    """Return a safe placeholder until a confirmed provider is connected."""

    runtime_config = VisionConfig() if config is None else config
    readiness = check_vision_ready(runtime_config)
    described_input = _describe_photo_input(photo_input)

    if not runtime_config.real_recognition_enabled:
        return _safe_not_called_result(
            "disabled",
            "Real Gemini recognition is disabled.",
            described_input,
            readiness,
        )

    if not runtime_config.api_key:
        return _safe_not_called_result(
            "missing_api_key",
            f"{runtime_config.api_key_env_var} is not configured.",
            described_input,
            readiness,
        )

    return _safe_not_called_result(
        "provider_not_configured",
        "No external Vision provider is connected.",
        described_input,
        readiness,
    )


def recognize_order_photo_stub(
    photo_input: str | bytes | Path | None = None,
    *,
    config: VisionConfig | None = None,
) -> dict[str, Any]:
    """Return a structured placeholder for future photo order recognition."""

    readiness = check_vision_ready(config)
    return {
        "status": "not_connected",
        "message": "Photo recognition is not enabled yet.",
        "real_recognition_enabled": False,
        "external_api_called": False,
        "input": _describe_photo_input(photo_input),
        "readiness": readiness,
        "confirmed_items": [],
        "disputed_items": [],
        "raw_text": None,
    }


def _safe_not_called_result(
    status: str,
    message: str,
    described_input: dict[str, Any],
    readiness: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": status,
        "message": message,
        "real_recognition_enabled": False,
        "external_api_called": False,
        "input": described_input,
        "readiness": readiness,
        "confirmed_items": [],
        "disputed_items": [],
        "raw_text": None,
    }


def _describe_photo_input(photo_input: str | bytes | Path | None) -> dict[str, Any]:
    if photo_input is None:
        return {"kind": "none"}
    if isinstance(photo_input, bytes):
        return {"kind": "bytes", "byte_length": len(photo_input)}
    if isinstance(photo_input, Path):
        return {"kind": "path", "name": photo_input.name}
    return {"kind": "description", "value": str(photo_input)}
