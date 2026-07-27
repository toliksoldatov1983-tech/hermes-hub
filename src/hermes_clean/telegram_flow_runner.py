"""ASCII-safe local runner for the Hermes-Clean Telegram dialog flow.

This module is intentionally local-only:
- no Telegram connection;
- no tokens or environment files;
- no external APIs;
- no real orders;
- no file export.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from hermes_modules.malyarka.dialog_bridge import MalyarkaDialogBridgeSession


FlowCase = Literal["clean", "disputed"]


@dataclass(frozen=True)
class TelegramFlowRunResult:
    scenario: str
    confirmed_rows: int
    initial_disputes: int
    resolved_disputes: int
    final_disputes: int
    final_phase: str
    export_ready: bool
    blocked_actions: tuple[str, ...]
    warnings: tuple[str, ...]
    steps: tuple[str, ...]


DEFAULT_CASE_INPUTS: dict[FlowCase, str] = {
    "clean": "paint | 2 | bucket\nroller | 3 | piece",
    "disputed": "paint | 2 | bucket\nneeds clarification\nbroken row\nroller | 3 | piece",
}


def _finish_result(
    *,
    scenario: str,
    session: MalyarkaDialogBridgeSession,
    initial_disputes: int,
    steps: list[str],
) -> TelegramFlowRunResult:
    order = session.order
    confirmed_rows = len(order.confirmed_rows) if order else 0
    final_disputes = len(order.disputed_rows) if order else 0
    export_ready = confirmed_rows > 0 and final_disputes == 0

    blocked_actions = [
        "live_telegram_send",
        "telegram_token_read",
        "external_api_call",
        "real_order_access",
        "file_export_write",
    ]

    warnings = [
        "dry_run_only",
        "synthetic_or_manual_test_input_only",
        "export_status_is_policy_check_only",
    ]

    return TelegramFlowRunResult(
        scenario=scenario,
        confirmed_rows=confirmed_rows,
        initial_disputes=initial_disputes,
        resolved_disputes=session.resolved_disputes,
        final_disputes=final_disputes,
        final_phase="done" if export_ready else "blocked",
        export_ready=export_ready,
        blocked_actions=tuple(blocked_actions),
        warnings=tuple(warnings),
        steps=tuple(steps),
    )


def run_telegram_flow_text(raw_text: str, *, auto_delete_disputes: bool = True) -> TelegramFlowRunResult:
    """Run one local Telegram-style dialog from raw text.

    Disputed rows are auto-deleted by default because this runner is a dry-run
    smoke path. It proves the dialog can progress without touching real data.
    """

    session = MalyarkaDialogBridgeSession()
    steps: list[str] = []

    session.run(f"/order {raw_text}")
    steps.append("receive_order")

    initial_disputes = len(session.order.disputed_rows) if session.order else 0
    if initial_disputes:
        session.run("/questions")
        steps.append("ask_questions")

    if auto_delete_disputes:
        disputed_count = len(session.order.disputed_rows) if session.order else 0
        if disputed_count:
            session.run("/resolve-all-delete")
            steps.append("resolve_all_disputes:delete")

    session.run("/preview")
    steps.append("show_preview")

    session.run("/export")
    steps.append("check_export_status")

    session.run("/report")
    steps.append("show_final_report")

    return _finish_result(
        scenario="custom",
        session=session,
        initial_disputes=initial_disputes,
        steps=steps,
    )


def run_telegram_flow_case(case: FlowCase) -> TelegramFlowRunResult:
    if case not in DEFAULT_CASE_INPUTS:
        raise ValueError(f"Unknown Telegram flow case: {case}")
    result = run_telegram_flow_text(DEFAULT_CASE_INPUTS[case], auto_delete_disputes=True)
    return TelegramFlowRunResult(
        scenario=case,
        confirmed_rows=result.confirmed_rows,
        initial_disputes=result.initial_disputes,
        resolved_disputes=result.resolved_disputes,
        final_disputes=result.final_disputes,
        final_phase=result.final_phase,
        export_ready=result.export_ready,
        blocked_actions=result.blocked_actions,
        warnings=result.warnings,
        steps=result.steps,
    )


def format_run_result(result: TelegramFlowRunResult) -> str:
    lines = [
        "telegram_flow=dry-run",
        f"scenario={result.scenario}",
        f"confirmed_rows={result.confirmed_rows}",
        f"initial_disputes={result.initial_disputes}",
        f"resolved_disputes={result.resolved_disputes}",
        f"final_disputes={result.final_disputes}",
        f"final_phase={result.final_phase}",
        f"export_ready={str(result.export_ready).lower()}",
        f"blocked_actions={','.join(result.blocked_actions)}",
        f"warnings={','.join(result.warnings)}",
        "steps:",
    ]
    lines.extend(f"- {step}" for step in result.steps)
    return "\n".join(lines)
