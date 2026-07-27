"""Compatibility wrappers for Malyarka dialog dry-runs.

The active business logic lives in ``hermes_modules.malyarka``. This module
keeps the old ``hermes_clean`` import path stable for CLI/tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from hermes_modules.malyarka.dialog_bridge import (
    SAFE_BLOCKED_ACTIONS,
    MalyarkaDialogBridgeSession,
)


@dataclass(frozen=True)
class DialogCommandResult:
    command: str
    status: str
    message: str
    confirmed_rows: int
    pending_disputes: int
    resolved_disputes: int
    export_ready: bool
    main_module: str = "hermes_modules.malyarka"
    blocked_actions: tuple[str, ...] = SAFE_BLOCKED_ACTIONS


@dataclass
class MalyarkaDialogCommandSession:
    """Compatibility shell backed by the main Malyarka module."""

    bridge: MalyarkaDialogBridgeSession = field(default_factory=MalyarkaDialogBridgeSession)

    def run(self, line: str) -> DialogCommandResult:
        result = self.bridge.run(line)
        return DialogCommandResult(
            command=result.command,
            status=result.status,
            message=result.message,
            confirmed_rows=result.confirmed_rows,
            pending_disputes=result.pending_disputes,
            resolved_disputes=result.resolved_disputes,
            export_ready=result.export_ready,
            main_module=result.main_module,
            blocked_actions=result.blocked_actions,
        )

    @staticmethod
    def help_text() -> str:
        return MalyarkaDialogBridgeSession.help_text()


def run_dialog_script(lines: list[str]) -> list[DialogCommandResult]:
    session = MalyarkaDialogCommandSession()
    return [session.run(line) for line in lines]


def format_command_result(result: DialogCommandResult) -> str:
    return "\n".join(
        [
            f"command={result.command}",
            f"status={result.status}",
            f"message={result.message}",
            f"confirmed_rows={result.confirmed_rows}",
            f"pending_disputes={result.pending_disputes}",
            f"resolved_disputes={result.resolved_disputes}",
            f"export_ready={str(result.export_ready).lower()}",
            f"blocked_actions={','.join(result.blocked_actions)}",
        ]
    )


def format_script_results(results: list[DialogCommandResult]) -> str:
    lines = ["malyarka_dialog=dry-run", f"commands={len(results)}"]
    for index, result in enumerate(results, start=1):
        lines.append(
            f"- {index}: command={result.command}; status={result.status}; "
            f"confirmed={result.confirmed_rows}; pending={result.pending_disputes}; "
            f"resolved={result.resolved_disputes}; export_ready={str(result.export_ready).lower()}; "
            f"module={result.main_module}; message={result.message}"
        )
    lines.append(f"blocked_actions={','.join(SAFE_BLOCKED_ACTIONS)}")
    return "\n".join(lines)
