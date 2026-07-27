"""Dispute resolver — разрешение спорных строк заказа.

Содержит:
- Шаблоны уточняющих вопросов для диспутов (_SUGGESTED_QUESTIONS)
- Контрактный Resolver с правилами разрешения
- Типы данных DisputeResolution и ResolverSummary

Без Telegram, API, БД и секретов. Только чистая логика.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Шаблоны уточняющих вопросов ────────────────────────────────

SUGGESTED_QUESTIONS: dict[str, str] = {
    "missing_width": "Уточнить ширину строки.",
    "missing_height": "Уточнить высоту строки.",
    "too_many_numbers": "Уточнить, какие числа являются высотой, шириной и количеством.",
    "unclear_quantity": "Уточнить количество.",
    "unparsed_order_text": "Уточнить, влияет ли текст на заказ.",
    "empty_or_garbage": "Проверить строку или удалить ее.",
    "unsupported_format": "Уточнить размер в формате высота ширина количество.",
    "unrecognized_digit": "Не удалось распознать цифру. Уточнить размеры.",
}

DISPUTE_ACTIONS = {
    "accept": "Принять строку с указанными высотой, шириной и количеством.",
    "split": "Разделить строку на несколько подтверждённых строк.",
    "delete": "Удалить спорную строку.",
    "clarify": "Запросить уточнение у пользователя.",
}


# ── Типы данных ──

@dataclass(frozen=True)
class DisputeResolution:
    """Результат разрешения одной спорной строки."""

    dispute_id: str
    resolved: bool
    action: str  # accept / split / delete / clarify
    confirmed_row: dict[str, Any] | None = None
    new_disputes: list[dict[str, Any]] = field(default_factory=list)
    note: str = ""


@dataclass(frozen=True)
class ResolverSummary:
    """Сводка после разрешения всех споров в заказе."""

    total_disputes: int
    resolved: int
    unresolved: int
    new_confirmed_rows: list[dict[str, Any]]
    remaining_disputes: list[dict[str, Any]]
    is_fully_resolved: bool
    export_unblocked: bool


def get_suggested_question(reason: str) -> str:
    """Получить шаблон уточняющего вопроса по причине спора."""
    return SUGGESTED_QUESTIONS.get(reason, "Уточнить строку.")


# ── Resolver ──

class DisputeResolver:
    """Контрактный resolver для спорных строк заказа.

    Правила:
      1. Результат разрешения должен содержать валидные строки.
      2. Resolver не читает .env, токены или внешние API.
      3. Resolver не изменяет исходный источник заказа.
      4. Каждое разрешение возвращает DisputeResolution.
    """

    def __init__(self, max_resolution_attempts: int = 3):
        self._max_attempts = max_resolution_attempts
        self._attempts: dict[str, int] = {}

    def resolve(
        self,
        disputed_row: dict[str, Any],
        resolution_data: dict[str, Any],
    ) -> DisputeResolution:
        """Разрешить одну спорную строку.

        resolution_data должен содержать:
          - action: 'accept', 'split', 'delete' или 'clarify'
          - Для 'accept': height, width, quantity
          - Для 'split': rows (список {height, width, quantity})
          - Для 'delete': без доп. полей
          - Для 'clarify': question (что спросить)
        """
        dispute_id = disputed_row.get("dispute_id", "?")
        self._attempts.setdefault(dispute_id, 0)
        self._attempts[dispute_id] += 1

        if self._attempts[dispute_id] > self._max_attempts:
            return DisputeResolution(
                dispute_id=dispute_id,
                resolved=False,
                action="clarify",
                note=f"Исчерпаны попытки разрешения ({self._max_attempts}). Требуется ручное решение.",
            )

        action = resolution_data.get("action", "clarify")

        if action == "accept":
            return self._resolve_accept(dispute_id, resolution_data)
        elif action == "split":
            return self._resolve_split(dispute_id, resolution_data)
        elif action == "delete":
            return self._resolve_delete(dispute_id)
        else:
            return self._resolve_clarify(dispute_id, resolution_data, disputed_row)

    def resolve_all(
        self,
        disputed_rows: list[dict[str, Any]],
        resolutions: dict[str, dict[str, Any]],
    ) -> ResolverSummary:
        """Разрешить все спорные строки через карту разрешений.

        resolutions: {dispute_id: resolution_data}
        """
        confirmed: list[dict[str, Any]] = []
        remaining: list[dict[str, Any]] = []
        resolved_count = 0

        for row in disputed_rows:
            dispute_id = row.get("dispute_id", f"dispute-{hash(str(row))}")
            if dispute_id in resolutions:
                outcome = self.resolve(row, resolutions[dispute_id])
                if outcome.resolved:
                    resolved_count += 1
                    if outcome.confirmed_row:
                        confirmed.append(outcome.confirmed_row)
                else:
                    remaining.append(row)
                    if outcome.new_disputes:
                        remaining.extend(outcome.new_disputes)
            else:
                remaining.append(row)

        is_fully_resolved = len(remaining) == 0
        export_unblocked = is_fully_resolved and len(confirmed) > 0

        return ResolverSummary(
            total_disputes=len(disputed_rows),
            resolved=resolved_count,
            unresolved=len(remaining),
            new_confirmed_rows=confirmed,
            remaining_disputes=remaining,
            is_fully_resolved=is_fully_resolved,
            export_unblocked=export_unblocked,
        )

    # ── Стратегии разрешения ──

    def _resolve_accept(
        self, dispute_id: str, data: dict[str, Any]
    ) -> DisputeResolution:
        height = data.get("height")
        width = data.get("width")
        quantity = data.get("quantity", 1)

        if height is None or width is None:
            return DisputeResolution(
                dispute_id=dispute_id,
                resolved=False,
                action="clarify",
                note="Для 'accept' нужны height и width.",
            )

        return DisputeResolution(
            dispute_id=dispute_id,
            resolved=True,
            action="accept",
            confirmed_row={
                "row_id": f"resolved-{dispute_id}",
                "height": int(height),
                "width": int(width),
                "quantity": int(quantity),
                "unit": "mm",
                "notes": [f"Разрешено: accept из dispute {dispute_id}"],
            },
        )

    def _resolve_split(
        self, dispute_id: str, data: dict[str, Any]
    ) -> DisputeResolution:
        rows = data.get("rows", [])
        if not rows:
            return DisputeResolution(
                dispute_id=dispute_id,
                resolved=False,
                action="clarify",
                note="Для 'split' нужен список 'rows'.",
            )

        first = rows[0]
        confirmed = {
            "row_id": f"resolved-{dispute_id}",
            "height": int(first.get("height", 0)),
            "width": int(first.get("width", 0)),
            "quantity": int(first.get("quantity", 1)),
            "unit": "mm",
            "notes": [f"Разрешено: split из dispute {dispute_id}"],
        }
        new_disputes = []
        for i, row in enumerate(rows[1:], start=1):
            new_disputes.append({
                "dispute_id": f"split-{dispute_id}-{i}",
                "raw_text": f"{row.get('height', '?')} {row.get('width', '?')}",
                "reason": "split_remainder",
                "note": f"Остаток от split dispute {dispute_id}",
            })

        return DisputeResolution(
            dispute_id=dispute_id,
            resolved=len(new_disputes) == 0,
            action="split",
            confirmed_row=confirmed,
            new_disputes=new_disputes,
        )

    def _resolve_delete(self, dispute_id: str) -> DisputeResolution:
        return DisputeResolution(
            dispute_id=dispute_id,
            resolved=True,
            action="delete",
            note=f"Спорная строка {dispute_id} удалена.",
        )

    def _resolve_clarify(
        self,
        dispute_id: str,
        data: dict[str, Any],
        disputed_row: dict[str, Any],
    ) -> DisputeResolution:
        question = data.get(
            "question",
            get_suggested_question(disputed_row.get("reason", "")),
        )
        return DisputeResolution(
            dispute_id=dispute_id,
            resolved=False,
            action="clarify",
            note=question,
        )
