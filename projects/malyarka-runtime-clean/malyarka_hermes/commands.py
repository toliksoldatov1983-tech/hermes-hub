"""Command text helpers for the read-only Hermes Router."""

HELP_TEXT = "\n".join(
    [
        "Доступные команды:",
        "- !статус",
        "- !следующий шаг",
        "- !помощь",
    ]
)


def normalize_command(text: str) -> str:
    return " ".join(text.strip().split()).lower()
