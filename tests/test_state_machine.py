"""Tests для Order State Machine Hermes-Clean.

Проверяет:
- Все разрешённые переходы
- Запрещённые переходы
- Свойства (state_label, is_terminal, can_export)
- Полный цикл RUN_FULL (clean и disputed)
- Сброс состояния
- История переходов
"""

import pytest

from hermes_clean import OrderState, OrderStateMachine, StateMachineResult, StateTransition


# ── Инициализация ──

def test_initial_state_is_raw_input():
    sm = OrderStateMachine()
    assert sm.state == OrderState.RAW_INPUT
    assert sm.state_label == "Сырые данные"
    assert sm.history == []
    assert sm.is_terminal is False
    assert sm.can_export is False


def test_custom_initial_state():
    sm = OrderStateMachine(OrderState.VALIDATED)
    assert sm.state == OrderState.VALIDATED


# ── Разрешённые переходы: RAW_INPUT → PARSED ──

def test_raw_to_parsed():
    sm = OrderStateMachine()
    result = sm.transition_to_parsed(confirmed_count=3, disputed_count=0, raw_text_length=20)
    assert result.success is True
    assert sm.state == OrderState.PARSED
    assert sm.state_label == "Разобрано"
    assert len(sm.history) == 1
    assert sm.history[0].trigger == "parse"
    assert sm.data["confirmed_count"] == 3


def test_raw_to_parses_same_state_does_nothing():
    sm = OrderStateMachine()
    sm.transition_to_parsed()
    result = sm.transition_to_parsed()
    assert result.success is True
    assert result.message == "Уже в состоянии Разобрано."


# ── PARSED → VALIDATED ──

def test_parsed_to_validated():
    sm = OrderStateMachine(OrderState.PARSED)
    result = sm.transition_to_validated(validation_result={"valid": True, "violations": []})
    assert result.success is True
    assert sm.state == OrderState.VALIDATED
    assert sm.state_label == "Валидировано"


def test_parsed_to_validated_with_violations():
    sm = OrderStateMachine(OrderState.PARSED)
    result = sm.transition_to_validated(
        validation_result={"valid": False, "violations": [{"field": "height", "reason": "out_of_range"}]}
    )
    assert result.success is True
    assert sm.state == OrderState.VALIDATED
    assert sm.data["violations_count"] == 1


# ── PARSED → HAS_DISPUTES ──

def test_parsed_to_disputed():
    sm = OrderStateMachine(OrderState.PARSED)
    result = sm.transition_to_disputed(
        dispute_count=2,
        dispute_reasons=["missing_width", "unparsed_order_text"],
    )
    assert result.success is True
    assert sm.state == OrderState.HAS_DISPUTES
    assert sm.state_label == "Есть споры"


def test_parsed_to_disputed_stores_reasons():
    sm = OrderStateMachine(OrderState.PARSED)
    reasons = ["missing_width", "too_many_numbers"]
    sm.transition_to_disputed(dispute_count=2, dispute_reasons=reasons)
    assert sm.data["dispute_reasons"] == reasons
    assert sm.data["dispute_count"] == 2


# ── HAS_DISPUTES → EXPORT_BLOCKED ──

def test_disputed_to_export_blocked():
    sm = OrderStateMachine(OrderState.HAS_DISPUTES)
    result = sm.transition_to_export_blocked(reason="Активные споры не разрешены.")
    assert result.success is True
    assert sm.state == OrderState.EXPORT_BLOCKED
    assert sm.state_label == "Экспорт заблокирован"


# ── HAS_DISPUTES → VALIDATED ──

def test_disputed_to_validated():
    sm = OrderStateMachine(OrderState.HAS_DISPUTES)
    result = sm.transition_to_validated(validation_result={"valid": True, "violations": []})
    assert result.success is True
    assert sm.state == OrderState.VALIDATED


# ── EXPORT_BLOCKED → VALIDATED ──

def test_export_blocked_to_validated():
    sm = OrderStateMachine(OrderState.EXPORT_BLOCKED)
    result = sm.transition_to_validated(validation_result={"valid": True, "violations": []})
    assert result.success is True
    assert sm.state == OrderState.VALIDATED


# ── VALIDATED → READY_FOR_PREVIEW ──

def test_validated_to_preview():
    sm = OrderStateMachine(OrderState.VALIDATED)
    result = sm.transition_to_preview()
    assert result.success is True
    assert sm.state == OrderState.READY_FOR_PREVIEW
    assert sm.state_label == "Готово к просмотру"


# ── READY_FOR_PREVIEW → READY_FOR_FUTURE_EXPORT ──

def test_preview_to_export_ready():
    sm = OrderStateMachine(OrderState.READY_FOR_PREVIEW)
    result = sm.transition_to_export_ready(approved_by="manager")
    assert result.success is True
    assert sm.state == OrderState.READY_FOR_FUTURE_EXPORT
    assert sm.state_label == "Готово к экспорту"
    assert sm.is_terminal is True
    assert sm.can_export is True
    assert sm.data["approved_by"] == "manager"


# ── READY_FOR_FUTURE_EXPORT: терминальное состояние ──

def test_terminal_state_cannot_transition():
    sm = OrderStateMachine(OrderState.READY_FOR_FUTURE_EXPORT)
    result = sm.transition_to_parsed()
    assert result.success is False
    assert "запрещён" in result.message


# ── Запрещённые переходы ──

def test_raw_input_cannot_skip_to_validated():
    sm = OrderStateMachine()
    result = sm.transition_to_validated()
    assert result.success is False
    assert "запрещён" in result.message


def test_raw_input_cannot_skip_to_export():
    sm = OrderStateMachine()
    result = sm.transition_to_export_ready()
    assert result.success is False


def test_parsed_cannot_skip_to_preview():
    sm = OrderStateMachine(OrderState.PARSED)
    result = sm.transition_to_preview()
    assert result.success is False


def test_validated_cannot_go_to_export_blocked():
    sm = OrderStateMachine(OrderState.VALIDATED)
    result = sm.transition_to_export_blocked()
    assert result.success is False


# ── Полный цикл: clean order ──

def test_full_cycle_clean_order():
    sm = OrderStateMachine()
    parse_result = {
        "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}],
        "disputed_rows": [],
    }
    validation_result = {"valid": True, "violations": []}

    results = sm.run_full_cycle(
        raw_text="1000 400 2",
        parse_result=parse_result,
        validation_result=validation_result,
        preview_approved_by="system",
    )

    assert len(results) == 4
    assert all(r.success for r in results)
    assert sm.state == OrderState.READY_FOR_FUTURE_EXPORT
    assert sm.can_export is True
    assert len(sm.history) == 4


def test_full_cycle_state_sequence_clean():
    sm = OrderStateMachine()
    parse_result = {"confirmed_rows": [{"height": 1000, "width": 400, "quantity": 2}], "disputed_rows": []}
    validation_result = {"valid": True, "violations": []}

    sm.run_full_cycle(raw_text="1000 400 2", parse_result=parse_result, validation_result=validation_result)
    states = [t.to_state for t in sm.history]
    assert states == [
        OrderState.PARSED,
        OrderState.VALIDATED,
        OrderState.READY_FOR_PREVIEW,
        OrderState.READY_FOR_FUTURE_EXPORT,
    ]


# ── Полный цикл: disputed order ──

def test_full_cycle_disputed_order():
    sm = OrderStateMachine()
    parse_result = {
        "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 1}],
        "disputed_rows": [{"dispute_id": "d1", "raw_text": "1000", "reason": "missing_width"}],
    }
    validation_result = {"valid": False, "violations": [{"field": "raw_text", "reason": "unparsed_order_text"}]}

    results = sm.run_full_cycle(
        raw_text="1000 400\n1000",
        parse_result=parse_result,
        validation_result=validation_result,
    )

    assert len(results) == 3
    assert all(r.success for r in results)
    assert sm.state == OrderState.EXPORT_BLOCKED
    assert sm.can_export is False


def test_full_cycle_state_sequence_disputed():
    sm = OrderStateMachine()
    parse_result = {
        "confirmed_rows": [{"height": 1000, "width": 400, "quantity": 1}],
        "disputed_rows": [{"dispute_id": "d1", "raw_text": "1000", "reason": "missing_width"}],
    }

    sm.run_full_cycle(
        raw_text="1000 400\n1000",
        parse_result=parse_result,
        validation_result={"valid": False, "violations": []},
    )
    states = [t.to_state for t in sm.history]
    assert states == [
        OrderState.PARSED,
        OrderState.HAS_DISPUTES,
        OrderState.EXPORT_BLOCKED,
    ]


# ── Disputed → resolve → export ready (ручной сценарий) ──

def test_disputed_resolve_to_export_ready():
    sm = OrderStateMachine(OrderState.HAS_DISPUTES)

    # 1. Block export
    sm.transition_to_export_blocked()
    assert sm.state == OrderState.EXPORT_BLOCKED

    # 2. Resolve disputes → validated
    sm.transition_to_validated(validation_result={"valid": True, "violations": []})
    assert sm.state == OrderState.VALIDATED

    # 3. Preview
    sm.transition_to_preview()
    assert sm.state == OrderState.READY_FOR_PREVIEW

    # 4. Approve export
    sm.transition_to_export_ready(approved_by="user")
    assert sm.state == OrderState.READY_FOR_FUTURE_EXPORT
    assert sm.can_export is True


# ── VALIDATED can go HAS_DISPUTES (новые споры после валидации) ──

def test_validated_to_disputed():
    sm = OrderStateMachine(OrderState.VALIDATED)
    result = sm.transition_to_disputed(dispute_count=1, dispute_reasons=["unparsed_order_text"])
    assert result.success is True
    assert sm.state == OrderState.HAS_DISPUTES


# ── Reset ──

def test_reset_clears_state():
    sm = OrderStateMachine(OrderState.READY_FOR_FUTURE_EXPORT)
    sm.reset()
    assert sm.state == OrderState.RAW_INPUT
    assert sm.history == []


def test_reset_keeps_history():
    sm = OrderStateMachine(OrderState.READY_FOR_FUTURE_EXPORT)
    history_len = len(sm.history)
    sm.reset(keep_history=True)
    assert sm.state == OrderState.RAW_INPUT
    assert len(sm.history) == history_len


# ── StateMachineResult ──

def test_result_type():
    sm = OrderStateMachine()
    result = sm.transition_to_parsed()
    assert isinstance(result, StateMachineResult)
    assert isinstance(result.transition, (StateTransition, type(None)))
    assert isinstance(result.message, str)
    assert isinstance(result.success, bool)


# ── STATE_LABELS coverage ──

def test_all_states_have_labels():
    from hermes_clean.state_machine import STATE_LABELS
    for state in OrderState:
        assert state in STATE_LABELS, f"State {state} missing label"
        assert STATE_LABELS[state], f"Empty label for {state}"
