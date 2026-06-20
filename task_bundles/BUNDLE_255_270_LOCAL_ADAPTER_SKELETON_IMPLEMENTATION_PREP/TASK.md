# TASK — Bundle 255-270 Local Adapter Skeleton Implementation Prep

Technical name: `BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP`

Status: planning bundle only.

Implementation is not allowed until separate explicit user permission.

## Goal

Prepare a connected plan for the first local Hermes server adapter skeleton implementation block `255-270`.

The future implementation must remain local-only and must not touch the existing live Telegram bot.

## Source Documents

This bundle is based on:

- `E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md`
- `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN_251_254.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN_247_250.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`

## Required Explicit Permission

Before implementation, user must explicitly approve the first local adapter skeleton implementation.

Acceptable permission must say:

```text
Разрешаю реализовать первый локальный adapter skeleton только в локальной зоне Hermes Hub,
без подключения к серверу, без live Telegram, без secrets, без production/staging code,
off by default, dry-run only, side_effects=[].
```

Vague commands are not enough:

```text
продолжай
делай
можно
+
пиши код
сделай adapter
```

## What Will Be Implemented Later

Future local implementation should create a local test-double/skeleton that models the future server adapter contract.

It should:

1. Accept a request dictionary.
2. Validate request fields.
3. Apply safe default feature flags.
4. Keep adapter off by default.
5. Require dry-run mode.
6. Require safe mode.
7. Return structured responses.
8. Preserve `side_effects=[]`.
9. Never send Telegram messages directly.
10. Return fallback when disabled, blocked, malformed, unsafe, or errored.
11. Support safe diagnostics only.
12. Block export/admin/write/unknown/unsafe actions.

Future target concept:

```text
malyarka_core/adapters/telegram.py
```

First local implementation zone:

```text
E:\Hermes-Hub\local_tests\server_adapter_skeleton\
```

This local zone is not server code and must not be copied to `/opt/malyarka-telegram-bot`.

## Files Allowed In Future Implementation

Allowed only after separate permission:

```text
E:\Hermes-Hub\local_tests\server_adapter_skeleton\server_adapter_skeleton.py
E:\Hermes-Hub\local_tests\server_adapter_skeleton\README.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_255_270_REPORT.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_255_270_SUMMARY.md
```

If tests are included in the future package, they must be separately and explicitly approved by filename.

## Files And Zones Forbidden

Do not touch:

```text
/opt/malyarka-telegram-bot
server files
live Telegram
polling/webhook
token
.env
config.py contents
os.environ
databases
logs
real orders
staging/production code
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_core/services/orders.py
Vision/API
.git
commit/push
```

Do not read:

- private keys;
- passwords;
- passphrases;
- token values;
- `.env` contents;
- `config.py` contents;
- environment variables;
- database/log/order contents;
- private IDs;
- API keys;
- webhook URLs.

## Contract Interface

Request fields:

```text
action
payload
dry_run
feature_flags
safe_mode
diagnostics
```

Response fields:

```text
ok
status
action
dry_run
blocked
fallback_required
reason
output_type
side_effects
diagnostics_safe
```

## Feature Flags

Safe defaults:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SERVER_ADAPTER_ENABLED=false
HERMES_TELEGRAM_INSERTION_ENABLED=false
HERMES_SAFE_MODE=true
HERMES_DRY_RUN_ONLY=true
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_ADMIN_CHANGES_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false
HERMES_ASSISTANT_MODE_ENABLED=false
```

Rules:

- missing flags default safe;
- unknown flags do not enable behavior;
- adapter disabled means fallback required;
- safe mode must be true;
- dry-run must be true;
- export/admin/write remain blocked.

## Contract Examples To Cover

Future skeleton must satisfy examples from `247-250`:

1. adapter off by default;
2. safe dry-run allowed;
3. export blocked;
4. admin blocked;
5. write blocked;
6. unknown action blocked;
7. malformed request;
8. `fallback_required=true`;
9. diagnostics safe-only;
10. unsafe diagnostics blocked.

Each scenario must preserve:

```text
side_effects=[]
no direct Telegram send
fallback to current flow when blocked/unsafe
no token/env/config/db/log/order/private data
```

## Block 255-270 Proposed Stages

### 255-258 — First Local Skeleton Implementation Plan

Plan exact local implementation files, contract shape, allowed scope, rollback, and verification.

No code unless user gives explicit permission.

### 259-262 — Local Skeleton Implementation

Only after permission:

- create local skeleton file;
- implement request/response validation;
- implement safe defaults;
- implement blocked/fallback/error shapes;
- no tests unless separately approved in this stage.

### 263-266 — Local Contract Checks Plan Or Tests

Depending on user permission:

- plan or create local checks for examples `247-250`;
- verify off-by-default, dry-run, fallback, no-side-effects.

No server/live interaction.

### 267-270 — Local Acceptance And Next Boundary Plan

Document acceptance of local skeleton.
Plan next boundary: how to later inspect selected non-secret server file contents or create a server-compatible adapter package.

No live integration.

## Rollback Plan

Rollback for local skeleton:

1. Set all enabling flags to false:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SERVER_ADAPTER_ENABLED=false
HERMES_TELEGRAM_INSERTION_ENABLED=false
```

2. Keep:

```text
HERMES_SAFE_MODE=true
HERMES_DRY_RUN_ONLY=true
```

3. Stop using local skeleton output.
4. Remove or ignore only local skeleton files if user explicitly requests.
5. Do not touch server files.
6. Do not touch live bot.
7. Do not touch production/staging code.

Rollback must never require live bot changes.

## Acceptance Checks

Before accepting future implementation:

- adapter off by default;
- dry-run required;
- safe mode required;
- feature flags required;
- `side_effects=[]`;
- no direct Telegram send;
- no file/db/log writes;
- no token/env/config reads;
- fallback response works;
- blocked response works;
- malformed response works;
- diagnostics safe-only;
- contract examples represented;
- no server/live/staging/production changes.

## Stop Conditions

Stop if any future step requires:

- server connection;
- reading server files;
- reading token/`.env`/`config.py` contents/`os.environ`;
- reading db/log/order contents;
- importing live bot modules;
- launching polling/webhook;
- direct Telegram send;
- network/API calls;
- editing production/staging code;
- touching `.git`;
- unclear permission.

## Next Step After This Bundle

Wait for separate explicit user permission for:

```text
BATCH_255_258_FIRST_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PLAN
```

or another exact user-defined package in the 255-270 range.
