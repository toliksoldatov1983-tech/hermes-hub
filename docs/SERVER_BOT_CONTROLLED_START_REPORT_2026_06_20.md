# Server Bot Controlled Start Report

Technical name: `SERVER_BOT_CONTROLLED_START_REPORT`

Date: 2026-06-20

Status: `CONTROLLED_START_AND_TELEGRAM_TEST_PASSED`

## Metadata

Approval phrase received:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

Target service:

```text
malyarka-telegram-bot.service
```

Server:

```text
178.104.95.187
```

Project path:

```text
/opt/malyarka-telegram-bot
```

## Precheck Result

Precheck before start:

- SSH access: available;
- service exists: yes;
- pre-start service state: `inactive/dead`;
- autostart state: `disabled`;
- entrypoint:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

- working directory:

```text
/opt/malyarka-telegram-bot
```

- service user:

```text
malyarka-bot
```

- adapter present: yes;
- `hermes_adapter.py`: present;
- `telegram.py`: present;
- `telegram.py.before_hook`: present;
- feature flag OFF: confirmed;

```text
_HERMES_ADAPTER_ENABLED = False
```

- no production enable: confirmed;
- no secrets read: confirmed.

## Start Result

Start command run once:

```text
systemctl start malyarka-telegram-bot.service
```

Start result:

```text
success
```

Post-start service state:

```text
ActiveState=active
SubState=running
MainPID=28149
```

Autostart state after start:

```text
disabled
```

Polling process:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

## Telegram Test Result

User performed safe phone test.

Test steps and observed results:

1. `/start` — bot answered with menu.
2. `700 x 500` outside order mode — bot answered that it looks like an order and suggested switching to `/заказ`.
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

Telegram test result:

```text
PASSED
```

## Rollback / Stop Result

Stop was not performed because user has not yet given a separate decision to stop.

Current state after test:

```text
service running
autostart disabled
feature flag OFF
production not enabled
```

## Final State

Final service state:

```text
ActiveState=active
SubState=running
MainPID=28149
```

Final enabled/autostart state:

```text
disabled
```

Final feature flag state:

```text
OFF
```

Production enable:

```text
not performed
```

Phase 2:

```text
not continued
```

## No-Touch Confirmations

Confirmed:

- `.env` was not read;
- `config.py` was not read;
- token was not read;
- `os.environ` was not read;
- DB was not read;
- logs were not read;
- real orders were not read;
- `.py` code was not changed;
- feature flag was not changed;
- git/commit/push was not used;
- production was not enabled;
- Phase 2 was not continued;
- `systemctl enable` was not run;
- `systemctl restart` was not run;
- stop was not run after test.

## Final Decision

```text
SUCCESS
```

## Required User Decision

The service is currently running.

Next step requires a separate user decision:

```text
leave service running
```

or:

```text
perform controlled stop
```

