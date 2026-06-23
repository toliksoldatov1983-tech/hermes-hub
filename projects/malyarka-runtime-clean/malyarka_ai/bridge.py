"""Safe bridge between local order preview and prepared DeepSeek analysis."""

from __future__ import annotations

from typing import Any

from malyarka_ai.config import DeepSeekConfig
from malyarka_ai.pipeline import prepare_deepseek_order_analysis
from malyarka_core.adapters.telegram import build_order_preview_from_text


def prepare_order_analysis_with_fallback(
    text: str | None,
    config: DeepSeekConfig | None = None,
) -> dict[str, Any]:
    """Prepare AI analysis while keeping the local parser as the active path."""

    runtime_config = DeepSeekConfig() if config is None else config
    safe_text = "" if text is None else text

    local_preview = build_order_preview_from_text(safe_text)
    prepared_ai_analysis = prepare_deepseek_order_analysis(safe_text, runtime_config)

    return {
        "status": "fallback_local",
        "provider": runtime_config.provider,
        "model": runtime_config.model,
        "real_ai_enabled": False,
        "configured_real_ai_enabled": bool(runtime_config.real_ai_enabled),
        "external_api_called": False,
        "fallback_used": True,
        "fallback_reason": _get_fallback_reason(runtime_config),
        "local_preview": local_preview,
        "local_result": {
            "confirmed_items": local_preview["confirmed_items"],
            "disputed_items": local_preview["disputed_items"],
            "corel_lines": _build_confirmed_corel_lines(local_preview),
        },
        "prepared_ai_analysis": prepared_ai_analysis,
        "prepared_ai_prompt": prepared_ai_analysis["prompt"],
        "export_allowed": bool(local_preview["can_export"]),
        "disputed_rows": {
            "has_disputed": bool(local_preview["disputed_items"]),
            "count": local_preview["disputed_count"],
            "items": local_preview["disputed_items"],
            "blocks_export": bool(local_preview["disputed_items"]),
        },
    }


def _get_fallback_reason(config: DeepSeekConfig) -> str:
    if not config.real_ai_enabled:
        return "real_ai_enabled is false; local parser is the active safe path."
    if not config.api_key:
        return "DeepSeek API key is not configured; local parser is the active safe path."
    return "DeepSeek API is intentionally not connected in this safe stage."


def _build_confirmed_corel_lines(preview: dict[str, Any]) -> list[str]:
    return [
        f"{item['height']} {item['width']} {item['quantity']}"
        for item in preview["confirmed_items"]
    ]
