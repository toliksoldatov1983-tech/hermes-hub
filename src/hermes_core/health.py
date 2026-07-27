from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hermes_core.memory.local_memory_store import LocalProjectMemoryStore, MemorySnapshot
from hermes_core.tasks.task_status_store import LocalTaskStatusStore, TaskStatusSnapshot


REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "START_HERE.md",
    "00_START/CURRENT_STATE.md",
    "03_TASKS/NEXT_TASK.md",
    "03_TASKS/DONE.md",
    "05_REPORTS/REPORT_TO_USER.md",
    "src/hermes_core",
    "src/hermes_modules/malyarka",
    "tests",
    "config",
    "scripts/hermes.cmd",
]

ENV_FILE_CANDIDATES = [
    ".env",
    "config/.env",
    "src/.env",
]


@dataclass(frozen=True)
class PathCheck:
    relative_path: str
    exists: bool


@dataclass(frozen=True)
class HealthCheckReport:
    project_root: str
    required_paths: list[PathCheck]
    env_files_found: list[str]
    task_snapshot: TaskStatusSnapshot
    memory_snapshot: MemorySnapshot

    @property
    def missing_required_paths(self) -> list[str]:
        return [item.relative_path for item in self.required_paths if not item.exists]

    @property
    def ok(self) -> bool:
        return not self.missing_required_paths and not self.env_files_found


class LocalHealthChecker:
    """Local-only Hermes-Clean health-check.

    The checker never reads secret file contents. It only checks whether known
    .env locations exist inside Hermes-Clean.
    """

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def run(self) -> HealthCheckReport:
        required = [
            PathCheck(relative_path=path, exists=(self.project_root / path).exists())
            for path in REQUIRED_PATHS
        ]
        env_files_found = [
            path for path in ENV_FILE_CANDIDATES if (self.project_root / path).exists()
        ]
        return HealthCheckReport(
            project_root=str(self.project_root),
            required_paths=required,
            env_files_found=env_files_found,
            task_snapshot=LocalTaskStatusStore(self.project_root).snapshot(),
            memory_snapshot=LocalProjectMemoryStore(self.project_root).snapshot(),
        )
