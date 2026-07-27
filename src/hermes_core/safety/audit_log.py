"""Safe local audit log for Hermes-Clean.

Logs only safe/synthetic/local events.  Never writes secrets, real orders,
tokens, .env content, or external API details.  Audit log lives inside
05_REPORTS/ and is a plain JSON-lines file.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hermes_core.types import ActionDecision

# ── Constants ──

AUDIT_LOG_FILE = "AUDIT_LOG.jsonl"
MAX_LOG_SIZE_BYTES = 500_000  # 500 KB, hard cap
MAX_LOG_ENTRIES = 200

# Categories that MUST NOT appear in audit log
FORBIDDEN_AUDIT_KEYS = {
    "token", "api_key", "secret", "password",
    "orders_db", "real_order", "client_name", "client_phone",
    "env_value",
}

# ── Data types ──

@dataclass(frozen=True)
class AuditEntry:
    """A single audit log entry."""

    timestamp: str
    action: str
    decision: str  # SAFE / CONFIRM_REQUIRED / BLOCKED
    source: str  # cli / test / smoke / batch
    detail: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "decision": self.decision,
            "source": self.source,
            "detail": self.detail,
            "extra": self.extra,
        }


@dataclass(frozen=True)
class AuditLogSnapshot:
    """Read-only snapshot of the current audit log."""

    entries: list[AuditEntry]
    total_entries: int
    safe_count: int
    confirm_count: int
    blocked_count: int
    log_path: str


# ── Audit log writer ──

class LocalAuditLog:
    """Writes safe events to a local audit log file.

    Rules:
      - Only SAFE / CONFIRM_REQUIRED / BLOCKED events.
      - Never writes secrets, tokens, .env contents.
      - Never writes real order data.
      - Truncates old entries when limit reached.
      - Validates every entry before writing.
    """

    def __init__(self, project_root: Path):
        self._log_dir = project_root / "05_REPORTS"
        self._log_path = self._log_dir / AUDIT_LOG_FILE

    # ── Writing ──

    def log(
        self,
        action: str,
        decision: ActionDecision,
        source: str = "cli",
        detail: str = "",
        extra: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Write one audit entry and return it.

        Raises ValueError if the entry contains forbidden keys.
        """
        _validate_no_secrets(action, detail, extra or {})

        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            action=action,
            decision=decision.value,
            source=source,
            detail=detail,
            extra=extra or {},
        )
        self._write_entry(entry)
        return entry

    def log_safe(
        self,
        action: str,
        source: str = "cli",
        detail: str = "",
        extra: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Shortcut for SAFE action."""
        return self.log(action, ActionDecision.SAFE, source, detail, extra)

    def log_confirm_required(
        self,
        action: str,
        source: str = "cli",
        detail: str = "",
        extra: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Shortcut for CONFIRM_REQUIRED action."""
        return self.log(action, ActionDecision.CONFIRM_REQUIRED, source, detail, extra)

    def log_blocked(
        self,
        action: str,
        source: str = "cli",
        detail: str = "",
        extra: dict[str, Any] | None = None,
    ) -> AuditEntry:
        """Shortcut for BLOCKED action."""
        return self.log(action, ActionDecision.BLOCKED, source, detail, extra)

    # ── Reading ──

    def read_all(self) -> list[AuditEntry]:
        """Read all audit log entries."""
        if not self._log_path.exists():
            return []
        entries = []
        for line in self._log_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                entries.append(AuditEntry(
                    timestamp=data.get("timestamp", ""),
                    action=data.get("action", ""),
                    decision=data.get("decision", ""),
                    source=data.get("source", ""),
                    detail=data.get("detail", ""),
                    extra=data.get("extra", {}),
                ))
            except (json.JSONDecodeError, TypeError):
                continue
        return entries

    def snapshot(self) -> AuditLogSnapshot:
        """Return a read-only snapshot of the audit log."""
        entries = self.read_all()
        safe = sum(1 for e in entries if e.decision == "SAFE")
        confirm = sum(1 for e in entries if e.decision == "CONFIRM_REQUIRED")
        blocked = sum(1 for e in entries if e.decision == "BLOCKED")
        return AuditLogSnapshot(
            entries=entries,
            total_entries=len(entries),
            safe_count=safe,
            confirm_count=confirm,
            blocked_count=blocked,
            log_path=str(self._log_path),
        )

    def clear(self):
        """Clear the audit log (only for testing/synthetic use)."""
        if self._log_path.exists():
            self._log_path.unlink()

    # ── Internal ──

    def _write_entry(self, entry: AuditEntry):
        self._log_dir.mkdir(parents=True, exist_ok=True)
        line = json.dumps(entry.to_dict(), ensure_ascii=False) + "\n"

        if self._log_path.exists():
            current = self._log_path.read_text(encoding="utf-8")
            # Truncate old entries if limit exceeded
            lines = [l for l in current.splitlines() if l.strip()]
            if len(lines) >= MAX_LOG_ENTRIES:
                lines = lines[-(MAX_LOG_ENTRIES - 1):]
            if len(current.encode("utf-8")) + len(line.encode("utf-8")) > MAX_LOG_SIZE_BYTES:
                # Drop oldest entries until under limit
                while len(lines) > 1 and sum(len(l.encode("utf-8")) for l in lines) + len(line.encode("utf-8")) > MAX_LOG_SIZE_BYTES:
                    lines.pop(0)
            self._log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(line)


# ── Validation ──

def _validate_no_secrets(action: str, detail: str, extra: dict[str, Any]) -> None:
    """Raise ValueError if any forbidden key appears in the entry."""
    check = f"{action} {detail} {json.dumps(extra)}".lower()
    for forbidden in FORBIDDEN_AUDIT_KEYS:
        if forbidden in check:
            raise ValueError(
                f"Audit log entry contains forbidden key '{forbidden}'. "
                f"Secret/real data must never be logged."
            )


def _sanitize_detail(detail: str) -> str:
    """Redact any accidental secret-like patterns from detail text."""
    if not detail:
        return detail
    # Redact key=value patterns
    import re
    detail = re.sub(r'(?:api_?key|token|secret|password)\s*[:=]\s*\S+', '[REDACTED]', detail, flags=re.IGNORECASE)
    return detail
