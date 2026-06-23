from pathlib import Path

from malyarka_telegram.handlers import (
    build_text_response,
    handle_text_message,
    handle_text_message_with_router,
)
from malyarka_telegram.modes import TelegramMode
from malyarka_telegram.session import InMemoryModeSessionStore


def test_old_handle_text_message_keeps_text_only_compatibility():
    message = handle_text_message("1000*400")

    assert isinstance(message, str)
    assert "1. 1000 400 1" in message
    assert "Предпросмотр заказа" in message


def test_old_handle_text_message_does_not_require_user_id_or_session_store():
    message = handle_text_message("1000*400")

    assert "1. 1000 400 1" in message


def test_order_command_switches_mode_without_parsing_the_command():
    store = InMemoryModeSessionStore()

    response = handle_text_message_with_router(
        "/заказ",
        user_id=10,
        session_store=store,
    )

    assert store.get_mode(10) == TelegramMode.ORDER
    assert "Включён режим заказа" in response.text
    assert response.copy_keyboard is None


def test_order_mode_routes_order_text_to_existing_local_preview():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/заказ", user_id=10, session_store=store)

    response = handle_text_message_with_router(
        "1000*400",
        user_id=10,
        session_store=store,
    )

    assert "1. 1000 400 1" in response.text
    assert "Предпросмотр заказа" in response.text
    assert response.copy_keyboard is not None
    assert response.copy_keyboard.buttons[0].action == "download_corel_excel"
    assert response.copy_keyboard.buttons[1].action == "download_malyarka_file"
    assert response.copy_keyboard.buttons[2].copy_text == "1000 400 1"


def test_order_mode_keeps_same_copy_keyboard_as_existing_preview_path():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/заказ", user_id=10, session_store=store)

    routed_response = handle_text_message_with_router(
        "1000*400\n1000*600",
        user_id=10,
        session_store=store,
    )
    old_response = build_text_response("1000*400\n1000*600")

    assert routed_response.copy_keyboard == old_response.copy_keyboard
    assert routed_response.copy_keyboard is not None
    assert routed_response.copy_keyboard.buttons[0].action == "download_corel_excel"
    assert routed_response.copy_keyboard.buttons[1].action == "download_malyarka_file"
    assert routed_response.copy_keyboard.buttons[2].copy_text == (
        "1000 400 1\n1000 600 1"
    )


def test_order_mode_disputed_order_shows_fix_copy_button():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/заказ", user_id=10, session_store=store)

    response = handle_text_message_with_router(
        "1000*400\nнепонятная строка\n1000*600",
        user_id=10,
        session_store=store,
    )

    assert response.copy_keyboard is not None
    labels = [button.label for button in response.copy_keyboard.buttons]
    assert " Скопировать для Corel" not in labels
    assert "Скачать Файл Малярки" not in labels
    assert " Скопировать подтверждённые" not in labels
    assert labels[0] == " Скопировать для исправления"
    assert response.copy_keyboard.buttons[0].copy_text == (
        "1000 400 1\nнепонятная строка\n1000 600 1"
    )


def test_chat_command_switches_mode():
    store = InMemoryModeSessionStore()

    response = handle_text_message_with_router(
        "/чат",
        user_id=11,
        session_store=store,
    )

    assert store.get_mode(11) == TelegramMode.CHAT
    assert "Включён режим чата" in response.text
    assert response.copy_keyboard is None


def test_chat_mode_does_not_send_order_like_text_to_parser():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/чат", user_id=11, session_store=store)

    response = handle_text_message_with_router(
        "1000*400",
        user_id=11,
        session_store=store,
    )

    assert "1. 1000 400 1" not in response.text
    assert "Предпросмотр заказа" not in response.text
    assert "/заказ" in response.text
    assert response.copy_keyboard is None


def test_neutral_mode_parses_order_like_text_automatically():
    store = InMemoryModeSessionStore()

    response = handle_text_message_with_router(
        "1000*400",
        user_id=12,
        session_store=store,
    )

    assert store.get_mode(12) == TelegramMode.ORDER
    assert "1. 1000 400 1" in response.text
    assert "Предпросмотр заказа" in response.text
    assert "/заказ" not in response.text
    assert response.copy_keyboard is not None


def test_clarify_intent_unknown_text_has_keyboard_with_four_buttons():
    store = InMemoryModeSessionStore()

    response = handle_text_message_with_router(
        "погода сегодня хорошая",
        user_id=50,
        session_store=store,
    )

    assert response.copy_keyboard is not None
    labels = [button.label for button in response.copy_keyboard.buttons]
    assert len(labels) == 4
    assert "🧾 Новый заказ" in labels
    assert "💬 Идея / обсуждение" in labels
    assert "🛠 Инженер" in labels
    assert "← Отмена" in labels
    # Admin button must NOT be in clarification buttons
    admin_label_found = any("админ" in label.lower() for label in labels)
    assert not admin_label_found, "Admin button must not appear in clarify intent keyboard"


def test_engineer_mode_returns_read_only_task_card_and_buttons():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/инженер", user_id=13, session_store=store, owner_id=13)

    response = handle_text_message_with_router(
        "сделать файл малярки",
        user_id=13,
        session_store=store,
        owner_id=13,
    )

    assert store.get_mode(13) == TelegramMode.ENGINEER
    assert response.text.startswith("ЗАДАЧА")
    assert "сделать файл малярки" in response.text
    assert "ОБЯЗАТЕЛЬНЫЕ ПРОВЕРКИ" in response.text
    assert "НЕЗАВИСИМОЕ РЕВЬЮ" in response.text
    assert "Codex/Hermes" in response.text
    assert "read-only / copy-ready" in response.text
    assert response.copy_keyboard is not None
    assert [button.label for button in response.copy_keyboard.buttons] == [
        "Разрешаю",
        "Отмена",
        "Исправить задачу",
    ]
    assert [button.action for button in response.copy_keyboard.buttons] == [
        "engineer_task_allow_read_only",
        "engineer_task_cancel_read_only",
        "engineer_task_edit_read_only",
    ]
    assert all(button.copy_text is None for button in response.copy_keyboard.buttons)


def test_ideas_command_switches_to_read_only_discussion_mode():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/идеи", user_id=16, session_store=store, owner_id=16)

    response = handle_text_message_with_router(
        "1000*400",
        user_id=16,
        session_store=store,
        owner_id=16,
    )

    assert store.get_mode(16) == TelegramMode.IDEAS
    assert "Режим идей включён" in response.text
    assert "Предпросмотр заказа" not in response.text
    assert response.copy_keyboard is None


def test_admin_command_is_owner_only_safe_diagnostics():
    store = InMemoryModeSessionStore()

    response = handle_text_message_with_router("/админ", user_id=17, session_store=store, owner_id=17)

    assert store.get_mode(17) == TelegramMode.ADMIN
    assert "Админ-диагностика" in response.text
    assert "owner_id_configured=true" in response.text
    assert "polling_started=false" in response.text
    assert response.copy_keyboard is None


def test_summary_mode_is_placeholder_and_does_not_create_task():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/выжимка", user_id=14, session_store=store)

    response = handle_text_message_with_router(
        "идея",
        user_id=14,
        session_store=store,
    )

    assert store.get_mode(14) == TelegramMode.SUMMARY
    assert "выжимки" in response.text
    assert response.copy_keyboard is None


def test_rules_mode_is_placeholder_and_does_not_change_rules():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/правила", user_id=15, session_store=store)

    response = handle_text_message_with_router(
        "размеры",
        user_id=15,
        session_store=store,
    )

    assert store.get_mode(15) == TelegramMode.RULES
    assert "правил" in response.text
    assert response.copy_keyboard is None


def test_hermes_bang_command_is_blocked_in_routed_order_mode():
    store = InMemoryModeSessionStore()
    handle_text_message_with_router("/заказ", user_id=18, session_store=store)

    response = handle_text_message_with_router("!помощь", user_id=18, session_store=store)

    assert "Hermes из Telegram на этом этапе не запускается" in response.text
    assert response.copy_keyboard is None


def test_routed_text_handling_does_not_import_ai_or_database_layers():
    source = Path("malyarka_telegram/handlers.py").read_text(encoding="utf-8")

    assert "deepseek" not in source.lower()
    assert "BOT_TOKEN" not in source
    assert "DEEPSEEK_API_KEY" not in source
    assert "GEMINI_API_KEY" not in source
    assert "sqlite" not in source.lower()


def test_app_py_is_connected_to_routed_handler():
    source = Path("malyarka_telegram/app.py").read_text(encoding="utf-8")

    assert "handle_text_message_with_router" in source
