"""Gemini provider — disabled placeholder with secret gate integration.

Real API calls require APPROVE_SECRET_SETUP, SecretGate pass, and a configured key.
This module never reads .env, never imports google.generativeai, and never
makes network calls.  All methods return BLOCKED responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hermes_core.ai.mock_provider import MockResponse
from hermes_core.ai.secret_gate import SecretGate, run_gate_check


@dataclass(frozen=True)
class GeminiBlockedResponse:
    text: str
    blocked: bool = True
    reason: str = ""
    gate_report: dict[str, Any] = field(default_factory=dict)
    is_mock: bool = True
    safety: dict[str, Any] = field(default_factory=lambda: {
        "real_api_called": False,
        "env_read": False,
        "token_used": False,
        "network_called": False,
    })


class GeminiProvider:
    """Placeholder for future Gemini integration.

    Never functional in local-safe mode:
      - Secret gate must pass
      - APPROVE_SECRET_SETUP must be explicitly given
      - GEMINI_API_KEY must be confirmed (but never read/stored)
      - google.generativeai must not be imported until gate passes
    """

    def __init__(self, enabled: bool = False, secret_gate: SecretGate | None = None) -> None:
        self.enabled = enabled
        self._secret_gate = secret_gate or SecretGate()

    def _blocked_response(self, reason: str = "") -> GeminiBlockedResponse:
        gate = run_gate_check()
        return GeminiBlockedResponse(
            text="BLOCKED: Gemini API is not enabled in this local-safe Hermes-Clean block.",
            reason=reason or "Provider is disabled.",
            gate_report={
                "all_passed": gate.all_passed,
                "ready": gate.ready_for_real_provider,
                "summary": gate.summary,
                "approval_granted": self._secret_gate.is_approved,
            },
        )

    def generate_response(self, prompt: str) -> GeminiBlockedResponse:
        return self._blocked_response("generate_response blocked.")

    def classify_intent(self, text: str) -> GeminiBlockedResponse:
        return self._blocked_response("classify_intent blocked.")

    def summarize_context(self, context: str) -> GeminiBlockedResponse:
        return self._blocked_response("summarize_context blocked.")

    def review_code(self, code: str) -> GeminiBlockedResponse:
        return self._blocked_response("review_code blocked.")

    def explain_error(self, error: str) -> GeminiBlockedResponse:
        return self._blocked_response("explain_error blocked.")

    def run_secret_gate_check(self) -> dict[str, Any]:
        """Run all mandatory secret gate checks and return report."""
        gate = run_gate_check()
        return {
            "all_passed": gate.all_passed,
            "ready": gate.ready_for_real_provider,
            "summary": gate.summary,
            "failed_checks": [c.id for c in gate.failed_checks],
            "approval_granted": self._secret_gate.is_approved,
        }

    @property
    def is_mock(self) -> bool:
        return True

    @property
    def is_real_api(self) -> bool:
        """Always False — real API requires APPROVE_SECRET_SETUP."""
        return False

    @property
    def is_real_api_ready(self) -> bool:
        """Check if all gates are passed and approval is granted.

        Returns False until:
          1. Secret gate: all 10 checks pass
          2. APPROVE_SECRET_SETUP explicitly approved
          3. Key availability confirmed (but key never read)
        """
        gate = run_gate_check()
        return gate.all_passed and self._secret_gate.is_approved

    @property
    def mode(self) -> str:
        return "gemini-disabled"
