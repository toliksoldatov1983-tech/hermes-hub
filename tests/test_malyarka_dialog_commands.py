from hermes_clean.malyarka_dialog_commands import (
    MalyarkaDialogCommandSession,
    format_script_results,
    run_dialog_script,
)


def test_clean_dialog_script_reaches_export_ready():
    results = run_dialog_script([
        "/order paint | 2 | bucket\\nroller | 3 | piece",
        "/preview",
        "/export",
        "/report",
    ])
    assert results[-1].export_ready is True
    assert results[-1].pending_disputes == 0
    assert results[-1].confirmed_rows == 2


def test_disputed_dialog_script_resolves_all_delete():
    results = run_dialog_script([
        "/order paint | 2 | bucket\\nneeds clarification\\nbroken row\\nroller | 3 | piece",
        "/questions",
        "/resolve-all-delete",
        "/preview",
        "/export",
    ])
    assert results[0].pending_disputes == 2
    assert results[-1].status == "ok"
    assert results[-1].export_ready is True
    assert results[-1].resolved_disputes == 2


def test_export_is_blocked_before_order_and_before_resolution():
    session = MalyarkaDialogCommandSession()
    before_order = session.run("/export")
    assert before_order.status == "blocked"
    session.run("/order paint | 2 | bucket\\nunknown")
    blocked = session.run("/export")
    assert blocked.status == "blocked"
    assert blocked.export_ready is False


def test_unknown_command_is_blocked():
    session = MalyarkaDialogCommandSession()
    result = session.run("/send-live")
    assert result.status == "blocked"
    assert "command" in result.message.lower() or "команда" in result.message.lower()
    assert "live_telegram_send" in result.blocked_actions


def test_dialog_uses_main_malyarka_module():
    result = run_dialog_script(["/order paint | 2 | bucket"])[0]
    assert result.main_module == "hermes_modules.malyarka"


def test_formatted_script_result_is_ascii_safe_summary():
    text = format_script_results(run_dialog_script(["/help"]))
    assert "malyarka_dialog=dry-run" in text
    assert "blocked_actions=" in text
    assert "commands=" in text
