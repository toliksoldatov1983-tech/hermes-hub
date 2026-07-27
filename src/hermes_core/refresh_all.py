from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hermes_core.daily_report import LocalDailyReport
from hermes_core.dashboard import LocalDashboard
from hermes_core.release_checklist import LocalReleaseChecklist
from hermes_core.status_export import LocalStatusExporter
from hermes_core.telegram.status_report import TelegramDryRunStatusReport
from hermes_modules.malyarka.status import MalyarkaStatusReport


@dataclass(frozen=True)
class RefreshAllResult:
    refreshed_paths: list[Path]

    @property
    def count(self) -> int:
        return len(self.refreshed_paths)


class LocalRefreshAll:
    """Refreshes local summary reports inside Hermes-Clean only."""

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def run(self) -> RefreshAllResult:
        paths = [
            LocalStatusExporter(self.project_root).export().path,
            LocalReleaseChecklist(self.project_root).write().path,
            TelegramDryRunStatusReport(self.project_root).write().path,
            MalyarkaStatusReport(self.project_root).write().path,
            LocalDashboard(self.project_root).write().path,
            LocalDailyReport(self.project_root).write().path,
        ]
        return RefreshAllResult(refreshed_paths=paths)
