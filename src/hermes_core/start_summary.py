from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hermes_core.health import LocalHealthChecker
from hermes_core.report_index import LocalReportIndex
from hermes_core.safe_commands import SAFE_COMMANDS


@dataclass(frozen=True)
class StartSummary:
    project_root: str
    health_status: str
    next_task: str
    active_batch: str
    done_count: int
    reports_count: int
    env_files_found: int
    safe_commands: list[str]


class LocalStartSummaryBuilder:
    """Builds a short daily local startup summary for Hermes-Clean."""

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def build(self) -> StartSummary:
        health = LocalHealthChecker(self.project_root).run()
        reports = LocalReportIndex(self.project_root).snapshot()
        return StartSummary(
            project_root=str(self.project_root),
            health_status="OK" if health.ok else "ATTENTION",
            next_task=health.task_snapshot.next_task,
            active_batch=health.task_snapshot.active_batch,
            done_count=health.task_snapshot.done_count,
            reports_count=reports.reports_count,
            env_files_found=len(health.env_files_found),
            safe_commands=list(SAFE_COMMANDS),
        )
