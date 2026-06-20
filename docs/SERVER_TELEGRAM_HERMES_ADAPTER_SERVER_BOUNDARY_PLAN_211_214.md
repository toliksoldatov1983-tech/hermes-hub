# Server adapter boundary plan

Technical name: `BATCH_SERIES_211_214_HERMES_ADAPTER_SERVER_BOUNDARY_PLAN`

## Status

This is only a server adapter boundary plan.

Server adapter is not implemented in this package.
Live Telegram bot is not connected.
Server files are not read.
Token, `.env`, and `config.py` are not read.
Production/staging bot code is not imported and not changed.

Any future transition to server adapter implementation requires separate explicit user permission.

## Purpose

Define a safe boundary through which a future Hermes server adapter may eventually interact with the existing server Telegram bot.

The future integration must go through a dedicated adapter boundary, not through direct chaotic changes to live `app.py`, `router.py`, `handlers.py`, polling, token handling, or production runtime.

The local fake adapter remains the safety baseline for future contract checks:

```text
local fake adapter -> contract tests -> dry-run validation -> boundary plan -> future server adapter
```

The future server adapter must be treated as a controlled layer between existing Telegram flow and Hermes logic.

## Future Boundary Position

Planned logical placement:

```text
Telegram
-> app.py
-> router.py / handlers.py
-> server adapter boundary
-> Hermes adapter logic
-> safe core/services/orders interaction
```

The boundary must protect the existing live bot. If the future adapter is disabled, unavailable, or unsafe, the existing Telegram flow must continue through fallback.

## Future Server Adapter Input

Future server adapter input may include only safe, pre-filtered data:

- `text`: user text after existing Telegram flow receives it;
- `user_id_safe`: redacted or non-secret user identity marker;
- `current_mode`: order/chat/engineer/admin/neutral;
- `route_result`: safe routing decision from current bot flow;
- `order_preview`: safe summary, not raw private files;
- `owner_access_status`: allowed/blocked/unknown, without exposing owner id;
- `feature_flags`: explicit safe flags;
- `safe_context_summary`: short project state without secrets;
- `dry_run`: must be true on first stages;
- `diagnostics_requested`: boolean.

Input must not contain:

- token;
- `.env`;
- `config.py`;
- `os.environ`;
- server file paths;
- database paths;
- live log paths;
- real order files;
- private customer data;
- raw server dumps.

## Future Server Adapter Output

Future server adapter output must be plain structured data:

- `ok`;
- `status`;
- `action`;
- `dry_run`;
- `blocked`;
- `fallback_required`;
- `reason`;
- `diagnostics_safe`;
- `side_effects`;
- `output_type`;
- optional `response_text`;
- optional `warnings`;
- optional `suggested_next_step`;
- optional `engineer_task_draft`.

Output must remain safe for validation before any live bot uses it.

## Dry-Run Only First Stages

The first future server adapter stages must be dry-run only.

Allowed dry-run actions:

- explain status;
- answer with safe text draft;
- suggest next safe step;
- prepare engineer task draft;
- summarize safe project state;
- explain order result;
- request fallback.

Dry-run output must not send messages itself. It may only return a proposed response for the existing bot layer to validate.

## Blocked By Default

The following must be blocked by default:

- sending Telegram messages directly;
- creating files;
- editing files;
- deleting files;
- changing prices;
- changing rules;
- changing databases;
- creating exports;
- sending files;
- running polling;
- restarting bot;
- reading token;
- reading `.env`;
- reading `config.py`;
- reading `os.environ`;
- calling APIs;
- processing real order files;
- touching live logs;
- touching production/staging bot code.

Unknown actions must also be blocked.

## Required Feature Flags

Future boundary must require explicit flags:

- `HERMES_ADAPTER_ENABLED`;
- `HERMES_ASSISTANT_MODE_ENABLED`;
- `HERMES_ENGINEER_MODE_ENABLED`;
- `HERMES_ADMIN_CHANGES_ENABLED`;
- `HERMES_EXPORT_CALLBACKS_ENABLED`;
- `HERMES_SAFE_MODE`.

Safe defaults:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_ASSISTANT_MODE_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false
HERMES_ADMIN_CHANGES_ENABLED=false
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_SAFE_MODE=true
```

No new behavior should run unless the required flag is explicitly enabled by a future approved package.

## Diagnostics

Diagnostics are allowed only in safe-only format.

Allowed diagnostics:

- adapter enabled/disabled;
- safe mode enabled;
- feature flags true/false;
- fallback active/inactive;
- current safe mode name;
- adapter status: ok/off/blocked/fallback;
- reason codes without secrets.

Forbidden diagnostics:

- token value;
- `.env` content;
- `config.py` content;
- environment variable values;
- owner id values;
- database paths;
- live log paths;
- server paths;
- stack traces with server paths;
- real order content;
- customer private data;
- polling/restart commands;
- API keys.

If diagnostics are uncertain, the boundary must block or redact them.

## Side Effects

Side effects are forbidden at the boundary.

Required invariant:

```text
side_effects=[]
```

The future adapter must not:

- write files;
- write logs;
- write databases;
- start subprocesses;
- make network/API calls;
- send Telegram messages;
- create exports;
- read server files;
- modify live bot state.

## Rollback And No-Touch Rules

Rollback must be simple:

1. set `HERMES_ADAPTER_ENABLED=false`;
2. keep `HERMES_SAFE_MODE=true`;
3. keep existing router/handlers/core flow;
4. do not change polling;
5. do not change token or `.env`;
6. do not change database;
7. do not change production/staging bot code.

If adapter output is unsafe, missing, malformed, unknown, or blocked, the existing Telegram bot must continue through fallback.

## Forbidden Direct Links

The future design forbids:

- direct import of live bot modules;
- direct import of `malyarka_telegram`;
- direct import of `malyarka_core` from production server code without a separate approved integration step;
- direct execution of handlers/router/app;
- direct polling/webhook start;
- direct token reading;
- direct `.env` reading;
- direct `config.py` reading;
- direct `os.environ` reading;
- direct server file reading;
- server/live/staging/production bot code changes;
- database writes;
- live log writes;
- network/API calls without separate approval;
- real order file operations.

## Future Safety Gates

Before any server adapter implementation, these gates must pass:

1. adapter off by default;
2. feature flags required;
3. dry-run required;
4. no side effects required;
5. diagnostics safe-only;
6. rollback-safe response;
7. no token/env/config/server path leaks;
8. no production imports;
9. no live Telegram calls;
10. explicit user approval before implementation.

The local fake adapter baseline is the current reference:

```text
local_tests\hermes_adapter_fake
```

The last local result before this plan:

```text
166 passed
```

## What This Plan Does Not Allow

This document does not allow:

- server connection;
- server file reading;
- token usage;
- `.env` usage;
- `config.py` usage;
- live Telegram launch;
- polling/webhook;
- code changes;
- pytest/test creation;
- staging/production bot code changes;
- real order work;
- database changes;
- Vision/API work.

## Next Safe Step

Series 215-218 — plan read-only server inventory procedure: only design future safe inventory of the server bot, without connecting to the server and without reading server files now.
