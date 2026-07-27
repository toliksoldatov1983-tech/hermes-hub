from __future__ import annotations

from dataclasses import dataclass


ALLOWED_PREVIEW_SOURCES = {"synthetic", "manual"}
BLOCKED_EXPORT_SOURCES = {"real_order", "archive", "imported", "google_drive", "unknown"}


@dataclass(frozen=True)
class ExportSourceDecision:
    source_type: str
    allowed_for_preview: bool
    allowed_for_file_write: bool
    reason: str

    @property
    def blocked(self) -> bool:
        return not self.allowed_for_preview


def classify_export_source(source_type: str | None) -> ExportSourceDecision:
    normalized = (source_type or "unknown").strip().lower()
    if normalized in ALLOWED_PREVIEW_SOURCES:
        return ExportSourceDecision(
            source_type=normalized,
            allowed_for_preview=True,
            allowed_for_file_write=False,
            reason="preview_allowed_file_write_blocked",
        )
    if normalized in BLOCKED_EXPORT_SOURCES:
        return ExportSourceDecision(
            source_type=normalized,
            allowed_for_preview=False,
            allowed_for_file_write=False,
            reason=f"source_type_blocked:{normalized}",
        )
    return ExportSourceDecision(
        source_type=normalized,
        allowed_for_preview=False,
        allowed_for_file_write=False,
        reason=f"source_type_blocked:{normalized}",
    )
