import ast
from pathlib import Path

from malyarka_telegram.app import create_app
from malyarka_telegram.config import TelegramConfig
from malyarka_telegram.handlers import (
    build_text_response,
    handle_command_message,
    handle_photo_message,
    handle_text_message,
)
from malyarka_telegram.keyboards import get_main_keyboard_labels
from malyarka_telegram.messages import (
    format_engineer_task_callback_message,
    format_engineer_task_card_message,
    format_voice_not_configured_message,
    format_voice_transcribed_message,
    format_voice_transcription_failed_message,
)


def test_photo_message_returns_not_supported_text():
    message = handle_photo_message()

    assert "Фото-режим ещё не подключён" in message
    assert "Пришлите заказ текстом" in message


def test_voice_messages_are_safe_and_do_not_expose_secrets():
    assert "OPENAI_API_KEY" in format_voice_not_configured_message()
    assert "токен" not in format_voice_not_configured_message().lower()
    assert "не смог распознать" in format_voice_transcription_failed_message()
    assert format_voice_transcribed_message("  заказ   1000*400 ") == (
        "Распознал голос:\nзаказ 1000*400"
    )


def test_greeting_returns_russian_hint():
    message = handle_text_message("здравствуйте")

    assert "Здравствуйте" in message
    assert "Выберите дверь личного бота" in message
    assert "🧾 Новый заказ" in message
    assert "🛠 Инженер проекта" in message
    assert "💬 Идеи / разговор" in message
    assert "Фото-режим пока не подключён" in message


def test_engineer_task_card_message_is_read_only_and_structured():
    message = format_engineer_task_card_message("сделать файл малярки")

    assert message.startswith("ЗАДАЧА")
    assert "сделать файл малярки" in message
    assert "ОЖИДАЕМЫЙ РЕЗУЛЬТАТ" in message
    assert "МОЖНО" in message
    assert "НЕЛЬЗЯ" in message
    assert "ОБЯЗАТЕЛЬНЫЕ ПРОВЕРКИ" in message
    assert "ФОРМАТ ОТЧЁТА ИСПОЛНИТЕЛЯ" in message
    assert "НЕЗАВИСИМОЕ РЕВЬЮ" in message
    assert "СТАТУС" in message
    assert "Codex/Hermes" in message
    assert "DeepSeek" in message
    assert "Исполнитель и ревьюер должны быть разными AI-провайдерами" in message
    assert "Запускать Hermes, Codex, gateway, polling или внешние AI/API" in message
    assert "read-only / copy-ready" in message


def test_engineer_task_callback_messages_are_read_only():
    allow = format_engineer_task_callback_message(
        "engineer_task_allow_read_only",
        task_text="сделать файл малярки",
    )
    cancel = format_engineer_task_callback_message("engineer_task_cancel_read_only")
    edit = format_engineer_task_callback_message("engineer_task_edit_read_only")
    unknown = format_engineer_task_callback_message("unknown")

    assert "ЗАДАНИЕ ДЛЯ CODEX/HERMES" in allow
    assert "ПАКЕТ ДЛЯ НЕЗАВИСИМОГО РЕВЬЮ" in allow
    assert "сделать файл малярки" in allow
    assert "Не запускать Hermes/Codex из Telegram" in allow
    assert "Не вызывать DeepSeek/OpenAI/API" in allow
    assert "ВЕРДИКТ: принять / не принимать / принять только после исправлений" in allow
    assert "отмен" in cancel.lower()
    assert "Никакие действия не выполнялись" in cancel
    assert "исправленный текст задачи" in edit
    assert "read-only" in edit
    assert "Неизвестная кнопка" in unknown
    assert "Hermes/Codex не запускаются" in unknown


def test_engineer_task_keeps_forbidden_zone_names_but_redacts_secret_values():
    task_text = (
        "Проверить .env, токены и ключи не трогать. "
        "BOT_TOKEN=123456:secret DEEPSEEK_API_KEY=abc"
    )

    message = format_engineer_task_callback_message(
        "engineer_task_allow_read_only",
        task_text=task_text,
    )

    assert "Проверить .env, токены и ключи не трогать." in message
    assert "BOT_TOKEN=<redacted>" in message
    assert "DEEPSEEK_API_KEY=<redacted>" in message
    assert "123456:secret" not in message
    assert "API_KEY=abc" not in message
    assert "запрос содержит защищённые данные" not in message


def test_text_order_without_disputes_returns_russian_summary():
    message = handle_text_message("500 700 2\n300 400")

    assert "Предпросмотр заказа" in message
    assert "Подтверждённые строки:" in message
    assert "1. 500 700 2" in message
    assert "2. 300 400 1" in message
    assert "Спорные строки:\nнет" in message
    assert "Всего деталей: 3" in message
    assert "Общая площадь: 0.820 м²" in message
    assert "Экспорт: доступен" in message


def test_text_order_accepts_star_separator_from_telegram():
    message = handle_text_message("1000*400\n1000*600")

    assert "Не вижу строк заказа" not in message
    assert "1. 1000 400 1" in message
    assert "2. 1000 600 1" in message
    assert "Экспорт: доступен" in message


def test_text_order_accepts_x_separators_from_telegram():
    response = build_text_response("1000x400\n1000х500\n1000×600")

    assert "1. 1000 400 1" in response.text
    assert "2. 1000 500 1" in response.text
    assert "3. 1000 600 1" in response.text
    assert response.copy_keyboard is not None
    assert response.copy_keyboard.buttons[0].action == "download_corel_excel"
    assert response.copy_keyboard.buttons[1].action == "download_malyarka_file"
    assert response.copy_keyboard.buttons[2].copy_text == (
        "1000 400 1\n1000 500 1\n1000 600 1"
    )


def test_text_order_accepts_separators_with_quantity_from_telegram():
    response = build_text_response(
        "1000*400*2\n1000 x 400 x 3\n1000х400х4\n1000×400×5"
    )

    assert "1. 1000 400 2" in response.text
    assert "2. 1000 400 3" in response.text
    assert "3. 1000 400 4" in response.text
    assert "4. 1000 400 5" in response.text
    assert response.copy_keyboard is not None
    assert response.copy_keyboard.buttons[0].action == "download_corel_excel"
    assert response.copy_keyboard.buttons[1].action == "download_malyarka_file"
    assert response.copy_keyboard.buttons[2].copy_text == (
        "1000 400 2\n1000 400 3\n1000 400 4\n1000 400 5"
    )


def test_text_order_without_disputes_has_corel_excel_download_button_first():
    response = build_text_response("700 500 1\n300 400 2\n1000 400 3")

    assert response.copy_keyboard is not None
    assert [button.label for button in response.copy_keyboard.buttons] == [
        "Скачать Excel для Corel",
        "Скачать Файл Малярки",
        " Скопировать для Corel",
    ]
    excel_button = response.copy_keyboard.buttons[0]
    malyarka_button = response.copy_keyboard.buttons[1]
    button = response.copy_keyboard.buttons[2]

    assert excel_button.action == "download_corel_excel"
    assert excel_button.copy_text is None
    assert malyarka_button.action == "download_malyarka_file"
    assert malyarka_button.copy_text is None
    assert button.label == " Скопировать для Corel"
    assert button.copy_text == "700 500 1\n300 400 2\n1000 400 3"
    assert "1." not in button.copy_text
    assert "Подтверждённые строки" not in button.copy_text
    assert "Скопировать" not in button.copy_text
    assert "Общая площадь" not in button.copy_text
    assert "Всего деталей" not in button.copy_text


def test_text_order_uses_core_telegram_preview_adapter(monkeypatch):
    from malyarka_telegram import handlers

    called = {}

    def fake_build_order_preview_from_text(text):
        called["text"] = text
        return {
            "confirmed_items": [
                {"height": 500, "width": 700, "quantity": 2},
            ],
            "disputed_items": [],
            "confirmed_count": 1,
            "disputed_count": 0,
            "total_quantity": 2,
            "total_area_m2": 0.7,
            "can_export": True,
        }

    monkeypatch.setattr(
        handlers, "build_order_preview_from_text", fake_build_order_preview_from_text
    )

    message = handlers.handle_text_message("500 700 2")

    assert called == {"text": "500 700 2"}
    assert "Предпросмотр заказа" in message
    assert "1. 500 700 2" in message


def test_text_order_with_disputed_line_blocks_export():
    message = handle_text_message("500 700 2\nтолько фасад")

    assert "Подтверждённые строки:" in message
    assert "Спорные строки:" in message
    assert "только фасад" in message
    assert "Экспорт: заблокирован" in message
    assert "Причина блокировки: есть спорные строки." in message


def test_text_order_with_dispute_has_separate_copy_buttons():
    response = build_text_response("700 500\nнепонятная строка\n300 400 2")

    assert response.copy_keyboard is not None
    assert [button.label for button in response.copy_keyboard.buttons] == [
        " Скопировать для исправления",
        " Скопировать спорные",
    ]
    assert response.copy_keyboard.buttons[0].copy_text == (
        "700 500 1\nнепонятная строка\n300 400 2"
    )
    assert response.copy_keyboard.buttons[1].copy_text == "непонятная строка"
    assert "700 500 1" not in response.copy_keyboard.buttons[1].copy_text
    assert "Экспорт: заблокирован" in response.text
    assert "Причина блокировки: есть спорные строки." in response.text


def test_clean_order_has_corel_excel_download_button_and_backup_copy_button():
    response = build_text_response("1000*400\n1000*600")

    assert response.copy_keyboard is not None
    assert [button.label for button in response.copy_keyboard.buttons] == [
        "Скачать Excel для Corel",
        "Скачать Файл Малярки",
        " Скопировать для Corel",
    ]
    excel_button = response.copy_keyboard.buttons[0]
    assert excel_button.action == "download_corel_excel"
    assert excel_button.copy_text is None

    malyarka_button = response.copy_keyboard.buttons[1]
    assert malyarka_button.action == "download_malyarka_file"
    assert malyarka_button.copy_text is None

    copy_text = response.copy_keyboard.buttons[2].copy_text
    assert copy_text == "1000 400 1\n1000 600 1"
    assert "1." not in copy_text
    assert "Предпросмотр заказа" not in copy_text
    assert "Общая площадь" not in copy_text
    assert "Всего деталей" not in copy_text
    assert "Спорные строки" not in copy_text


def test_disputed_order_has_editable_fix_copy_button_in_source_order():
    response = build_text_response("1000*400\nнепонятная строка\n1000*600")

    assert response.copy_keyboard is not None
    labels = [button.label for button in response.copy_keyboard.buttons]
    assert "Скачать Excel для Corel" not in labels
    assert "Скачать Файл Малярки" not in labels
    assert " Скопировать для Corel" not in labels
    assert labels[0] == " Скопировать для исправления"

    copy_text = response.copy_keyboard.buttons[0].copy_text
    assert copy_text == "1000 400 1\nнепонятная строка\n1000 600 1"
    assert "Предпросмотр заказа" not in copy_text
    assert "Общая площадь" not in copy_text
    assert "Всего деталей" not in copy_text
    assert "Причина" not in copy_text
    assert "Экспорт" not in copy_text
    assert "Скопировать" not in copy_text


def test_disputed_order_keeps_only_fix_and_disputed_copy_buttons():
    response = build_text_response("1000*400\nнепонятная строка\n1000*600")

    assert response.copy_keyboard is not None
    buttons = {button.label: button.copy_text for button in response.copy_keyboard.buttons}
    assert " Скопировать подтверждённые" not in buttons
    assert buttons[" Скопировать для исправления"] == "1000 400 1\nнепонятная строка\n1000 600 1"
    assert buttons[" Скопировать спорные"] == "непонятная строка"


def test_fixed_editable_text_can_be_sent_back_as_clean_order():
    fixed_text = "1000 400 1\n500 700 2\n1000 600 1"

    response = build_text_response(fixed_text)

    assert "Экспорт: доступен" in response.text
    assert response.copy_keyboard is not None
    assert [button.label for button in response.copy_keyboard.buttons] == [
        "Скачать Excel для Corel",
        "Скачать Файл Малярки",
        " Скопировать для Corel",
    ]
    assert response.copy_keyboard.buttons[0].action == "download_corel_excel"
    assert response.copy_keyboard.buttons[1].action == "download_malyarka_file"
    assert response.copy_keyboard.buttons[2].copy_text == fixed_text


def test_long_copy_block_keeps_text_and_skips_copy_button():
    long_order = "\n".join(f"{100 + index} 500 1" for index in range(30))

    response = build_text_response(long_order)

    assert response.copy_keyboard is not None
    assert [button.label for button in response.copy_keyboard.buttons] == [
        "Скачать Excel для Corel",
        "Скачать Файл Малярки",
    ]
    assert response.copy_keyboard.buttons[0].action == "download_corel_excel"
    assert response.copy_keyboard.buttons[1].action == "download_malyarka_file"
    assert response.copy_keyboard.warnings == (
        "Блок слишком длинный для кнопки копирования",
    )
    assert "Скопировать подтверждённые строки:" in response.text
    assert "100 500 1" in response.text
    assert "129 500 1" in response.text
    assert "Блок слишком длинный для кнопки копирования" in response.text


def test_text_order_with_dispute_contains_copy_paste_blocks():
    message = handle_text_message("700 500\nнепонятная строка\n300 400 2")

    assert (
        "Предпросмотр заказа\n\n"
        "Подтверждённые строки:\n"
        "1. 700 500 1\n"
        "2. 300 400 2\n\n"
        "Спорные строки:\n"
        "1. непонятная строка\n\n"
        "Всего деталей: 3\n"
        "Общая площадь: 0.590 м²\n"
        "Экспорт: заблокирован\n"
        "Причина блокировки: есть спорные строки.\n\n"
        "Скопировать подтверждённые строки:\n"
        "700 500 1\n"
        "300 400 2\n\n"
        "Скопировать спорные строки:\n"
        "непонятная строка"
    ) == message


def test_messages_do_not_require_english_commands_as_main_flow():
    combined = "\n".join(
        [
            handle_text_message("здравствуйте"),
            handle_text_message("помощь"),
            handle_text_message("формат заказа"),
            handle_command_message("/start"),
            "\n".join(get_main_keyboard_labels()),
        ]
    )

    assert "/start" not in combined
    assert "/help" not in combined
    assert "/cancel" not in combined
    assert "🧾 Новый заказ" in combined
    assert "🛠 Инженер проекта" in combined
    assert "💬 Идеи / разговор" in combined
    assert "/админ" not in combined


def test_new_layer_does_not_import_old_bot_py():
    imported_names = _collect_imported_names(Path("malyarka_telegram"))

    assert "bot" not in imported_names
    assert "bot_backup_before_vision" not in imported_names


def test_new_layer_imports_openai_only_in_voice_module():
    imported_names = _collect_imported_names(
        Path("malyarka_telegram"),
        exclude_files={"voice.py"},
    )

    assert "openai" not in imported_names
    assert "vision" not in imported_names

    voice_imports = _collect_imported_names(Path("malyarka_telegram"), only_files={"voice.py"})
    assert "openai" in voice_imports


def test_app_import_and_create_app_do_not_require_token_or_aiogram():
    app = create_app(TelegramConfig(bot_token=None))

    assert app["has_token"] is False
    assert "ready" in app


def _collect_imported_names(
    root: Path,
    *,
    exclude_files: set[str] | None = None,
    only_files: set[str] | None = None,
) -> set[str]:
    imported_names: set[str] = set()

    for path in root.glob("*.py"):
        if exclude_files and path.name in exclude_files:
            continue
        if only_files and path.name not in only_files:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names.update(
                    alias.name.split(".")[0].lower() for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_names.add(node.module.split(".")[0].lower())

    return imported_names
