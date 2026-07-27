from pathlib import Path

from hermes_clean.malyarka_dialog_commands import run_dialog_script
from hermes_clean.malyarka_transcript_report import build_transcript_markdown, write_transcript_report


def test_build_transcript_markdown_contains_safety_and_results():
    commands = ["/order paint | 2 | bucket", "/export"]
    results = run_dialog_script(commands)
    text = build_transcript_markdown(script_name="unit", commands=commands, results=results)
    assert "# MALYARKA_DIALOG_TRANSCRIPT" in text
    assert "local dry-run only" in text
    assert "real orders" in text
    assert "| # | command | status | confirmed | pending | resolved | export_ready | message |" in text
    assert "hermes_modules.malyarka" in text


def test_write_transcript_report_creates_markdown(tmp_path: Path):
    result = write_transcript_report(project_root=tmp_path, script_name="disputed")
    assert result.path.exists()
    assert result.commands_count == 6
    assert result.final_status == "ok"
    assert result.final_export_ready is True
    assert result.final_pending_disputes == 0
    text = result.path.read_text(encoding="utf-8")
    assert "MALYARKA_DIALOG_TRANSCRIPT" in text
    assert "live_telegram_send" in text


def test_clean_transcript_is_export_ready(tmp_path: Path):
    result = write_transcript_report(project_root=tmp_path, script_name="clean")
    assert result.commands_count == 4
    assert result.final_export_ready is True
    assert result.final_pending_disputes == 0
