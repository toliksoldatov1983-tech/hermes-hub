"""Command help registry for Hermes-Clean local CLI.

Lists every available command with purpose, mode, and approval requirements.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandHelpEntry:
    command: str
    purpose: str
    mode: str
    approval_required: str


APPROVAL_GATES = [
    "APPROVE_GOOGLE_DRIVE_MOVE",
    "APPROVE_GOOGLE_DRIVE_REAUTH",
    "APPROVE_SECRET_SETUP",
    "APPROVE_TELEGRAM_LIVE",
    "APPROVE_REAL_ORDER_ACCESS",
    "APPROVE_MALYARKA_ARCHIVE_IMPORT",
    "APPROVE_DELETE",
    "APPROVE_ARCHIVE_UNPACK",
]


LOCAL_COMMANDS = [
    # ── Core status ──
    CommandHelpEntry("status", "Show local Hermes-Clean status", "local/read-only", "no"),
    CommandHelpEntry("start-summary", "Daily local startup summary", "local/read-only", "no"),
    CommandHelpEntry("health", "Check required local files and .env presence", "local/read-only", "no"),
    CommandHelpEntry("app-status", "Write local app runtime status", "local/read-only", "no"),
    CommandHelpEntry("dashboard", "Write local Hermes-Clean dashboard", "local/read-only", "no"),
    CommandHelpEntry("daily-report", "Write local daily project report", "local/read-only", "no"),
    CommandHelpEntry("project-audit", "Audit local structure, safety, docs coverage", "local/read-only", "no"),
    CommandHelpEntry("refresh-all", "Refresh all local Hermes-Clean summary reports", "local", "no"),
    CommandHelpEntry("export-status", "Export status to markdown", "local/read-only", "no"),
    CommandHelpEntry("release-checklist", "Write release checklist", "local/read-only", "no"),

    # ── Reports ──
    CommandHelpEntry("reports", "List local reports from 05_REPORTS", "local/read-only", "no"),
    CommandHelpEntry("tasks", "Show local task snapshot", "local/read-only", "no"),
    CommandHelpEntry("memory", "Show trusted local memory snapshot", "local/read-only", "no"),
    CommandHelpEntry("help-local", "Show all local commands and approval gates", "local/read-only", "no"),

    # ── Telegram dry-run ──
    CommandHelpEntry("message", "Simulate Telegram incoming message", "dry-run", "no live send"),
    CommandHelpEntry("telegram-scenarios", "Run Telegram dry-run usage scenarios", "dry-run", "no live send"),
    CommandHelpEntry("telegram-status", "Write Telegram dry-run status report", "dry-run", "no live send"),
    CommandHelpEntry("telegram-flow", "Run local Malyarka Telegram dialog flow", "dry-run", "no live send; no real orders"),

    # ── Malyarka ──
    CommandHelpEntry("malyarka-preview", "Preview Malyarka parsing contract", "dry-run", "no real orders"),
    CommandHelpEntry("malyarka-dialog", "Run operator-style local Malyarka dialog commands", "dry-run", "no real orders; no live Telegram"),
    CommandHelpEntry("malyarka-transcript", "Write local Malyarka dialog transcript report", "local/dry-run", "no real orders; report only"),
    CommandHelpEntry("malyarka-fixtures", "Run synthetic Malyarka fixture scenarios", "local/synthetic", "no real orders"),
    CommandHelpEntry("malyarka-disputes", "Classify synthetic Malyarka disputed rows", "local/synthetic", "no real orders"),
    CommandHelpEntry("malyarka-combined", "Show parse, disputes and pricing together", "local/synthetic", "no real orders"),
    CommandHelpEntry("malyarka-schema", "Show Malyarka export schema", "local/synthetic", "no real orders"),
    CommandHelpEntry("malyarka-demo", "Show Malyarka module demo summary", "local/synthetic", "no real orders"),
    CommandHelpEntry("malyarka-pricing", "Show synthetic Malyarka pricing", "local/synthetic", "no real orders"),
    CommandHelpEntry("malyarka-resolve", "Dry-run disputed row replacement", "dry-run", "no real orders"),
    CommandHelpEntry("malyarka-workflow", "Show synthetic Malyarka workflow", "local/synthetic", "no real orders"),
    CommandHelpEntry("malyarka-status", "Write Malyarka module status report", "local/synthetic", "no real orders"),

    # ── AI providers ──
    CommandHelpEntry("ai-provider", "Select mock or disabled AI provider", "dry-run/gated", "APPROVE_SECRET_SETUP"),
    CommandHelpEntry("review-provider", "Select mock or disabled review provider", "dry-run/gated", "APPROVE_SECRET_SETUP"),
    CommandHelpEntry("ai-provider-list", "List all registered AI providers with status", "local/read-only", "no"),
    CommandHelpEntry("ai-provider-status", "Show router status for a specific provider", "local/read-only", "no"),
    CommandHelpEntry("ai-provider-mock", "Select mock provider explicitly", "local/read-only", "no"),
    CommandHelpEntry("ai-provider-router", "Test router decision for a provider", "local/read-only", "no"),
    CommandHelpEntry("ai-provider-capabilities", "Show capabilities of all registered providers", "local/read-only", "no"),
    CommandHelpEntry("secret-gate", "Show secret gate status from universal provider layer", "local/read-only", "no"),
    CommandHelpEntry("review-provider-mock", "Select mock review provider explicitly", "local/read-only", "no"),
    CommandHelpEntry("review-provider-disabled", "Show disabled review provider status", "local/read-only", "no"),

    # ── Daily Assistant ──
    CommandHelpEntry("daily-assistant", "Show daily assistant — full project snapshot", "local/read-only", "no"),
    CommandHelpEntry("daily-brief", "One-screen daily brief summary", "local/read-only", "no"),
    CommandHelpEntry("what-next", "Show next steps and safe commands", "local/read-only", "no"),
    CommandHelpEntry("local-health", "Fast local health check", "local/read-only", "no"),
    CommandHelpEntry("project-status", "Quick project status overview", "local/read-only", "no"),
    CommandHelpEntry("malyarka-mode-status", "Malyarka AI review path status", "local/read-only", "no"),

    # ── Runtime Bridge ──
    CommandHelpEntry("bridge", "Route through Old Hermes → Hermes-Clean bridge", "local/read-only", "no"),

    # ── Mobile Gateway ──
    CommandHelpEntry("mobile-gateway-status", "Show mobile gateway status", "local/read-only", "no"),
    CommandHelpEntry("mobile-api-contract", "Show all mobile API endpoints", "local/read-only", "no"),
    CommandHelpEntry("mobile-api-dry-run", "Dry-run all mobile API endpoints", "local/read-only", "no"),
    CommandHelpEntry("mobile-api-server-check", "Quick self-check of local API server", "local/read-only", "no"),

    # ── Mobile Web UI ──
    CommandHelpEntry("mobile-web-status", "Show mobile web UI status", "local/read-only", "no"),
    CommandHelpEntry("mobile-web-preview", "Show mobile web UI preview info", "local/read-only", "no"),
    CommandHelpEntry("mobile-web-files", "List mobile web UI files", "local/read-only", "no"),
    CommandHelpEntry("mobile-web-self-check", "Self-check mobile web UI files", "local/read-only", "no"),

    # ── Android WebView Shell ──
    CommandHelpEntry("android-shell-status", "Show Android shell scaffold status", "local/read-only", "no"),
    CommandHelpEntry("android-shell-files", "List Android shell files", "local/read-only", "no"),
    CommandHelpEntry("android-shell-security-check", "Security check of Android shell", "local/read-only", "no"),
    CommandHelpEntry("android-shell-build-info", "Show Android shell build info", "local/read-only", "no"),

    # ── Safety ──
    CommandHelpEntry("safety", "Classify a requested action via safety gate", "local/read-only", "no"),
    CommandHelpEntry("safety-audit", "Show local safety audit log", "local/read-only", "no"),

    # ── Smoke ──
    CommandHelpEntry("smoke", "Run local Hermes-Clean smoke checks", "local/read-only", "no"),
]


@dataclass(frozen=True)
class CommandHelp:
    commands: list[CommandHelpEntry]
    approval_gates: list[str]


def build_command_help() -> CommandHelp:
    return CommandHelp(commands=list(LOCAL_COMMANDS), approval_gates=list(APPROVAL_GATES))
