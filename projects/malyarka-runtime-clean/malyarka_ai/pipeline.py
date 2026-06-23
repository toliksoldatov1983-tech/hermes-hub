"""Safe preparation pipeline for future DeepSeek order analysis."""

from __future__ import annotations

from typing import Any

from malyarka_ai.config import DeepSeekConfig
from malyarka_ai.prompts import build_deepseek_order_prompt


def prepare_deepseek_order_analysis(
    text: str | None,
    config: DeepSeekConfig | None = None,
) -> dict[str, Any]:
    """Prepare a DeepSeek request shape without reading keys or calling APIs."""

    runtime_config = DeepSeekConfig() if config is None else config
    safe_text = "" if text is None else text

    return {
        "status": "prepared",
        "provider": runtime_config.provider,
        "model": runtime_config.model,
        "real_ai_enabled": bool(runtime_config.real_ai_enabled),
        "external_api_called": False,
        "prompt": build_deepseek_order_prompt(safe_text),
        "input": {
            "kind": "none" if text is None else "text",
            "length": len(safe_text),
        },
    }
