"""Tests для Preview Report Generator Hermes-Clean.

Проверяет:
- Базовую генерацию отчёта (все 6 блоков)
- Чистый заказ (clean) → без нарушений, pricing, export ready
- Заказ со спорами → блоки, disputed, export blocked
- Пустой заказ → empty_or_invalid
- Интеграцию с OrderStateMachine
- Markdown-формат
- Next safe action для всех состояний
"""

import pytest

from hermes_clean import (
    OrderState,
    OrderStateMachine,
    PreviewReport,
    generate_preview,
    preview_to_markdown,
    validate_order_result,
)


# ── Вспомогательные фабрики ────────────────────────────────────

def _clean_order() -> dict:
    return {
        "status": "clean",
        "confirmed_rows": [
            {"row_id": "row-1", "height": 1000, "width": 400, "quantity": 2},
            {"row_id": "row-2", "height": 700, "width": 300, "quantity": 1},
        ],
        "disputed_rows": [],
        "total_area_m2": 1.01,
    }


def _disputed_order() -> dict:
    return {
        "status": "has_disputes",
        "confirmed_rows": [{"row_id": "row-1", "height": 1000, "width": 400, "quantity": 1}],
        "disputed_rows": [
            {"dispute_id": "d1", "source_line": 2, "raw_text": "мусор",
             "reason": "unparsed_order_text", "suggested_question": "Уточнить строку."},
            {"dispute_id": "d2", "source_line": 3, "raw_text": "1000",
             "reason": "missing_width", "suggested_question": "Уточнить ширину строки."},
        ],
        "total_area_m2": 0.4,
    }


def _empty_order() -> dict:
    return {"status": "empty_or_invalid", "confirmed_rows": [], "disputed_rows": [], "total_area_m2": 0}


# ── 1. Базовая генерация: clean ──

def test_preview_clean_has_all_blocks():
    report = generate_preview(_clean_order())
    assert isinstance(report, PreviewReport)
    # Блок 1
    assert report.confirmed_total == 2
    assert len(report.confirmed_rows_preview) == 2
    assert report.confirmed_area_m2 == 1.01
    # Блок 2
    assert report.disputed_total == 0
    assert report.disputed_rows_preview == []
    # Блок 3
    assert report.validation_valid is True
    assert report.validation_violations_count == 0
    # Блок 4
    assert report.pricing_total_revenue > 0
    assert report.pricing_total_cost > 0
    assert len(report.pricing_rows) == 2
    # Блок 5
    assert report.export_blocked is False
    assert "не заблокирован" in report.export_block_reasons[0]
    # Блок 6
    assert report.next_safe_action


def test_preview_clean_export_ready():
    sm = OrderStateMachine()
    sm.transition_to_parsed(confirmed_count=2)
    sm.transition_to_validated(validation_result={"valid": True, "violations": []})
    sm.transition_to_preview()
    sm.transition_to_export_ready()

    report = generate_preview(_clean_order(), state_machine=sm)
    assert report.export_ready is True
    assert report.current_state == "READY_FOR_FUTURE_EXPORT"
    assert "готов к экспорту" in report.next_safe_action


def test_preview_clean_summary():
    report = generate_preview(_clean_order())
    assert "2 подтверждено" in report.summary
    assert "руб" in report.summary


# ── 2. Заказ со спорами ──

def test_preview_disputed_blocks():
    report = generate_preview(_disputed_order())
    # Блок 1
    assert report.confirmed_total == 1
    # Блок 2
    assert report.disputed_total == 2
    assert len(report.disputed_rows_preview) == 2
    assert report.disputed_rows_preview[0]["reason"] == "unparsed_order_text"
    assert report.disputed_rows_preview[1]["reason"] == "missing_width"
    # Блок 3
    assert report.validation_valid is False
    assert report.validation_violations_count >= 1
    # Блок 5
    assert report.export_blocked is True
    assert any("спорн" in r for r in report.export_block_reasons)
    assert any("Нарушения валидации" in r for r in report.export_block_reasons)


def test_preview_disputed_with_state_machine():
    sm = OrderStateMachine()
    sm.transition_to_parsed(confirmed_count=1, disputed_count=2)
    sm.transition_to_disputed(dispute_count=2, dispute_reasons=["unparsed_order_text", "missing_width"])
    sm.transition_to_export_blocked()

    report = generate_preview(_disputed_order(), state_machine=sm)
    assert report.current_state == "EXPORT_BLOCKED"
    assert report.current_state_label == "Экспорт заблокирован"
    assert report.export_blocked is True
    assert "DisputeResolver" in report.next_safe_action or "споры" in report.next_safe_action


def test_preview_disputed_summary():
    report = generate_preview(_disputed_order())
    assert "1 подтверждено" in report.summary
    assert "2 спорно" in report.summary
    assert "экспорт заблокирован" in report.summary


# ── 3. Пустой заказ ──

def test_preview_empty():
    report = generate_preview(_empty_order())
    assert report.confirmed_total == 0
    assert report.disputed_total == 0
    assert report.confirmed_rows_preview == []
    assert report.validation_valid is True
    assert report.export_blocked is True
    assert any("empty_or_invalid" in r for r in report.export_block_reasons)
    assert report.pricing_total_revenue == 0
    assert report.pricing_total_cost == 0


# ── 4. Synthetic pricing ──

def test_pricing_single_row():
    report = generate_preview({
        "status": "clean",
        "confirmed_rows": [{"row_id": "row-1", "height": 1000, "width": 1000, "quantity": 1}],
        "disputed_rows": [],
        "total_area_m2": 1.0,
    })
    assert len(report.pricing_rows) == 1
    # 1 m² * 150 руб = 150 руб
    assert report.pricing_total_revenue == 150.0
    assert report.pricing_total_cost == 80.0
    # margin = (150-80)/150 * 100 = 46.7%
    assert report.pricing_avg_margin_pct == 46.7


def test_pricing_multi_row():
    report = generate_preview({
        "status": "clean",
        "confirmed_rows": [
            {"height": 1000, "width": 400, "quantity": 2},   # 0.8 m² → 120 руб
            {"height": 500, "width": 500, "quantity": 1},     # 0.25 m² → 37.5 руб
        ],
        "disputed_rows": [],
        "total_area_m2": 1.05,
    })
    # revenue: 0.8*150 + 0.25*150 = 120 + 37.5 = 157.5
    assert report.pricing_total_revenue == 157.5
    # cost: 0.8*80 + 0.25*80 = 64 + 20 = 84
    assert report.pricing_total_cost == 84.0


def test_pricing_zero_rows():
    report = generate_preview(_empty_order())
    assert report.pricing_rows == []
    assert report.pricing_total_revenue == 0
    assert report.pricing_avg_margin_pct == 0.0
    assert report.pricing_is_profitable is False


def test_pricing_profitability_flag():
    report1 = generate_preview({
        "status": "clean",
        "confirmed_rows": [{"height": 1000, "width": 1000, "quantity": 10}],
        "disputed_rows": [],
        "total_area_m2": 10.0,
    })
    # margin 46.7% > 30% → profitable
    assert report1.pricing_is_profitable is True

    # Low-margin order (via thin margin percent threshold crossing)
    # Actually any standard rate always gives 46.7%, so test a near-zero-area case
    report2 = generate_preview({
        "status": "clean",
        "confirmed_rows": [{"height": 1, "width": 1, "quantity": 1}],
        "disputed_rows": [],
        "total_area_m2": 0.000001,
    })
    # 1*1*1/1e6 = 1e-6 m² → revenue=0.0 (rounded from 0.00015)
    # margin = 0.0, so not profitable
    assert report2.pricing_is_profitable is False


def test_pricing_large_order_is_profitable():
    report = generate_preview({
        "status": "clean",
        "confirmed_rows": [{"height": 500, "width": 500, "quantity": 3}],
        "disputed_rows": [],
        "total_area_m2": 0.75,
    })
    assert report.pricing_total_revenue > 0
    assert report.pricing_is_profitable is True


# ── 5. Export block reasons ──

def test_export_block_reasons_clean():
    report = generate_preview(_clean_order())
    assert report.export_blocked is False
    assert len(report.export_block_reasons) == 1
    assert "не заблокирован" in report.export_block_reasons[0]


def test_export_block_reasons_disputed():
    report = generate_preview(_disputed_order())
    assert report.export_blocked is True
    assert len(report.export_block_reasons) >= 2


def test_export_block_reasons_manual_block():
    order = _clean_order()
    order["export_blocked"] = True
    report = generate_preview(order)
    assert report.export_blocked is True
    assert any("Ручная блокировка" in r for r in report.export_block_reasons)


# ── 6. Next safe action — все состояния ──

def test_next_action_raw_input():
    sm = OrderStateMachine()
    report = generate_preview(_empty_order(), state_machine=sm)
    assert "разобрать" in report.next_safe_action.lower()


def test_next_action_parsed():
    sm = OrderStateMachine(OrderState.PARSED)
    report = generate_preview(_empty_order(), state_machine=sm)
    assert "валидаци" in report.next_safe_action.lower()


def test_next_action_validated_clean():
    sm = OrderStateMachine(OrderState.VALIDATED)
    report = generate_preview(_clean_order(), state_machine=sm)
    assert "PREVIEW" in report.next_safe_action or "preview" in report.next_safe_action.lower()


def test_next_action_validated_with_disputes():
    sm = OrderStateMachine(OrderState.VALIDATED)
    report = generate_preview(_disputed_order(), state_machine=sm)
    assert "спорн" in report.next_safe_action


def test_next_action_has_disputes():
    sm = OrderStateMachine(OrderState.HAS_DISPUTES)
    report = generate_preview(_disputed_order(), state_machine=sm)
    assert "диспут-резолвера" in report.next_safe_action or "DisputeResolver" in report.next_safe_action


def test_next_action_export_blocked():
    sm = OrderStateMachine(OrderState.EXPORT_BLOCKED)
    report = generate_preview(_disputed_order(), state_machine=sm)
    assert "заблокирован" in report.next_safe_action or "разрешите" in report.next_safe_action.lower()


def test_next_action_preview_ready():
    sm = OrderStateMachine(OrderState.READY_FOR_PREVIEW)
    report = generate_preview(_clean_order(), state_machine=sm)
    assert "export_ready" in report.next_safe_action or "одобрения" in report.next_safe_action


def test_next_action_export_ready():
    sm = OrderStateMachine(OrderState.READY_FOR_FUTURE_EXPORT)
    report = generate_preview(_clean_order(), state_machine=sm)
    assert "экспорт" in report.next_safe_action.lower()


# ── 7. Markdown format ──

def test_markdown_contains_all_sections():
    report = generate_preview(_disputed_order())
    md = preview_to_markdown(report)
    assert "# Preview Report" in md
    assert "## Подтверждённые строки" in md
    assert "## Спорные строки" in md
    assert "## Валидация" in md
    assert "## Стоимость (синтетическая)" in md
    assert "## Экспорт" in md
    assert "## Рекомендация" in md


def test_markdown_contains_state():
    report = generate_preview(_clean_order())
    md = preview_to_markdown(report)
    assert "Состояние:" in md


def test_markdown_contains_next_action():
    report = generate_preview(_clean_order())
    md = preview_to_markdown(report)
    assert ">" in md  # blockquote for recommendation


def test_markdown_contains_summary():
    report = generate_preview(_clean_order())
    md = preview_to_markdown(report)
    assert "*" in md and "руб" in md  # italic summary


# ── 8. PreviewReport dataclass ──

def test_preview_report_fields():
    report = generate_preview(_clean_order())
    assert isinstance(report, PreviewReport)
    assert report.confirmed_total is not None
    assert report.disputed_total is not None
    assert report.validation_valid is not None
    assert report.validation_violations is not None
    assert report.pricing_total_revenue is not None
    assert report.export_blocked is not None
    assert report.current_state is not None
    assert report.next_safe_action is not None
    assert report.summary is not None


def test_preview_report_no_state_machine():
    """Должен работать и без state_machine."""
    report = generate_preview(_clean_order(), state_machine=None)
    assert report.confirmed_total == 2
    assert report.current_state == "CLEAN"


# ── 9. Edge: более 20 confirmed строк ──

def test_preview_truncates_rows():
    many_rows = [{"row_id": f"row-{i}", "height": 1000, "width": 400, "quantity": 1} for i in range(30)]
    order = {"status": "clean", "confirmed_rows": many_rows, "disputed_rows": [], "total_area_m2": 12.0}
    report = generate_preview(order)
    assert report.confirmed_total == 30
    assert len(report.confirmed_rows_preview) == 20  # truncated
    assert len(report.pricing_rows) == 30  # pricing не truncated
