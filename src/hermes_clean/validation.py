"""Validation layer — чистая логика валидации строк заказа.

Проверки (все локальные, без API/БД/секретов):
- диапазоны размеров (1 <= h,w <= 20000 мм)
- неотрицательные значения
- разумная площадь (<= 200 м² на строку)
- обнаружение дубликатов
- пустые/невалидные поля

Возвращает отчёт о валидации для дальнейшей обработки.
"""

from __future__ import annotations

from typing import Any

# ── Безопасные диапазоны ──────────────────────────────────────
MIN_SIZE_MM = 1
MAX_SIZE_MM = 20_000
MAX_AREA_M2_PER_ROW = 200.0


def validate_order_result(order_result: dict[str, Any]) -> dict[str, Any]:
    """Запустить все проверки на существующем результате заказа.

    Возвращает словарь с:
      - valid: bool (True если нет нарушений)
      - violations: list словарей с описанием нарушений
      - summary: человекочитаемая сводка на русском
      - blocked: bool (True = экспорт должен быть заблокирован)
    """
    violations: list[dict[str, Any]] = []

    _check_confirmed_rows(order_result.get("confirmed_rows", []), violations)
    _check_disputed_rows(order_result.get("disputed_rows", []), violations)
    _check_duplicate_rows(order_result.get("confirmed_rows", []), violations)
    _check_total_area(order_result.get("total_area_m2", 0), violations)

    valid = len(violations) == 0
    blocked = len(violations) > 0

    return {
        "valid": valid,
        "violations": violations,
        "blocked": blocked,
        "block_reason": _summarize(violations),
        "summary": _build_summary(violations),
    }


def validate_single_row(row: dict[str, Any]) -> dict[str, Any]:
    """Проверить одну строку (например, перед добавлением в confirmed)."""
    violations: list[dict[str, Any]] = []
    height = row.get("height", row.get("height_mm"))
    width = row.get("width", row.get("width_mm"))
    quantity = row.get("quantity", 1)

    if not isinstance(height, (int, float)) or height < MIN_SIZE_MM or height > MAX_SIZE_MM:
        violations.append({
            "field": "height",
            "value": height,
            "reason": "out_of_range",
            "message": f"Высота {height} вне допустимого диапазона ({MIN_SIZE_MM}-{MAX_SIZE_MM} мм).",
        })

    if not isinstance(width, (int, float)) or width < MIN_SIZE_MM or width > MAX_SIZE_MM:
        violations.append({
            "field": "width",
            "value": width,
            "reason": "out_of_range",
            "message": f"Ширина {width} вне допустимого диапазона ({MIN_SIZE_MM}-{MAX_SIZE_MM} мм).",
        })

    if not isinstance(quantity, (int,)) or quantity < 1:
        violations.append({
            "field": "quantity",
            "value": quantity,
            "reason": "invalid_quantity",
            "message": f"Количество {quantity} должно быть целым положительным числом.",
        })

    if isinstance(height, (int, float)) and isinstance(width, (int, float)):
        area_m2 = height * width * max(1, int(quantity if isinstance(quantity, (int,)) else 1)) / 1_000_000
        if area_m2 > MAX_AREA_M2_PER_ROW:
            violations.append({
                "field": "area",
                "value": area_m2,
                "reason": "area_too_large",
                "message": f"Площадь строки {area_m2:.6g} м² превышает лимит {MAX_AREA_M2_PER_ROW} м².",
            })

    return {
        "valid": len(violations) == 0,
        "violations": violations,
    }


# ── Внутренние helpers ────────────────────────────────────────

def _check_confirmed_rows(rows: list[dict[str, Any]], violations: list) -> None:
    for row in rows:
        result = validate_single_row(row)
        if not result["valid"]:
            for v in result["violations"]:
                violations.append({
                    "row_id": row.get("row_id", "?"),
                    "source_line": row.get("source_line", "?"),
                    **v,
                })


def _check_disputed_rows(disputed: list[dict[str, Any]], violations: list) -> None:
    for row in disputed:
        reason = row.get("reason", "")
        if reason in ("empty_or_garbage", "unparsed_order_text"):
            violations.append({
                "row_id": row.get("dispute_id", "?"),
                "source_line": row.get("source_line", "?"),
                "field": "raw_text",
                "value": row.get("raw_text", ""),
                "reason": reason,
                "message": f"Строка {row.get('source_line', '?')} не может быть разобрана: {row.get('raw_text', '')}",
            })


def _check_duplicate_rows(rows: list[dict[str, Any]], violations: list) -> None:
    seen: set[tuple] = set()
    for row in rows:
        key = (
            row.get("height", row.get("height_mm", 0)),
            row.get("width", row.get("width_mm", 0)),
            row.get("quantity", 0),
        )
        if key in seen:
            violations.append({
                "row_id": row.get("row_id", "?"),
                "source_line": row.get("source_line", "?"),
                "field": "duplicate",
                "value": key,
                "reason": "duplicate_row",
                "message": f"Строка {row.get('source_line', '?')} дублирует другую подтверждённую строку: {key}.",
            })
        seen.add(key)


def _check_total_area(total_area_m2: float, violations: list) -> None:
    if total_area_m2 < 0:
        violations.append({
            "field": "total_area",
            "value": total_area_m2,
            "reason": "negative_area",
            "message": f"Общая площадь {total_area_m2} м² отрицательная.",
        })


def _build_summary(violations: list) -> str:
    if not violations:
        return "Проверка пройдена. Нарушений нет."
    count = len(violations)
    reasons = {v.get("reason", "?") for v in violations}
    return f"Найдено {count} нарушений: {', '.join(sorted(reasons))}."


def _summarize(violations: list) -> str | None:
    if not violations:
        return None
    return "validation_failed"
