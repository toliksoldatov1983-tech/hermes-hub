# LOCAL_APP_READINESS_PLAN

## Status

Hermes-Clean is ready for local-safe daily use as a command-line application skeleton.

It is not ready for live Telegram, real AI API calls, Google Drive writes or real order processing.

## Daily Local Start

Run from:

```cmd
cd /d C:\Users\user\Desktop\Hermes-Clean
```

Recommended daily sequence:

```cmd
scripts\start_hermes.cmd
scripts\hermes.cmd refresh-all
scripts\hermes.cmd dashboard
scripts\hermes.cmd daily-report
scripts\hermes.cmd smoke
```

Optional full check:

```cmd
scripts\run_tests.cmd
```

## Ready Local Commands

Read-only status and reports:

- `scripts\hermes.cmd start-summary`
- `scripts\hermes.cmd health`
- `scripts\hermes.cmd reports`
- `scripts\hermes.cmd tasks`
- `scripts\hermes.cmd memory`
- `scripts\hermes.cmd app-status`
- `scripts\hermes.cmd daily-report`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd dashboard`
- `scripts\hermes.cmd refresh-all`
- `scripts\hermes.cmd help-local`

Dry-run and synthetic commands:

- `scripts\hermes.cmd message /status`
- `scripts\hermes.cmd telegram-scenarios`
- `scripts\hermes.cmd telegram-status`
- `scripts\hermes.cmd malyarka-preview`
- `scripts\hermes.cmd malyarka-fixtures`
- `scripts\hermes.cmd malyarka-schema`
- `scripts\hermes.cmd malyarka-pricing`
- `scripts\hermes.cmd malyarka-disputes`
- `scripts\hermes.cmd malyarka-combined`
- `scripts\hermes.cmd malyarka-demo`
- `scripts\hermes.cmd ai-provider --mode mock`
- `scripts\hermes.cmd review-provider --mode mock-review`
- `scripts\hermes.cmd safety delete`

Checks:

- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## Disabled Until Approval

These subsystems stay disabled:

- live Telegram;
- real Gemini API;
- real DeepSeek / DeepSig API;
- Google Drive write/move;
- real order access;
- old archive unpack/import.

## Approval Gates

Live or external work requires one of these gates:

- `APPROVE_SECRET_SETUP`
- `APPROVE_TELEGRAM_LIVE`
- `APPROVE_GOOGLE_DRIVE_MOVE`
- `APPROVE_GOOGLE_DRIVE_REAUTH`
- `APPROVE_REAL_ORDER_ACCESS`
- `APPROVE_MALYARKA_ARCHIVE_IMPORT`
- `APPROVE_ARCHIVE_UNPACK`
- `APPROVE_DELETE`

## Current Safety Guarantees

- No `.env` is required for local-safe use.
- No token or key is read.
- No external API is called.
- No Google Drive write is performed.
- No live Telegram polling or webhook is started.
- No real order is processed.
- No old archive is unpacked.

## Next Readiness Layer

The next safe local layer can be one of:

- add a local app launcher summary;
- improve command docs coverage;
- deepen Telegram dry-run routing;
- deepen Malyarka synthetic workflow;
- prepare a UI/dashboard wrapper;
- prepare a future Gemini/DeepSeek secret setup checklist without keys.
