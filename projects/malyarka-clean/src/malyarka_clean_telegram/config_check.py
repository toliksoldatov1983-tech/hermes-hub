"""Safe static Telegram configuration check for Malyarka Clean.

This module never reads environment variables, never reads .env files and
never starts Telegram. It only returns static safety diagnostics.
"""


def build_telegram_config_check_report() -> dict:
    """Return a static report proving the config check is safe to run."""
    return {
        "live_telegram": False,
        "polling": False,
        "token_required": False,
        "real_token_used": False,
        "reads_env_file": False,
        "uses_old_bot_py": False,
        "safe_to_run_without_token": True,
    }
