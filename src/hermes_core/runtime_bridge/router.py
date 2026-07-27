"""Runtime bridge router — routes bridge requests to existing Hermes-Clean modules.

Does NOT duplicate logic. Calls existing functions/modules directly.
"""

from __future__ import annotations

from pathlib import Path

from hermes_core.runtime_bridge.contract import (
    ACTION_TO_ROUTE,
    BridgeActionType,
    BridgeRequest,
    BridgeResponse,
)
from hermes_core.runtime_bridge.safety import get_default_policy

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class BridgeRouter:
    """Routes bridge requests to Hermes-Clean commands.

    Safety policy is checked FIRST. Then existing command functions are called.
    """

    def __init__(self) -> None:
        self._policy = get_default_policy()
        self._route = ACTION_TO_ROUTE.get

    def handle(self, request: BridgeRequest) -> BridgeResponse:
        """Handle a bridge request: check safety, then route.

        Returns BridgeResponse with status OK/BLOCKED/ERROR.
        """
        # 1. Safety check
        block = self._policy.check(request)
        if block is not None:
            return block

        # 2. Route to handler
        action = request.action
        route_name = self._route(action) or action.name.lower()

        try:
            handler = _HANDLERS.get(action)
            if handler is None:
                return BridgeResponse.error_action(
                    action.name,
                    f"No handler for action '{action.name}'",
                )

            output_lines = handler(request)
            return BridgeResponse.ok_action(
                action.name,
                output_lines=output_lines,
                route=route_name,
            )

        except Exception as exc:
            return BridgeResponse.error_action(
                action.name,
                f"Bridge routing error: {exc}",
            )

    def route_text(self, action_text: str) -> BridgeResponse:
        """Convenience: handle a text-based action name."""
        request = BridgeRequest.from_string(action_text)
        return self.handle(request)


# ── Handlers — call existing Hermes-Clean functions ──


def _capture_stdout(fn, *args, **kwargs) -> list[str]:
    """Capture print output from a function into a list of lines."""
    import io
    import sys
    old_stdout = sys.stdout
    buf = io.StringIO()
    try:
        sys.stdout = buf
        fn(*args, **kwargs)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue().strip().splitlines()


def _status_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import status_command
    import argparse
    return _capture_stdout(status_command, argparse.Namespace())


def _dashboard_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import dashboard_command
    import argparse
    return _capture_stdout(dashboard_command, argparse.Namespace())


def _daily_report_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import daily_report_command
    import argparse
    return _capture_stdout(daily_report_command, argparse.Namespace())


def _daily_assistant_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import daily_assistant_command
    import argparse
    return _capture_stdout(daily_assistant_command, argparse.Namespace())


def _daily_brief_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import daily_brief_command
    import argparse
    return _capture_stdout(daily_brief_command, argparse.Namespace())


def _what_next_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import what_next_command
    import argparse
    return _capture_stdout(what_next_command, argparse.Namespace())


def _local_health_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import local_health_command
    import argparse
    return _capture_stdout(local_health_command, argparse.Namespace())


def _project_status_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import project_status_command
    import argparse
    return _capture_stdout(project_status_command, argparse.Namespace())


def _malyarka_status_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import malyarka_status_command
    import argparse
    return _capture_stdout(malyarka_status_command, argparse.Namespace())


def _malyarka_dialog_handler(req: BridgeRequest) -> list[str]:
    from hermes_core.cli import malyarka_dialog_command
    import argparse
    script = req.payload.get("script", "clean")
    return _capture_stdout(
        malyarka_dialog_command,
        argparse.Namespace(script=script, commands=[]),
    )


def _malyarka_transcript_handler(req: BridgeRequest) -> list[str]:
    from hermes_core.cli import malyarka_transcript_command
    import argparse
    script = req.payload.get("script", "clean")
    return _capture_stdout(
        malyarka_transcript_command,
        argparse.Namespace(script=script, output="BRIDGE_TRANSCRIPT.md"),
    )


def _malyarka_fixtures_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import malyarka_fixtures_command
    import argparse
    return _capture_stdout(malyarka_fixtures_command, argparse.Namespace())


def _malyarka_combined_handler(req: BridgeRequest) -> list[str]:
    from hermes_core.cli import malyarka_combined_command
    import argparse
    text = req.payload.get("text", [])
    return _capture_stdout(
        malyarka_combined_command,
        argparse.Namespace(text=text if isinstance(text, list) else [text]),
    )


def _telegram_flow_handler(req: BridgeRequest) -> list[str]:
    from hermes_core.cli import telegram_flow_command
    import argparse
    case = req.payload.get("case", "clean")
    return _capture_stdout(
        telegram_flow_command,
        argparse.Namespace(case=case, text=[], auto_resolve=True),
    )


def _ai_provider_status_handler(req: BridgeRequest) -> list[str]:
    from hermes_core.cli import ai_provider_status_command
    import argparse
    pid = req.payload.get("provider_id", "mock")
    return _capture_stdout(
        ai_provider_status_command,
        argparse.Namespace(provider_id=pid, approved=False),
    )


def _ai_provider_list_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import ai_provider_list_command
    import argparse
    return _capture_stdout(ai_provider_list_command, argparse.Namespace())


def _secret_gate_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import secret_gate_command
    import argparse
    return _capture_stdout(secret_gate_command, argparse.Namespace())


def _project_audit_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import project_audit_command
    import argparse
    return _capture_stdout(project_audit_command, argparse.Namespace())


def _smoke_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import smoke_command
    import argparse
    return _capture_stdout(smoke_command, argparse.Namespace())


def _help_local_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import help_local_command
    import argparse
    return _capture_stdout(help_local_command, argparse.Namespace())


def _memory_handler(_req: BridgeRequest) -> list[str]:
    from hermes_core.cli import memory_command
    import argparse
    return _capture_stdout(memory_command, argparse.Namespace())


# ── Handler registry ──

_HANDLERS: dict[BridgeActionType, callable] = {
    BridgeActionType.STATUS: _status_handler,
    BridgeActionType.DASHBOARD: _dashboard_handler,
    BridgeActionType.DAILY_REPORT: _daily_report_handler,
    BridgeActionType.DAILY_ASSISTANT: _daily_assistant_handler,
    BridgeActionType.DAILY_BRIEF: _daily_brief_handler,
    BridgeActionType.WHAT_NEXT: _what_next_handler,
    BridgeActionType.LOCAL_HEALTH: _local_health_handler,
    BridgeActionType.PROJECT_STATUS: _project_status_handler,
    BridgeActionType.MALYARKA_STATUS: _malyarka_status_handler,
    BridgeActionType.MALYARKA_DIALOG: _malyarka_dialog_handler,
    BridgeActionType.MALYARKA_TRANSCRIPT: _malyarka_transcript_handler,
    BridgeActionType.MALYARKA_FIXTURES: _malyarka_fixtures_handler,
    BridgeActionType.MALYARKA_COMBINED: _malyarka_combined_handler,
    BridgeActionType.TELEGRAM_FLOW_DRY_RUN: _telegram_flow_handler,
    BridgeActionType.AI_PROVIDER_STATUS: _ai_provider_status_handler,
    BridgeActionType.AI_PROVIDER_LIST: _ai_provider_list_handler,
    BridgeActionType.SECRET_GATE_STATUS: _secret_gate_handler,
    BridgeActionType.PROJECT_AUDIT: _project_audit_handler,
    BridgeActionType.SMOKE: _smoke_handler,
    BridgeActionType.HELP_LOCAL: _help_local_handler,
    BridgeActionType.MEMORY_SNAPSHOT: _memory_handler,
}
