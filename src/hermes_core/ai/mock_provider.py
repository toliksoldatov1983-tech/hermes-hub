"""Safe mock AI provider — returns only local/synthetic responses.

Never calls external APIs. Never reads .env or tokens.
Generates predictable mock responses for testing and dry-run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MockResponse:
    text: str
    intent: str = "general"
    confidence: float = 1.0
    is_mock: bool = True
    safety: dict[str, Any] = field(default_factory=lambda: {
        "blocked": False,
        "real_api_called": False,
        "env_read": False,
        "token_used": False,
    })


class MockProvider:
    """Local mock provider — no external calls, no secrets.

    All methods return MockResponse with is_mock=True and safety metadata.
    """

    def generate_response(self, prompt: str) -> MockResponse:
        return MockResponse(
            text=f"MOCK: {prompt[:100]}",
            intent="general",
            confidence=1.0,
            safety={"blocked": False, "real_api_called": False, "env_read": False, "token_used": False},
        )

    def classify_intent(self, text: str) -> MockResponse:
        lowered = text.lower()
        if "статус" in lowered or "status" in lowered:
            intent = "status"
        elif "малярка" in lowered or "заказ" in lowered:
            intent = "malyarka"
        elif "тест" in lowered or "test" in lowered:
            intent = "test"
        else:
            intent = "general"
        return MockResponse(
            text=f"MOCK_INTENT: {intent}",
            intent=intent,
            safety={"blocked": False, "real_api_called": False, "env_read": False, "token_used": False},
        )

    def summarize_context(self, context: str) -> MockResponse:
        return MockResponse(
            text=f"MOCK_SUMMARY: {context[:120]}",
            intent="summary",
            safety={"blocked": False, "real_api_called": False, "env_read": False, "token_used": False},
        )

    def review_code(self, code: str) -> MockResponse:
        return MockResponse(
            text="MOCK_REVIEW: Code review completed locally. No external review provider configured.",
            intent="review",
            safety={"blocked": False, "real_api_called": False, "env_read": False, "token_used": False},
        )

    def explain_error(self, error: str) -> MockResponse:
        return MockResponse(
            text=f"MOCK_ERROR: {error[:150]}",
            intent="error",
            safety={"blocked": False, "real_api_called": False, "env_read": False, "token_used": False},
        )

    @property
    def is_mock(self) -> bool:
        return True

    @property
    def is_real_api(self) -> bool:
        return False

    @property
    def mode(self) -> str:
        return "mock"
