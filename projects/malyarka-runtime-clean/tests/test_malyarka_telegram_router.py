from pathlib import Path

from malyarka_telegram.modes import TelegramMode
from malyarka_telegram.router import route_telegram_text
from malyarka_telegram.session import InMemoryModeSessionStore


def test_user_without_mode_is_neutral():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="hello", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert result.action == "clarify_intent"
    assert result.should_parse_order is False


def test_start_resets_to_neutral_mode():
    store = InMemoryModeSessionStore()
    store.set_mode(1, TelegramMode.ORDER)

    result = route_telegram_text(user_id=1, text="/start", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert store.get_mode(1) == TelegramMode.NEUTRAL
    assert result.should_parse_order is False


def test_mode_commands_switch_modes():
    store = InMemoryModeSessionStore()

    assert route_telegram_text(user_id=1, text="/заказ", session_store=store).mode == TelegramMode.ORDER
    assert store.get_mode(1) == TelegramMode.ORDER
    assert route_telegram_text(user_id=1, text="/чат", session_store=store).mode == TelegramMode.CHAT
    assert route_telegram_text(user_id=1, text="/инженер", session_store=store, owner_id=1).mode == TelegramMode.ENGINEER
    assert route_telegram_text(user_id=1, text="/идеи", session_store=store, owner_id=1).mode == TelegramMode.IDEAS
    assert route_telegram_text(user_id=1, text="/админ", session_store=store, owner_id=1).mode == TelegramMode.ADMIN
    assert route_telegram_text(user_id=1, text="/выжимка", session_store=store).mode == TelegramMode.SUMMARY
    assert route_telegram_text(user_id=1, text="/правила", session_store=store).mode == TelegramMode.RULES


def test_plain_phone_mode_words_switch_modes_without_slash():
    store = InMemoryModeSessionStore()

    assert route_telegram_text(user_id=1, text="заказ", session_store=store).mode == TelegramMode.ORDER
    assert store.get_mode(1) == TelegramMode.ORDER
    assert route_telegram_text(user_id=1, text="отмена", session_store=store).mode == TelegramMode.NEUTRAL
    assert route_telegram_text(user_id=1, text="🛠 Инженер проекта", session_store=store, owner_id=1).mode == TelegramMode.ENGINEER
    assert route_telegram_text(user_id=1, text="💬 Идеи / разговор", session_store=store, owner_id=1).mode == TelegramMode.IDEAS


def test_owner_only_modes_are_denied_without_matching_owner_id():
    store = InMemoryModeSessionStore()

    for command in ("/инженер", "/идеи", "/админ"):
        result = route_telegram_text(user_id=2, text=command, session_store=store, owner_id=1)
        assert result.action == "access_denied"
        assert result.should_parse_order is False
        assert store.get_mode(2) == TelegramMode.NEUTRAL


def test_owner_only_modes_fail_closed_when_owner_id_is_not_configured():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="/админ", session_store=store)

    assert result.action == "access_denied"
    assert "Доступ закрыт" in result.message


def test_chat_mode_does_not_parse_order_like_text():
    store = InMemoryModeSessionStore()
    store.set_mode(1, TelegramMode.CHAT)

    result = route_telegram_text(user_id=1, text="1000*400", session_store=store)

    assert result.mode == TelegramMode.CHAT
    assert result.should_parse_order is False
    assert result.should_call_ai is False
    assert "/заказ" in result.message


def test_order_mode_marks_order_text_for_parser():
    store = InMemoryModeSessionStore()
    store.set_mode(1, TelegramMode.ORDER)

    result = route_telegram_text(user_id=1, text="1000*400", session_store=store)

    assert result.mode == TelegramMode.ORDER
    assert result.action == "parse_order"
    assert result.should_parse_order is True
    assert result.should_call_ai is False


def test_neutral_mode_does_not_parse_regular_text_as_order():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="привет", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert result.action == "clarify_intent"
    assert result.should_parse_order is False


def test_neutral_mode_clarifies_unknown_text():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="погода сегодня хорошая", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert result.action == "clarify_intent"
    assert result.should_parse_order is False
    assert "Выберите" in result.message


def test_neutral_mode_parses_order_like_text_immediately():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="1000*400", session_store=store)

    assert result.mode == TelegramMode.ORDER
    assert store.get_mode(1) == TelegramMode.ORDER
    assert result.action == "parse_order"
    assert result.should_parse_order is True


def test_neutral_mode_suggests_ideas_mode_for_ideas_text():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="у меня есть идея", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert result.action == "suggest_ideas_mode"
    assert result.should_parse_order is False
    assert "/идеи" in result.message


def test_neutral_mode_suggests_engineer_mode_for_engineer_text():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="какой статус проекта", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert result.action == "suggest_engineer_mode"
    assert result.should_parse_order is False
    assert "/инженер" in result.message


def test_neutral_mode_clarifies_low_conf_admin_text():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="админ", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert result.action == "clarify_intent"
    assert result.should_parse_order is False
    assert "Выберите" in result.message or "Отмена" in result.message


def test_neutral_mode_blocks_dangerous_content():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="где .env", session_store=store)

    assert result.mode == TelegramMode.NEUTRAL
    assert result.action == "blocked"
    assert result.should_parse_order is False
    assert "заблокирован" in result.message


def test_summary_mode_does_not_change_code_or_create_task():
    store = InMemoryModeSessionStore()
    store.set_mode(1, TelegramMode.SUMMARY)

    result = route_telegram_text(user_id=1, text="идея", session_store=store)

    assert result.should_make_summary is True
    assert result.should_change_code is False
    assert result.should_parse_order is False
    assert result.should_call_ai is False


def test_engineer_mode_does_not_launch_codex_or_change_files():
    store = InMemoryModeSessionStore()
    store.set_mode(1, TelegramMode.ENGINEER)

    result = route_telegram_text(user_id=1, text="подготовь задачу", session_store=store)

    assert result.action == "engineer_task_card"
    assert result.should_change_code is False
    assert result.should_parse_order is False
    assert result.should_call_ai is False
    assert result.message.startswith("ЗАДАЧА")
    assert "подготовь задачу" in result.message
    assert "ОЖИДАЕМЫЙ РЕЗУЛЬТАТ" in result.message
    assert "МОЖНО" in result.message
    assert "НЕЛЬЗЯ" in result.message
    assert "ОБЯЗАТЕЛЬНЫЕ ПРОВЕРКИ" in result.message
    assert "ФОРМАТ ОТЧЁТА ИСПОЛНИТЕЛЯ" in result.message
    assert "НЕЗАВИСИМОЕ РЕВЬЮ" in result.message
    assert "СТАТУС" in result.message
    assert "read-only / copy-ready" in result.message


def test_ideas_mode_does_not_parse_order_like_text_or_call_ai():
    store = InMemoryModeSessionStore()
    store.set_mode(1, TelegramMode.IDEAS)

    result = route_telegram_text(user_id=1, text="1000*400", session_store=store, owner_id=1)

    assert result.action == "ideas_placeholder"
    assert result.should_parse_order is False
    assert result.should_call_ai is False
    assert "Режим идей включён" in result.message


def test_admin_mode_returns_safe_diagnostics_only():
    store = InMemoryModeSessionStore()

    result = route_telegram_text(user_id=1, text="/админ", session_store=store, owner_id=1)

    assert result.mode == TelegramMode.ADMIN
    assert "owner_id_configured=true" in result.message
    assert "polling_started=false" in result.message
    assert "state_version=" in result.message
    assert "1" not in result.message.split("owner_id_configured", 1)[0]


def test_rules_mode_does_not_change_rules_directly():
    store = InMemoryModeSessionStore()
    store.set_mode(1, TelegramMode.RULES)

    result = route_telegram_text(user_id=1, text="размеры", session_store=store)

    assert result.should_use_rules is True
    assert result.should_change_code is False
    assert result.should_parse_order is False
    assert result.should_call_ai is False


def test_should_call_ai_is_false_in_all_modes():
    store = InMemoryModeSessionStore()

    for mode in TelegramMode:
        store.set_mode(1, mode)
        result = route_telegram_text(user_id=1, text="1000*400", session_store=store)
        assert result.should_call_ai is False


def test_new_modules_do_not_import_polling_app_or_handlers():
    source = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in [
            "malyarka_telegram/modes.py",
            "malyarka_telegram/session.py",
            "malyarka_telegram/router.py",
        ]
    )

    assert "malyarka_telegram.app" not in source
    assert "malyarka_telegram.handlers" not in source
    assert "start_polling" not in source
    assert "run_polling" not in source


def test_orders_db_is_not_used_by_mode_router_modules():
    source = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in [
            "malyarka_telegram/modes.py",
            "malyarka_telegram/session.py",
            "malyarka_telegram/router.py",
        ]
    )

    assert "orders.db" not in source
    assert "sqlite" not in source.lower()
