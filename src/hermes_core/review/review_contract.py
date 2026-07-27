from __future__ import annotations

from typing import Protocol

from hermes_core.review.review_result import ReviewResult


class CodeReviewer(Protocol):
    def review(self, code: str, cycles_used: int = 0) -> ReviewResult: ...
