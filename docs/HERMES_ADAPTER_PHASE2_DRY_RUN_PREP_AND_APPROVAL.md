# HERMES_ADAPTER_PHASE2_DRY_RUN_PREP_AND_APPROVAL

Дата: 2026-06-20

Технический пакет: `BATCH_PHASE2_PREP_SSH_VERIFY_ROLLBACK`

## Current accepted status

```text
server: hermes / 178.104.95.187
service: malyarka-telegram-bot.service
service state: active/running
autostart: disabled
Hermes adapter: installed
feature flag: _HERMES_ADAPTER_ENABLED = False
Telegram test: passed
production: OFF / not enabled
Phase 2: OFF / not started
SSH: verified read-only
```

## Phase 2 status

Phase 2 is not running.

The feature flag remains OFF.

Production remains OFF.

The bot was previously controlled-started and the Telegram phone test passed.

## Approval gate

Future Phase 2 dry-run may happen only after this exact approval phrase:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

Messages like `+`, `continue`, `делай дальше`, or general approval do not permit Phase 2.

## SSH dependency

SSH is currently verified read-only.

If SSH later becomes unavailable, Phase 2 is blocked until SSH verification/fix is separately confirmed.

## Forbidden without separate approval

- enable Hermes adapter flag;
- restart service;
- stop service;
- enable autostart;
- enable production;
- run Phase 2;
- read `.env`, `config.py`, token, `os.environ`;
- read DB/live logs/real orders;
- change `.py` code;
- git/commit/push.

