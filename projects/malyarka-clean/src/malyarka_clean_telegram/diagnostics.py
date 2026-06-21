"""Diagnostics for the safe Telegram skeleton."""


def get_telegram_skeleton_diagnostics() -> dict:
    """Return static safety flags for the non-live Telegram skeleton."""
    return {
        "layer": "telegram_skeleton",
        "live_telegram": False,
        "polling": False,
        "token_required": False,
        "reads_env_file": False,
        "uses_old_bot_py": False,
        "sends_files": False,
        "creates_excel": False,
    }

