"""Safe first AI layer for Malyarka."""

from malyarka_ai.config import (
    DEFAULT_AI_PROVIDER,
    DEFAULT_DEEPSEEK_API_KEY_ENV_VAR,
    DEFAULT_DEEPSEEK_BASE_URL,
    DEFAULT_DEEPSEEK_MODEL,
    DeepSeekConfig,
)
from malyarka_ai.deepseek import (
    analyze_order_text_with_deepseek,
    check_deepseek_ready,
)
from malyarka_ai.contracts import (
    ALLOWED_DEEPSEEK_ITEM_TYPES,
    DEEPSEEK_ORDER_RESPONSE_CONTRACT,
    parse_deepseek_json_response,
    validate_deepseek_order_response,
)
from malyarka_ai.bridge import prepare_order_analysis_with_fallback
from malyarka_ai.pipeline import prepare_deepseek_order_analysis
from malyarka_ai.prompts import build_deepseek_order_prompt

__all__ = [
    "ALLOWED_DEEPSEEK_ITEM_TYPES",
    "DEFAULT_AI_PROVIDER",
    "DEFAULT_DEEPSEEK_API_KEY_ENV_VAR",
    "DEFAULT_DEEPSEEK_BASE_URL",
    "DEFAULT_DEEPSEEK_MODEL",
    "DEEPSEEK_ORDER_RESPONSE_CONTRACT",
    "DeepSeekConfig",
    "analyze_order_text_with_deepseek",
    "build_deepseek_order_prompt",
    "check_deepseek_ready",
    "parse_deepseek_json_response",
    "prepare_deepseek_order_analysis",
    "prepare_order_analysis_with_fallback",
    "validate_deepseek_order_response",
]
