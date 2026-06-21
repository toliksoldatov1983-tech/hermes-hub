"""Read-only collector for mapping an existing server Telegram bot.

The collector reads only allowlisted text files from a provided project copy
or mounted directory. It never imports bot modules, never executes bot code,
never starts processes and never reads environment or secret files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


WHITELIST_FILES: tuple[str, ...] = (
    "malyarka_telegram/app.py",
    "malyarka_telegram/router.py",
    "malyarka_telegram/handlers.py",
    "malyarka_telegram/keyboards.py",
    "malyarka_telegram/messages.py",
    "malyarka_telegram/access.py",
    "malyarka_telegram/modes.py",
    "malyarka_telegram/session.py",
    "malyarka_telegram/intent.py",
    "malyarka_telegram/models.py",
    "malyarka_core/services/orders.py",
    "malyarka_core/services/archive.py",
    "malyarka_core/parsing.py",
    "malyarka_core/validation.py",
    "malyarka_core/calculations.py",
    "requirements.txt",
    "MALYARKA_CURRENT_STATE.md",
)

FORBIDDEN_PATH_PARTS: tuple[str, ...] = (
    ".env",
    "env",
    "token",
    "secret",
    "secrets",
    "password",
    "private_key",
    "private-key",
    "orders.db",
    ".db",
    ".sqlite",
    ".sqlite3",
    "logs",
    "log",
)

SENSITIVE_LINE_PATTERN = re.compile(
    r"(TOKEN|SECRET|API_KEY|PASSWORD|PRIVATE_KEY|bot_token|\.env)",
    re.IGNORECASE,
)

ENTRYPOINT_PATTERN = re.compile(r"(__main__|run_polling|Dispatcher|Router|Bot\(|main\()", re.IGNORECASE)
MODE_PATTERN = re.compile(r"\b(mode|state|fsm|session)\b", re.IGNORECASE)
HANDLER_PATTERN = re.compile(r"(@\w+\.message|@\w+\.callback_query|message_handler|callback_query|Command\()", re.IGNORECASE)
CALLBACK_PATTERN = re.compile(r"(callback|Callback|callback_data)")
KEYBOARD_PATTERN = re.compile(r"(Keyboard|Button|ReplyKeyboard|InlineKeyboard|callback_data)")
CORE_PATTERN = re.compile(r"(malyarka_core|orders|archive|parsing|validation|calculations)")
EXPORT_PATTERN = re.compile(r"(export|xlsx|excel|corel|file|document)", re.IGNORECASE)
ACCESS_PATTERN = re.compile(r"(owner|admin|access|allow|deny|permission|role)", re.IGNORECASE)


@dataclass(frozen=True)
class FileScan:
    relative_path: str
    exists: bool
    redacted_lines: list[str]
    entrypoints: list[str]
    modes: list[str]
    handlers: list[str]
    callbacks: list[str]
    keyboards: list[str]
    telegram_to_core: list[str]
    exports: list[str]
    owner_access_checks: list[str]


def redact_line(line: str) -> str:
    """Mask suspicious lines before they can be written to a report."""
    if SENSITIVE_LINE_PATTERN.search(line):
        return "[REDACTED: suspicious secret-like line]"
    return line.rstrip()


def is_forbidden_path(relative_path: str) -> bool:
    """Return whether a path is outside the safe read-only boundary."""
    lowered = relative_path.replace("\\", "/").lower()
    parts = [part for part in lowered.split("/") if part]
    return any(
        part in FORBIDDEN_PATH_PARTS
        or part.endswith(".log")
        or any(marker in part for marker in ("token", "secret", "password", "private_key"))
        for part in parts
    )


def collect(source_root: Path) -> list[FileScan]:
    """Collect a static report model from allowlisted files only."""
    root = source_root.resolve()
    scans: list[FileScan] = []
    for relative_path in WHITELIST_FILES:
        if is_forbidden_path(relative_path):
            continue
        path = (root / relative_path).resolve()
        if not _is_inside(path, root):
            continue
        if not path.exists() or not path.is_file():
            scans.append(_missing_scan(relative_path))
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        scans.append(_scan_text(relative_path, text))
    return scans


def build_report(source_root: Path, scans: Iterable[FileScan]) -> str:
    """Build a markdown report with safety status and static maps."""
    scans = list(scans)
    checked = [scan.relative_path for scan in scans if scan.exists]
    missing = [scan.relative_path for scan in scans if not scan.exists]
    lines: list[str] = [
        "# Server Bot Read-Only Report",
        "",
        "## Safety status",
        "",
        "```text",
        "read_only: true",
        "whitelist_only: true",
        "bot_code_executed: false",
        "bot_modules_imported: false",
        "processes_started: false",
        "environment_read: false",
        "env_file_read: false",
        "token_read: false",
        "files_changed: false",
        "```",
        "",
        "## Source",
        "",
        "```text",
        str(source_root),
        "```",
        "",
        "## Whitelist files checked",
        "",
        *_bullet_lines(checked),
        "",
        "## Whitelist files missing",
        "",
        *_bullet_lines(missing),
        "",
        "## What was not read",
        "",
        "- .env",
        "- token-like files",
        "- secret files",
        "- environment variables",
        "- databases",
        "- logs",
        "- private keys",
        "",
        "## What was not executed",
        "",
        "- Telegram bot",
        "- polling",
        "- webhook",
        "- subprocesses",
        "- bot module imports",
        "- server commands",
        "",
    ]
    for title, attr in (
        ("Entry points", "entrypoints"),
        ("Modes", "modes"),
        ("Handlers", "handlers"),
        ("Callbacks", "callbacks"),
        ("Keyboards", "keyboards"),
        ("Telegram to core", "telegram_to_core"),
        ("Exports", "exports"),
        ("Owner/access checks", "owner_access_checks"),
    ):
        lines.extend(_section_from_scans(title, scans, attr))
    lines.extend(
        [
            "## Redaction",
            "",
            "Lines containing TOKEN, SECRET, API_KEY, PASSWORD, PRIVATE_KEY, bot_token or .env are replaced with:",
            "",
            "```text",
            "[REDACTED: suspicious secret-like line]",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(source_root: Path, output_path: Path) -> Path:
    """Collect and write the markdown report."""
    scans = collect(source_root)
    report = build_report(source_root, scans)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe read-only server bot collector")
    parser.add_argument("--source", required=True, help="Path to a local copy or mounted server bot root")
    parser.add_argument("--output", default="SERVER_BOT_READ_ONLY_REPORT.md", help="Report path")
    args = parser.parse_args()
    write_report(Path(args.source), Path(args.output))
    return 0


def _scan_text(relative_path: str, text: str) -> FileScan:
    redacted_lines: list[str] = []
    entrypoints: list[str] = []
    modes: list[str] = []
    handlers: list[str] = []
    callbacks: list[str] = []
    keyboards: list[str] = []
    telegram_to_core: list[str] = []
    exports: list[str] = []
    owner_access_checks: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        redacted = redact_line(line)
        redacted_lines.append(redacted)
        marker = f"{relative_path}:{line_number}: {redacted.strip()}"
        if ENTRYPOINT_PATTERN.search(line):
            entrypoints.append(marker)
        if MODE_PATTERN.search(line):
            modes.append(marker)
        if HANDLER_PATTERN.search(line):
            handlers.append(marker)
        if CALLBACK_PATTERN.search(line):
            callbacks.append(marker)
        if KEYBOARD_PATTERN.search(line):
            keyboards.append(marker)
        if CORE_PATTERN.search(line):
            telegram_to_core.append(marker)
        if EXPORT_PATTERN.search(line):
            exports.append(marker)
        if ACCESS_PATTERN.search(line):
            owner_access_checks.append(marker)

    return FileScan(
        relative_path=relative_path,
        exists=True,
        redacted_lines=redacted_lines,
        entrypoints=entrypoints,
        modes=modes,
        handlers=handlers,
        callbacks=callbacks,
        keyboards=keyboards,
        telegram_to_core=telegram_to_core,
        exports=exports,
        owner_access_checks=owner_access_checks,
    )


def _missing_scan(relative_path: str) -> FileScan:
    return FileScan(relative_path, False, [], [], [], [], [], [], [], [], [])


def _is_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _section_from_scans(title: str, scans: list[FileScan], attr: str) -> list[str]:
    items: list[str] = []
    for scan in scans:
        items.extend(getattr(scan, attr))
    return [f"## {title}", "", *_bullet_lines(items), ""]


def _bullet_lines(items: Iterable[str]) -> list[str]:
    values = list(items)
    if not values:
        return ["- none"]
    return [f"- {item}" for item in values]


if __name__ == "__main__":
    raise SystemExit(main())
