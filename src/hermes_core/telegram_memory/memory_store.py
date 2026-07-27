"""In-Memory Store — safe, dry-run only. No persistent storage.

No database. No real user data. No secrets.
"""

from __future__ import annotations

from hermes_core.telegram_memory.conversation_memory import ConversationSession, ConversationMode


class InMemoryMemoryStore:
    """In-memory conversation store. Dry-run only.

    Sessions are lost on restart. No persistence.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, ConversationSession] = {}

    def create_session(self, session_id: str = "dry-run-session-001") -> ConversationSession:
        s = ConversationSession(session_id=session_id)
        self._sessions[session_id] = s
        return s

    def get_session(self, session_id: str) -> ConversationSession | None:
        return self._sessions.get(session_id)

    def get_or_create(self, session_id: str = "dry-run-session-001") -> ConversationSession:
        if session_id not in self._sessions:
            return self.create_session(session_id)
        return self._sessions[session_id]

    def reset_session(self, session_id: str) -> ConversationSession:
        return self.create_session(session_id)

    def delete_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def list_sessions(self) -> list[str]:
        return list(self._sessions.keys())

    def count(self) -> int:
        return len(self._sessions)

    @property
    def is_persistent(self) -> bool:
        return False

    @property
    def is_in_memory(self) -> bool:
        return True

    def status_report(self) -> dict:
        return {
            "store_type": "in_memory",
            "persistent": False,
            "sessions_count": self.count(),
            "session_ids": self.list_sessions(),
            "safe_local": True,
            "no_database": True,
            "no_real_data": True,
        }


# Singleton
_default_store = InMemoryMemoryStore()


def get_memory_store() -> InMemoryMemoryStore:
    return _default_store
