# WINDOWS_COMMANDS

Run all commands from:

```text
C:\Users\user\Desktop\Hermes-Clean
```

## Core Checks

```cmd
scripts\run_tests.cmd
scripts\hermes.cmd smoke
scripts\hermes.cmd project-audit
scripts\hermes.cmd health
scripts\hermes.cmd release-checklist
```

Current verified state:

- tests: 278 passed
- smoke: 23 checks, 0 failed
- project audit: 25 checks, 0 failed
- CLI commands: 35

## Reports

```cmd
scripts\hermes.cmd dashboard
scripts\hermes.cmd daily-report
scripts\hermes.cmd app-status
scripts\hermes.cmd reports
scripts\hermes.cmd export-status
scripts\hermes.cmd refresh-all
```

## Task And Memory

```cmd
scripts\hermes.cmd tasks
scripts\hermes.cmd memory
scripts\hermes.cmd start-summary
```

## Telegram Dry-Run

```cmd
scripts\hermes.cmd message /status
scripts\hermes.cmd telegram-scenarios
scripts\hermes.cmd telegram-status
scripts\hermes.cmd telegram-flow --case clean
scripts\hermes.cmd telegram-flow --case disputed
scripts\telegram_flow.cmd --case disputed
```

No live Telegram is started.

## Malyarka Synthetic

```cmd
scripts\hermes.cmd malyarka-demo
scripts\hermes.cmd malyarka-fixtures
scripts\hermes.cmd malyarka-combined
scripts\hermes.cmd malyarka-disputes
scripts\hermes.cmd malyarka-pricing
scripts\hermes.cmd malyarka-schema
scripts\hermes.cmd malyarka-status
scripts\hermes.cmd malyarka-workflow
scripts\hermes.cmd malyarka-resolve "paint 2 bucket" --replacement "paint | 2 | bucket"
scripts\hermes.cmd malyarka-dialog --script disputed
scripts\hermes.cmd malyarka-transcript --script disputed
scripts\malyarka_dialog.cmd --script disputed
scripts\malyarka_transcript.cmd --script disputed
```

Malyarka uses synthetic/manual test strings only. Real orders remain blocked.

## AI And Review Providers

```cmd
scripts\hermes.cmd ai-provider --mode mock
scripts\hermes.cmd ai-provider --mode gemini-disabled
scripts\hermes.cmd review-provider --mode mock-review
scripts\hermes.cmd review-provider --mode deepseek-disabled
```

Real providers require `APPROVE_SECRET_SETUP`.

## Safety

```cmd
scripts\hermes.cmd safety delete
scripts\hermes.cmd safety-audit
```

`safety delete` must return `BLOCKED`.

## Disabled Until Approval

- live Telegram: `APPROVE_TELEGRAM_LIVE`
- real AI providers: `APPROVE_SECRET_SETUP`
- Google Drive write/move: `APPROVE_GOOGLE_DRIVE_MOVE`
- real orders: `APPROVE_REAL_ORDER_ACCESS`
- archive import: `APPROVE_ARCHIVE_UNPACK`
- delete operations: `APPROVE_DELETE`

## Safety Reminder

These local commands do not read real `.env`, tokens, keys, Google Drive files, real orders, old projects or old archives.
