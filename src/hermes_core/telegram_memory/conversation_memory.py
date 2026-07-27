"""Conversation Memory — safe-local dry-run session state.

No real user data. No persistent storage. In-memory only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
from typing import Any


class ConversationMode(Enum):
    GENERAL_CHAT = "general_chat"
    MALYARKA_ORDER = "malyarka_order"
    MALYARKA_CORRECTION = "malyarka_correction"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    PROJECT_STATUS = "project_status"
    DAILY_ASSISTANT = "daily_assistant"
    SAFETY_BLOCKED = "safety_blocked"
    IDLE = "idle"


class ReplyExpectation(Enum):
    NONE = "none"
    YES_NO = "yes_no"
    CORRECTION = "correction"
    CLARIFICATION = "clarification"
    CONFIRMATION = "confirmation"
    FREE_TEXT = "free_text"


@dataclass
class ConversationTurn:
    """One turn in the conversation."""

    role: str  # "user" or "bot"
    text: str
    intent: str = ""
    confidence: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        return {
            "role": self.role, "text": self.text[:200],
            "intent": self.intent, "confidence": self.confidence,
            "timestamp": self.timestamp,
        }


@dataclass
class ConversationSession:
    """A conversation session — in-memory, dry-run only."""

    session_id: str = "dry-run-session-001"
    mode: ConversationMode = ConversationMode.IDLE
    last_intent: str = ""
    last_confidence: float = 0.0
    active_order_draft_id: str = ""
    pending_question: str = ""
    expected_reply_type: ReplyExpectation = ReplyExpectation.NONE
    last_user_message_summary: str = ""
    last_bot_response_summary: str = ""
    turns: list[ConversationTurn] = field(default_factory=list)
    turn_count: int = 0
    safe_local: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "real_user": False,
        "real_session": False,
        "persistent_storage": False,
        "in_memory_only": True,
        "telegram_token_used": False,
        "env_read": False,
    })

    @property
    def has_active_draft(self) -> bool:
        return bool(self.active_order_draft_id)

    @property
    def is_awaiting_reply(self) -> bool:
        return self.expected_reply_type != ReplyExpectation.NONE

    def add_turn(self, role: str, text: str, intent: str = "", confidence: float = 0.0) -> None:
        self.turns.append(ConversationTurn(role=role, text=text, intent=intent, confidence=confidence))
        self.turn_count = len(self.turns)
        self.updated_at = datetime.utcnow().isoformat()
        if role == "user":
            self.last_user_message_summary = text[:100]
        else:
            self.last_bot_response_summary = text[:100]

    def set_mode(self, mode: ConversationMode) -> None:
        self.mode = mode
        self.updated_at = datetime.utcnow().isoformat()

    def set_pending_question(self, question: str, expectation: ReplyExpectation) -> None:
        self.pending_question = question
        self.expected_reply_type = expectation

    def clear_pending_question(self) -> None:
        self.pending_question = ""
        self.expected_reply_type = ReplyExpectation.NONE

    def attach_draft(self, draft_id: str) -> None:
        self.active_order_draft_id = draft_id

    def detach_draft(self) -> None:
        self.active_order_draft_id = ""

    def last_n_turns(self, n: int = 5) -> list[ConversationTurn]:
        return self.turns[-n:] if self.turns else []

    def context_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "mode": self.mode.value,
            "last_intent": self.last_intent,
            "has_draft_order": self.has_active_draft,
            "has_disputed_rows": False,  # set externally
            "awaiting_confirmation": self.expected_reply_type == ReplyExpectation.CONFIRMATION,
            "pending_question": self.pending_question,
            "turn_count": self.turn_count,
        }

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "mode": self.mode.value,
            "last_intent": self.last_intent,
            "active_order_draft_id": self.active_order_draft_id,
            "pending_question": self.pending_question,
            "expected_reply_type": self.expected_reply_type.value,
            "turn_count": self.turn_count,
            "safe_local": self.safe_local,
            "audit_metadata": self.audit_metadata,
        }
