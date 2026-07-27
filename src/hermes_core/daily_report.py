"""Local daily report — maximum coverage edition.

Shows: today status, last smoke checks, safe commands, runtime,
Malyarka readiness, Telegram readiness, pending approvals, disabled subsystems.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hermes_core.runtime_status import LocalRuntimeStatusBuilder
from hermes_core.safe_commands import SAFE_COMMANDS
from hermes_core.smoke import LocalSmokeTester
from hermes_core.start_summary import LocalStartSummaryBuilder
from hermes_core.tasks.task_status_store import LocalTaskStatusStore
from hermes_core.telegram.blocked_actions import blocked_summary
from hermes_core.telegram.scenarios import SCENARIOS
from hermes_modules.malyarka.combined_preview import build_combined_preview
from hermes_modules.malyarka.demo import build_demo


@dataclass(frozen=True)
class DailyReportResult:
    path: Path
    health_status: str
    smoke_status: str
    next_task: str
    disabled_subsystems_count: int


class LocalDailyReport:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.output_path = self.project_root / "05_REPORTS" / "DAILY_LOCAL_REPORT.md"

    def write(self) -> DailyReportResult:
        summary = LocalStartSummaryBuilder(self.project_root).build()
        tasks = LocalTaskStatusStore(self.project_root).snapshot()
        smoke = LocalSmokeTester(self.project_root).run(include_daily_report=False)
        runtime = LocalRuntimeStatusBuilder(self.project_root).build()
        malyarka = build_combined_preview()
        demo = build_demo()
        blocked = blocked_summary()

        text = self._render(summary, tasks, smoke, runtime, malyarka, demo, blocked)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(text, encoding="utf-8")
        return DailyReportResult(
            path=self.output_path,
            health_status=summary.health_status,
            smoke_status=smoke.status,
            next_task=summary.next_task,
            disabled_subsystems_count=len(runtime.disabled_subsystems),
        )

    def _render(self, summary, tasks, smoke, runtime, malyarka, demo, blocked) -> str:
        # ── Smoke details ──
        smoke_checks = "\n".join(
            f"- {check.name}: {'OK' if check.ok else 'FAIL'} — {check.detail[:60]}"
            for check in smoke.checks
        )

        # ── Safe commands ──
        safe_cmd = "\n".join(f"- `{cmd}`" for cmd in SAFE_COMMANDS)

        # ── Task queue ──
        task_queue = (
            f"- Active batch: `{tasks.active_batch}`\n"
            f"- Next task: `{tasks.next_task}`\n"
            f"- Done count: `{tasks.done_count}`\n"
            f"- Blocked count: `{tasks.blocked_count}`\n"
            f"- Last done: `{tasks.last_done}`\n"
        )

        # ── Pending ──
        pending = tasks.pending_approvals_preview or "None"

        # ── Runtime ──
        disabled = "\n".join(
            f"- `{item.name}`: {item.status}; gate={item.approval_gate}"
            for item in runtime.disabled_subsystems
        )

        # ── Malyarka Readiness ──
        malyarka_text = (
            f"- Confirmed: `{malyarka.confirmed_count}`\n"
            f"- Disputed: `{malyarka.disputed_count}`\n"
            f"- Pricing total: `{malyarka.pricing.total}`\n"
            f"- Can write file: `{malyarka.can_write_file}`\n"
            f"- Can use as real order: `{malyarka.can_use_as_real_order}`\n"
            f"- Demo fixtures: `{demo.fixtures_count}`\n"
            f"- Export gated: `{demo.export_gated}`\n"
            f"- **Malyarka readiness: `{'DRY-RUN' if demo.export_gated else 'READY'}`**\n"
        )

        # ── Telegram ──
        scenarios = "\n".join(
            f"- `{s.name}` → `{s.command}`" for s in SCENARIOS[:8]
        )
        telegram_text = f"Scenarios: `{len(SCENARIOS)}`\n\n{scenarios}"

        # ── Blocked ──
        blocked_text = "\n".join(
            f"- {cat}: {cnt}" for cat, cnt in sorted(blocked.items())
        )

        return (
            "# DAILY LOCAL REPORT\n\n"
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
            "## Today Status\n\n"
            f"- Health: `{summary.health_status}`\n"
            f"- Smoke: `{smoke.status}`\n"
            f"- Active batch: `{summary.active_batch}`\n"
            f"- Next task: `{summary.next_task}`\n"
            f"- Done count: `{summary.done_count}`\n"
            f"- Reports count: `{summary.reports_count}`\n"
            f"- .env files: `{summary.env_files_found}`\n\n"
            "## Smoke Checks\n\n"
            f"{smoke_checks}\n\n"
            "## Task Queue\n\n"
            f"{task_queue}\n\n"
            "## Runtime\n\n"
            f"- App mode: `{runtime.app_mode}`\n"
            f"- Enabled: `{len(runtime.enabled_subsystems)}`\n"
            f"- Disabled: `{len(runtime.disabled_subsystems)}`\n"
            f"- Can read secrets: `{runtime.can_read_secrets}`\n"
            f"- Can start live services: `{runtime.can_start_live_services}`\n"
            f"- Can touch real orders: `{runtime.can_touch_real_orders}`\n"
            f"- Can change Google Drive: `{runtime.can_change_google_drive}`\n\n"
            "## Disabled Subsystems\n\n"
            f"{disabled}\n\n"
            "## Malyarka Readiness\n\n"
            f"{malyarka_text}\n\n"
            "## Telegram Dry-Run\n\n"
            f"{telegram_text}\n\n"
            "## Blocked Actions\n\n"
            f"{blocked_text}\n\n"
            "## Safe Commands\n\n"
            f"{safe_cmd}\n\n"
            "## Pending Approvals\n\n"
            f"{pending}\n\n"
            "## Safety\n\n"
            "This report is local to Hermes-Clean. It does not read secrets, `.env`, "
            "Google Drive, real orders, client documents, old archives or live Telegram.\n"
        )
