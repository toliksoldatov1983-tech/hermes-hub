# Server Bot Controlled Start Precheck Checklist

Date: 2026-06-20

Mode: markdown-only checklist.

Status: `PLAN_ONLY`

## Purpose

Define the checklist that must pass before a future approved controlled start of:

```text
malyarka-telegram-bot.service
```

## Required Precheck Items

The future operator must confirm:

- [ ] Exact approval phrase was given:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

- [ ] SSH access is available.
- [ ] Service exists:

```text
malyarka-telegram-bot.service
```

- [ ] Service is currently inactive/dead.
- [ ] Service is disabled; autostart is not enabled.
- [ ] Entrypoint is known and unchanged:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

- [ ] Working directory is:

```text
/opt/malyarka-telegram-bot
```

- [ ] Service user is:

```text
malyarka-bot
```

- [ ] Adapter is present:

```text
malyarka_core/adapters/hermes_adapter.py
malyarka_core/adapters/telegram.py
```

- [ ] Backup marker is present:

```text
telegram.py.before_hook
```

- [ ] Feature flag is confirmed OFF.
- [ ] No production enable is requested.
- [ ] No secrets are required for the check.
- [ ] No logs, DB, real orders or token values are required.

## Feature Flag OFF Requirement

Expected state:

```text
_HERMES_ADAPTER_ENABLED = False
```

If this cannot be confirmed safely, stop before service start.

## Precheck Stop Conditions

Stop if:

- approval phrase is missing;
- service is already active unexpectedly;
- service file points to an unexpected entrypoint;
- feature flag appears ON or cannot be safely confirmed OFF;
- any step requires reading `.env`, `config.py`, token, DB, logs or real orders;
- user asks to enable autostart;
- user asks to continue Phase 2 or production enable in the same step.

## No-Touch Rule

This checklist is documentation only.

Do not run commands until separate approval is given.

