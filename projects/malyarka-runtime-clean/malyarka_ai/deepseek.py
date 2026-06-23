"""Safe DeepSeek placeholder.

This module defines diagnostics and a disabled text-analysis result for the
first AI layer. It never imports a provider SDK and never calls an external API.
"""

from __future__ import annotations

from typing import Any

from malyarka_ai.config import DeepSeekConfig
from malyarka_ai.pipeline import prepare_deepseek_order_analysis


def check_deepseek_ready(config: DeepSeekConfig | None = None) -> dict[str, Any]:
    """Return safe DeepSeek readiness diagnostics without exposing secrets."""

    runtime_config = DeepSeekConfig() if config is None else config
    has_api_key = bool(runtime_config.api_key)
    real_enabled = bool(runtime_config.real_ai_enabled)

    if not real_enabled:
        reason = "Real DeepSeek AI is disabled in this safe stage."
    elif not has_api_key:
        reason = f"{runtime_config.api_key_env_var} is not configured for this process."
    else:
        reason = "DeepSeek config is present, but external API calls are disabled here."

    return {
        "provider": runtime_config.provider,
        "has_api_key": has_api_key,
        "real_ai_enabled": real_enabled,
        "base_url": runtime_config.base_url,
        "model": runtime_config.model,
        "reason": reason,
    }


def analyze_order_text_with_deepseek(
    text: str | None,
    config: DeepSeekConfig | None = None,
) -> dict[str, Any]:
    """Return a safe disabled result until real DeepSeek calls are approved."""

    runtime_config = DeepSeekConfig() if config is None else config
    readiness = check_deepseek_ready(runtime_config)
    prepared = prepare_deepseek_order_analysis(text, runtime_config)

    if not runtime_config.real_ai_enabled:
        return _safe_not_called_result(
            status="disabled",
            message="Real DeepSeek AI is disabled.",
            text=text,
            readiness=readiness,
            prepared=prepared,
        )

    if not runtime_config.api_key:
        return _safe_not_called_result(
            status="missing_api_key",
            message=f"{runtime_config.api_key_env_var} is not configured.",
            text=text,
            readiness=readiness,
            prepared=prepared,
        )

    return _safe_not_called_result(
        status="provider_not_connected",
        message="DeepSeek API is not connected in this safe stage.",
        text=text,
        readiness=readiness,
        prepared=prepared,
    )


def _safe_not_called_result(
    *,
    status: str,
    message: str,
    text: str | None,
    readiness: dict[str, Any],
    prepared: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": status,
        "message": message,
        "external_api_called": False,
        "provider": prepared["provider"],
        "model": prepared["model"],
        "real_ai_enabled": prepared["real_ai_enabled"],
        "input": _describe_text_input(text),
        "readiness": readiness,
        "prepared": prepared,
        "confirmed_items": [],
        "disputed_items": [],
        "raw_response": None,
    }


def _describe_text_input(text: str | None) -> dict[str, Any]:
    if text is None:
        return {"kind": "none", "length": 0}
    return {"kind": "text", "length": len(text)}
