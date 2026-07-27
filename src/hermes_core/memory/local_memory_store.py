from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hermes_core.memory.memory_index import HERMES_CLEAN_MEMORY_FILES


@dataclass(frozen=True)
class MemoryDocument:
    name: str
    relative_path: str
    exists: bool
    preview: str = ""


@dataclass(frozen=True)
class MemorySnapshot:
    source_of_truth: str
    documents: list[MemoryDocument]
    next_task: str
    pending_approvals_preview: str
    prohibitions_preview: str


class LocalProjectMemoryStore:
    """Reads only Hermes-Clean local markdown memory files."""

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def read_document(self, relative_path: Path) -> MemoryDocument:
        path = self.project_root / relative_path
        if not path.exists() or not path.is_file():
            return MemoryDocument(relative_path.stem, relative_path.as_posix(), False)
        text = path.read_text(encoding="utf-8-sig")
        preview = self._preview(text)
        return MemoryDocument(relative_path.stem, relative_path.as_posix(), True, preview)

    def snapshot(self) -> MemorySnapshot:
        docs = [self.read_document(path) for path in HERMES_CLEAN_MEMORY_FILES]
        return MemorySnapshot(
            source_of_truth=str(self.project_root),
            documents=docs,
            next_task=self._document_preview("03_TASKS/NEXT_TASK.md"),
            pending_approvals_preview=self._document_preview("03_TASKS/PENDING_APPROVALS.md"),
            prohibitions_preview=self._document_preview("00_START/PROJECT_PROHIBITIONS.md"),
        )

    def _document_preview(self, relative_path: str) -> str:
        doc = self.read_document(Path(relative_path))
        return doc.preview if doc.exists else "missing"

    @staticmethod
    def _preview(text: str, max_lines: int = 4) -> str:
        lines = [line.strip().replace("\ufeff", "") for line in text.splitlines() if line.strip()]
        return " ".join(lines[:max_lines])
