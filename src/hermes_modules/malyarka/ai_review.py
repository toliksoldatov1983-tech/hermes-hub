"""Malyarka → AI Provider Router integration (dry-run only).

All Malyarka AI calls go through AIProviderRouter, never directly to Gemini/DeepSeek.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from hermes_core.ai_provider import AIProviderRequest, AIProviderResponse, AIProviderRouter


@dataclass(frozen=True)
class MalyarkaAIReviewResult:
    """Result of AI review for a disputed Malyarka row."""

    raw_text: str
    explanation: str
    recommended_action: str
    provider_id: str = "mock"
    is_mock: bool = True
    safety: dict = field(default_factory=lambda: {
        "real_api_called": False,
        "env_read": False,
        "token_used": False,
        "network_called": False,
        "direct_gemini_call": False,
        "direct_deepseek_call": False,
    })


def review_disputed_row(raw_text: str) -> MalyarkaAIReviewResult:
    """Review a single disputed row through the AI Provider Router.

    This is the ONLY path Malyarka uses for AI review.
    No direct Gemini or DeepSeek calls.
    """

    router = AIProviderRouter()

    # Always use "mock" in safe-local mode — router enforces policy
    response = router.generate(
        provider_id="mock",
        request=AIProviderRequest(
            prompt=raw_text,
            system_prompt=(
                "Ты — Malyarka AI ассистент. Анализируй спорную строку заказа и объясни, "
                "почему она спорная и что рекомендуется сделать (delete или clarify). "
                "Отвечай на русском."
            ),
        ),
    )

    return MalyarkaAIReviewResult(
        raw_text=raw_text,
        explanation=_build_explanation(raw_text, response.text),
        recommended_action=_recommend_action(raw_text),
        provider_id=response.provider_id,
        is_mock=response.is_mock,
        safety={
            "real_api_called": response.safety.get("real_api_called", False),
            "env_read": response.safety.get("env_read", False),
            "token_used": response.safety.get("token_used", False),
            "network_called": response.safety.get("network_called", False),
            "direct_gemini_call": False,
            "direct_deepseek_call": False,
        },
    )


def review_disputed_rows(rows: list[str]) -> list[MalyarkaAIReviewResult]:
    """Review multiple disputed rows through the router."""
    return [review_disputed_row(r) for r in rows]


def ai_explain_dispute_category(category: str, raw_text: str) -> MalyarkaAIReviewResult:
    """Provide AI explanation for a dispute category."""
    router = AIProviderRouter()
    response = router.generate(
        provider_id="mock",
        request=AIProviderRequest(
            prompt=f"Category: {category}\nText: {raw_text}",
            system_prompt="Объясни, почему эта строка попала в категорию спора. Ответь на русском.",
        ),
    )
    return MalyarkaAIReviewResult(
        raw_text=raw_text,
        explanation=response.text,
        recommended_action="clarify",
        provider_id=response.provider_id,
        is_mock=response.is_mock,
    )


# ── helpers ──


def _build_explanation(raw_text: str, router_text: str) -> str:
    """Build a human-readable explanation from router output."""
    if router_text.startswith("MOCK:"):
        if "нет разделителя" in raw_text.lower() or "|" not in raw_text:
            return (
                f"Спорная строка '{raw_text}' — отсутствует или нарушен разделитель '|'. "
                "Рекомендуется удалить строку или уточнить у заказчика."
            )
        if "не указана" in raw_text.lower() or raw_text.count("|") < 2:
            return (
                f"Спорная строка '{raw_text}' — неполный формат. "
                "Рекомендуется уточнить количество и единицу измерения."
            )
        return f"Спорная строка '{raw_text}' — требуется уточнение у заказчика."
    return router_text


def _recommend_action(raw_text: str) -> str:
    """Recommend action for a disputed row."""
    if "|" not in raw_text or raw_text.count("|") < 2:
        return "delete"
    return "clarify"
