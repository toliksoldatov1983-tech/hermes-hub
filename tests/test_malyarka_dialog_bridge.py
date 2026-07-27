from hermes_modules.malyarka.dialog_bridge import MalyarkaDialogBridgeSession, run_dialog_bridge_script


def test_dialog_bridge_uses_main_module_and_blocks_disputed_export():
    session = MalyarkaDialogBridgeSession()

    first = session.run("/order paint | 2 | bucket\\nneeds clarification")
    blocked = session.run("/export")

    assert first.main_module == "hermes_modules.malyarka"
    assert first.confirmed_rows == 1
    assert first.pending_disputes == 1
    assert blocked.status == "blocked"
    assert blocked.export_ready is False


def test_dialog_bridge_questions_are_based_on_main_module_disputes():
    session = MalyarkaDialogBridgeSession()
    session.run("/order paint | many | bucket")

    questions = session.run("/questions")

    assert questions.status == "ok"
    assert "positive numeric quantity" in questions.message


def test_dialog_bridge_resolve_all_delete_reaches_export_ready():
    results = run_dialog_bridge_script([
        "/order paint | 2 | bucket\\nneeds clarification\\nbroken row\\nroller | 3 | piece",
        "/questions",
        "/resolve-all-delete",
        "/export",
        "/report",
    ])

    assert results[0].pending_disputes == 2
    assert results[-1].confirmed_rows == 2
    assert results[-1].pending_disputes == 0
    assert results[-1].export_ready is True
    assert results[-1].main_module == "hermes_modules.malyarka"
