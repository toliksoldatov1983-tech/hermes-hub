"""Order Draft State — dry-run order draft lifecycle.

No real orders. No export files. In-memory only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from typing import Any


class OrderDraftStatus(Enum):
    NEW = "new"
    PARSING = "parsing"
    PREVIEW_READY = "preview_ready"
    HAS_DISPUTES = "has_disputes"
    AWAITING_USER_CORRECTION = "awaiting_user_correction"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


@dataclass
class OrderDraftLine:
    """One line in an order draft."""

    raw_text: str
    item: str = ""
    quantity: str = ""
    unit: str = ""
    is_confirmed: bool = True
    is_disputed: bool = False
    dispute_reason: str = ""

    def to_dict(self) -> dict:
        return {
            "raw_text": self.raw_text,
            "item": self.item, "quantity": self.quantity, "unit": self.unit,
            "is_confirmed": self.is_confirmed, "is_disputed": self.is_disputed,
            "dispute_reason": self.dispute_reason,
        }


@dataclass
class OrderDraft:
    """An order draft — mutable, in-memory, dry-run only."""

    draft_id: str = "draft-001"
    source_text: str = ""
    confirmed_rows: list[OrderDraftLine] = field(default_factory=list)
    disputed_rows: list[OrderDraftLine] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    blocked_reason: str = ""
    export_allowed: bool = False
    revision_number: int = 1
    status: OrderDraftStatus = OrderDraftStatus.NEW
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "real_order": False,
        "synthetic": True,
        "export_created": False,
        "file_written": False,
        "env_read": False,
    })

    @property
    def has_disputes(self) -> bool:
        return len(self.disputed_rows) > 0

    @property
    def is_ready_for_confirmation(self) -> bool:
        return not self.has_disputes and len(self.confirmed_rows) > 0

    @property
    def is_confirmed(self) -> bool:
        return self.status == OrderDraftStatus.CONFIRMED

    def add_confirmed(self, line: OrderDraftLine) -> None:
        self.confirmed_rows.append(line)
        self._touch()

    def add_disputed(self, line: OrderDraftLine) -> None:
        self.disputed_rows.append(line)
        self._touch()

    def add_question(self, q: str) -> None:
        self.questions.append(q)

    def correct_disputed(self, index: int, new_text: str) -> None:
        if 0 <= index < len(self.disputed_rows):
            corrected = OrderDraftLine(
                raw_text=new_text,
                item=new_text.split("|")[0].strip() if "|" in new_text else new_text,
            )
            self.confirmed_rows.append(corrected)
            self.disputed_rows.pop(index)
            self.revision_number += 1
            self._touch()

    def confirm(self) -> None:
        """Confirm draft — dry-run only, no export."""
        if self.has_disputes:
            self.status = OrderDraftStatus.HAS_DISPUTES
            self.export_allowed = False
            return
        self.status = OrderDraftStatus.CONFIRMED
        self.export_allowed = True  # dry-run flag, no real file
        self._touch()

    def cancel(self) -> None:
        self.status = OrderDraftStatus.CANCELLED
        self._touch()

    def block(self, reason: str) -> None:
        self.status = OrderDraftStatus.BLOCKED
        self.blocked_reason = reason
        self._touch()

    def reset(self) -> None:
        self.__init__(draft_id=self.draft_id)

    def _touch(self) -> None:
        self.updated_at = datetime.utcnow().isoformat()

    def preview_lines(self) -> list[str]:
        lines = []
        for r in self.confirmed_rows:
            lines.append(f"✓ {r.raw_text}")
        for r in self.disputed_rows:
            lines.append(f"⚠ {r.raw_text} — {r.dispute_reason}")
        return lines

    def to_dict(self) -> dict:
        return {
            "draft_id": self.draft_id,
            "source_text": self.source_text[:200],
            "confirmed_count": len(self.confirmed_rows),
            "disputed_count": len(self.disputed_rows),
            "status": self.status.value,
            "revision_number": self.revision_number,
            "export_allowed": self.export_allowed,
            "questions": self.questions,
            "audit_metadata": self.audit_metadata,
        }
