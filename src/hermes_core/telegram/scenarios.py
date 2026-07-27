"""Telegram dry-run usage scenarios for Hermes-Clean.

Expanded with order, disputes, fix, export-blocked, audit scenarios.
All scenarios are dry-run — no live Telegram, no token, no network.
"""

from __future__ import annotations

from dataclasses import dataclass

from hermes_core.telegram.dry_run_gateway import TelegramDryRunGateway
from hermes_core.telegram.message_contract import TelegramMessage


@dataclass(frozen=True)
class TelegramDryRunScenario:
    name: str
    command: str
    purpose: str


@dataclass(frozen=True)
class TelegramDryRunScenarioResult:
    name: str
    command: str
    planned_response: str
    next_step: str
    blocked_actions_count: int
    warnings_count: int


SCENARIOS = [
    # ── Core ──
    TelegramDryRunScenario("morning_status", "/status", "Start the day with local Hermes-Clean status."),
    TelegramDryRunScenario("project_report", "/report", "Read local report index summary."),
    TelegramDryRunScenario("safety_check", "/check", "Run local smoke summary."),

    # ── Malyarka ──
    TelegramDryRunScenario("malyarka_check", "/malyarka", "Check local synthetic Malyarka module state."),
    TelegramDryRunScenario("malyarka_combined_preview", "/malyarka-combined", "Preview local Malyarka parse, disputes and synthetic pricing."),

    # ── Order / disputes / fix / export ──
    TelegramDryRunScenario("order_clean", "/order paint | 2 | bucket\\nroller | 3 | piece", "Parse a clean synthetic order in dry-run."),
    TelegramDryRunScenario("order_disputed", "/order paint 2 bucket", "Parse a disputed format in dry-run."),
    TelegramDryRunScenario("disputes_fixtures", "/disputes", "Show synthetic dispute classification summary."),
    TelegramDryRunScenario("disputes_input", "/disputes paint 2 bucket", "Classify disputes for a specific input."),
    TelegramDryRunScenario("fix_guidance", "/fix paint 2 bucket", "Show how to fix a disputed row."),
    TelegramDryRunScenario("export_blocked_info", "/export-blocked", "Show why export is blocked in dry-run."),

    # ── Safety / audit ──
    TelegramDryRunScenario("blocked_actions_list", "/blocked", "Show all dry-run blocked actions."),
    TelegramDryRunScenario("safety_classify", "/safety delete", "Classify a deletion action via safety gate."),
    TelegramDryRunScenario("audit_summary", "/audit", "Show audit log summary."),

    # ── Russian aliases ──
    TelegramDryRunScenario("status_ru", "/статус", "Russian alias for /status."),
    TelegramDryRunScenario("order_ru", "/заказ краска | 2 | ведро", "Russian alias for /order."),
    TelegramDryRunScenario("disputes_ru", "/споры", "Russian alias for /disputes."),
    TelegramDryRunScenario("export_blocked_ru", "/экспорт-заблокирован", "Russian alias for /export-blocked."),
]


def run_telegram_scenarios() -> list[TelegramDryRunScenarioResult]:
    gateway = TelegramDryRunGateway()
    results = []
    for scenario in SCENARIOS:
        result = gateway.simulate_incoming(TelegramMessage(scenario.command))
        results.append(
            TelegramDryRunScenarioResult(
                name=scenario.name,
                command=scenario.command,
                planned_response=result.planned_response,
                next_step=result.next_step,
                blocked_actions_count=len(result.blocked_actions),
                warnings_count=len(result.warnings),
            )
        )
    return results
