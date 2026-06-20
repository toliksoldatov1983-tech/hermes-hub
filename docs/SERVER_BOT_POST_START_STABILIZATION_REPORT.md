# Server Bot Post-Start Stabilization Report

Technical name: `BATCH_SERVER_BOT_POST_START_STABILIZATION`

Date: 2026-06-20

Status: `SERVER_BOT_POST_START_STABILIZATION_DOCUMENTED`

## Scope

Document the state after controlled start and Telegram phone test.

This batch does not authorize or perform restart, stop, enable, Phase 2, production, feature flag changes, code changes, or secret reads.

## Controlled Start Result

Approval used:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

Controlled start result:

```text
success
```

Service:

```text
malyarka-telegram-bot.service
```

Current read-only status check:

```text
ActiveState=active
SubState=running
MainPID=28149
```

Polling process:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

Autostart:

```text
disabled
```

Feature flag:

```text
_HERMES_ADAPTER_ENABLED = False  # off by default
```

## Telegram Test Result

User performed phone test.

Result:

1. `/start` — bot answered with menu.
2. `700 x 500` outside order mode — bot said it looked like an order and suggested switching to `/заказ`.
3. User pressed `Новый заказ`.
4. Bot enabled order mode.
5. User sent `700 x 500` again.
6. Bot returned order preview:
   - confirmed rows: `700 500 1`;
   - disputed rows: none;
   - total details: `1`;
   - total area: `0.350 м²`;
   - export available;
   - buttons appeared:
     - `Скачать Excel для Corel`;
     - `Скачать файл Малярки`;
     - `Скопировать для Corel`.

Telegram test:

```text
PASSED
```

## Safety State

Confirmed:

- service is running;
- autostart remains disabled;
- feature flag remains OFF;
- production enable not performed;
- Phase 2 not continued;
- no real orders used;
- no photos used;
- Vision/API not tested;
- no logs/DB/orders/secrets read.

## Restrictions Going Forward

Do not perform without separate approval:

- restart;
- stop;
- enable/autostart;
- disable;
- feature flag change;
- Phase 2 dry-run;
- production enable;
- reading `.env`, `config.py`, token, `os.environ`;
- reading DB/logs/real orders;
- `.py` code changes;
- git/commit/push.

## Next User Decision Required

Choose one:

```text
A. leave service running
B. perform controlled stop
C. prepare Phase 2 dry-run plan only
D. discuss autostart enable later
E. discuss production much later after gates
```

