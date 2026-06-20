# Server adapter insertion design plan

Technical name: `BATCH_235_238_SERVER_ADAPTER_INSERTION_DESIGN_PLAN`

Date: 2026-06-16

## Status

This is a markdown-only design plan.

No Python code is written.
No tests are created.
No server connection is made in this package.
No live bot modules are imported.
No polling/webhook is launched.
No collector is launched.
No server files are read, changed, or created.

Secrets are not touched:

- token: not read;
- `.env`: not read;
- `config.py` contents: not read;
- `os.environ`: not read;
- databases: not read;
- logs: not read;
- real orders: not read;
- private IDs: not read;
- API keys: not read;
- webhook URLs: not read.

## Sources Read

Local markdown sources:

- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C_SUMMARY.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_SERVER_BOUNDARY_PLAN_211_214.md`
- `E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md`
- `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`

Only presence-only inventory data was used.
No server code contents were read.

## Presence-Only Server Layers Found

Top-level layers:

```text
.venv
MALYARKA_CURRENT_STATE.md
malyarka_ai
malyarka_core
malyarka_telegram
malyarka_vision
requirements.txt
```

Telegram layer filenames:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_telegram/modes.py
malyarka_telegram/engineer_tasks.py
malyarka_telegram/obsidian_inbox.py
malyarka_telegram/voice.py
malyarka_telegram/config.py
```

Core layer filenames:

```text
malyarka_core/adapters/telegram.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
malyarka_core/exports/corel.py
malyarka_core/exports/malyarka.py
malyarka_core/exports/malyarka_file.py
malyarka_core/storage/repository.py
malyarka_core/storage/schema.py
malyarka_core/security/permissions.py
```

Auxiliary layers:

```text
malyarka_ai/*
malyarka_vision/*
```

Sensitive/root zones by presence-only check:

```text
present malyarka_telegram/config.py
not_present .env
not_present orders.db
not_present db
not_present database
not_present logs
not_present log
```

`malyarka_telegram/config.py` is only known by filename.
Its contents were not read and must remain off-limits unless a later package explicitly permits a safe, redacted, non-secret review.

## Candidate Adapter Boundary Points

Inventory and previous boundary planning identify these candidates:

1. `malyarka_telegram/app.py`
2. `malyarka_telegram/router.py`
3. `malyarka_telegram/handlers.py`
4. `malyarka_core/adapters/telegram.py`
5. `malyarka_core/services/orders.py`

Additional structural neighbors:

- `malyarka_telegram/access.py`
- `malyarka_telegram/intent.py`
- `malyarka_telegram/session.py`
- `malyarka_telegram/modes.py`
- `malyarka_core/security/permissions.py`
- `malyarka_core/exports/*`

## Candidate Assessment

### `malyarka_telegram/app.py`

Role by filename:

- likely entry point for live Telegram polling/application setup.

Risk:

- highest risk because it may be close to polling, token/config setup, startup lifecycle, and live runtime.

Design decision:

- not the first insertion point.
- do not directly edit `app.py` in the first implementation.

### `malyarka_telegram/router.py`

Role by filename:

- likely routes messages/callbacks to handlers.

Risk:

- close to live message flow.
- direct changes may affect all Telegram behavior.

Design decision:

- possible later call-site for adapter integration, but not the first code location to implement new logic.
- should only receive a tiny guarded call after local adapter skeleton and tests exist.

### `malyarka_telegram/handlers.py`

Role by filename:

- likely contains user-facing message/callback handling.

Risk:

- direct behavior changes could affect live UX.
- may contain mode-specific logic or access checks.

Design decision:

- possible later call-site, but not the first place to create adapter logic.
- any future handler touch must be tiny, flag-gated, dry-run, and fallback-safe.

### `malyarka_core/adapters/telegram.py`

Role by filename:

- already appears to be an adapter layer between Telegram and core.

Risk:

- lower than `app.py/router.py/handlers.py` because it is structurally an adapter boundary.
- still unknown because contents were not read.

Design decision:

- best minimal insertion design target by filename/structure only.
- future server adapter should be designed as a separate module/layer adjacent to or behind this adapter, not as chaotic logic in live handlers.

### `malyarka_core/services/orders.py`

Role by filename:

- likely order service logic.

Risk:

- touching it could affect core order behavior.

Design decision:

- not an adapter insertion point.
- should be called only through existing safe interfaces after adapter validation.
- do not change order service in first server adapter stage.

## Minimal Safe Insertion Point

Chosen minimal design point:

```text
malyarka_core/adapters/telegram.py
```

Design position:

```text
Telegram live flow
-> malyarka_telegram/router.py or handlers.py
-> tiny future guarded call-site
-> malyarka_core/adapters/telegram.py or adjacent Hermes server adapter bridge
-> Hermes adapter contract validation
-> dry-run response only
-> fallback to existing Telegram behavior if disabled/unsafe
```

Why this is minimal:

- it matches an existing adapter-shaped filename;
- it avoids putting Hermes logic directly into `app.py`;
- it keeps router/handlers as future thin call-sites only;
- it keeps `services/orders.py` protected from first-stage changes;
- it supports rollback by disabling feature flags;
- it can remain off by default and dry-run only.

Recommended future module shape, only as design:

```text
malyarka_core/adapters/telegram.py
or
malyarka_core/adapters/hermes_adapter.py
```

No file is created in this package.

## Why Direct Import / Launch Of Live Modules Is Forbidden

Directly importing or launching live modules is forbidden because:

- `app.py` may initialize Telegram, token/config, polling, or runtime state;
- `router.py` and `handlers.py` may register live handlers or trigger side effects;
- importing modules can execute top-level code;
- live bot state may change unexpectedly;
- token/config paths may be touched indirectly;
- polling/webhook could be affected;
- rollback would be harder.

Future design must treat live modules as production runtime, not as a sandbox.

## Required Feature Flags

Minimum flags:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SAFE_MODE=true
HERMES_DRY_RUN_ONLY=true
HERMES_SERVER_ADAPTER_ENABLED=false
HERMES_TELEGRAM_INSERTION_ENABLED=false
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_ADMIN_CHANGES_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false
HERMES_ASSISTANT_MODE_ENABLED=false
```

From the earlier boundary plan:

```text
HERMES_ADAPTER_ENABLED
HERMES_ASSISTANT_MODE_ENABLED
HERMES_ENGINEER_MODE_ENABLED
HERMES_ADMIN_CHANGES_ENABLED
HERMES_EXPORT_CALLBACKS_ENABLED
HERMES_SAFE_MODE
```

First implementation defaults:

- all new behavior off;
- safe mode on;
- dry-run only;
- no file writes;
- no Telegram sends from adapter itself;
- no exports;
- no admin changes;
- no database changes.

## First Future Implementation Should Be Off By Default

The first implementation must be off by default because:

- live polling is already running;
- handler/router behavior is production-sensitive;
- adapter contents are not yet reviewed;
- token/config contents are intentionally unread;
- fallback must preserve current bot behavior;
- errors in adapter logic must not reach users.

Required first-stage invariant:

```text
if feature flag is off:
    existing Telegram bot flow continues exactly as before
```

## First Future Implementation Should Be Dry-Run Only

The first implementation must be dry-run only because:

- it should validate contract compatibility before behavior changes;
- it must return proposed responses/actions, not execute them;
- Telegram message sending should stay in existing controlled bot flow;
- no files, exports, databases, logs, or real orders should be changed;
- safety can be verified before any live integration.

Allowed first-stage dry-run outputs:

- safe response draft;
- diagnostics status without secrets;
- fallback_required flag;
- blocked reason;
- suggested next safe step.

Forbidden first-stage actions:

- send Telegram message directly;
- edit files;
- create files;
- write logs/databases;
- read token/env/config contents;
- run polling/webhook;
- call APIs;
- process real order files;
- change prices/rules/materials.

## Minimal Future Insertion Sequence

Recommended sequence for later packages:

1. Create local server adapter skeleton outside live server code.
2. Validate skeleton against fake adapter contract.
3. Add local tests for dry-run/off-by-default behavior.
4. Design a read-only file-content review plan for selected non-secret files if needed.
5. Only after separate permission, inspect selected server file contents safely and redacted.
6. Prepare a tiny feature-flagged call-site plan for `router.py` or `handlers.py`.
7. Keep `app.py` untouched in the first live-adjacent stage.
8. Keep `services/orders.py` untouched in the first live-adjacent stage.
9. Implement only after separate explicit user permission.

## Risks

Risks:

- `malyarka_telegram/config.py` exists and may contain secrets; contents must not be read without a specific redaction plan.
- `malyarka_telegram/app.py` may manage polling/runtime; touching it is high risk.
- `router.py` and `handlers.py` may affect all live Telegram behavior.
- `malyarka_ai` and `malyarka_vision` exist; they are outside the current path and must not be pulled in accidentally.
- `malyarka_core/exports/*` exists; export callbacks must stay off until separately planned.
- No file contents were read, so exact function names/imports are unknown.
- `.venv` exists; runtime dependencies were not inspected.

## No-Touch Confirmation

For `235-238`:

- server files were not read;
- server files were not changed;
- live Telegram was not touched;
- polling/webhook were not launched;
- token was not read;
- `.env` was not read;
- `config.py` contents were not read;
- `os.environ` was not read;
- databases/logs/real orders were not read;
- staging/production bot code was not changed;
- Vision/API were not touched;
- collector was not launched;
- commit/push was not performed;
- no Python code or tests were created.

## Next Safe Step

```text
239-242 — план локального server adapter skeleton без подключения к live-боту.
```
