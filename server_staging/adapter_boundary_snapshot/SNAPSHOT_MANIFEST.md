# Adapter Boundary Snapshot Manifest

Дата: 2026-06-20

Batch:

```text
BATCH_PHASE2_FETCH_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

Итоговый статус:

```text
ADAPTER_BOUNDARY_SNAPSHOT_READY
```

## Source

Server:

```text
hermes / 178.104.95.187
```

Source files:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

## Local snapshot

Destination folder:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot
```

Local files:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
```

## File hashes

```text
telegram.py       SHA256 000A04938F3AA6BFAF099564AE2CD4FC83E9534354F85C010F4C59CD927EA8503
hermes_adapter.py SHA256 E542114DDDAAB0FE6EE3F68FD9B695E837D4D96104F39F3335B2674E7AB461C0
```

## Safety statement

This is a read-only snapshot for local analysis and future contract tests.

It is not live code.

Server files were not modified.

Not performed:

- systemctl start/restart/stop/enable/disable;
- feature flag change;
- Phase 2 launch;
- production enable;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- live Telegram test;
- git/commit/push.

