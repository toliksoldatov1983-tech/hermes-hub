"""Review provider factory — compatibility bridge to universal AI Provider Router.

This file keeps the old API for backward compatibility but delegates
to the new AIProviderRouter + BaseProviderAdapter architecture internally.
"""

from __future__ import annotations

from dataclasses import dataclass

from hermes_core.ai_provider import AIProviderRouter, AIProviderRequest
from hermes_core.review.review_result import ReviewResult


@dataclass(frozen=True)
class ReviewProviderConfig:
    mode: str = "mock-review"
    secret_setup_approved: bool = False
    key_available: bool = False


@dataclass(frozen=True)
class ReviewProviderSelection:
    provider_name: str
    mode: str
    blocked_reason: str | None = None

    @property
    def is_blocked(self) -> bool:
        return self.blocked_reason is not None

    def review(self, code: str, cycles_used: int = 0) -> ReviewResult:
        """Review code through the universal AI Provider Router."""
        if self.is_blocked:
            return ReviewResult(
                provider=self.provider_name,
                approved=False,
                findings=[self.blocked_reason or "Review provider is blocked."],
                cycles_used=cycles_used,
                can_edit_project=False,
                blocked_reason=self.blocked_reason,
            )

        router = AIProviderRouter()
        provider_id = _mode_to_provider_id(self.mode)
        response = router.generate(
            provider_id=provider_id,
            request=AIProviderRequest(
                prompt=code,
                system_prompt="Review this code for safety, structure, and correctness.",
            ),
        )

        return ReviewResult(
            provider=self.provider_name,
            approved=not response.is_blocked,
            findings=[response.text] if response.text else ["Review completed via router."],
            cycles_used=cycles_used + 1,
            can_edit_project=False,
            blocked_reason=response.blocked_reason if response.is_blocked else None,
        )


class ReviewProviderFactory:
    """Compatibility layer over the universal AI Provider Router.

    Old API preserved. Internally delegates to AIProviderRouter.
    """

    def select(self, config: ReviewProviderConfig | None = None) -> ReviewProviderSelection:
        config = config or ReviewProviderConfig()
        mode = config.mode.strip().lower()
        provider_id = _mode_to_provider_id(mode)

        if mode in {"", "mock-review"}:
            return ReviewProviderSelection("mock-review", "mock-review")

        if mode in {"deepseek-disabled", "deepsig-disabled"}:
            return ReviewProviderSelection(
                "deepseek-review",
                mode,
                "DeepSeek review is disabled until APPROVE_SECRET_SETUP.",
            )

        if mode in {"deepseek", "deepsig"}:
            if not config.secret_setup_approved:
                return ReviewProviderSelection(
                    "deepseek-review",
                    mode,
                    "APPROVE_SECRET_SETUP is required before external review can run.",
                )
            if not config.key_available:
                return ReviewProviderSelection(
                    "deepseek-review",
                    mode,
                    "Review provider key availability must be confirmed without storing the key.",
                )
            return ReviewProviderSelection(
                "deepseek-review",
                mode,
                "Real external review client is not implemented in this local-safe block.",
            )

        return ReviewProviderSelection(
            "mock-review",
            "mock-review",
            f"Unknown review provider mode: {mode}",
        )


def _mode_to_provider_id(mode: str) -> str:
    """Map old review factory mode to new universal provider_id."""
    mapping = {
        "": "mock-review",
        "mock-review": "mock-review",
        "deepseek-disabled": "deepseek-review-disabled",
        "deepsig-disabled": "deepseek-review-disabled",
        "deepseek": "deepseek-review-disabled",
        "deepsig": "deepseek-review-disabled",
    }
    return mapping.get(mode, "mock-review")
