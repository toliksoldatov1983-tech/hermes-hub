# Safe server inventory approval gate plan

Technical name: `BATCH_SERIES_223_226_HERMES_ADAPTER_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN`

## Status

This is only an approval gate plan.

Future server inventory is not executed in this package.
The server is not connected.
Server files are not read.
Token, `.env`, `config.py`, and `os.environ` are not read.
Live Telegram, polling, and webhook are not touched.
Staging/production bot code is not read or changed.
Databases, live logs, and real orders are not read.

No code is written.
No tests are created.
No shell scripts, SSH commands, collectors, or migration scripts are created.

Any future read-only inventory run requires a separate explicit user command.
That permission must be limited, one-time, and scoped precisely.

## Purpose

The approval gate prevents accidental server access, secret reading, live bot execution, or production/staging code changes.

It defines what must be present in a future user instruction before Codex may even begin a read-only server inventory procedure.

Without this gate, a vague command like `continue` must not be treated as permission to connect to the server.

## Explicit Approval Phrase

The future approval must clearly name:

- `read-only server inventory`;
- approved procedure `215-218`;
- approved report template `219-222`;
- no secret values;
- no code execution;
- no polling/webhook;
- no file changes.

Example of an explicit approval phrase:

```text
Разрешаю выполнить read-only server inventory по утверждённой процедуре 215–218 и шаблону 219–222.
Без чтения secret values, без запуска кода, без polling/webhook, без изменений файлов.
```

Equivalent future approval is acceptable only if it includes the same boundaries:

- server inventory is explicitly named;
- mode is explicitly read-only;
- secret values are explicitly forbidden;
- code execution is explicitly forbidden;
- polling/webhook are explicitly forbidden;
- file modifications are explicitly forbidden;
- scope is tied to the approved planning documents or restates their boundaries.

## Not Approval

These phrases are not approval:

```text
продолжай
+
делай дальше
посмотри сервер
проверь бота
иди дальше
можно
ок
запускай
проверь Telegram
разберись с сервером
```

Any message without a precise reference to read-only inventory and its boundaries is not approval.

Any message that is ambiguous about secrets, execution, polling/webhook, or file changes is not approval.

Any message that asks to read `.env`, token values, databases, live logs, real orders, or `config.py` secrets is not approval for the safe inventory procedure.

## Zones Allowed Only After Approval

After a valid future approval, only these may be inspected, and only as allowed by procedure `215-218` and template `219-222`:

- top-level project folder names;
- Python module filenames;
- presence of Telegram entry layers by filename only;
- presence of router/handler layers by filename only;
- presence of core/service/order layers by filename only;
- presence of config/token/env zones as facts only;
- presence of database/log zones as facts only;
- possible adapter insertion points by names and structure only.

These facts must remain presence-only.

## Zones Forbidden Even After Approval

The following remain forbidden even after a future read-only inventory approval:

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
- full customer messages;
- any write operations.

If a file, value, or zone may contain secrets or private data, it must be treated as forbidden.

## Presence-Only Data

The future inventory may record only presence/absence facts for sensitive areas.

Allowed examples:

```text
config zone: present by filename only, content not read.
.env zone: presence-only, values not read.
database zone: present by name only, contents not read.
logs zone: present by name only, contents not read.
adapter insertion candidate: router/handlers layer by filename only.
```

Not allowed:

```text
token = ...
OWNER_ID = ...
DATABASE_URL = ...
webhook URL = ...
chat_id = ...
```

## Always Redacted

These are always redacted and never written into reports, console output, bundles, state files, or chat:

- tokens;
- API keys;
- passwords;
- private keys;
- `.env` values;
- secret values from `config.py`;
- environment variable values;
- private IDs;
- database rows;
- log entries;
- real order contents;
- webhook URLs;
- production credentials.

Unsafe findings may be recorded only as:

```text
unsafe value detected: redacted, value not read or not recorded.
```

## Actions That Remain Forbidden

Even with a future read-only inventory approval, these actions remain forbidden:

- execution;
- imports of live bot modules;
- polling;
- webhook;
- subprocess;
- network/API calls beyond the approved inventory channel, if any;
- file modifications;
- database reads;
- live log reads;
- real order reads;
- commit/push;
- deployment;
- dependency installation;
- service changes;
- systemd/cron changes.

## Stop Conditions

Codex must stop the task and report a blocker if any of these occur:

- a secret value must be read to continue;
- code must be executed to continue;
- a live bot module must be imported to continue;
- database contents must be opened;
- live log contents must be opened;
- real order contents must be opened;
- Telegram/API/network connection is required outside explicit scope;
- a file must be changed;
- commit/push is requested;
- permission scope is unclear;
- a requested action exceeds the approved one-time scope;
- there is a risk of exposing private data;
- the user message is vague and does not explicitly approve read-only inventory;
- the task would touch polling/webhook/live runtime.

When a stop condition is hit, the next response must explain:

- which boundary was reached;
- what was not done;
- what explicit approval or safer plan would be needed.

## Approval Lifetime

Future approval is one-time only.

It applies only to the specific inventory package named by the user.
It does not carry over to later packages.
It does not authorize implementation.
It does not authorize live Telegram changes.
It does not authorize reading secrets.
It does not authorize file modifications.

## Current No-Touch Confirmation

For series 223-226:

- server was not touched;
- live Telegram was not touched;
- polling/webhook were not touched;
- token was not touched;
- `.env` was not touched;
- `config.py` was not touched;
- `os.environ` was not read;
- databases and live logs were not touched;
- real orders were not touched;
- staging/production bot code was not read or changed;
- Vision/API were not touched;
- code and tests were not created.

## Next Safe Step

```text
227-230 — финальная сверка документов server inventory readiness:
только проверка готовности планов 215-226 перед возможным отдельным разрешением на read-only inventory,
без подключения к серверу и без чтения server files.
```
