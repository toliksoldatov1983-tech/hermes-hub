"""Markdown transcript reports for local Malyarka dialog dry-runs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .malyarka_dialog_commands import DialogCommandResult, SAFE_BLOCKED_ACTIONS, run_dialog_script


DEFAULT_TRANSCRIPT_SCRIPTS: dict[str, list[str]] = {
    "clean": [
        "/order paint | 2 | bucket\\nroller | 3 | piece",
        "/preview",
        "/export",
        "/report",
    ],
    "disputed": [
        "/order paint | 2 | bucket\\nneeds clarification\\nbroken row\\nroller | 3 | piece",
        "/questions",
        "/resolve-all-delete",
        "/preview",
        "/export",
        "/report",
    ],
}


@dataclass(frozen=True)
class TranscriptReportResult:
    path: Path
    script_name: str
    commands_count: int
    final_status: str
    final_export_ready: bool
    final_pending_disputes: int


def build_transcript_markdown(
    *,
    script_name: str,
    commands: list[str],
    results: list[DialogCommandResult],
) -> str:
    final = results[-1] if results else None
    command_lines = "\n".join(f"{index}. `{command}`" for index, command in enumerate(commands, start=1))
    result_lines = "\n".join(
        (
            f"| {index} | `{result.command}` | `{result.status}` | "
            f"{result.confirmed_rows} | {result.pending_disputes} | "
            f"{result.resolved_disputes} | `{str(result.export_ready).lower()}` | "
            f"{result.message} |"
        )
        for index, result in enumerate(results, start=1)
    )

    return (
        "# MALYARKA_DIALOG_TRANSCRIPT\n\n"
        f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
        "## Safety\n\n"
        "This report is local dry-run only.\n\n"
        "It does not start Telegram, read tokens, read `.env`, call external APIs, "
        "touch real orders, write export files, change Google Drive, or touch old projects.\n\n"
        "## Script\n\n"
        f"- name: `{script_name}`\n"
        f"- commands: `{len(commands)}`\n"
        f"- final_status: `{final.status if final else 'none'}`\n"
        f"- final_export_ready: `{str(final.export_ready if final else False).lower()}`\n"
        f"- final_pending_disputes: `{final.pending_disputes if final else 0}`\n\n"
        f"- main_module: `{final.main_module if final else 'none'}`\n\n"
        "## Input Commands\n\n"
        f"{command_lines}\n\n"
        "## Results\n\n"
        "| # | command | status | confirmed | pending | resolved | export_ready | message |\n"
        "|---|---|---|---:|---:|---:|---|---|\n"
        f"{result_lines}\n\n"
        "## Blocked Actions\n\n"
        + "\n".join(f"- `{action}`" for action in SAFE_BLOCKED_ACTIONS)
        + "\n"
    )


def write_transcript_report(
    *,
    project_root: Path | str,
    script_name: str = "disputed",
    commands: list[str] | None = None,
    output_name: str = "MALYARKA_DIALOG_TRANSCRIPT.md",
) -> TranscriptReportResult:
    root = Path(project_root).resolve()
    selected_commands = list(commands or DEFAULT_TRANSCRIPT_SCRIPTS[script_name])
    results = run_dialog_script(selected_commands)
    output_path = root / "05_REPORTS" / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_transcript_markdown(script_name=script_name, commands=selected_commands, results=results),
        encoding="utf-8",
    )
    final = results[-1]
    return TranscriptReportResult(
        path=output_path,
        script_name=script_name,
        commands_count=len(results),
        final_status=final.status,
        final_export_ready=final.export_ready,
        final_pending_disputes=final.pending_disputes,
    )
