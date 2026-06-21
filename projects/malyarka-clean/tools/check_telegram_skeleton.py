"""Safe offline check for the Malyarka Clean Telegram skeleton."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from malyarka_clean_telegram import (  # noqa: E402
    build_telegram_order_reply,
    get_telegram_skeleton_diagnostics,
)


EXPECTED_DIAGNOSTICS = {
    "live_telegram": False,
    "polling": False,
    "token_required": False,
    "reads_env_file": False,
    "uses_old_bot_py": False,
    "sends_files": False,
    "creates_excel": False,
}

CHECK_CASES = [
    ("clean", "1000 400 2\n700 300"),
    ("has_disputes", "1000 400 2\n1000"),
    ("empty_or_invalid", "привет\nничего непонятно"),
]


def main() -> int:
    """Run the dry Telegram skeleton check and return a process exit code."""
    print("Безопасная проверка Telegram-каркаса Malyarka Clean")
    print("=" * 58)
    print("Это dry-check: без Telegram live, polling, token, .env, отправки сообщений и Excel.")
    print()

    diagnostics = get_telegram_skeleton_diagnostics()
    diagnostics_ok = _check_diagnostics(diagnostics)
    replies_ok = _check_replies()

    print()
    if diagnostics_ok and replies_ok:
        print("Итог: OK. Telegram-каркас импортируется и работает в безопасном dry-check режиме.")
        return 0

    print("Итог: FAIL. Найдены расхождения в безопасной проверке Telegram-каркаса.")
    return 1


def _check_diagnostics(diagnostics: dict) -> bool:
    print("Diagnostics:")
    ok = True
    for key, expected_value in EXPECTED_DIAGNOSTICS.items():
        actual_value = diagnostics.get(key)
        status = "OK" if actual_value is expected_value else "FAIL"
        print(f"- {key}: {str(actual_value).lower()} [{status}]")
        ok = ok and actual_value is expected_value
    return ok


def _check_replies() -> bool:
    print()
    print("Проверка adapter:")
    ok = True

    for expected_status, order_text in CHECK_CASES:
        reply = build_telegram_order_reply(order_text)
        found = f"Статус: {expected_status}" in reply
        status = "OK" if found else "FAIL"
        print(f"- {expected_status}: ответ содержит нужный статус [{status}]")
        ok = ok and found

    return ok


if __name__ == "__main__":
    raise SystemExit(main())
