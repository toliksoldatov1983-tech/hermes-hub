"""Синтетические фикстуры для тестирования и сухих прогонов.

Все фикстуры на 100% синтетические — никаких реальных заказов,
клиентов или цен. Созданы вручную для безопасной локальной разработки.

Использование:
    from hermes_clean.fixtures import FIXTURES, get_fixture

    fixture = get_fixture("clean_single")
    row = {"height": 1000, "width": 400, "quantity": 2}
"""

from __future__ import annotations

from typing import Any

# ── Реестр фикстур ─────────────────────────────────────────────

FIXTURE_REGISTRY: dict[str, dict[str, Any]] = {
    # ── Чистые заказы ──
    "clean_single": {
        "id": "syn-clean-single",
        "label": "Одиночная чистая строка",
        "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}],
        "disputed_rows": [],
        "expected_status": "clean",
        "expected_area_m2": 0.8,
        "tags": ["clean", "minimal"],
    },
    "clean_multi": {
        "id": "syn-clean-multi",
        "label": "Несколько чистых строк",
        "confirmed_rows": [
            {"height": 1000, "width": 400, "quantity": 2},
            {"height": 700, "width": 300, "quantity": 1},
            {"height": 500, "width": 500, "quantity": 3},
        ],
        "disputed_rows": [],
        "expected_status": "clean",
        "expected_area_m2": 0.8 + 0.21 + 0.75,
        "tags": ["clean", "multi"],
    },
    "malyarka_reference_uch_002": {
        "id": "syn-malyarka-uch-002",
        "label": "Учебный многогрупповой заказ: фрезеровка + покраска",
        "order_type": "Фрезеровка + покраска",
        "confirmed_rows": [
            {"height": 720, "width": 496, "quantity": 2, "thickness": 16, "color": "H91", "routing": "модерн"},
            {"height": 920, "width": 446, "quantity": 3, "thickness": 16, "color": "H91", "routing": "модерн"},
            {"height": 700, "width": 397, "quantity": 4, "thickness": 18, "color": "1002Y50R", "routing": "выборка"},
            {"height": 860, "width": 297, "quantity": 2, "thickness": 18, "color": "1002Y50R", "routing": "выборка"},
            {"height": 600, "width": 246, "quantity": 5, "thickness": 16, "color": "1002Y50R", "routing": "расчёска"},
            {"height": 740, "width": 296, "quantity": 1, "thickness": 16, "color": "1002Y50R", "routing": "расчёска", "notes": "краска с 2х сторон"},
            {"height": 500, "width": 196, "quantity": 2, "thickness": 12, "color": "H91", "routing": "модерн"},
            {"height": 450, "width": 420, "quantity": 2, "thickness": 12, "color": "H91", "routing": "модерн"},
            {"height": 300, "width": 1100, "quantity": 1, "thickness": 19, "color": "S5010G50Y-20", "routing": "выборка"},
            {"height": 300, "width": 850, "quantity": 1, "thickness": 19, "color": "S5010G50Y-20", "routing": "выборка"},
        ],
        "disputed_rows": [],
        "expected_status": "clean",
        "expected_area_m2": 5.68368,
        "expected_calculation_area_m2": 5.90272,
        "expected_group_count": 5,
        "tags": ["clean", "multi", "malyarka_reference", "synthetic"],
    },
    "malyarka_reference_uch_003": {
        "id": "syn-malyarka-uch-003",
        "label": "Учебный многогрупповой заказ: только покраска",
        "order_type": "Покраска",
        "confirmed_rows": [
            {"height": 720, "width": 496, "quantity": 2, "thickness": 16, "color": "H91", "routing": "модерн"},
            {"height": 920, "width": 446, "quantity": 1, "thickness": 16, "color": "H91", "routing": "модерн"},
            {"height": 700, "width": 397, "quantity": 3, "thickness": 16, "color": "1002Y50R", "routing": "расчёска"},
            {"height": 860, "width": 297, "quantity": 2, "thickness": 16, "color": "1002Y50R", "routing": "расчёска", "notes": "краска с 2х сторон"},
            {"height": 500, "width": 600, "quantity": 2, "thickness": 18, "color": "S5010G50Y-20", "routing": "выборка"},
            {"height": 500, "width": 350, "quantity": 2, "thickness": 18, "color": "S5010G50Y-20", "routing": "выборка"},
            {"height": 450, "width": 300, "quantity": 4, "thickness": 12, "color": "H91", "routing": "модерн"},
            {"height": 300, "width": 1100, "quantity": 1, "thickness": 19, "color": "H91", "routing": "выборка"},
            {"height": 300, "width": 850, "quantity": 1, "thickness": 19, "color": "H91", "routing": "выборка"},
        ],
        "disputed_rows": [],
        "expected_status": "clean",
        "expected_area_m2": 4.54410,
        "expected_calculation_area_m2": 5.05494,
        "expected_group_count": 5,
        "tags": ["clean", "multi", "malyarka_reference", "synthetic"],
    },
    "clean_large": {
        "id": "syn-clean-large",
        "label": "Крупные размеры",
        "confirmed_rows": [
            {"height": 3000, "width": 2000, "quantity": 1},
            {"height": 5000, "width": 2500, "quantity": 2},
        ],
        "disputed_rows": [],
        "expected_status": "clean",
        "expected_area_m2": 6.0 + 25.0,
        "tags": ["clean", "large"],
    },
    "clean_zero_rows": {
        "id": "syn-clean-zero",
        "label": "Ни одной строки",
        "confirmed_rows": [],
        "disputed_rows": [],
        "expected_status": "empty_or_invalid",
        "expected_area_m2": 0,
        "tags": ["empty", "edge"],
    },

    # ── Заказы со спорами ──
    "dispute_missing_width": {
        "id": "syn-disp-width",
        "label": "Не хватает ширины",
        "confirmed_rows": [],
        "disputed_rows": [
            {"dispute_id": "dispute-1", "raw_text": "1000", "reason": "missing_width", "source_line": 1},
        ],
        "expected_status": "has_disputes",
        "expected_dispute_reasons": ["missing_width"],
        "tags": ["disputed", "single"],
    },
    "dispute_too_many_numbers": {
        "id": "syn-disp-numbers",
        "label": "Слишком много чисел",
        "confirmed_rows": [],
        "disputed_rows": [
            {"dispute_id": "dispute-1", "raw_text": "1000 400 2 5", "reason": "too_many_numbers", "source_line": 1},
        ],
        "expected_status": "has_disputes",
        "expected_dispute_reasons": ["too_many_numbers"],
        "tags": ["disputed", "format"],
    },
    "dispute_mixed": {
        "id": "syn-disp-mixed",
        "label": "Смешанный: часть чисто, часть спорно",
        "confirmed_rows": [
            {"height": 1000, "width": 400, "quantity": 2},
            {"height": 700, "width": 300, "quantity": 1},
        ],
        "disputed_rows": [
            {"dispute_id": "dispute-1", "raw_text": "мусор", "reason": "unparsed_order_text", "source_line": 3},
        ],
        "expected_status": "has_disputes",
        "expected_area_m2": 0.8 + 0.21,
        "expected_dispute_reasons": ["unparsed_order_text"],
        "tags": ["disputed", "mixed"],
    },
    "dispute_garbage": {
        "id": "syn-disp-garbage",
        "label": "Только мусор",
        "confirmed_rows": [],
        "disputed_rows": [
            {"dispute_id": "dispute-1", "raw_text": "привет", "reason": "unparsed_order_text", "source_line": 1},
            {"dispute_id": "dispute-2", "raw_text": "ничего непонятно", "reason": "unparsed_order_text", "source_line": 2},
        ],
        "expected_status": "empty_or_invalid",
        "expected_dispute_reasons": ["unparsed_order_text"],
        "tags": ["disputed", "garbage"],
    },

    # ── Граничные случаи ──
    "edge_negative": {
        "id": "syn-edge-neg",
        "label": "Отрицательное число (должен быть disputed)",
        "confirmed_rows": [],
        "disputed_rows": [
            {"dispute_id": "dispute-1", "raw_text": "-1000 400", "reason": "unparsed_order_text", "source_line": 1},
        ],
        "expected_status": "has_disputes",
        "tags": ["edge", "safety"],
    },
    "edge_zero_size": {
        "id": "syn-edge-zero",
        "label": "Нулевой размер",
        "confirmed_rows": [{"height": 0, "width": 400, "quantity": 1}],
        "disputed_rows": [],
        "expected_status": "clean",
        "expected_area_m2": 0,
        "tags": ["edge"],
    },
}


def get_fixture(name: str) -> dict[str, Any]:
    """Вернуть фикстуру по имени. Возбуждает KeyError если не найдена."""
    if name not in FIXTURE_REGISTRY:
        available = ", ".join(sorted(FIXTURE_REGISTRY))
        raise KeyError(f"Фикстура '{name}' не найдена. Доступные: {available}")
    return dict(FIXTURE_REGISTRY[name])


def list_fixtures(tag: str | None = None) -> list[str]:
    """Список имён фикстур, опционально отфильтрованных по тегу."""
    if tag is None:
        return sorted(FIXTURE_REGISTRY)
    return sorted(
        name for name, f in FIXTURE_REGISTRY.items()
        if tag in f.get("tags", [])
    )


FIXTURES = FIXTURE_REGISTRY  # сокращение
