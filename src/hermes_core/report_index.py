from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hermes_core.tasks.task_status_store import LocalTaskStatusStore, TaskStatusSnapshot


KEY_REPORTS = [
    "REPORT_TO_USER.md",
    "FINAL_MASTER_PROJECT_REPORT.md",
    "LOCAL_HEALTH_CHECK_REPORT.md",
    "LOCAL_TASK_STATUS_MANAGER_REPORT.md",
    "LOCAL_PROJECT_MEMORY_STORE_REPORT.md",
    "GOOGLE_DRIVE_WRITE_ACCESS_DIAGNOSTIC.md",
    "QUARANTINE_MOVE_REPORT.md",
]


@dataclass(frozen=True)
class ReportEntry:
    name: str
    relative_path: str
    size_bytes: int
    modified_at: str
    is_key_report: bool


@dataclass(frozen=True)
class ReportIndexSnapshot:
    project_root: str
    reports_count: int
    key_reports: list[ReportEntry]
    recent_reports: list[ReportEntry]
    task_snapshot: TaskStatusSnapshot


class LocalReportIndex:
    """Builds a local metadata index for Hermes-Clean reports."""

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.reports_dir = self.project_root / "05_REPORTS"

    def snapshot(self, recent_limit: int = 8) -> ReportIndexSnapshot:
        reports = self._reports()
        key_reports = [entry for entry in reports if entry.name in KEY_REPORTS]
        recent_reports = sorted(reports, key=lambda entry: entry.modified_at, reverse=True)[:recent_limit]
        return ReportIndexSnapshot(
            project_root=str(self.project_root),
            reports_count=len(reports),
            key_reports=key_reports,
            recent_reports=recent_reports,
            task_snapshot=LocalTaskStatusStore(self.project_root).snapshot(),
        )

    def _reports(self) -> list[ReportEntry]:
        if not self.reports_dir.exists() or not self.reports_dir.is_dir():
            return []
        entries = []
        for path in sorted(self.reports_dir.glob("*.md")):
            stat = path.stat()
            entries.append(
                ReportEntry(
                    name=path.name,
                    relative_path=path.relative_to(self.project_root).as_posix(),
                    size_bytes=stat.st_size,
                    modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
                    is_key_report=path.name in KEY_REPORTS,
                )
            )
        return entries
