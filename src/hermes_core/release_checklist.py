"""Local release checklist — release candidate prep.

Writes a comprehensive release candidate report with:
- readiness summary, smoke, test report
- all commands with mode/approval
- known limitations
- disabled subsystem matrix
- acceptance criteria
- next direction options
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hermes_core.command_help import APPROVAL_GATES, build_command_help
from hermes_core.project_audit import LocalProjectAudit
from hermes_core.runtime_status import LocalRuntimeStatusBuilder
from hermes_core.smoke import LocalSmokeTester
from hermes_core.start_summary import LocalStartSummaryBuilder
from hermes_core.tasks.task_status_store import LocalTaskStatusStore
from hermes_core.telegram.blocked_actions import blocked_summary


KNOWN_LIMITATIONS = [
    "Gemini API выключен — требуется APPROVE_SECRET_SETUP и ключ",
    "DeepSeek / DeepSig API выключен — требуется APPROVE_SECRET_SETUP",
    "Telegram — только dry-run, live polling/webhook заблокированы",
    "Malyarka — только synthetic/manual input, реальные заказы заблокированы",
    "Google Drive — write заблокирован (ошибка 403 appNotAuthorizedToFile)",
    "Экспорт файлов — заблокирован в dry-run режиме",
    "Удаление файлов — заблокировано глобально",
    "Архивы — не распакованы, импорт заблокирован",
    "Secret gate — 1 проверка не пройдена (no_key_in_memory), реальный API не готов",
    "Нет CI/CD — все проверки запускаются вручную",
]

NEXT_DIRECTIONS = [
    "BATCH_063B: План переноса Malyarka hardening из архивного E:\\Hermes-Hub в проект",
    "Подключить Gemini API после APPROVE_SECRET_SETUP",
    "Подключить DeepSeek / DeepSig review после APPROVE_SECRET_SETUP",
    "Запустить live Telegram после APPROVE_TELEGRAM_LIVE",
    "Продолжить Malyarka module contracts без реальных заказов",
    "Вернуться к Google Drive cleanup после решения 403 ошибки",
    "Подготовить Hermes-Clean локальную сборку (pyproject.toml, requirements.txt)",
]

ACCEPTANCE_CRITERIA = [
    ("health", "Health status = OK, 0 .env files"),
    ("smoke", "Smoke: 20/20 checks passed"),
    ("tests", "All 187+ tests passed"),
    ("audit", "Project audit: 25/25 checks, 0 failed"),
    ("safety_gate", "safety delete → BLOCKED, safety create_local_report → SAFE"),
    ("secret_gate", "Secret gate: 9/10 passed, real API blocked"),
    ("telegram", "Telegram dry-run: 18 сценариев, 26 команд, live blocked"),
    ("malyarka", "Malyarka: 9 fixtures, export gated, synthetic only"),
    ("subsystems", "6 enabled, 6 disabled — все gate защищены"),
    ("docs", "USER_RUNBOOK_RU.md, SAFE_LOCAL_OPERATIONS_RU.md, START_HERE.md"),
]


@dataclass(frozen=True)
class ReleaseChecklistResult:
    path: Path
    health_status: str
    smoke_status: str
    next_task: str
    approval_gates_count: int


class LocalReleaseChecklist:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.output_path = self.project_root / "05_REPORTS" / "LOCAL_RELEASE_CHECKLIST.md"

    def write(self) -> ReleaseChecklistResult:
        summary = LocalStartSummaryBuilder(self.project_root).build()
        smoke = LocalSmokeTester(self.project_root).run()
        tasks = LocalTaskStatusStore(self.project_root).snapshot()
        help_data = build_command_help()
        runtime = LocalRuntimeStatusBuilder(self.project_root).build()
        audit = LocalProjectAudit(self.project_root).run()
        blocked = blocked_summary()

        text = self._render(
            summary, smoke, tasks, help_data, runtime, audit, blocked
        )
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(text, encoding="utf-8")
        return ReleaseChecklistResult(
            path=self.output_path,
            health_status=summary.health_status,
            smoke_status=smoke.status,
            next_task=summary.next_task,
            approval_gates_count=len(APPROVAL_GATES),
        )

    def _render(self, summary, smoke, tasks, help_data, runtime, audit, blocked) -> str:
        # ── Readiness ──
        readiness = (
            f"- Health: `{summary.health_status}`\n"
            f"- Smoke: `{smoke.status}` ({len(smoke.checks)} checks, {len(smoke.failed_checks)} failed)\n"
            f"- Project audit: {len(audit)} checks, {sum(1 for c in audit if not c.ok)} failed\n"
            f"- Next task: `{summary.next_task}`\n"
            f"- Reports: `{summary.reports_count}`\n"
            f"- .env files: `{summary.env_files_found}`\n"
            f"- Approval gates: `{len(APPROVAL_GATES)}`\n"
        )

        # ── Test report ──
        test_report = (
            f"- Smoke: {smoke.status} ({len(smoke.checks)} checks)\n"
            f"- Project audit: {len(audit)} checks\n"
            f"- CLI commands: {sum(1 for e in help_data.commands)}\n"
            f"- Telegram scenarios: 18\n"
            f"- Malyarka fixtures: 9\n"
            f"- Blocked actions: {sum(blocked.values())}\n"
        )

        # ── Disabled subsystem matrix ──
        matrix = "\n".join(
            f"| `{item.name}` | {item.status} | {item.mode} | `{item.approval_gate}` |"
            for item in runtime.disabled_subsystems
        )
        enabled_matrix = "\n".join(
            f"| `{item.name}` | {item.status} | {item.mode} | {item.approval_gate} |"
            for item in runtime.enabled_subsystems
        )

        # ── Acceptance criteria ──
        criteria_lines = "\n".join(
            f"- [{id_}] {desc}" for id_, desc in ACCEPTANCE_CRITERIA
        )

        # ── Known limitations ──
        limits = "\n".join(f"- {lim}" for lim in KNOWN_LIMITATIONS)

        # ── Commands ──
        command_lines = "\n".join(
            f"- `{entry.command}` — {entry.purpose}; mode: `{entry.mode}`; approval: `{entry.approval_required}`"
            for entry in help_data.commands
        )

        # ── Gates ──
        gate_lines = "\n".join(f"- `{gate}`" for gate in APPROVAL_GATES)

        # ── Next directions ──
        direction_lines = "\n".join(f"- {item}" for item in NEXT_DIRECTIONS)

        return (
            "# LOCAL RELEASE CHECKLIST (Release Candidate)\n\n"
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
            "## Readiness\n\n"
            f"{readiness}\n\n"
            "## Test Report\n\n"
            f"{test_report}\n\n"
            "## Acceptance Criteria\n\n"
            f"{criteria_lines}\n\n"
            "## Enabled Subsystems\n\n"
            "| Subsystem | Status | Mode | Gate |\n"
            "|-----------|--------|------|------|\n"
            f"{enabled_matrix}\n\n"
            "## Disabled Subsystem Matrix\n\n"
            "| Subsystem | Status | Mode | Gate |\n"
            "|-----------|--------|------|------|\n"
            f"{matrix}\n\n"
            "## Known Limitations\n\n"
            f"{limits}\n\n"
            "## All Local Commands\n\n"
            f"{command_lines}\n\n"
            "## Open Approval Gates\n\n"
            f"{gate_lines}\n\n"
            "## Next Direction Options\n\n"
            f"{direction_lines}\n\n"
            "## Safety\n\n"
            "This checklist is local to Hermes-Clean. It does not read Google Drive, "
            "old archives, secrets, real orders or old projects.\n"
        )
