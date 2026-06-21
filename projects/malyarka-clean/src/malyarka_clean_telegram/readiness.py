"""Safe pre-token Telegram readiness check for Malyarka Clean.

This module is a dry-run readiness layer. It never reads environment
variables, never reads .env files, never uses tokens and never starts
Telegram or polling.
"""


def build_pre_token_readiness_report() -> dict:
    """Return a static report for the safe pre-token readiness check."""
    return {
        "telegram_skeleton_ready": True,
        "adapter_ready": True,
        "safe_check_ready": True,
        "config_check_ready": True,
        "token_env_safety_plan_ready": True,
        "ready_for_token_stage": False,
        "requires_user_permission_for_token": True,
        "requires_user_permission_for_env": True,
        "live_telegram_allowed": False,
        "polling_allowed": False,
        "token_used": False,
        "env_read": False,
        "old_bot_py_used": False,
    }
