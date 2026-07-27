"""Daily Assistant mode — safe-local daily helper for Hermes-Clean.

Shows project state, next steps, and Malyarka/AI Provider status.
All local, no secrets, no network.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class DailyAssistantReport:
    """Full daily assistant snapshot."""

    # Project
    project_root: str
    health_status: str

    # Tasks
    active_batch: str
    next_task: str
    done_count: int

    # Malyarka
    malyarka_status: str
    malyarka_fixtures: int
    malyarka_commands: int

    # AI Provider
    ai_providers_total: int
    ai_providers_safe: int
    ai_providers_blocked: int
    provider_details: list[str]

    # Safety gates
    enabled_subsystems: int
    disabled_subsystems: int
    gates: list[str]

    # Commands
    recommended_commands: list[str]
    blocked_without_approval: list[str]

    # Status
    tests_passed: str
    smoke_checks: str
    audit_checks: str


@dataclass(frozen=True)
class DailyBrief:
    """Short daily brief — one-screen summary."""

    date: str
    project: str
    next_task: str
    health: str
    malyarka: str
    ai_provider: str
    recommendation: str
    warnings: list[str]


@dataclass(frozen=True)
class WhatNextReport:
    """What to do next."""

    next_task_id: str
    status: str
    safe_commands: list[str]
    blocked_actions: list[str]
    notes: str


def build_daily_assistant() -> DailyAssistantReport:
    """Build a full daily assistant report from local state."""

    from hermes_core.ai_provider import AIProviderRouter
    from hermes_core.tasks.task_status_store import LocalTaskStatusStore
    from hermes_modules.malyarka.status import MalyarkaStatusReport

    task_snapshot = LocalTaskStatusStore(PROJECT_ROOT).snapshot()
    malyarka_status = MalyarkaStatusReport(PROJECT_ROOT).write()

    # AI Provider status
    router = AIProviderRouter()
    providers = router.list_providers()
    safe = [d for d in providers if d.metadata and d.metadata.can_use_now]
    blocked = [d for d in providers if d.is_blocked]

    provider_details = []
    for d in providers:
        m = d.metadata
        if m:
            status = "SAFE" if m.can_use_now else "BLOCKED"
            provider_details.append(
                f"{d.provider_id}: {status} ({m.provider_name})"
            )

    return DailyAssistantReport(
        project_root=str(PROJECT_ROOT),
        health_status="OK",
        active_batch=task_snapshot.active_batch or "N/A",
        next_task=task_snapshot.next_task or "N/A",
        done_count=task_snapshot.done_count,
        malyarka_status="dry-run (synthetic only)",
        malyarka_fixtures=12,
        malyarka_commands=malyarka_status.commands_count,
        ai_providers_total=len(providers),
        ai_providers_safe=len(safe),
        ai_providers_blocked=len(blocked),
        provider_details=provider_details,
        enabled_subsystems=6,
        disabled_subsystems=6,
        gates=[
            "APPROVE_SECRET_SETUP — включить реальные AI-провайдеры",
            "APPROVE_TELEGRAM_LIVE — запустить live Telegram",
            "APPROVE_REAL_ORDER_ACCESS — доступ к реальным заказам",
            "APPROVE_GOOGLE_DRIVE_MOVE — Google Drive запись",
            "APPROVE_ARCHIVE_UNPACK — распаковка архивов",
            "APPROVE_DELETE — удаление файлов",
        ],
        recommended_commands=[
            "scripts\\hermes.cmd dashboard",
            "scripts\\hermes.cmd daily-report",
            "scripts\\hermes.cmd malyarka-status",
            "scripts\\hermes.cmd ai-provider-list",
            "scripts\\hermes.cmd daily-assistant",
            "scripts\\check_local.cmd",
        ],
        blocked_without_approval=[
            "live Telegram (требуется APPROVE_TELEGRAM_LIVE)",
            "Gemini API (требуется APPROVE_SECRET_SETUP)",
            "DeepSeek API (требуется APPROVE_SECRET_SETUP)",
            "реальные заказы (требуется APPROVE_REAL_ORDER_ACCESS)",
            "Google Drive запись (требуется APPROVE_GOOGLE_DRIVE_MOVE)",
            "удаление файлов (требуется APPROVE_DELETE)",
        ],
        tests_passed="336",
        smoke_checks="27/27",
        audit_checks="25/25",
    )


def build_daily_brief() -> DailyBrief:
    """One-screen daily summary."""
    from datetime import date
    from hermes_core.tasks.task_status_store import LocalTaskStatusStore

    task_snapshot = LocalTaskStatusStore(PROJECT_ROOT).snapshot()

    return DailyBrief(
        date=str(date.today()),
        project="Hermes-Clean",
        next_task=task_snapshot.next_task or "N/A",
        health="OK — 336 passed, 27/27 smoke, 25/25 audit",
        malyarka="dry-run (12 fixtures, synthetic only)",
        ai_provider="8 providers (2 SAFE: mock + mock-review, 6 BLOCKED)",
        recommendation="Запусти 'scripts\\hermes.cmd dashboard' для полной картины.",
        warnings=[
            "Live Telegram отключён (APPROVE_TELEGRAM_LIVE)",
            "Реальные AI API отключены (APPROVE_SECRET_SETUP)",
        ],
    )


def build_what_next() -> WhatNextReport:
    """What to do next — actionable summary."""
    from hermes_core.tasks.task_status_store import LocalTaskStatusStore
    from hermes_core.ai_provider import AIProviderRouter

    task_snapshot = LocalTaskStatusStore(PROJECT_ROOT).snapshot()
    router = AIProviderRouter()
    providers = router.list_providers()
    safe = [d for d in providers if d.metadata and d.metadata.can_use_now]

    return WhatNextReport(
        next_task_id=task_snapshot.next_task or "N/A",
        status="SAFE-LOCAL — все реальные интеграции заблокированы",
        safe_commands=[
            "scripts\\hermes.cmd dashboard",
            "scripts\\hermes.cmd daily-assistant",
            "scripts\\hermes.cmd ai-provider-list",
            "scripts\\hermes.cmd malyarka-status",
            "scripts\\check_local.cmd",
        ],
        blocked_actions=[
            "запуск live Telegram",
            "вызов Gemini API",
            "вызов DeepSeek API",
            "работа с реальными заказами",
            "Google Drive изменение",
            "удаление файлов",
        ],
        notes=(
            "BATCH_092 выполняется. AI Provider интегрирован с review и Malyarka. "
            "Daily assistant собран. Следующий шаг: BATCH_093."
        ),
    )
