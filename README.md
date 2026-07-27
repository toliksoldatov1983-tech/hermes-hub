# Hermes-Clean

Hermes-Clean is the clean local workspace for the new Hermes assistant.

Project path:

```text
C:\Users\user\Desktop\Hermes-Clean
```

Old archives, quarantine folders, Google Drive documents and old Hermes/Malyarka projects are archive sources only. They are not the current source of truth.

## Quick Start

Run from `C:\Users\user\Desktop\Hermes-Clean`:

```cmd
scripts\hermes.cmd refresh-all
scripts\hermes.cmd dashboard
scripts\hermes.cmd smoke
```

Open:

```text
05_REPORTS\LOCAL_DASHBOARD.md
```

## Current Verified State

- CLI commands: 35
- Tests: 278 passed
- Project audit: 25 checks, 0 failed
- Smoke: 23 checks, 0 failed
- Release checklist: OK
- Source of truth: Hermes-Clean only

## Ready Locally

- Local CLI and reports
- Safety gate
- Secret Guard
- Memory Sync
- Telegram dry-run
- Malyarka synthetic dialogs
- Malyarka transcript reports
- Google Drive blocked-state freeze/stub

## Dry-Run Only

- Telegram
- Gemini / DeepSeek / DeepSig providers
- Malyarka orders
- File exports
- Google Drive write/move
- Archive import

## Main Commands

```cmd
scripts\run_tests.cmd
scripts\hermes.cmd smoke
scripts\hermes.cmd project-audit
scripts\hermes.cmd release-checklist
scripts\hermes.cmd dashboard
scripts\hermes.cmd help-local
```

## Malyarka

```cmd
scripts\hermes.cmd malyarka-demo
scripts\hermes.cmd malyarka-fixtures
scripts\hermes.cmd malyarka-combined
scripts\hermes.cmd malyarka-dialog --script disputed
scripts\hermes.cmd malyarka-transcript --script disputed
```

Malyarka currently uses synthetic/manual test input only. Real orders are blocked until a separate approval gate.

## Telegram

```cmd
scripts\hermes.cmd message /status
scripts\hermes.cmd telegram-scenarios
scripts\hermes.cmd telegram-status
scripts\hermes.cmd telegram-flow --case disputed
```

Telegram is dry-run only. Live polling, webhooks and real sends are disabled.

## Safety

Do not touch without a separate approval gate:

- real `.env`, tokens or keys;
- live Telegram;
- real orders or client documents;
- Google Drive writes;
- old archives as working projects;
- delete operations.

## Approval Gates

```text
APPROVE_SECRET_SETUP
APPROVE_TELEGRAM_LIVE
APPROVE_REAL_ORDER_ACCESS
APPROVE_GOOGLE_DRIVE_MOVE
APPROVE_GOOGLE_DRIVE_REAUTH
APPROVE_MALYARKA_ARCHIVE_IMPORT
APPROVE_ARCHIVE_UNPACK
APPROVE_DELETE
```

## Key Docs

- `START_HERE.md`
- `docs\WINDOWS_COMMANDS.md`
- `docs\RELEASE_READINESS_SUMMARY.md`
- `docs\LOCAL_SAFETY_MAP.md`
- `docs\MALYARKA_DIALOG_COMMANDS.md`
- `docs\MALYARKA_TRANSCRIPT_REPORTS.md`
- `03_TASKS\NEXT_TASK.md`
