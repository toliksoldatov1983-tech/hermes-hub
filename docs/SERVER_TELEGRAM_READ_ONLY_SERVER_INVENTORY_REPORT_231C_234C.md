# Read-only server inventory report

Technical name: `BATCH_231C_234C_EXPLICIT_SSH_KEY_INVENTORY_RETRY`

Date: 2026-06-16

## Result

SSH access with explicit key succeeded.

Connection check:

```text
ssh -i "%USERPROFILE%\.ssh\hetzner_hermes" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=10 root@178.104.95.187 "printf 'ssh_ok\n'"
```

Observed:

```text
ssh_ok
```

Read-only presence-only inventory was completed for:

```text
/opt/malyarka-telegram-bot
```

## Inventory Scope

Allowed:

- check whether `/opt/malyarka-telegram-bot` exists;
- collect top-level file/folder names;
- collect `.py` filenames up to depth 3;
- record app/router/handlers/services/orders/config/env/db/log zones only as presence facts.

Forbidden:

- read `.env`;
- read `config.py` contents;
- read token values;
- read `os.environ`;
- read databases;
- read logs;
- read real orders;
- read private IDs;
- read API keys;
- read webhook URLs;
- launch Python code;
- import live bot modules;
- launch app/router/handlers;
- launch polling/webhook;
- launch collector;
- change or create server files.

## What Was Checked

Root path:

```text
ROOT_PRESENT yes
```

Top-level presence-only structure:

```text
d .venv
f MALYARKA_CURRENT_STATE.md
d malyarka_ai
d malyarka_core
d malyarka_telegram
d malyarka_vision
f requirements.txt
```

Python filenames up to depth 3:

```text
malyarka_ai/__init__.py
malyarka_ai/bridge.py
malyarka_ai/config.py
malyarka_ai/contracts.py
malyarka_ai/deepseek.py
malyarka_ai/diagnostics.py
malyarka_ai/pipeline.py
malyarka_ai/prompts.py
malyarka_core/__init__.py
malyarka_core/adapters/__init__.py
malyarka_core/adapters/cli.py
malyarka_core/adapters/telegram.py
malyarka_core/calculations.py
malyarka_core/exports/__init__.py
malyarka_core/exports/corel.py
malyarka_core/exports/malyarka.py
malyarka_core/exports/malyarka_file.py
malyarka_core/models.py
malyarka_core/parsing.py
malyarka_core/security/__init__.py
malyarka_core/security/permissions.py
malyarka_core/services/__init__.py
malyarka_core/services/archive.py
malyarka_core/services/orders.py
malyarka_core/storage/__init__.py
malyarka_core/storage/reference_data.py
malyarka_core/storage/repository.py
malyarka_core/storage/schema.py
malyarka_core/validation.py
malyarka_telegram/__init__.py
malyarka_telegram/access.py
malyarka_telegram/app.py
malyarka_telegram/config.py
malyarka_telegram/engineer_tasks.py
malyarka_telegram/handlers.py
malyarka_telegram/intent.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/modes.py
malyarka_telegram/obsidian_inbox.py
malyarka_telegram/router.py
malyarka_telegram/session.py
malyarka_telegram/voice.py
malyarka_vision/__init__.py
malyarka_vision/config.py
malyarka_vision/gemini.py
```

Zone presence:

```text
present malyarka_telegram/app.py
present malyarka_telegram/router.py
present malyarka_telegram/handlers.py
present malyarka_core/services
present malyarka_core/services/orders.py
present malyarka_telegram/config.py
not_present .env
not_present orders.db
not_present db
not_present database
not_present logs
not_present log
```

## What Was Not Checked

Not checked or opened:

- `.env` contents;
- `config.py` contents;
- token values;
- `os.environ`;
- database contents;
- live logs contents;
- real order contents;
- private IDs;
- API keys;
- webhook URLs;
- private credentials;
- file contents of Python modules;
- file contents of markdown/txt/config-like files.

## Presence-Only Structure

Presence-only project layers observed:

- `malyarka_telegram`: present;
- `malyarka_core`: present;
- `malyarka_core/services`: present;
- `malyarka_core/services/orders.py`: present;
- `malyarka_core/exports`: present by Python filenames;
- `malyarka_core/storage`: present by Python filenames;
- `malyarka_core/security`: present by Python filenames;
- `malyarka_ai`: present;
- `malyarka_vision`: present;
- `.venv`: present;
- `requirements.txt`: present;
- `MALYARKA_CURRENT_STATE.md`: present.

Sensitive zones:

- `.env`: not present at project root by presence-only check;
- `orders.db`: not present at project root by presence-only check;
- `db`: not present at project root by presence-only check;
- `database`: not present at project root by presence-only check;
- `logs`: not present at project root by presence-only check;
- `log`: not present at project root by presence-only check;
- `malyarka_telegram/config.py`: present by filename only, content not read.

## Bot Layer Map By Filenames Only

Presence-only map:

```text
Telegram layer
-> malyarka_telegram/app.py
-> malyarka_telegram/router.py
-> malyarka_telegram/handlers.py
-> malyarka_telegram/keyboards.py
-> malyarka_telegram/messages.py
-> malyarka_telegram/access.py
-> malyarka_telegram/session.py
-> malyarka_telegram/intent.py
-> malyarka_telegram/modes.py

Core layer
-> malyarka_core/services/orders.py
-> malyarka_core/services/archive.py
-> malyarka_core/parsing.py
-> malyarka_core/validation.py
-> malyarka_core/calculations.py
-> malyarka_core/exports/corel.py
-> malyarka_core/exports/malyarka.py
-> malyarka_core/exports/malyarka_file.py
-> malyarka_core/storage/repository.py
-> malyarka_core/storage/schema.py

Auxiliary layers
-> malyarka_ai/*
-> malyarka_vision/*
```

This is a filename-only map. No module contents were read.

## Potential Adapter Boundary Points

Potential adapter insertion points by filename/structure only:

- `malyarka_telegram/router.py`;
- `malyarka_telegram/handlers.py`;
- `malyarka_telegram/app.py`;
- `malyarka_core/adapters/telegram.py`;
- `malyarka_core/services/orders.py`;
- `malyarka_core/exports/*`.

These are structural candidates only.
No implementation decision is made in this report.
No code was read or changed.

## Forbidden Zones Not Inspected

Forbidden zones were not opened:

- token values;
- `.env` values;
- `config.py` secret values;
- `os.environ` values;
- database contents;
- live logs contents;
- real orders;
- chat IDs;
- user IDs;
- owner IDs;
- private credentials;
- API keys;
- webhook URLs;
- production secrets.

## Redaction Confirmation

Mandatory redaction statement:

```text
Secret values were not read, copied, displayed, summarized, logged, or stored.
Sensitive zones are recorded only as presence/category, not content.
```

## Runtime / Live Safety Confirmation

Confirmed:

- Python code was not launched;
- live bot modules were not imported;
- app/router/handlers were not launched;
- polling was not launched;
- webhook was not launched;
- collector was not launched;
- Telegram/API calls were not made by this inventory;
- server files were not changed;
- server files were not created;
- databases/logs were not written;
- commit/push was not performed.

## Risks And Unknowns

Risks/unknowns:

- `malyarka_telegram/config.py` exists, but content was not read by design;
- `.venv` exists, but contents were not inspected;
- `malyarka_ai` and `malyarka_vision` layers exist, but were not analyzed;
- no runtime process/autostart check was performed in this package;
- no file contents were read, so imports, handlers, routes and permissions are not confirmed beyond filenames;
- future adapter design must avoid direct chaotic changes to `app.py`, `router.py`, and `handlers.py`.

## Questions Before Implementation

Before any implementation:

- Which boundary file should host the future server adapter integration point?
- Should `malyarka_core/adapters/telegram.py` be treated as the preferred safe adapter bridge?
- Which feature flags should gate any server-side dry-run adapter?
- How will rollback be handled without touching live polling?
- Is a separate safe file-content read plan needed for selected non-secret files?

## No-Touch Confirmation

For `231C-234C`:

- `.env` was not read;
- `config.py` content was not read;
- token values were not read;
- `os.environ` was not read;
- databases were not read;
- logs were not read;
- real orders were not read;
- private IDs were not read;
- API keys were not read;
- webhook URLs were not read;
- Python code was not launched;
- polling/webhook were not launched;
- server files were not changed or created.

## Next Safe Step

```text
235-238 — анализ read-only inventory report и план минимального server adapter insertion design,
без реализации кода и без изменения live-бота.
```
