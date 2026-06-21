"""Safe Telegram-facing text adapter for Malyarka Clean.

This package does not start Telegram, does not read tokens and does not read
.env files. It only formats replies from the existing Malyarka Clean core.
"""

from .adapter import build_telegram_order_reply
from .config_check import build_telegram_config_check_report
from .diagnostics import get_telegram_skeleton_diagnostics
from .readiness import build_pre_token_readiness_report

__all__ = [
    "build_telegram_order_reply",
    "build_telegram_config_check_report",
    "build_pre_token_readiness_report",
    "get_telegram_skeleton_diagnostics",
]
