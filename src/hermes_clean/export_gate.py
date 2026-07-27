"""Политика обработки источников экспорта (Export Source Policy).

Определяет, можно ли экспортировать заказ в Corel-формат.
Блокирует экспорт если есть:
- спорные строки (disputed_rows)
- статус empty_or_invalid
- ручная блокировка export_blocked=True

strict=True превращает блокировку в исключение ExportBlockedError.
"""

from __future__ import annotations


class ExportBlockedError(ValueError):
    """Возбуждается когда экспорт заблокирован гейтом безопасности."""

    def __init__(self, reason: str, source_status: str):
        super().__init__(f"Экспорт заблокирован: {reason} (статус: {source_status})")
        self.reason = reason
        self.source_status = source_status


def build_export_model(order_result: dict, *, strict: bool = False) -> dict:
    """Построить модель экспорта из результата заказа.

    Args:
        order_result: Словарь с ключами status, disputed_rows, confirmed_rows и др.
        strict: Если True, возбуждает ExportBlockedError вместо возврата blocked dict.

    Returns:
        Словарь с export_rows, export_blocked, reason, source_status.

    Raises:
        ExportBlockedError: Когда strict=True и экспорт заблокирован.
    """
    status = order_result.get("status")
    disputed_rows = order_result.get("disputed_rows", [])

    if status == "empty_or_invalid":
        return _block_or_raise(status, "empty_or_invalid", strict)
    if disputed_rows:
        return _block_or_raise(status, "disputed_rows_present", strict)
    if order_result.get("export_blocked"):
        return _block_or_raise(status, "export_blocked", strict)
    if status != "clean":
        return _block_or_raise(status, "source_not_clean", strict)

    return {
        "export_rows": [_export_row(row) for row in order_result.get("confirmed_rows", [])],
        "export_blocked": False,
        "reason": "ready",
        "source_status": status,
    }


def _export_row(row: dict) -> dict:
    return {
        "height_mm": row.get("height_mm", row.get("height")),
        "width_mm": row.get("width_mm", row.get("width")),
        "quantity": row.get("quantity", 1),
    }


def _block_or_raise(status: str, reason: str, strict: bool) -> dict:
    if strict:
        raise ExportBlockedError(reason, status)
    return _blocked(status, reason)


def _blocked(status: str, reason: str) -> dict:
    return {
        "export_rows": [],
        "export_blocked": True,
        "reason": reason,
        "source_status": status,
    }
