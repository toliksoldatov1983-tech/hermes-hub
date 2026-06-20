# Server Bot Controlled Stop Plan Only

Date: 2026-06-20

Mode: plan only.

Status: `STOP_NOT_APPROVED`

## Purpose

Prepare a future controlled stop plan for:

```text
malyarka-telegram-bot.service
```

This batch does not stop the service.

## Required Approval Phrase

Future stop requires:

```text
APPROVE_SERVER_BOT_CONTROLLED_STOP_ONCE
```

## Future Stop Command

Only after exact approval:

```text
systemctl stop malyarka-telegram-bot.service
```

## Future Post-Stop Checks

```text
systemctl is-active malyarka-telegram-bot.service
systemctl show malyarka-telegram-bot.service --property=ActiveState,SubState,MainPID --no-pager
pgrep -af 'malyarka_telegram.app --run-polling'
```

Expected:

```text
inactive
ActiveState=inactive
SubState=dead
no polling process
```

## No-Secrets Policy

Do not read:

- `.env`;
- `config.py`;
- token;
- `os.environ`;
- DB;
- logs;
- real orders.

## Stop Report

After future stop, document:

- approval phrase;
- stop command result;
- final service state;
- autostart state;
- feature flag state if safely checked;
- no-touch confirmations.

