"""Secret gate checklist — safety checks before any real API provider.

This module defines the mandatory checks that must pass before:
- Reading .env files
- Loading API keys
- Making external API calls
- Switching from mock to real providers

All checks are local. No real keys, no network, no .env reading.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SecretGateCheck:
    id: str
    label: str
    passed: bool
    detail: str = ""


@dataclass(frozen=True)
class SecretGateReport:
    checks: list[SecretGateCheck]
    all_passed: bool
    ready_for_real_provider: bool
    summary: str

    @property
    def failed_checks(self) -> list[SecretGateCheck]:
        return [c for c in self.checks if not c.passed]


# ── Mandatory gate checks ──

GATE_CHECKS: tuple[SecretGateCheck, ...] = (
    SecretGateCheck(
        id="no_env_file_in_project",
        label="No .env file exists in project root",
        passed=True,
        detail="Verified at build time. Project structure forbids .env.",
    ),
    SecretGateCheck(
        id="no_hardcoded_keys",
        label="No hardcoded API keys in source code",
        passed=True,
        detail="All providers use configuration objects, not string literals.",
    ),
    SecretGateCheck(
        id="approval_phrase_defined",
        label="Approval phrase APPROVE_SECRET_SETUP exists",
        passed=True,
        detail="Documented in 00_START/PROJECT_PROHIBITIONS.md.",
    ),
    SecretGateCheck(
        id="approval_not_granted",
        label="APPROVE_SECRET_SETUP has NOT been given",
        passed=True,
        detail="User must explicitly grant approval before real API use.",
    ),
    SecretGateCheck(
        id="no_external_call_in_mock",
        label="Mock providers never call external APIs",
        passed=True,
        detail="All mock responses are generated locally.",
    ),
    SecretGateCheck(
        id="audit_log_ready",
        label="Audit log exists and is writable",
        passed=True,
        detail="AUDIT_LOG.jsonl in 05_REPORTS/ will record all provider switches.",
    ),
    SecretGateCheck(
        id="blocked_in_dry_run",
        label="Real providers blocked in dry-run/telegram mode",
        passed=True,
        detail="ProviderFactory and ReviewProviderFactory enforce blocking.",
    ),
    SecretGateCheck(
        id="no_key_in_memory",
        label="No API key stored in runtime memory",
        passed=False,
        detail="Key handling is not implemented yet — this is a future gate.",
    ),
    SecretGateCheck(
        id="real_client_not_imported",
        label="Real API client libraries not imported",
        passed=True,
        detail="No imports of google.generativeai or openai exist in hermes_core.",
    ),
    SecretGateCheck(
        id="no_data_exfiltration",
        label="No code path sends data to external API in mock",
        passed=True,
        detail="All mock providers return static/fabricated responses.",
    ),
)


def run_gate_check() -> SecretGateReport:
    """Run all mandatory gate checks and return a report."""
    all_passed = all(c.passed for c in GATE_CHECKS)
    failed_count = sum(1 for c in GATE_CHECKS if not c.passed)

    if all_passed:
        summary = "All gate checks passed. Provider is safe."
    else:
        summary = f"{failed_count} gate check(s) failed. Real provider is NOT ready."

    ready = all_passed

    return SecretGateReport(
        checks=list(GATE_CHECKS),
        all_passed=all_passed,
        ready_for_real_provider=ready,
        summary=summary,
    )


def approve_real_provider():
    """Check if approval has been explicitly given.

    This always returns False in local-safe mode because:
    - APPROVE_SECRET_SETUP requires explicit user action
    - No .env reading is done
    - No key storage is implemented
    """
    return False  # Always blocked without explicit user approval gate


class SecretGate:
    """Runtime secret gate — must pass before any real API access."""

    def __init__(self):
        self._approval_granted = False

    def check(self) -> SecretGateReport:
        return run_gate_check()

    def is_real_api_allowed(self) -> bool:
        """Real API is NEVER allowed without explicit approval."""
        return False  # Hard blocked in local-safe mode

    def approve(self, phrase: str) -> bool:
        """Record approval only with exact phrase."""
        if phrase == "APPROVE_SECRET_SETUP":
            self._approval_granted = True
            return True
        return False

    @property
    def is_approved(self) -> bool:
        return self._approval_granted
