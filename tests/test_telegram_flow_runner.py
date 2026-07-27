from hermes_clean.telegram_flow_runner import format_run_result, run_telegram_flow_case, run_telegram_flow_text


def test_clean_case_finishes_without_disputes():
    result = run_telegram_flow_case("clean")
    assert result.scenario == "clean"
    assert result.confirmed_rows == 2
    assert result.initial_disputes == 0
    assert result.final_disputes == 0
    assert result.export_ready is True
    assert "telegram_token_read" in result.blocked_actions


def test_disputed_case_resolves_locally():
    result = run_telegram_flow_case("disputed")
    assert result.scenario == "disputed"
    assert result.initial_disputes == 2
    assert result.resolved_disputes == 2
    assert result.final_disputes == 0
    assert result.export_ready is True
    assert "show_final_report" in result.steps


def test_custom_text_can_keep_export_blocked():
    result = run_telegram_flow_text("paint | 2 | bucket\nunknown line", auto_delete_disputes=False)
    assert result.confirmed_rows == 1
    assert result.initial_disputes == 1
    assert result.final_disputes == 1
    assert result.export_ready is False


def test_format_is_ascii_safe_summary():
    result = run_telegram_flow_case("clean")
    text = format_run_result(result)
    assert "telegram_flow=dry-run" in text
    assert "scenario=clean" in text
    assert "blocked_actions=" in text
    assert "steps:" in text
