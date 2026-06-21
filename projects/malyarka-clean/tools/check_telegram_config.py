"""Safe Telegram configuration check for Malyarka Clean."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from malyarka_clean_telegram.config_check import (  # noqa: E402
    build_telegram_config_check_report,
)


EXPECTED_REPORT = {
    "live_telegram": False,
    "polling": False,
    "token_required": False,
    "real_token_used": False,
    "reads_env_file": False,
    "uses_old_bot_py": False,
    "safe_to_run_without_token": True,
}


def main() -> int:
    """Run the safe config check and return a process exit code."""
    print("Безопасная Telegram config-check проверка Malyarka Clean")
    print("=" * 64)
    print("Это не live Telegram: без polling, token, .env, окружения и отправки сообщений.")
    print()

    report = build_telegram_config_check_report()
    ok = True

    print("Diagnostics:")
    for key, expected_value in EXPECTED_REPORT.items():
        actual_value = report.get(key)
        status = "OK" if actual_value is expected_value else "FAIL"
        print(f"- {key}: {str(actual_value).lower()} [{status}]")
        ok = ok and actual_value is expected_value

    print()
    if ok:
        print("Итог: OK. Config-check безопасен и запускается без Telegram token и без .env.")
        return 0

    print("Итог: FAIL. Config-check вернул небезопасные diagnostics.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
