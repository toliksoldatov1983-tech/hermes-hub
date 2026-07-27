# TELEGRAM_DRY_RUN_PLAN

Telegram starts as dry-run only.

No polling, no webhook, no token reads, no outbound messages.

Dry-run output:

- planned_response;
- blocked_actions;
- warnings;
- next_step.

Future commands: `/статус`, `/задача`, `/память`, `/малярка`, `/инженер`, `/отчёт`.

## Implemented dry-run commands

All commands work locally through:

```cmd
scripts\hermes.cmd message /статус
scripts\hermes.cmd message /задача
scripts\hermes.cmd message /память
scripts\hermes.cmd message /малярка "пример заказа"
scripts\hermes.cmd message /инженер
scripts\hermes.cmd message /отчёт
```

## Structured response

Dry-run returns:

- `command`;
- `planned_response`;
- `blocked_actions`;
- `warnings`;
- `next_step`;
- `payload.*`.

## Safety

`/малярка` blocks real order access and final export. Live Telegram remains disabled until `APPROVE_TELEGRAM_LIVE`.
