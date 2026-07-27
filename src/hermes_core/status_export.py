from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hermes_core.smoke import LocalSmokeTester
from hermes_core.start_summary import LocalStartSummaryBuilder
from hermes_core.tasks.task_status_store import LocalTaskStatusStore


@dataclass(frozen=True)
class StatusExportResult:
    path: Path
    status: str
    next_task: str
    reports_count: int
    smoke_status: str


class LocalStatusExporter:
    """Writes a local markdown status export inside Hermes-Clean."""

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.output_path = self.project_root / "05_REPORTS" / "LOCAL_STATUS_EXPORT.md"

    def export(self) -> StatusExportResult:
        summary = LocalStartSummaryBuilder(self.project_root).build()
        tasks = LocalTaskStatusStore(self.project_root).snapshot()
        smoke = LocalSmokeTester(self.project_root).run()
        text = self._render(summary, tasks.pending_approvals_preview, smoke.status)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(text, encoding="utf-8")
        return StatusExportResult(
            path=self.output_path,
            status=summary.health_status,
            next_task=summary.next_task,
            reports_count=summary.reports_count,
            smoke_status=smoke.status,
        )

    def _render(self, summary, pending_approvals: str, smoke_status: str) -> str:
        commands = "\n".join(f"- `{command}`" for command in summary.safe_commands)
        return (
            "# LOCAL_STATUS_EXPORT\n\n"
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
            "## Summary\n\n"
            f"- Project root: `{summary.project_root}`\n"
            f"- Health status: `{summary.health_status}`\n"
            f"- Smoke status: `{smoke_status}`\n"
            f"- Active batch: `{summary.active_batch}`\n"
            f"- Next task: `{summary.next_task}`\n"
            f"- Done count: `{summary.done_count}`\n"
            f"- Reports count: `{summary.reports_count}`\n"
            f"- Env files found: `{summary.env_files_found}`\n\n"
            "## Safe Commands\n\n"
            f"{commands}\n\n"
            "## Pending Approvals Preview\n\n"
            f"{pending_approvals}\n\n"
            "## Safety\n\n"
            "This export is local to Hermes-Clean. It does not read Google Drive, old archives, secrets, real orders or old projects.\n"
        )
