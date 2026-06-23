"""Safety checks for read-only Hermes commands."""

import re

DANGEROUS_RESPONSE = "Это действие требует отдельного подтверждения пользователя."

_DANGEROUS_SUBSTRINGS = (
    ".env",
    "token",
    "токен",
    "orders.db",
    "git add .",
    "commit",
    "push",
    "bot.py",
    "vision",
    "фото",
    "удалить",
    "переименовать",
    "переместить",
    "delete",
    "remove",
    "chmod",
    "os.remove",
    "shutil",
    "hermes_bot.py",
)

_DANGEROUS_TOKEN_PATTERN = re.compile(r"(?<![\w.])(?:mv|cp)(?![\w.])", re.IGNORECASE)


def is_dangerous_text(text: str) -> bool:
    lowered = text.lower()
    if any(item in lowered for item in _DANGEROUS_SUBSTRINGS):
        return True
    return bool(_DANGEROUS_TOKEN_PATTERN.search(text))


def dangerous_response() -> str:
    return DANGEROUS_RESPONSE
