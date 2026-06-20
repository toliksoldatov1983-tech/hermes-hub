# SERVER_SSH_ACCESS_CURRENT_STATUS

Дата: 2026-06-20

Технический пакет: `BATCH_PHASE2_PREP_SSH_VERIFY_ROLLBACK`

## Статус SSH

SSH-доступ к серверу `hermes / 178.104.95.187` подтверждён read-only проверкой.

Способ подтверждения:

```text
ssh root@178.104.95.187
```

Проверка выполнялась с коротким timeout и без изменения серверных файлов.

Результат:

```text
SSH_OK
```

## Runtime status

Service:

```text
malyarka-telegram-bot.service
```

Read-only status:

```text
LoadState=loaded
ActiveState=active
SubState=running
UnitFileState=disabled
MainPID=28149
```

Process command line:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

## Hermes adapter feature flag

Read-only flag check:

```text
malyarka_core/adapters/telegram.py: _HERMES_ADAPTER_ENABLED = False
```

Interpretation:

```text
Hermes adapter feature flag is OFF.
```

## Blockers

No SSH blocker found in this verification.

Phase 2 is still not allowed to run without separate approval phrase:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

## No-touch confirmation

No server changes were made.

Not performed:

- service start/restart/stop/enable/disable;
- feature flag changes;
- production enable;
- Phase 2 launch;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- `.py` code change;
- git/commit/push.

