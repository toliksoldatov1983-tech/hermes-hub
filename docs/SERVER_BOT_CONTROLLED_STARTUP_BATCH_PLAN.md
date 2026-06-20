# Server Bot Controlled Startup Batch Plan

Technical name: `SERVER_BOT_CONTROLLED_STARTUP_BATCH_PLAN`

Date: 2026-06-20

Mode: markdown-only batch packet.

Status: `PLAN_ONLY_NOT_APPROVED_FOR_START`

## Purpose

Prepare a complete documentation packet for a future one-time controlled start of the existing server Telegram bot service:

```text
malyarka-telegram-bot.service
```

This document does not authorize any server action.

## Current Status

Server:

```text
178.104.95.187
```

Project path:

```text
/opt/malyarka-telegram-bot
```

Service:

```text
malyarka-telegram-bot.service
```

Systemd facts:

```text
FragmentPath=/etc/systemd/system/malyarka-telegram-bot.service
ExecStart=/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
WorkingDirectory=/opt/malyarka-telegram-bot
User=malyarka-bot
```

Current runtime state:

```text
ActiveState=inactive
SubState=dead
is-enabled=disabled
```

Project facts:

- adapter is installed;
- `malyarka_core/adapters/hermes_adapter.py` exists;
- `malyarka_core/adapters/telegram.py` exists;
- `telegram.py.before_hook` exists;
- feature flag should be OFF according to project documents;
- live dry-run is not currently confirmed;
- production enable has not been performed;
- Gate 9 must not be treated as complete without separate user decision.

## Why Start Requires Separate Approval

Starting the service is a live server action.

It may:

- connect to Telegram polling;
- make the bot visible to users;
- execute runtime code;
- expose unknown runtime behavior;
- require rollback if unsafe.

Therefore start is forbidden until the user gives the exact approval phrase:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

## Future Pre-Start Checks

Before any future start, the controlled run must verify:

- SSH access is available;
- service exists;
- service is currently inactive/dead;
- service remains disabled;
- entrypoint matches expected `--run-polling`;
- working directory is `/opt/malyarka-telegram-bot`;
- user is `malyarka-bot`;
- adapter files are present;
- feature flag is OFF;
- no production enable is requested;
- no secrets are read.

See:

```text
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_PRECHECK_CHECKLIST.md
```

## Future Start

The future start command is documented only:

```text
systemctl start malyarka-telegram-bot.service
```

Do not run it without the exact approval phrase.

Do not use `restart` or `enable` as part of the first controlled start.

## Future Post-Start Checks

After a future approved start:

- confirm service becomes active/running;
- confirm one polling process exists;
- perform only safe Telegram phone tests;
- do not test Vision/API;
- do not use real orders;
- do not enable production;
- document final service state.

## Fast Stop

If the service behaves unexpectedly, the future rollback action is:

```text
systemctl stop malyarka-telegram-bot.service
```

Then confirm:

```text
systemctl is-active malyarka-telegram-bot.service
```

Expected:

```text
inactive
```

## Success Criteria

Future controlled start is successful only if:

- approval phrase was given;
- precheck passed;
- service started once;
- service became active/running;
- Telegram phone test passed with safe dummy messages;
- no secrets were read;
- feature flag stayed OFF;
- production enable was not performed;
- final state was documented.

## Failure Criteria

The future controlled start fails if:

- approval phrase is missing;
- service is already in an unexpected state;
- feature flag is not confirmed OFF;
- service fails to start;
- more than one bot process appears;
- unsafe behavior is observed;
- secrets/logs/DB/orders are required for diagnosis;
- production behavior is triggered.

On failure, stop and record result.

## Strict No-Touch For This Batch

For this markdown-only batch:

- server was not touched;
- SSH was not started;
- service start/restart/enable was not performed;
- bot was not started;
- `.env`, `config.py`, token, `os.environ`, DB, logs and real orders were not read;
- `.py` code was not changed;
- git/commit/push was not performed;
- production was not enabled;
- Phase 2 was not continued.

## Batch Documents

This batch includes:

```text
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_STARTUP_BATCH_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_PRECHECK_CHECKLIST.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_COMMAND_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_TELEGRAM_TEST_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_APPROVAL_GATE.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_REPORT_TEMPLATE.md
E:\Hermes-Hub\docs\SERVER_BOT_CONTROLLED_START_DECISION_MAP.md
```

## Final Batch Status

```text
SERVER_BOT_CONTROLLED_STARTUP_BATCH_PLAN_READY
```

Next step:

```text
Wait for APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

