# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_ROLLBACK_PLAN

Дата: 2026-06-20

## Purpose

Plan rollback for a future approved live patch of `hermes_adapter.py`.

This document does not perform rollback and does not touch the server.

## Required backup before future patch

Before applying the patch, create a timestamped backup of:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Backup must be created before upload.

If backup cannot be created, stop before patch.

## Rollback trigger

Rollback if:

- syntax check fails;
- import check fails;
- service becomes unstable;
- ordinary bot sanity check fails;
- `/start` behavior is broken;
- order flow is still broken;
- feature flag state becomes unclear;
- production risk appears.

## Rollback action

Future rollback should restore the exact backup file over:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Then run syntax/import checks again.

Restart service only if the approved future patch plan requires restart.

## Final rollback confirmations

After rollback, confirm:

```text
feature flag: OFF
production: OFF
service state: recorded
autostart: disabled
Phase 2: OFF
```

## Always forbidden

- enabling production;
- enabling autostart;
- reading `.env`, `config.py`, token, `os.environ`;
- reading DB/live logs/real orders;
- changing unrelated files;
- git/commit/push.

