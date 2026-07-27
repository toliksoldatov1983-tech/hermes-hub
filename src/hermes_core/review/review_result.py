from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReviewResult:
    provider: str
    approved: bool
    findings: list[str] = field(default_factory=list)
    cycles_used: int = 0
    can_edit_project: bool = False
    blocked_reason: str | None = None
