# Read-only server inventory report

Technical name: `BATCH_SERIES_231_234_HERMES_ADAPTER_READ_ONLY_SERVER_INVENTORY_RUN`

## Inventory Scope

Target server:

```text
178.104.95.187
```

Target path:

```text
/opt/malyarka-telegram-bot
```

Approved mode:

```text
read-only / presence-only / redact-by-default
```

Inventory result:

```text
blocked before server presence-only collection
```

Reason:

```text
SSH authentication failed for the attempted non-interactive read-only connection.
No server file or folder names were collected in this run.
```

## Approval Reference

User explicitly allowed:

```text
Разрешаю выполнить read-only server inventory по утверждённой процедуре 215–218 и шаблону 219–222.
Без чтения secret values, без запуска кода, без polling/webhook, без изменений файлов.
```

The approval matched the approval gate from `223-226`.

## Local Documents Read

Only local Hermes Hub markdown documents were read before the server attempt:

- `E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md`
- `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_PROCEDURE_PLAN_215_218.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_INVENTORY_REPORT_TEMPLATE_PLAN_219_222.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN_223_226.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_SERVER_INVENTORY_READINESS_FINAL_CHECK_227_230.md`

## What Was Checked

Attempted:

- non-interactive SSH access for presence-only inventory;
- target server: `178.104.95.187`;
- target user attempted: `root`;
- target path intended: `/opt/malyarka-telegram-bot`.

Observed result:

```text
Permission denied (publickey,password).
```

No server directory listing was returned.
No server file names were returned.
No server folder names were returned.

## What Was Not Checked

Because authentication failed before inventory collection, these were not checked on the server:

- whether `/opt/malyarka-telegram-bot` exists;
- top-level folder names;
- Python filenames;
- markdown/txt/config-like filenames;
- app/router/handlers layer presence;
- core/services/orders layer presence;
- config/token/env/db/log zones as presence-only facts;
- potential adapter boundary points by server structure.

## Presence-Only Structure

No new server presence-only structure was collected during this run.

Previously known structure from earlier user-provided/manual inventory remains background context only and was not re-verified in this package.

Current run result:

```text
server structure: not collected due SSH authentication failure
```

## Bot Layer Map By Filenames Only

No current server-side filename map was collected.

Expected future map shape remains:

```text
Telegram
-> app.py presence
-> router.py presence
-> handlers.py presence
-> core/services/orders layer presence
-> possible adapter boundary points by filename
```

But this run did not verify it on the server.

## Potential Adapter Boundary Points

No new server-derived adapter boundary points were confirmed in this run.

Planned boundary from previous local documents remains:

```text
Telegram -> app.py -> router.py / handlers.py -> server adapter boundary -> Hermes adapter logic -> safe core/services/orders interaction
```

This is based on prior planning documents, not on new server inventory data from this run.

## Forbidden Zones Not Inspected

The following zones were not opened or inspected:

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
- production secrets;
- private keys;
- shell history;
- full customer messages.

No secret-like file was opened.
No database was opened.
No log was opened.
No real order was opened.

## Secrets Redaction Confirmation

Mandatory redaction statement:

```text
Secret values were not read, copied, displayed, summarized, logged, or stored.
Sensitive zones are recorded only as presence/category, not content.
```

In this run, even presence/category server data was not collected because authentication failed before listing.

## Runtime / Live Safety Confirmation

Confirmed for this run:

- live bot was not stopped;
- live bot was not restarted;
- polling was not started;
- webhook was not started;
- Telegram was not contacted by this task;
- Python code was not run on the server;
- live bot modules were not imported;
- app/router/handlers were not started;
- collector was not run;
- subprocess from bot code was not run;
- network/API calls from bot code were not made;
- server files were not changed;
- server files were not created;
- databases/logs were not written.

## Risks And Unknowns

Risks/unknowns after this run:

- non-interactive SSH credentials/key are not available in the current Codex environment;
- `/opt/malyarka-telegram-bot` was not re-verified by this package;
- current server structure remains uncollected for this package;
- potential adapter boundary points remain based on prior local planning and earlier documented/manual inventory, not on a fresh server listing.

## Questions Before Implementation

Before any future inventory retry:

- What exact SSH user/key or access method should be used for read-only presence-only inventory?
- Should the user perform the server listing manually and paste only safe presence-only output?
- Should a new approval package specify the safe connection method explicitly?
- Should inventory remain blocked until non-interactive read-only access is available?

## No-Touch Confirmation

For series `231-234`:

- secret values were not read;
- `.env` was not read;
- `config.py` content was not read;
- `os.environ` was not read;
- database contents were not read;
- live logs contents were not read;
- real orders were not read;
- private IDs were not read;
- API keys were not read;
- webhook URLs were not read;
- code was not launched;
- polling/webhook were not launched;
- server files were not modified;
- server files were not created;
- commit/push was not performed.

## Next Safe Step

Because the inventory did not complete, the immediate safe step is:

```text
Уточнить безопасный read-only способ доступа или предоставить пользователю ручной presence-only список.
```

The originally planned next analysis step `235-238` should wait until a real safe inventory report contains server presence-only data.
