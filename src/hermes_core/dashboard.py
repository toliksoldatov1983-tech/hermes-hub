"""Local Hermes-Clean dashboard — maximum coverage edition.

Shows: core status, runtime, Malyarka readiness, Telegram dry-run readiness,
task queue, pending approvals, blocked actions summary, safety locks.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hermes_core.command_help import build_command_help
from hermes_core.runtime_status import LocalRuntimeStatusBuilder
from hermes_core.smoke import LocalSmokeTester
from hermes_core.start_summary import LocalStartSummaryBuilder
from hermes_core.tasks.task_status_store import LocalTaskStatusStore
from hermes_core.telegram.blocked_actions import blocked_summary
from hermes_core.telegram.scenarios import SCENARIOS
from hermes_core.telegram.status_report import ALIASES, SAFETY_LIMITS, TelegramDryRunStatusReport
from hermes_modules.malyarka.demo import build_demo
from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.fixtures import run_all_fixtures
from hermes_modules.malyarka.parser_contract import ParserContract


@dataclass(frozen=True)
class DashboardResult:
    path: Path
    health_status: str
    smoke_status: str
    next_task: str
    malyarka_fixtures: int
    telegram_aliases: int


class LocalDashboard:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.output_path = self.project_root / "05_REPORTS" / "LOCAL_DASHBOARD.md"

    def write(self) -> DashboardResult:
        summary = LocalStartSummaryBuilder(self.project_root).build()
        smoke = LocalSmokeTester(self.project_root).run(include_daily_report=False)
        tasks = LocalTaskStatusStore(self.project_root).snapshot()
        runtime = LocalRuntimeStatusBuilder(self.project_root).build()
        telegram = TelegramDryRunStatusReport(self.project_root).write()
        command_help = build_command_help()
        fixtures = run_all_fixtures()
        demo = build_demo()
        blocked = blocked_summary()

        # Malyarka readiness score
        fixtures_ready = sum(1 for f in fixtures if f.final_ready)
        order = ParserContract().parse("paint | 1 | bucket")
        export_gated = export_blocked_until_confirmed(order)

        text = self._render(
            summary, smoke, tasks, runtime, telegram,
            command_help, fixtures, fixtures_ready, demo, export_gated, blocked
        )
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(text, encoding="utf-8")
        return DashboardResult(
            path=self.output_path,
            health_status=summary.health_status,
            smoke_status=smoke.status,
            next_task=summary.next_task,
            malyarka_fixtures=demo.fixtures_count,
            telegram_aliases=telegram.aliases_count,
        )

    def _render(self, summary, smoke, tasks, runtime, telegram,
                command_help, fixtures, fixtures_ready, demo, export_gated, blocked) -> str:

        # ── Core ──
        core = (
            f"- Health: `{summary.health_status}`\n"
            f"- Smoke: `{smoke.status}`\n"
            f"- Active batch: `{summary.active_batch}`\n"
            f"- Next task: `{summary.next_task}`\n"
            f"- Done count: `{summary.done_count}`\n"
            f"- Reports count: `{summary.reports_count}`\n"
            f"- .env files: `{summary.env_files_found}`\n"
        )

        # ── Smoke details ──
        smoke_details = "\n".join(
            f"- {check.name}: {'OK' if check.ok else 'FAIL'}"
            for check in smoke.checks[:10]  # top 10
        )

        # ── Task queue ──
        task_queue = (
            f"- Active batch: `{tasks.active_batch}`\n"
            f"- Next task: `{tasks.next_task}`\n"
            f"- Done count: `{tasks.done_count}`\n"
            f"- Blocked count: `{tasks.blocked_count}`\n"
            f"- Last done: `{tasks.last_done}`\n"
        )

        # ── Pending approvals ──
        pending = tasks.pending_approvals_preview if tasks.pending_approvals_preview else "None"

        # ── Runtime ──
        enabled_runtime = "\n".join(
            f"- `{item.name}`: {item.status}; mode={item.mode}"
            for item in runtime.enabled_subsystems
        )
        disabled_runtime = "\n".join(
            f"- `{item.name}`: {item.status}; gate={item.approval_gate}"
            for item in runtime.disabled_subsystems
        )

        # ── Malyarka Readiness ──
        malyarka = (
            f"- Fixtures: `{len(fixtures)}` total, `{fixtures_ready}` ready\n"
            f"- Demo fixtures: `{demo.fixtures_count}`\n"
            f"- Ready fixtures: `{demo.ready_fixtures}`\n"
            f"- Disputed fixtures: `{demo.disputed_fixtures}`\n"
            f"- Workflow status: `{demo.workflow_status}`\n"
            f"- Export gated: `{demo.export_gated}`\n"
            f"- Real export blocked: `{export_gated}`\n"
            f"- **Malyarka readiness: `{'READY' if fixtures_ready >= 5 and demo.export_gated else 'NOT READY'}`**\n"
        )

        # ── Telegram Dry-Run Readiness ──
        telegram_text = (
            f"- Aliases: `{telegram.aliases_count}`\n"
            f"- Scenarios: `{telegram.scenarios_count}`\n"
            f"- Safety limits: `{telegram.safety_limits_count}`\n"
            f"- Blocked actions: `{telegram.blocked_actions_count}`\n"
            f"- **Telegram readiness: `DRY-RUN ONLY`** (live blocked)\n"
        )
        telegram_aliases = "\n".join(f"- `{alias}`" for alias in ALIASES[:15])
        telegram_scenarios = "\n".join(
            f"- `{scenario.name}` → `{scenario.command}`" for scenario in SCENARIOS[:10]
        )

        # ── Blocked Actions Summary ──
        blocked_text = "\n".join(
            f"- {category}: {count} blocked" for category, count in sorted(blocked.items())
        )

        # ── Command Center ──
        command_lines = "\n".join(
            f"- `scripts\\hermes.cmd {entry.command}` — {entry.purpose} ({entry.mode})"
            for entry in command_help.commands[:15]  # top 15
        )

        # ── Safety ──
        safety_locks = "\n".join(f"- {limit}" for limit in SAFETY_LIMITS)

        return (
            "# LOCAL DASHBOARD\n\n"
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
            "## Core\n\n"
            f"{core}\n\n"
            "## Smoke Top-10\n\n"
            f"{smoke_details}\n\n"
            "## Task Queue\n\n"
            f"{task_queue}\n\n"
            "## Pending Approvals\n\n"
            f"{pending}\n\n"
            "## Runtime Status\n\n"
            f"- App mode: `{runtime.app_mode}`\n"
            f"- Can start live services: `{runtime.can_start_live_services}`\n"
            f"- Can read secrets: `{runtime.can_read_secrets}`\n"
            f"- Can touch real orders: `{runtime.can_touch_real_orders}`\n"
            f"- Can change Google Drive: `{runtime.can_change_google_drive}`\n\n"
            "### Enabled\n\n"
            f"{enabled_runtime}\n\n"
            "### Disabled\n\n"
            f"{disabled_runtime}\n\n"
            "## Malyarka Readiness\n\n"
            f"{malyarka}\n\n"
            "## Telegram Dry-Run Readiness\n\n"
            f"{telegram_text}\n\n"
            "### Telegram Commands (first 15)\n\n"
            f"{telegram_aliases}\n\n"
            "### Telegram Scenarios (first 10)\n\n"
            f"{telegram_scenarios}\n\n"
            "## Blocked Actions\n\n"
            f"{blocked_text}\n\n"
            "## Command Center (first 15)\n\n"
            f"{command_lines}\n\n"
            "## Safety Locks\n\n"
            f"{safety_locks}\n\n"
            "## Safety\n\n"
            "This dashboard is local. It does not read secrets, start live Telegram, "
            "change Google Drive, read real orders or unpack old archives.\n"
        )
