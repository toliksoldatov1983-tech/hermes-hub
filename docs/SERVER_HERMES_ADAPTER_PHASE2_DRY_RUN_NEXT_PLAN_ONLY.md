# Server Hermes Adapter Phase 2 Dry-Run Next Plan Only

Date: 2026-06-20

Mode: plan only.

Status: `PHASE_2_NOT_APPROVED`

## Current Position

Telegram bot controlled start passed.

Service is running.

Hermes adapter feature flag remains OFF.

Production is not enabled.

Phase 2 is not running and must not start automatically after controlled start.

## What Phase 2 Would Mean Later

Future Phase 2 dry-run may mean:

- explicitly enabling Hermes adapter dry-run path;
- keeping production disabled;
- using safe dummy inputs only;
- monitoring behavior;
- preserving rollback.

It is not authorized now.

## Required Future Approval Phrase

Future Phase 2 dry-run requires:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

## Prerequisites Before Any Phase 2 Dry-Run

- service stable/running;
- feature flag currently OFF;
- controlled start report accepted;
- no real orders;
- no production;
- rollback plan ready;
- user explicitly approves the Phase 2 phrase.

## Strict Prohibitions Now

Do not:

- enable Hermes adapter flag;
- change `.py` code;
- run production;
- use real orders;
- read secrets;
- read DB/logs/orders;
- restart/stop/enable service as part of Phase 2 planning.

## Next Step

Wait for user decision:

```text
leave running
controlled stop
Phase 2 dry-run plan only
```

