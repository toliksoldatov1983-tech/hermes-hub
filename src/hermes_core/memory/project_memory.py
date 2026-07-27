from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProjectMemory:
    decisions: list[str] = field(default_factory=list)
    prohibitions: list[str] = field(default_factory=list)
    pending_approvals: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

    def remember_decision(self, decision: str) -> None:
        self.decisions.append(decision)

    def add_pending_approval(self, approval: str) -> None:
        self.pending_approvals.append(approval)
