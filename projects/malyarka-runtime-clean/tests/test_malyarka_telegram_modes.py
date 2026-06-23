from malyarka_telegram.modes import (
    TelegramMode,
    get_mode_label,
    is_mode_command,
    mode_from_command,
)


def test_mode_commands_map_to_modes():
    assert mode_from_command("/заказ") == TelegramMode.ORDER
    assert mode_from_command("заказ") == TelegramMode.ORDER
    assert mode_from_command("новый заказ") == TelegramMode.ORDER
    assert mode_from_command("🧾 Новый заказ") == TelegramMode.ORDER
    assert mode_from_command("/чат") == TelegramMode.CHAT
    assert mode_from_command("/инженер") == TelegramMode.ENGINEER
    assert mode_from_command("инженер") == TelegramMode.ENGINEER
    assert mode_from_command("🛠 Инженер проекта") == TelegramMode.ENGINEER
    assert mode_from_command("идеи") == TelegramMode.IDEAS
    assert mode_from_command("💬 Идеи / разговор") == TelegramMode.IDEAS
    assert mode_from_command("идея") is None
    assert mode_from_command("/выжимка") == TelegramMode.SUMMARY
    assert mode_from_command("/правила") == TelegramMode.RULES


def test_mode_commands_ignore_extra_text_and_case():
    assert mode_from_command(" /ЗАКАЗ 1000*400 ") == TelegramMode.ORDER
    assert mode_from_command(" ЗАКАЗ ") == TelegramMode.ORDER


def test_unknown_command_is_not_mode_command():
    assert mode_from_command("/unknown") is None
    assert is_mode_command("/unknown") is False


def test_empty_text_is_not_mode_command():
    assert mode_from_command("") is None
    assert mode_from_command(None) is None
    assert is_mode_command("") is False
    assert is_mode_command(None) is False


def test_mode_label_is_safe():
    assert get_mode_label(TelegramMode.ORDER) == "режим заказа"
    assert get_mode_label("chat") == "режим чата"
    assert get_mode_label("unknown") == "нейтральный режим"
    assert get_mode_label(None) == "нейтральный режим"
