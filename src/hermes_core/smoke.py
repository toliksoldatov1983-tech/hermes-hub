from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hermes_core.ai.provider_factory import ProviderConfig, ProviderFactory
from hermes_core.command_help import build_command_help
from hermes_core.health import LocalHealthChecker
from hermes_core.memory.local_memory_store import LocalProjectMemoryStore
from hermes_core.project_audit import LocalProjectAudit
from hermes_core.report_index import LocalReportIndex
from hermes_core.review.review_provider_factory import ReviewProviderConfig, ReviewProviderFactory
from hermes_core.runtime_status import LocalRuntimeStatusBuilder
from hermes_core.safety.action_policy import classify_action
from hermes_core.start_summary import LocalStartSummaryBuilder
from hermes_core.tasks.task_status_store import LocalTaskStatusStore
from hermes_core.telegram.dry_run_gateway import TelegramDryRunGateway
from hermes_core.telegram.message_contract import TelegramMessage
from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.demo import build_demo
from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.fixtures import run_all_fixtures
from hermes_modules.malyarka.schema_contract import export_preview_columns
from hermes_modules.malyarka.synthetic_pricing import build_synthetic_pricing_preview
from hermes_modules.malyarka.dispute_classifier import build_fixture_dispute_summary
from hermes_modules.malyarka.combined_preview import build_combined_preview
from hermes_clean.telegram_flow_runner import run_telegram_flow_case
from hermes_clean.malyarka_dialog_commands import run_dialog_script
from hermes_clean.malyarka_transcript_report import write_transcript_report


@dataclass(frozen=True)
class SmokeCheck:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class SmokeReport:
    checks: list[SmokeCheck]

    @property
    def status(self) -> str:
        return "OK" if all(check.ok for check in self.checks) else "ATTENTION"

    @property
    def failed_checks(self) -> list[SmokeCheck]:
        return [check for check in self.checks if not check.ok]


class LocalSmokeTester:
    """Runs safe local smoke checks without external services."""

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def run(self, include_daily_report: bool = True) -> SmokeReport:
        checks = [
            self._check_start_summary(),
            self._check_health(),
            self._check_reports(),
            self._check_tasks(),
            self._check_memory(),
            self._check_app_status(),
            self._check_project_audit(),
            self._check_help_local(),
            self._check_message_dry_run(),
            self._check_telegram_flow_runner(),
            self._check_malyarka_preview(),
            self._check_malyarka_dialog(),
            self._check_malyarka_transcript(),
            self._check_malyarka_fixtures(),
            self._check_malyarka_schema(),
            self._check_malyarka_pricing(),
            self._check_malyarka_disputes(),
            self._check_malyarka_combined(),
            self._check_malyarka_demo(),
            self._check_ai_provider_disabled(),
            self._check_review_provider_disabled(),
            self._check_safety_delete(),
            self._check_ai_provider_registry(),
            self._check_ai_provider_router_mock(),
            self._check_ai_provider_router_unknown(),
            self._check_ai_provider_gemini_disabled(),
        ]
        if include_daily_report:
            checks.insert(6, self._check_daily_report())
        return SmokeReport(checks=checks)

    def _check_start_summary(self) -> SmokeCheck:
        summary = LocalStartSummaryBuilder(self.project_root).build()
        return SmokeCheck("start-summary", summary.health_status == "OK", summary.next_task)

    def _check_health(self) -> SmokeCheck:
        health = LocalHealthChecker(self.project_root).run()
        return SmokeCheck("health", health.ok, f"env_files_found={len(health.env_files_found)}")

    def _check_reports(self) -> SmokeCheck:
        reports = LocalReportIndex(self.project_root).snapshot()
        return SmokeCheck("reports", reports.reports_count > 0, f"reports_count={reports.reports_count}")

    def _check_tasks(self) -> SmokeCheck:
        tasks = LocalTaskStatusStore(self.project_root).snapshot()
        valid_next = tasks.next_task in {"END_OF_PIPELINE", "END_OF_PIPELINE_ARCHIVED"} or tasks.next_task.startswith("BATCH_")
        return SmokeCheck("tasks", valid_next, tasks.next_task)

    def _check_memory(self) -> SmokeCheck:
        memory = LocalProjectMemoryStore(self.project_root).snapshot()
        return SmokeCheck("memory", len(memory.documents) > 0, f"documents={len(memory.documents)}")

    def _check_app_status(self) -> SmokeCheck:
        status = LocalRuntimeStatusBuilder(self.project_root).build()
        return SmokeCheck(
            "app-status",
            not status.can_start_live_services and not status.can_read_secrets,
            f"enabled={len(status.enabled_subsystems)}; disabled={len(status.disabled_subsystems)}",
        )

    def _check_daily_report(self) -> SmokeCheck:
        from hermes_core.daily_report import LocalDailyReport

        result = LocalDailyReport(self.project_root).write()
        return SmokeCheck("daily-report", result.path.exists() and result.smoke_status == "OK", result.next_task)

    def _check_project_audit(self) -> SmokeCheck:
        result = LocalProjectAudit(self.project_root).write()
        return SmokeCheck("project-audit", result.status == "OK", f"checks={result.checks_count}; failed={result.failed_count}")

    def _check_help_local(self) -> SmokeCheck:
        help_data = build_command_help()
        commands = {entry.command for entry in help_data.commands}
        return SmokeCheck("help-local", "health" in commands and "safety" in commands, f"commands={len(commands)}")

    def _check_message_dry_run(self) -> SmokeCheck:
        result = TelegramDryRunGateway().simulate_incoming(TelegramMessage("/status"))
        return SmokeCheck("message", bool(result.planned_response), result.next_step)

    def _check_telegram_flow_runner(self) -> SmokeCheck:
        result = run_telegram_flow_case("disputed")
        return SmokeCheck(
            "telegram-flow",
            result.initial_disputes > 0 and result.final_disputes == 0 and result.export_ready,
            f"resolved={result.resolved_disputes}; export_ready={result.export_ready}",
        )

    def _check_malyarka_preview(self) -> SmokeCheck:
        order = ParserContract().parse("paint | 1 | bucket")
        return SmokeCheck("malyarka-preview", export_blocked_until_confirmed(order), "export_blocked=True")

    def _check_malyarka_dialog(self) -> SmokeCheck:
        results = run_dialog_script([
            "/order paint | 2 | bucket\\nneeds clarification",
            "/questions",
            "/resolve-all-delete",
            "/export",
        ])
        final = results[-1]
        return SmokeCheck(
            "malyarka-dialog",
            final.export_ready and final.pending_disputes == 0,
            f"commands={len(results)}; export_ready={final.export_ready}",
        )

    def _check_malyarka_transcript(self) -> SmokeCheck:
        result = write_transcript_report(
            project_root=self.project_root,
            script_name="clean",
            output_name="MALYARKA_DIALOG_TRANSCRIPT_SMOKE.md",
        )
        return SmokeCheck(
            "malyarka-transcript",
            result.path.exists() and result.final_export_ready,
            f"path={result.path.name}; export_ready={result.final_export_ready}",
        )

    def _check_malyarka_fixtures(self) -> SmokeCheck:
        results = run_all_fixtures()
        return SmokeCheck("malyarka-fixtures", len(results) >= 9, f"fixtures={len(results)}")

    def _check_malyarka_schema(self) -> SmokeCheck:
        columns = export_preview_columns()
        return SmokeCheck("malyarka-schema", "line_total" in columns, f"columns={len(columns)}")

    def _check_malyarka_pricing(self) -> SmokeCheck:
        order = ParserContract().parse("wall paint | 2 | bucket")
        preview = build_synthetic_pricing_preview(order)
        return SmokeCheck("malyarka-pricing", preview.total == 200.0, f"total={preview.total}")

    def _check_malyarka_disputes(self) -> SmokeCheck:
        summary = build_fixture_dispute_summary()
        return SmokeCheck(
            "malyarka-disputes",
            summary.total_disputes >= 5 and summary.blocks_final,
            f"disputes={summary.total_disputes}; categories={len(summary.categories)}",
        )

    def _check_malyarka_combined(self) -> SmokeCheck:
        preview = build_combined_preview()
        return SmokeCheck(
            "malyarka-combined",
            preview.confirmed_count == 2 and preview.disputed_count == 1 and not preview.can_write_file,
            f"confirmed={preview.confirmed_count}; disputed={preview.disputed_count}",
        )

    def _check_malyarka_demo(self) -> SmokeCheck:
        demo = build_demo()
        return SmokeCheck("malyarka-demo", demo.export_gated, f"fixtures={demo.fixtures_count}")

    def _check_ai_provider_disabled(self) -> SmokeCheck:
        selection = ProviderFactory().select(ProviderConfig(mode="gemini-disabled"))
        return SmokeCheck("ai-provider", selection.is_blocked, selection.blocked_reason or "-")

    def _check_review_provider_disabled(self) -> SmokeCheck:
        selection = ReviewProviderFactory().select(ReviewProviderConfig(mode="deepseek-disabled"))
        return SmokeCheck("review-provider", selection.is_blocked, selection.blocked_reason or "-")

    def _check_safety_delete(self) -> SmokeCheck:
        policy = classify_action("delete")
        return SmokeCheck("safety", policy.decision.value == "BLOCKED", policy.reason)

    # ── Universal AI provider checks ──

    def _check_ai_provider_registry(self) -> SmokeCheck:
        from hermes_core.ai_provider import get_default_registry
        reg = get_default_registry()
        count = reg.count()
        has_mock = reg.get("mock") is not None
        has_gemini = reg.get("gemini-disabled") is not None
        return SmokeCheck(
            "ai-provider-registry",
            count == 6 and has_mock and has_gemini,
            f"providers={count}; mock={has_mock}; gemini={has_gemini}",
        )

    def _check_ai_provider_router_mock(self) -> SmokeCheck:
        from hermes_core.ai_provider import AIProviderRouter
        router = AIProviderRouter()
        decision = router.select("mock")
        return SmokeCheck(
            "ai-provider-router-mock",
            not decision.is_blocked,
            f"provider=mock; blocked={decision.is_blocked}",
        )

    def _check_ai_provider_router_unknown(self) -> SmokeCheck:
        from hermes_core.ai_provider import AIProviderRouter
        router = AIProviderRouter()
        decision = router.select("nonexistent")
        return SmokeCheck(
            "ai-provider-router-unknown",
            decision.is_blocked,
            f"blocked={decision.is_blocked}; reason={decision.blocked_reason}",
        )

    def _check_ai_provider_gemini_disabled(self) -> SmokeCheck:
        from hermes_core.ai_provider import AIProviderRouter
        router = AIProviderRouter()
        decision = router.select("gemini-disabled")
        return SmokeCheck(
            "ai-provider-gemini-disabled",
            decision.is_blocked,
            f"blocked={decision.is_blocked}; reason={decision.blocked_reason}",
        )
