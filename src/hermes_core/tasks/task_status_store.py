from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TaskStatusSnapshot:
    active_batch: str
    next_task: str
    done_count: int
    last_done: str
    blocked_count: int
    pending_approvals_preview: str


class LocalTaskStatusStore:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def snapshot(self) -> TaskStatusSnapshot:
        done_lines = self._task_lines("03_TASKS/DONE.md")
        blocked = [line for line in done_lines if "заблок" in line.lower() or "blocked" in line.lower()]
        return TaskStatusSnapshot(
            active_batch=self._first_task_id("03_TASKS/ACTIVE_BATCH.md"),
            next_task=self._first_task_id("03_TASKS/NEXT_TASK.md"),
            done_count=len(done_lines),
            last_done=done_lines[-1] if done_lines else "-",
            blocked_count=len(blocked),
            pending_approvals_preview=self._preview("03_TASKS/PENDING_APPROVALS.md"),
        )

    def _read(self, relative_path: str) -> str:
        path = self.project_root / relative_path
        if not path.exists() or not path.is_file():
            return ""
        return path.read_text(encoding="utf-8-sig")

    def _first_task_id(self, relative_path: str) -> str:
        for line in self._read(relative_path).splitlines():
            stripped = line.strip()
            if stripped in {"END_OF_PIPELINE", "END_OF_PIPELINE_ARCHIVED"} or stripped.startswith("BATCH_") or stripped.startswith("HERMES_"):
                return stripped
        return "missing"

    def _task_lines(self, relative_path: str) -> list[str]:
        return [line.strip() for line in self._read(relative_path).splitlines() if line.strip().startswith("- ")]

    def _preview(self, relative_path: str, max_lines: int = 4) -> str:
        lines = [line.strip() for line in self._read(relative_path).splitlines() if line.strip()]
        return " ".join(lines[:max_lines]) if lines else "missing"
