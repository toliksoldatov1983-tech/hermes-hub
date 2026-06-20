# Server Runtime Startup Read-Only Reconciliation

Date: 2026-06-20

Mode: markdown-only fixation from prior read-only observation.

## Scope

This document fixes the factual runtime state of the existing server Telegram bot line after the read-only check.

No new server action is authorized by this document.

## Current Runtime State

The systemd unit exists:

```text
malyarka-telegram-bot.service
```

Current recorded state:

```text
ActiveState=inactive
SubState=dead
is-enabled=disabled
```

Conclusion:

```text
The server Telegram bot is not currently running.
The service exists, but it is inactive/dead and disabled.
```

## Known Entrypoint

The known service entrypoint is:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

Known working directory:

```text
/opt/malyarka-telegram-bot
```

Known service user:

```text
malyarka-bot
```

## Adapter State

The Hermes adapter is recorded as installed on the server line:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
```

The adapter must remain off by default unless a separate explicit approval changes that.

## Gate 9 Reconciliation

Gate 9 must not be treated as completed without a separate decision.

Reason:

- some project documents claim bot running / live dry-run passed;
- the read-only runtime observation records the service as inactive/dead and disabled;
- live dry-run is not currently confirmed;
- production enable is not performed.

Current safe conclusion:

```text
Gate 9 is disputed / not accepted as complete for operational decisions.
```

## Production State

Production enable has not been performed.

Do not enable the feature flag, start/restart the service, enable the service, or perform production rollout without a separate explicit approval.

## No-Touch Confirmation

For this markdown-only fixation:

- server was not touched;
- Telegram bot was not started;
- service start/restart/enable was not performed;
- `.env`, `config.py`, token, `os.environ`, databases, logs and real orders were not read;
- `.py` code was not changed;
- git/commit/push was not performed.

## Next Safe Step

Prepare a separate approval-gated plan if the user wants to decide what to do with the inactive service:

1. keep the bot stopped;
2. inspect startup policy read-only;
3. prepare a guarded start/restart plan;
4. prepare rollback and monitoring before any live action.

