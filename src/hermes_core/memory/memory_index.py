from __future__ import annotations

from pathlib import Path


HERMES_CLEAN_MEMORY_FILES = [
    Path("00_START/CURRENT_STATE.md"),
    Path("00_START/PROJECT_DECISIONS.md"),
    Path("00_START/PROJECT_PROHIBITIONS.md"),
    Path("03_TASKS/NEXT_TASK.md"),
    Path("03_TASKS/DONE.md"),
    Path("03_TASKS/PENDING_APPROVALS.md"),
]

FORBIDDEN_MEMORY_SOURCES = [
    "Obsidian memory",
    "Open WebUI memory",
    "Google Drive documents",
    "old archives",
    "real orders",
    "secrets",
]
