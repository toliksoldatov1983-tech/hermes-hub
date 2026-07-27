"""DeepSeek / DeepSig review loop — mock with safety metadata.

All reviews are local-only. No external API, no key reading, no network.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hermes_core.review.review_result import ReviewResult


@dataclass(frozen=True)
class MockReviewMetadata:
    provider: str
    mock_pattern: str
    safety: dict[str, Any] = field(default_factory=lambda: {
        "real_api_called": False,
        "env_read": False,
        "token_used": False,
        "network_called": False,
        "can_edit_project": False,
    })


class DeepSeekReviewLoop:
    MAX_CYCLES = 2

    # ── Mock review patterns ──
    MOCK_PATTERNS = {
        "safety": "MOCK_REVIEW [safety]: Code passes local safety checks. No secrets, no external calls detected.",
        "structure": "MOCK_REVIEW [structure]: Code follows Hermes-Clean conventions. Module boundaries respected.",
        "malyarka": "MOCK_REVIEW [malyarka]: Malyarka module uses synthetic data only. Export gate enforced.",
        "telegram": "MOCK_REVIEW [telegram]: Telegram module is dry-run only. No live polling/webhook.",
        "general": "MOCK_REVIEW [general]: Local mock review completed. No external review provider configured.",
    }

    def __init__(self, provider_name: str = "mock-review") -> None:
        self.provider_name = provider_name

    def review(self, code: str, cycles_used: int = 0) -> ReviewResult:
        if cycles_used >= self.MAX_CYCLES:
            return ReviewResult(
                self.provider_name,
                approved=False,
                findings=["Review cycle limit reached (max 2)."],
                cycles_used=cycles_used,
                can_edit_project=False,
            )

        pattern = self._detect_pattern(code)
        findings = [self.MOCK_PATTERNS.get(pattern, self.MOCK_PATTERNS["general"])]

        return ReviewResult(
            self.provider_name,
            approved=True,
            findings=findings,
            cycles_used=cycles_used + 1,
            can_edit_project=False,
        )

    def _detect_pattern(self, code: str) -> str:
        """Detect what kind of code is being reviewed for appropriate mock pattern."""
        lowered = code.lower()
        if "token" in lowered or "secret" in lowered or "api_key" in lowered:
            return "safety"
        if "malyarka" in lowered or "order" in lowered:
            return "malyarka"
        if "telegram" in lowered or "polling" in lowered:
            return "telegram"
        if "class " in lowered or "def " in lowered:
            return "structure"
        return "general"

    def review_with_metadata(self, code: str, cycles_used: int = 0) -> tuple[ReviewResult, MockReviewMetadata]:
        """Review and also return safety metadata."""
        result = self.review(code, cycles_used)
        meta = MockReviewMetadata(
            provider=self.provider_name,
            mock_pattern=self._detect_pattern(code),
        )
        return result, meta

    @property
    def is_mock(self) -> bool:
        return True

    @property
    def is_real_api(self) -> bool:
        return False

    @property
    def is_real_api_ready(self) -> bool:
        """Always False — external review requires APPROVE_SECRET_SETUP."""
        return False
