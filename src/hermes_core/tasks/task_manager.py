from __future__ import annotations

from hermes_core.tasks.task_state import TaskState, TaskStatus


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[str, TaskState] = {}

    def add(self, task: TaskState) -> None:
        self._tasks[task.task_id] = task

    def mark_done(self, task_id: str) -> None:
        self._tasks[task_id].status = TaskStatus.DONE

    def get(self, task_id: str) -> TaskState | None:
        return self._tasks.get(task_id)
