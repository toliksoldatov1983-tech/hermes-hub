"""Tests для Telegram Dialog Flow Hermes-Clean.

Проверяет полную цепочку диалога:
- Приём заказа (raw_text → парсинг)
- Обнаружение споров → HAS_DISPUTES
- Уточняющие вопросы
- Разрешение споров (accept, delete)
- Preview report
- Export blocked/ready
- Финальный отчёт
- Чистый заказ (clean, без споров)
- Сброс диалога
"""

import pytest

from hermes_clean import (
    TelegramDialogFlow,
    DialogMessage,
    DialogState,
    OrderState,
)


# ── 1. Чистый заказ (clean flow) ──

def test_clean_order_receive():
    flow = TelegramDialogFlow()
    msg = flow.receive_order("1000 400 2\n700 300")
    assert "Заказ принят" in msg.text
    assert "Подтверждено строк: 2" in msg.text
    assert "Спорных строк:" not in msg.text  # нет споров
    assert flow.current_state_name == "Готово к просмотру"
    assert flow.state.phase == "input"


def test_clean_order_preview():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2")
    msg = flow.show_preview()
    assert "Preview Report" in msg.text
    assert "Подтверждённые строки" in msg.text
    assert "Спорных строк" in msg.text
    assert "Валидация" in msg.text
    assert "Стоимость" in msg.text


def test_clean_order_export_status():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2")
    msg = flow.check_export_status()
    assert "Экспорт РАЗРЕШЁН" in msg.text or "не заблокирован" in msg.text


def test_clean_order_final_report():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2")
    msg = flow.show_final_report()
    assert "ИТОГОВЫЙ ОТЧЁТ" in msg.text
    assert "Подтверждено строк: 1" in msg.text
    assert "Спорных строк: 0" in msg.text
    assert "заблокирован" not in msg.text or "разрешён" in msg.text


# ── 2. Заказ со спорами (disputed flow) ──

def test_disputed_order_receive():
    flow = TelegramDialogFlow()
    msg = flow.receive_order("1000 400 2\nмусор\n1000")
    assert "Заказ принят" in msg.text
    assert "Подтверждено строк: 1" in msg.text
    assert "Спорных строк: 2" in msg.text
    assert "Экспорт заблокирован" in msg.text
    assert flow.state.phase == "disputes"
    assert len(flow.state.pending_questions) == 2


def test_disputed_order_ask_questions():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nмусор")
    msg = flow.ask_questions()
    assert "Уточняющие вопросы" in msg.text
    assert "dispute-2" in msg.text or "dispute-1" in msg.text
    assert "Причина:" in msg.text or "Вопрос:" in msg.text
    assert "resolve_dispute" in msg.text
    assert flow.state.phase == "resolving"


def test_disputed_order_resolve_delete():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nмусор")
    flow.ask_questions()
    msg = flow.resolve_dispute("dispute-2", {"action": "delete"})
    assert "разрешён" in msg.text
    assert "delete" in msg.text
    assert flow.state.resolved_count == 1
    assert len(flow.state.pending_questions) == 0  # all resolved
    assert flow.state.phase == "done"


def test_disputed_order_resolve_accept():
    flow = TelegramDialogFlow()
    flow.receive_order("1000\n400 300")
    flow.ask_questions()
    msg = flow.resolve_dispute("dispute-1", {
        "action": "accept",
        "height": 1000,
        "width": 400,
        "quantity": 2,
    })
    assert "разрешён" in msg.text
    assert flow.state.resolved_count == 1
    # Now check that the confirmed row was added
    assert len(flow.order_result["confirmed_rows"]) == 2


def test_disputed_order_resolve_invalid():
    flow = TelegramDialogFlow()
    flow.receive_order("1000\n400 300")
    flow.ask_questions()
    msg = flow.resolve_dispute("nonexistent", {"action": "delete"})
    assert "не найден" in msg.text


def test_disputed_order_resolve_accept_partial_then_done():
    """Один спор → resolve → phase=done."""
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nмусор")
    flow.ask_questions()
    flow.resolve_dispute("dispute-2", {"action": "delete"})
    assert flow.state.phase == "done"
    assert flow.state.resolved_count == 1
    assert flow.state.total_disputes == 1


# ── 3. Disputed → preview после разрешения ──

def test_disputed_resolve_then_preview():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nмусор")
    flow.ask_questions()
    flow.resolve_dispute("dispute-2", {"action": "delete"})
    msg = flow.show_preview()
    assert "Preview Report" in msg.text
    assert "Подтверждённые строки" in msg.text


def test_disputed_resolve_then_export_check():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nмусор")
    flow.ask_questions()
    flow.resolve_dispute("dispute-2", {"action": "delete"})
    msg = flow.check_export_status()
    assert "РАЗРЕШЁН" in msg.text


# ── 4. Disputed → final report ──

def test_disputed_final_report():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nмусор")
    flow.ask_questions()
    flow.resolve_dispute("dispute-2", {"action": "delete"})
    msg = flow.show_final_report()
    assert "ИТОГОВЫЙ ОТЧЁТ" in msg.text
    assert "Все споры разрешены" in msg.text
    assert "Подтверждено строк: 1" in msg.text


# ── 5. Парсинг: граничные случаи ──

def test_parse_missing_width():
    flow = TelegramDialogFlow()
    flow.receive_order("1000")
    assert len(flow.order_result["disputed_rows"]) == 1
    assert flow.order_result["disputed_rows"][0]["reason"] == "missing_width"


def test_parse_too_many_numbers():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2 5 10")
    assert len(flow.order_result["disputed_rows"]) == 1
    assert flow.order_result["disputed_rows"][0]["reason"] == "too_many_numbers"


def test_parse_garbage_text():
    flow = TelegramDialogFlow()
    flow.receive_order("срочно заказ на двери")
    assert flow.order_result["status"] == "empty_or_invalid"
    assert len(flow.order_result["disputed_rows"]) >= 0


def test_parse_empty_text():
    flow = TelegramDialogFlow()
    flow.receive_order("")
    assert flow.order_result["status"] == "empty_or_invalid"
    assert len(flow.order_result["confirmed_rows"]) == 0


def test_parse_mixed():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nсрочно\n700 300")
    assert len(flow.order_result["confirmed_rows"]) == 2
    assert len(flow.order_result["disputed_rows"]) == 1


# ── 6. Reset ──

def test_reset():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2")
    msg = flow.reset()
    assert "сброшен" in msg.text
    assert flow.state.phase == "initial"
    assert flow.order_result == {}
    assert flow.state_machine.state == OrderState.RAW_INPUT


# ── 7. Messages ──

def test_messages_history():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2")
    flow.show_preview()
    assert len(flow.messages) == 2
    assert flow.messages[0].role == "assistant"
    assert flow.messages[0].step == "receive_order"
    assert flow.messages[1].step == "show_preview"


def test_get_last_message():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2")
    last = flow.get_last_message()
    assert "Заказ принят" in last
    flow.show_preview()
    last = flow.get_last_message()
    assert "Preview Report" in last


# ── 8. DialogState ──

def test_dialog_state_fields():
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2\nмусор")
    assert isinstance(flow.state, DialogState)
    assert flow.state.phase == "disputes"
    assert flow.state.total_disputes == 1
    assert flow.state.resolved_count == 0
    assert len(flow.state.pending_questions) == 1


def test_empty_order_flow():
    """Пустой заказ — просто проверяем что не падает."""
    flow = TelegramDialogFlow()
    msg = flow.receive_order("")
    assert "Заказ принят" in msg.text


# ── 9. Полный сценарий: clean ──

def test_full_scenario_clean():
    """Полный цикл: ввод → preview → export → report."""
    flow = TelegramDialogFlow()
    flow.receive_order("1000 400 2")
    pv = flow.show_preview()
    assert pv is not None
    ex = flow.check_export_status()
    assert ex is not None
    fr = flow.show_final_report()
    assert fr is not None
    assert len(flow.messages) == 4


# ── 10. Полный сценарий: disputed → resolve → done ──

def test_full_scenario_disputed():
    """Полный цикл: ввод → вопросы → resolve → preview → export → report."""
    flow = TelegramDialogFlow()

    # 1. Ввод
    flow.receive_order("1000 400 2\nмусор")
    assert flow.state.phase == "disputes"

    # 2. Вопросы
    q = flow.ask_questions()
    assert flow.state.phase == "resolving"

    # 3. Resolve
    flow.resolve_dispute("dispute-2", {"action": "delete"})
    assert flow.state.phase == "done"

    # 4. Preview
    pv = flow.show_preview()
    assert "Preview Report" in pv.text

    # 5. Export
    ex = flow.check_export_status()
    assert "РАЗРЕШЁН" in ex.text

    # 6. Report
    fr = flow.show_final_report()
    assert "Все споры разрешены" in fr.text
    assert len(flow.messages) == 6


# ── 11. DialogMessage dataclass ──

def test_dialog_message_fields():
    msg = DialogMessage(role="operator", text="hello", step="input")
    assert msg.role == "operator"
    assert msg.text == "hello"
    assert msg.step == "input"
