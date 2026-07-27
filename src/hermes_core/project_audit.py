"""Local Hermes-Clean project audit — maximum coverage edition.

Checks:
  - Required paths and files
  - NEXT_TASK content (has valid BATCH_ id, END_OF_PIPELINE or END_OF_PIPELINE_ARCHIVED)
  - .env presence across all project subdirectories
  - Disabled subsystems (all 6 must be DISABLED)
  - Command docs coverage for all commands
  - Report count and key reports
  - Actionable findings summary
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from hermes_core.command_help import build_command_help
from hermes_core.health import LocalHealthChecker
from hermes_core.runtime_status import LocalRuntimeStatusBuilder


COMMAND_COVERAGE_DOCS = [
    "START_HERE.md",
    "README.md",
    "docs/USER_GUIDE_RU.md",
    "docs/LOCAL_DAILY_REPORT.md",
    "docs/LOCAL_PROJECT_AUDIT.md",
    "docs/LOCAL_APP_READINESS_PLAN.md",
    "docs/WINDOWS_COMMANDS.md",
    "docs/TELEGRAM_DRY_RUN_PLAN.md",
    "docs/GEMINI_SETUP.md",
    "docs/DEEPSEEK_REVIEW_SETUP.md",
    "05_REPORTS/LOCAL_DASHBOARD.md",
    "05_REPORTS/DAILY_LOCAL_REPORT.md",
    "05_REPORTS/TELEGRAM_DRY_RUN_STATUS.md",
    "05_REPORTS/LOCAL_RUNTIME_STATUS.md",
]


@dataclass(frozen=True)
class AuditCheck:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class ProjectAuditResult:
    path: Path
    status: str
    checks_count: int
    failed_count: int


class LocalProjectAudit:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def run(self) -> list[AuditCheck]:
        health = LocalHealthChecker(self.project_root).run()
        runtime = LocalRuntimeStatusBuilder(self.project_root).build()

        checks: list[AuditCheck] = []

        # ── Required paths ──
        checks.append(AuditCheck(
            "required_paths",
            health.ok,
            f"missing={len(health.missing_required_paths)}; env_files={len(health.env_files_found)}"
        ))

        # ── .env scan (deep) ──
        env_files = self._find_all_env_files()
        checks.append(AuditCheck(
            "no_env_anywhere",
            len(env_files) == 0,
            f"found={len(env_files)}: {', '.join(env_files)}" if env_files else "found=0"
        ))

        # ── NEXT_TASK exists and has valid id ──
        nt, nt_id = self._check_next_task()
        checks.append(AuditCheck("next_task_exists", nt, "03_TASKS/NEXT_TASK.md"))
        checks.append(AuditCheck("next_task_has_id", self._is_valid_task_id(nt_id),
                                  f"id={nt_id or 'MISSING'}"))

        # ── Report coverage ──
        reports_dir = self.project_root / "05_REPORTS"
        report_files = list(reports_dir.glob("*.md")) if reports_dir.exists() else []
        checks.append(AuditCheck(
            "reports_count_adequate",
            len(report_files) >= 30,
            f"count={len(report_files)}"
        ))

        # ── Dashboard / daily report ──
        checks.append(AuditCheck(
            "dashboard_exists",
            (self.project_root / "05_REPORTS" / "LOCAL_DASHBOARD.md").exists(),
            "05_REPORTS/LOCAL_DASHBOARD.md"
        ))
        checks.append(AuditCheck(
            "daily_report_exists",
            (self.project_root / "05_REPORTS" / "DAILY_LOCAL_REPORT.md").exists(),
            "05_REPORTS/DAILY_LOCAL_REPORT.md"
        ))
        checks.append(AuditCheck(
            "runtime_status_exists",
            (self.project_root / "05_REPORTS" / "LOCAL_RUNTIME_STATUS.md").exists(),
            "05_REPORTS/LOCAL_RUNTIME_STATUS.md"
        ))
        checks.append(AuditCheck(
            "telegram_status_exists",
            (self.project_root / "05_REPORTS" / "TELEGRAM_DRY_RUN_STATUS.md").exists(),
            "05_REPORTS/TELEGRAM_DRY_RUN_STATUS.md"
        ))

        # ── Live services disabled ──
        checks.append(AuditCheck(
            "live_services_disabled",
            not runtime.can_start_live_services,
            "live services disabled"
        ))
        checks.append(AuditCheck(
            "secret_reading_disabled",
            not runtime.can_read_secrets,
            "secret reading disabled"
        ))
        checks.append(AuditCheck(
            "real_order_access_disabled",
            not runtime.can_touch_real_orders,
            "real order access disabled"
        ))
        checks.append(AuditCheck(
            "google_drive_write_disabled",
            not runtime.can_change_google_drive,
            "google drive write disabled"
        ))

        # ── Disabled subsystems check (all 6) ──
        disabled_names = [d.name for d in runtime.disabled_subsystems]
        required_disabled = ["live_telegram", "real_ai_providers", "google_drive_write",
                            "real_order_access", "archive_import", "delete_files"]
        for name in required_disabled:
            checks.append(AuditCheck(
                f"disabled_{name}",
                name in disabled_names,
                f"{name} is {'DISABLED' if name in disabled_names else 'MISSING'}"
            ))

        # ── Enabled subsystems count ──
        checks.append(AuditCheck(
            "enabled_subsystems_count",
            len(runtime.enabled_subsystems) >= 6,
            f"enabled={len(runtime.enabled_subsystems)}"
        ))

        # ── Command docs coverage ──
        checks.extend(self._command_coverage_checks())

        # ── Git status (non-blocking) ──
        git_ok, git_detail = self._check_git()
        checks.append(AuditCheck("git_status", git_ok, git_detail))

        # ── Source modules exist ──
        src_dir = self.project_root / "src" / "hermes_core"
        src_count = len(list(src_dir.rglob("*.py"))) if src_dir.exists() else 0
        checks.append(AuditCheck(
            "source_modules_exist",
            src_count > 0,
            f"hermes_core modules={src_count}"
        ))

        # ── Malyarka module exists ──
        mal_dir = self.project_root / "src" / "hermes_modules" / "malyarka"
        mal_count = len(list(mal_dir.glob("*.py"))) if mal_dir.exists() else 0
        checks.append(AuditCheck(
            "malyarka_module_exists",
            mal_count > 0,
            f"modules={mal_count}"
        ))

        return checks

    def write(self) -> ProjectAuditResult:
        checks = self.run()
        failed = [check for check in checks if not check.ok]
        output_path = self.project_root / "05_REPORTS" / "LOCAL_PROJECT_AUDIT.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self._render(checks, failed), encoding="utf-8")
        return ProjectAuditResult(
            path=output_path,
            status="OK" if not failed else "ATTENTION",
            checks_count=len(checks),
            failed_count=len(failed),
        )

    def _render(self, checks: list[AuditCheck], failed: list[AuditCheck]) -> str:
        check_lines = "\n".join(
            f"- `{check.name}`: {'OK' if check.ok else 'FAIL'}; {check.detail}"
            for check in checks
        )
        findings = self._actionable_findings(checks, failed)
        return (
            "# LOCAL_PROJECT_AUDIT\n\n"
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
            "## Summary\n\n"
            f"- status: `{'OK' if not failed else 'ATTENTION'}`\n"
            f"- checks: `{len(checks)}`\n"
            f"- failed: `{len(failed)}`\n\n"
            "## Checks\n\n"
            f"{check_lines}\n\n"
            "## Actionable Findings\n\n"
            f"{findings}\n\n"
            "## Safety\n\n"
            "This audit is local to Hermes-Clean. It does not read `.env`, tokens, keys, "
            "real orders, client documents, Google Drive files or old archives.\n"
        )

    # ── Internal checks ──

    def _find_all_env_files(self) -> list[str]:
        """Recursively find .env files in project root (max depth 4)."""
        env_files = []
        for path in self.project_root.rglob(".env"):
            if ".git" not in str(path) and "__pycache__" not in str(path):
                # Check depth
                rel = path.relative_to(self.project_root)
                if len(rel.parts) <= 4:
                    env_files.append(str(rel))
        return env_files

    def _check_next_task(self) -> tuple[bool, str | None]:
        """Check NEXT_TASK.md exists and has a valid task id."""
        path = self.project_root / "03_TASKS" / "NEXT_TASK.md"
        if not path.exists():
            return False, None
        content = path.read_text(encoding="utf-8")
        for line in content.splitlines():
            stripped = line.strip()
            if self._is_valid_task_id(stripped):
                return True, stripped
        return True, None  # file exists but no BATCH_ found

    def _is_valid_task_id(self, value: str | None) -> bool:
        return bool(
            value == "END_OF_PIPELINE"
            or value == "END_OF_PIPELINE_ARCHIVED"
            or (value and (value.startswith("BATCH_") or value.startswith("HERMES_")))
        )

    def _check_git(self) -> tuple[bool, str]:
        """Non-blocking git status check."""
        git_dir = self.project_root / ".git"
        if not git_dir.exists():
            return True, "no git repo (not required)"
        return True, "git exists (not checked)"

    def _command_coverage_checks(self) -> list[AuditCheck]:
        docs_text = []
        missing_docs = []
        for relative_path in COMMAND_COVERAGE_DOCS:
            path = self.project_root / relative_path
            if not path.exists():
                missing_docs.append(relative_path)
                continue
            docs_text.append(path.read_text(encoding="utf-8-sig"))
        combined_text = "\n".join(docs_text)
        commands = [entry.command for entry in build_command_help().commands]
        missing_commands = [command for command in commands if command not in combined_text]
        return [
            AuditCheck("command_docs_exist", not missing_docs,
                       f"missing_docs={len(missing_docs)}: {', '.join(missing_docs[:3])}" if missing_docs else "all found"),
            AuditCheck("command_coverage", not missing_commands,
                       f"missing={len(missing_commands)}: {', '.join(missing_commands[:5])}" if missing_commands else "full coverage"),
        ]

    def _actionable_findings(self, checks: list[AuditCheck], failed: list[AuditCheck]) -> str:
        if not failed:
            return "All checks passed. No actionable findings."

        lines = []
        for f in failed:
            advice = _FINDINGS_ADVICE.get(f.name, "Review and fix this check.")
            lines.append(f"- **{f.name}**: {f.detail} → {advice}")
        return "\n".join(lines)


_FINDINGS_ADVICE = {
    "next_task_has_id": "Update 03_TASKS/NEXT_TASK.md with a valid BATCH_ id, END_OF_PIPELINE or END_OF_PIPELINE_ARCHIVED.",
    "next_task_exists": "Create 03_TASKS/NEXT_TASK.md with the next safe local block.",
    "no_env_anywhere": "Remove .env files from Hermes-Clean. They belong outside the project.",
    "required_paths": "Run scripts\\hermes.cmd health to see missing files.",
    "dashboard_exists": "Run scripts\\hermes.cmd dashboard to generate.",
    "daily_report_exists": "Run scripts\\hermes.cmd daily-report to generate.",
    "telegram_status_exists": "Run scripts\\hermes.cmd telegram-status to generate.",
    "live_services_disabled": "This should remain disabled in local-safe mode.",
    "secret_reading_disabled": "This should remain disabled in local-safe mode.",
    "real_order_access_disabled": "This should remain disabled in local-safe mode.",
    "google_drive_write_disabled": "This should remain disabled in local-safe mode.",
    "command_coverage": "Update docs to cover missing commands.",
    "command_docs_exist": "Create the missing docs files listed above.",
    "reports_count_adequate": "Generate more reports via hermes.cmd commands.",
}
