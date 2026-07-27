"""Telegram dry-run status report generator (improved)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hermes_core.telegram.blocked_actions import BLOCKED, blocked_by_category, blocked_summary
from hermes_core.telegram.scenarios import SCENARIOS


ALIASES = [
    "/status", "/task", "/memory", "/malyarka", "/malyarka-combined",
    "/engineer", "/report", "/check",
    "/order", "/disputes", "/fix", "/export-blocked", "/audit", "/safety", "/blocked",
    "/статус", "/задача", "/память", "/малярка", "/инженер", "/отчёт",
    "/заказ", "/споры", "/исправить", "/экспорт-заблокирован", "/аудит",
]

SAFETY_LIMITS = [
    "live polling disabled",
    "webhook disabled",
    "token reading disabled",
    "message sending disabled",
    "real order access disabled",
    ".env reading disabled",
    "API key access disabled",
    "file export disabled",
    "Google Drive write disabled",
    "archive reading disabled",
]


@dataclass(frozen=True)
class TelegramStatusResult:
    path: Path
    aliases_count: int
    scenarios_count: int
    safety_limits_count: int
    blocked_actions_count: int
    blocked_categories: dict[str, int]


class TelegramDryRunStatusReport:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.output_path = self.project_root / "05_REPORTS" / "TELEGRAM_DRY_RUN_STATUS.md"

    def write(self) -> TelegramStatusResult:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self._render(), encoding="utf-8")
        return TelegramStatusResult(
            path=self.output_path,
            aliases_count=len(ALIASES),
            scenarios_count=len(SCENARIOS),
            safety_limits_count=len(SAFETY_LIMITS),
            blocked_actions_count=len(BLOCKED),
            blocked_categories=blocked_summary(),
        )

    def _render(self) -> str:
        aliases = "\n".join(f"- `{alias}`" for alias in ALIASES)
        scenarios = "\n".join(
            f"- `{s.name}` → `{s.command}` — {s.purpose}" for s in SCENARIOS
        )
        limits = "\n".join(f"- {limit}" for limit in SAFETY_LIMITS)

        blocked_telegram = blocked_by_category("telegram")
        blocked_secrets = blocked_by_category("secrets")
        blocked_orders = blocked_by_category("orders")
        blocked_export = blocked_by_category("export")
        blocked_external = blocked_by_category("external")

        def _fmt_blocked(items):
            return "\n".join(f"- {ba.id}: {ba.label}" for ba in items)

        return (
            "# TELEGRAM_DRY_RUN_STATUS\n\n"
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
            f"## Summary\n\n"
            f"- Aliases: {len(ALIASES)}\n"
            f"- Scenarios: {len(SCENARIOS)}\n"
            f"- Safety limits: {len(SAFETY_LIMITS)}\n"
            f"- Blocked actions: {len(BLOCKED)}\n\n"
            "## Aliases\n\n"
            f"{aliases}\n\n"
            "## Scenarios\n\n"
            f"{scenarios}\n\n"
            "## Safety Limits\n\n"
            f"{limits}\n\n"
            "## Blocked Actions — Telegram\n\n"
            f"{_fmt_blocked(blocked_telegram)}\n\n"
            "## Blocked Actions — Secrets\n\n"
            f"{_fmt_blocked(blocked_secrets)}\n\n"
            "## Blocked Actions — Orders\n\n"
            f"{_fmt_blocked(blocked_orders)}\n\n"
            "## Blocked Actions — Export\n\n"
            f"{_fmt_blocked(blocked_export)}\n\n"
            "## Blocked Actions — External\n\n"
            f"{_fmt_blocked(blocked_external)}\n\n"
            "## Approval Gate\n\n"
            "`APPROVE_TELEGRAM_LIVE` is required before live Telegram polling, "
            "webhook, token use or outbound messages.\n"
        )
