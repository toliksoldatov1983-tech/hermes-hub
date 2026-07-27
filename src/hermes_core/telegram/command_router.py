"""Telegram command router — maps dry-run slash commands to responses.

Expanded with order/scenarios, disputes, fix, export-blocked, and audit commands.
All commands run in dry-run mode — no live Telegram, no token, no network.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from hermes_core.report_index import LocalReportIndex
from hermes_core.safety.action_policy import classify_action
from hermes_core.safety.audit_log import LocalAuditLog
from hermes_core.start_summary import LocalStartSummaryBuilder
from hermes_core.telegram.blocked_actions import BLOCKED, blocked_labels
from hermes_modules.malyarka.combined_preview import build_combined_preview
from hermes_modules.malyarka.demo import build_demo
from hermes_modules.malyarka.dispute_classifier import build_fixture_dispute_summary
from hermes_modules.malyarka.fixtures import run_all_fixtures


PROJECT_ROOT = Path(__file__).resolve().parents[3]

# ── Shared blocked/warning constants ──

BLOCKED_REAL_ORDER = ["Real order access is blocked.", "File export is blocked.", "Live Telegram send is blocked."]
BLOCKED_EXPORT = ["Real file export is blocked.", "Excel/Corel output is blocked."]
WARNING_SYNTHETIC = ["Input is treated as synthetic/manual test text only.", "No files, archives or real orders are read."]


@dataclass(frozen=True)
class DryRunCommandResponse:
    command: str
    planned_response: str
    blocked_actions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    next_step: str = "Continue local dry-run work."
    payload: dict[str, str] = field(default_factory=dict)


def normalize_command(text: str) -> tuple[str, str]:
    stripped = text.strip()
    if not stripped:
        return "/status", ""
    first, _, rest = stripped.partition(" ")
    return first.lower(), rest.strip()


class TelegramCommandRouter:
    def route(self, text: str) -> DryRunCommandResponse:
        command, argument = normalize_command(text)
        handlers: dict[str, Callable[[str, str], DryRunCommandResponse]] = {
            "/status": self._status,
            "/task": self._task,
            "/memory": self._memory,
            "/malyarka": self._malyarka,
            "/malyarka-combined": self._malyarka_combined,
            "/engineer": self._engineer,
            "/report": self._report,
            "/check": self._check,
            # ── New commands ──
            "/order": self._order,
            "/disputes": self._disputes,
            "/fix": self._fix,
            "/export-blocked": self._export_blocked,
            "/audit": self._audit,
            "/safety": self._safety,
            "/blocked": self._blocked_actions_list,
            # ── Russian aliases ──
            "/статус": self._status,
            "/задача": self._task,
            "/память": self._memory,
            "/малярка": self._malyarka,
            "/инженер": self._engineer,
            "/отчёт": self._report,
            "/заказ": self._order,
            "/споры": self._disputes,
            "/исправить": self._fix,
            "/экспорт-заблокирован": self._export_blocked,
            "/аудит": self._audit,
        }
        handler = handlers.get(command)
        if handler is None:
            handler = self._legacy_mojibake_handler(command, argument)
        if handler is None and argument:
            handler = self._malyarka
        if handler is None:
            return DryRunCommandResponse(
                command=command,
                planned_response="Command is not recognized in dry-run mode.",
                warnings=["Available: /status /order /disputes /fix /export-blocked /malyarka /report /check /audit /safety /blocked"],
                next_step="Use one of the supported dry-run commands.",
                payload={"argument": argument},
            )
        return handler(command, argument)

    def _legacy_mojibake_handler(self, command: str, argument: str) -> Callable[[str, str], DryRunCommandResponse] | None:
        if "\ufffd" in command:
            return self._malyarka if argument else self._status
        if command.startswith("/с"):
            return self._status
        if command.startswith("/рј"):
            return self._malyarka
        if command.startswith("/р·"):
            return self._task
        if command.startswith("/рї"):
            return self._memory
        if command.startswith("/рё"):
            return self._engineer
        if command.startswith("/рѕ"):
            return self._report
        return None

    def _read_file_preview(self, relative_path: str, fallback: str) -> str:
        path = PROJECT_ROOT / relative_path
        if not path.exists():
            return fallback
        text = path.read_text(encoding="utf-8-sig")
        lines = [line.strip().replace("\ufeff", "") for line in text.splitlines() if line.strip()]
        return " ".join(lines[:4]) if lines else fallback

    # ── Core commands (existing) ──

    def _status(self, command: str, _: str) -> DryRunCommandResponse:
        summary = LocalStartSummaryBuilder(PROJECT_ROOT).build()
        return DryRunCommandResponse(
            command=command,
            planned_response="Hermes-Clean is running locally in dry-run mode.",
            next_step="Open NEXT_TASK.md or choose the next safe local block.",
            payload={
                "mode": "dry-run",
                "source_of_truth": "Hermes-Clean",
                "health_status": summary.health_status,
                "next_task": summary.next_task,
                "reports_count": str(summary.reports_count),
            },
        )

    def _task(self, command: str, _: str) -> DryRunCommandResponse:
        preview = self._read_file_preview("03_TASKS/NEXT_TASK.md", "No next task recorded.")
        return DryRunCommandResponse(
            command=command,
            planned_response="Current next task is loaded from NEXT_TASK.md.",
            next_step="Continue only if the task is local-safe or approved.",
            payload={"next_task_preview": preview},
        )

    def _memory(self, command: str, _: str) -> DryRunCommandResponse:
        decisions = self._read_file_preview("00_START/PROJECT_DECISIONS.md", "Project decisions file not found.")
        prohibitions = self._read_file_preview("00_START/PROJECT_PROHIBITIONS.md", "Project prohibitions file not found.")
        return DryRunCommandResponse(
            command=command,
            planned_response="Project memory is loaded only from Hermes-Clean.",
            next_step="Use Hermes-Clean memory files; do not import old memory automatically.",
            payload={"decisions": decisions, "prohibitions": prohibitions},
        )

    def _malyarka(self, command: str, argument: str) -> DryRunCommandResponse:
        demo = build_demo()
        return DryRunCommandResponse(
            command=command,
            planned_response="Malyarka is available as a local synthetic dry-run module.",
            blocked_actions=["Real order access is blocked.", "Final export is blocked."],
            warnings=["Old Malyarka documents and real orders are not touched."],
            next_step="Use /malyarka-combined, /order, /disputes or /fix locally.",
            payload={
                "input_preview": argument[:120],
                "module": "hermes_modules.malyarka",
                "fixtures": str(demo.fixtures_count),
                "workflow_status": demo.workflow_status,
                "export_gated": str(demo.export_gated),
            },
        )

    def _malyarka_combined(self, command: str, argument: str) -> DryRunCommandResponse:
        preview = build_combined_preview(argument)
        return DryRunCommandResponse(
            command=command,
            planned_response="Malyarka combined preview is available in Telegram dry-run mode.",
            blocked_actions=BLOCKED_REAL_ORDER,
            warnings=WARNING_SYNTHETIC,
            next_step="Use scripts\\hermes.cmd malyarka-combined locally for full details.",
            payload={
                "source_mode": preview.source_mode,
                "confirmed_rows": str(preview.confirmed_count),
                "disputed_rows": str(preview.disputed_count),
                "final_ready": str(preview.final_ready),
                "pricing_total": str(preview.pricing.total),
                "can_write_file": str(preview.can_write_file),
                "can_use_as_real_order": str(preview.can_use_as_real_order),
            },
        )

    def _engineer(self, command: str, _: str) -> DryRunCommandResponse:
        return DryRunCommandResponse(
            command=command,
            planned_response="Engineering dry-run mode: local tests and safety gate only.",
            next_step="Run scripts\\run_tests.cmd or scripts\\hermes.cmd safety delete.",
            payload={"tests": "scripts\\run_tests.cmd", "safety": "scripts\\hermes.cmd safety delete"},
        )

    def _report(self, command: str, _: str) -> DryRunCommandResponse:
        reports = LocalReportIndex(PROJECT_ROOT).snapshot()
        return DryRunCommandResponse(
            command=command,
            planned_response="Local report index is ready.",
            next_step="Run scripts\\hermes.cmd reports for details.",
            payload={
                "reports_count": str(reports.reports_count),
                "next_task": reports.task_snapshot.next_task,
                "done_count": str(reports.task_snapshot.done_count),
            },
        )

    def _check(self, command: str, _: str) -> DryRunCommandResponse:
        from hermes_core.smoke import LocalSmokeTester
        smoke = LocalSmokeTester(PROJECT_ROOT).run()
        return DryRunCommandResponse(
            command=command,
            planned_response="Local smoke check completed in dry-run mode.",
            next_step="Run scripts\\hermes.cmd smoke for full details.",
            payload={
                "smoke_status": smoke.status,
                "checks": str(len(smoke.checks)),
                "failed": str(len(smoke.failed_checks)),
            },
        )

    # ── New commands ──

    def _order(self, command: str, argument: str) -> DryRunCommandResponse:
        """Show synthetic order flow."""
        if not argument:
            fixtures = run_all_fixtures()
            return DryRunCommandResponse(
                command=command,
                planned_response="Synthetic Malyarka fixtures (dry-run only).",
                blocked_actions=["Real order access is blocked."],
                warnings=["These are 100% synthetic fixtures. No real client data."],
                next_step="Use '/order <text>' or '/malyarka-combined <text>' for custom input.",
                payload={
                    "fixtures_count": str(len(fixtures)),
                    "ready_fixtures": str(sum(1 for f in fixtures if f.final_ready)),
                },
            )
        preview = build_combined_preview(argument)
        return DryRunCommandResponse(
            command=command,
            planned_response=f"Order preview: {preview.confirmed_count} confirmed, {preview.disputed_count} disputed.",
            blocked_actions=BLOCKED_REAL_ORDER,
            warnings=WARNING_SYNTHETIC,
            next_step="If disputed rows exist, use /disputes to see details or /fix to resolve.",
            payload={
                "confirmed": str(preview.confirmed_count),
                "disputed": str(preview.disputed_count),
                "final_ready": str(preview.final_ready),
                "can_use_as_real_order": str(preview.can_use_as_real_order),
            },
        )

    def _disputes(self, command: str, argument: str) -> DryRunCommandResponse:
        """Show dispute classification."""
        if argument:
            preview = build_combined_preview(argument)
            cats = preview.dispute_categories
            return DryRunCommandResponse(
                command=command,
                planned_response=f"Disputes found: {preview.disputed_count} rows.",
                blocked_actions=BLOCKED_REAL_ORDER,
                warnings=WARNING_SYNTHETIC,
                next_step="Use /fix to resolve disputes or inspect with /malyarka-combined.",
                payload={
                    "disputed_count": str(preview.disputed_count),
                    "categories": ", ".join(f"{k}={v}" for k, v in sorted(cats.items())),
                },
            )
        summary = build_fixture_dispute_summary()
        return DryRunCommandResponse(
            command=command,
            planned_response="Synthetic dispute classification summary.",
            blocked_actions=["Real order access is blocked."],
            warnings=["Fixture-based dispute stats only. Not real orders."],
            next_step="Use '/disputes <text>' to classify a specific input.",
            payload={
                "total_disputes": str(sum(summary.categories.values())),
                "categories": ", ".join(f"{k}={v}" for k, v in sorted(summary.categories.items())),
            },
        )

    def _fix(self, command: str, argument: str) -> DryRunCommandResponse:
        """Show how to fix a disputed row."""
        return DryRunCommandResponse(
            command=command,
            planned_response="Dispute fix is available in dry-run mode only.",
            blocked_actions=["Real file modification is blocked.", "Real order change is blocked."],
            warnings=["Fix suggestions are synthetic. They do not modify any real files or orders."],
            next_step="Use scripts\\hermes.cmd malyarka-resolve --replacement '<corrected>' for local dry-run fix.",
            payload={
                "argument": argument[:200] if argument else "(no input)",
                "available_tools": "malyarka-resolve, malyarka-combined",
            },
        )

    def _export_blocked(self, command: str, _: str) -> DryRunCommandResponse:
        """Explain why export is blocked."""
        blocked = blocked_labels()
        return DryRunCommandResponse(
            command=command,
            planned_response="Export is blocked in dry-run mode. Here is why:",
            blocked_actions=[f"{ba}" for ba in blocked if "export" in ba.lower() or "file" in ba.lower()][:5],
            warnings=["All exports are synthetic/manual only. No real files are created."],
            next_step="Export will be allowed only after APPROVE_TELEGRAM_LIVE gate and with clean orders only.",
            payload={
                "blocked_count": str(len(blocked)),
                "blocked_categories": "telegram, export, secrets, orders, external",
            },
        )

    def _audit(self, command: str, _: str) -> DryRunCommandResponse:
        """Show safety audit log summary."""
        audit = LocalAuditLog(PROJECT_ROOT)
        snapshot = audit.snapshot()
        return DryRunCommandResponse(
            command=command,
            planned_response=f"Audit log: {snapshot.total_entries} entries.",
            warnings=[],
            next_step="Use scripts\\hermes.cmd safety-audit for full log.",
            payload={
                "total": str(snapshot.total_entries),
                "safe": str(snapshot.safe_count),
                "confirm_required": str(snapshot.confirm_count),
                "blocked": str(snapshot.blocked_count),
            },
        )

    def _safety(self, command: str, argument: str) -> DryRunCommandResponse:
        """Classify an action via safety gate."""
        action_type = argument.strip() or "dry_run"
        policy = classify_action(action_type)
        response = DryRunCommandResponse(
            command=command,
            planned_response=f"Action '{action_type}' classified as {policy.decision.value}.",
            next_step="Use /audit to see the full audit log.",
            payload={
                "action": action_type,
                "decision": policy.decision.value,
                "reason": policy.reason,
            },
        )
        if policy.decision.value == "BLOCKED":
            response = DryRunCommandResponse(
                command=command,
                planned_response=response.planned_response,
                blocked_actions=[f"Action '{action_type}' is {policy.decision.value}: {policy.reason}"],
                warnings=response.warnings,
                next_step=response.next_step,
                payload=response.payload,
            )
        return response

    def _blocked_actions_list(self, command: str, _: str) -> DryRunCommandResponse:
        """List all blocked actions in dry-run mode."""
        summary = {}
        for ba in BLOCKED:
            summary.setdefault(ba.category, []).append(ba.label)
        return DryRunCommandResponse(
            command=command,
            planned_response=f"All {len(BLOCKED)} actions blocked in dry-run mode.",
            blocked_actions=[f"{ba.category}: {ba.label}" for ba in BLOCKED],
            warnings=["This list is enforced by Hermes-Clean safety gate."],
            next_step="Use /safety <action> to classify a specific action.",
            payload={
                "total_blocked": str(len(BLOCKED)),
                "categories": ", ".join(f"{k}={len(v)}" for k, v in summary.items()),
            },
        )
