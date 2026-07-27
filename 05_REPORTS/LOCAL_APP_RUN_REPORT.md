# LOCAL_APP_RUN_REPORT

## Block

BATCH_011_PREPARE_LOCAL_HERMES_APP_RUN

## Done

Hermes-Clean now has a safe local CLI runner:

- `python -m hermes_core status`
- `scripts\hermes.cmd status`
- `scripts\hermes.cmd message /статус`
- `scripts\hermes.cmd route "удали файл"`
- `scripts\hermes.cmd safety delete`
- `scripts\hermes.cmd malyarka-preview "пример заказа"`

## Safety

The local app does not touch:

- Google Drive;
- old archives;
- quarantine;
- real orders;
- client documents;
- tokens;
- keys;
- `.env`;
- live Telegram;
- old projects.

## Checks

- `scripts\hermes.cmd status` — OK.
- `scripts\hermes.cmd message /статус` — OK.
- `scripts\hermes.cmd safety delete` — OK, returns `BLOCKED`.
- `scripts\hermes.cmd malyarka-preview "пример заказа"` — OK, final export remains blocked.
- `python -m unittest discover -s tests` — OK, 15 tests.

## Next

Recommended next local safe block: deepen Telegram dry-run command handling without live Telegram.
