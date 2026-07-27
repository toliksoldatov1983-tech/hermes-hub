from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MemorySource:
    name: str
    path: str
    trusted: bool
    notes: str = ""
