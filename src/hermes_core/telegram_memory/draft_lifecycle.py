"""Draft Lifecycle — manages order draft state transitions.

Dry-run only. No real files. No export.
"""

from __future__ import annotations

from hermes_core.telegram_memory.order_draft import (
    OrderDraft,
    OrderDraftLine,
    OrderDraftStatus,
)


class DraftLifecycle:
    """Manages the lifecycle of an order draft."""

    def __init__(self, store: dict | None = None) -> None:
        self._drafts: dict[str, OrderDraft] = store or {}

    def create(self, source_text: str, draft_id: str = "") -> OrderDraft:
        did = draft_id or f"draft-{len(self._drafts) + 1:03d}"
        draft = OrderDraft(draft_id=did, source_text=source_text, status=OrderDraftStatus.NEW)
        self._drafts[did] = draft
        return draft

    def get(self, draft_id: str) -> OrderDraft | None:
        return self._drafts.get(draft_id)

    def parse_from_text(self, draft_id: str, text: str) -> OrderDraft:
        """Parse text into draft lines and detect disputes."""
        draft = self.get(draft_id)
        if not draft:
            draft = self.create(text, draft_id)

        draft.status = OrderDraftStatus.PARSING
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        for line in lines:
            parts = line.split("|")
            if len(parts) >= 3:
                draft.add_confirmed(OrderDraftLine(
                    raw_text=line,
                    item=parts[0].strip(),
                    quantity=parts[1].strip(),
                    unit=parts[2].strip(),
                    is_confirmed=True,
                ))
            elif "|" in line and len(parts) < 3:
                draft.add_disputed(OrderDraftLine(
                    raw_text=line,
                    is_confirmed=False,
                    is_disputed=True,
                    dispute_reason="Неполный формат: нужно item|qty|unit",
                ))
                draft.add_question(f"Уточни: '{line}' — нужен формат название|количество|единица")
            elif any(c.isdigit() for c in line) and len(line) > 5:
                # Possible order without pipes
                draft.add_disputed(OrderDraftLine(
                    raw_text=line,
                    is_confirmed=False,
                    is_disputed=True,
                    dispute_reason="Нет разделителя '|'. Формат: название|количество|единица",
                ))
                draft.add_question(f"'{line}' — это заказ? Укажи в формате: название|количество|единица")

        if draft.has_disputes:
            draft.status = OrderDraftStatus.HAS_DISPUTES
        elif draft.confirmed_rows:
            draft.status = OrderDraftStatus.PREVIEW_READY
        else:
            draft.status = OrderDraftStatus.NEW

        return draft

    def correct(self, draft_id: str, index: int, new_text: str) -> OrderDraft | None:
        draft = self.get(draft_id)
        if not draft:
            return None
        draft.correct_disputed(index, new_text)
        if not draft.has_disputes:
            draft.status = OrderDraftStatus.AWAITING_CONFIRMATION
        else:
            draft.status = OrderDraftStatus.HAS_DISPUTES
        return draft

    def confirm(self, draft_id: str) -> OrderDraft | None:
        draft = self.get(draft_id)
        if not draft:
            return None
        draft.confirm()
        return draft

    def cancel(self, draft_id: str) -> OrderDraft | None:
        draft = self.get(draft_id)
        if not draft:
            return None
        draft.cancel()
        return draft

    def list_drafts(self) -> list[str]:
        return list(self._drafts.keys())

    def count(self) -> int:
        return len(self._drafts)

    def status_report(self) -> dict:
        return {
            "total_drafts": self.count(),
            "draft_ids": self.list_drafts(),
            "real_export": False,
            "dry_run_only": True,
        }
