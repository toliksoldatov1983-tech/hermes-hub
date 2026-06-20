# Read-only server inventory procedure plan

Technical name: `BATCH_SERIES_215_218_HERMES_ADAPTER_READ_ONLY_SERVER_INVENTORY_PROCEDURE_PLAN`

## Status

This is only a plan for a future read-only server inventory procedure.

Current package does not allow:

- connecting to the server;
- reading server files;
- reading token;
- reading `.env`;
- reading `config.py`;
- reading `os.environ`;
- touching live Telegram;
- touching polling/webhook;
- reading staging/production bot code;
- reading databases;
- reading live logs;
- reading real orders.

No code is written.
No tests are created.
No shell scripts or SSH commands are created.

Any future inventory run requires separate explicit user permission.

## Purpose

Before any future server adapter implementation, Hermes Hub needs a safe procedure for understanding the existing server Telegram bot without breaking it and without exposing secrets.

The future inventory must be:

- read-only;
- presence-only for sensitive zones;
- no execution;
- no imports;
- no polling/webhook;
- no token/env/config content reading;
- no database/log/order content reading;
- no file modifications.

## Future Inventory Scope

The future inventory may inspect only after separate user permission.

Allowed inventory zones in a future approved run:

- top-level project folder names;
- Python module file names;
- presence of Telegram entry layers by filename only;
- presence of router/handler layers by filename only;
- presence of core/service/order layers by filename only;
- presence of config/token/env files as facts only;
- presence of database/log folders as facts only;
- possible adapter insertion points by names and structure only.

The procedure must separate project structure from secrets and runtime data.

## Presence-Only Data

These may be recorded only as presence/absence facts, without content:

- top-level folders;
- Python module filenames;
- `app.py` presence;
- `router.py` presence;
- `handlers.py` presence;
- `services` layer presence;
- `orders` layer presence;
- `config.py` presence;
- `.env` presence;
- token-like file presence;
- database folder/file presence;
- logs folder/file presence;
- runtime/service files presence;
- possible adapter insertion point filenames.

Examples of allowed wording:

```text
config.py: present, content not read.
.env: presence unknown/not checked, content not read.
orders database: present by name only, content not read.
```

## Forbidden Data

The future inventory must not record:

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
- webhook runtime details;
- polling runtime command details beyond previously approved high-level fact;
- private server credentials;
- API keys;
- contents of production secret files;
- raw stack traces with paths or secrets;
- customer data.

If a value may be secret, it must be treated as secret and omitted.

## Future Read-Only Procedure

The future procedure should follow this order only after separate approval:

1. Confirm the approved scope in writing.
2. Confirm forbidden zones before any action.
3. Collect only directory/file names allowed by the scope.
4. Do not open secret-like files.
5. Do not open databases.
6. Do not open live logs.
7. Do not inspect real order folders.
8. Record only presence-only facts for sensitive paths.
9. Identify possible adapter boundary points by filenames and structure.
10. Produce a safe report with no secrets.
11. Stop before any implementation step.

The procedure must not include commands in this planning document. Commands can be designed only in a later package if the user explicitly permits them.

## Zones That May Be Inventoried Later

Only after separate permission:

- project root structure by names;
- Telegram package structure by filenames;
- core package structure by filenames;
- service layer names;
- export-related names;
- access-control file names;
- documented existing process fact if already known or separately approved;
- possible adapter insertion points by file/layer names.

## Zones That Stay Forbidden

Forbidden even during read-only inventory unless a later package gives special explicit permission:

- token values;
- `.env` content;
- `config.py` content if it may contain secrets;
- environment variables;
- database contents;
- live logs contents;
- real orders;
- private keys;
- API keys;
- production secrets;
- full customer chat/message contents;
- server credentials;
- shell history.

## No Secret Disclosure Rules

Use redact-by-default:

- secret-like values are never copied;
- secret-like files are not opened;
- secret-like paths are presence-only;
- unknown sensitivity means treat as sensitive;
- report only safe labels;
- do not include raw command output if it may contain secrets;
- do not paste large server data into ChatGPT.

## No Live Bot Impact Rules

The future inventory must not:

- start live bot;
- stop live bot;
- restart polling;
- start webhook;
- import production modules;
- run app/router/handlers;
- run subprocess from server bot;
- make network/API calls;
- change files;
- change permissions;
- change systemd/cron;
- change database;
- write logs.

## Future Safety Rules

Required rules for any future inventory package:

- read-only only;
- no execution;
- no imports;
- no polling/webhook;
- no subprocess;
- no network/API calls;
- no token/env/config reads;
- no database reads;
- no live log reads;
- no file modifications;
- no commit/push;
- redact-by-default;
- secrets-as-presence-only;
- explicit approval required before inventory run.

## Future Inventory Report Template Requirements

The future report should include:

1. what was checked;
2. what was not checked;
3. which files/folders were visible by name only;
4. which zones were forbidden;
5. possible adapter boundary points found;
6. risks found;
7. what must be clarified before implementation;
8. no-touch confirmation;
9. confirmation that secrets were not read;
10. confirmation that live bot was not started/stopped/restarted.

The report must avoid:

- secret values;
- raw `.env`;
- raw `config.py`;
- database/log contents;
- real order contents;
- runtime credentials;
- private user identifiers.

## Relation To Server Adapter Boundary

The future read-only inventory exists to support the already planned adapter boundary:

```text
Telegram
-> app.py
-> router.py / handlers.py
-> server adapter boundary
-> Hermes adapter logic
-> safe core/services/orders interaction
```

Inventory should clarify where a boundary may sit, but it must not implement or modify the boundary.

## Current No-Touch Confirmation

During this planning package:

- server was not connected;
- server files were not read;
- token was not read;
- `.env` was not read;
- `config.py` was not read;
- `os.environ` was not read;
- live Telegram was not touched;
- polling/webhook was not touched;
- staging/production bot code was not read or changed;
- databases/live logs/real orders were not read;
- code/tests/scripts were not created.

## Next Safe Step

Series 219-222 — plan safe inventory report template: only design the template for a future read-only server inventory report, without connecting to the server and without reading server files.
