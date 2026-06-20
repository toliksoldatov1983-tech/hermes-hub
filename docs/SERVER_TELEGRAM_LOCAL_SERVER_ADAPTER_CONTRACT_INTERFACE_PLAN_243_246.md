# Local server adapter contract interface plan

Technical name: `BATCH_243_246_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN`

Date: 2026-06-16

## Status

This is a markdown-only contract interface plan.

No Python code is written.
No tests are created.
No server connection is made.
No live bot modules are imported.
No polling/webhook is launched.
No server files are read, changed, or created.

## Sources Read

Local markdown sources:

- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`
- `E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md`
- `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`

## Purpose

Define the future local contract interface for the Hermes server adapter layer before any implementation.

Future target by design:

```text
malyarka_core/adapters/telegram.py
```

This contract is intended to be validated locally first.
It must not depend on live Telegram runtime.
It must not import production bot modules.
It must not send Telegram messages directly.

## Contract Principles

The future adapter interface must be:

- local-first;
- off by default;
- dry-run only at first;
- feature-flag gated;
- safe-mode required;
- fallback-safe;
- no-side-effects;
- diagnostics safe-only;
- compatible with future tiny guarded call-sites in `router.py` or `handlers.py`;
- isolated from `app.py` and polling lifecycle;
- isolated from `services/orders.py` changes in the first stage.

## Request Fields

Required request fields:

```text
action
payload
dry_run
feature_flags
safe_mode
diagnostics
```

### `action`

Type:

```text
string
```

Purpose:

- describes the requested adapter behavior.

Allowed first-stage values:

```text
answer_text
explain_status
suggest_next_safe_step
diagnostics
fallback
```

Blocked first-stage values:

```text
send_telegram_message
create_file
edit_file
delete_file
change_database
change_price
change_rules
run_polling
restart_bot
read_token
read_env
read_config
call_api
process_real_order_files
```

Unknown action must be blocked.

### `payload`

Type:

```text
dict
```

Purpose:

- carries safe input data for the adapter.

Allowed content examples:

```text
text
current_mode
route_result
order_preview_safe
owner_access_status
safe_context_summary
```

Forbidden payload content:

```text
token
.env values
config.py values
os.environ values
database contents
log contents
real order contents
private IDs
API keys
webhook URLs
server credentials
```

### `dry_run`

Type:

```text
bool
```

Required first-stage value:

```text
true
```

If `dry_run=false`, response must be blocked and fallback required.

### `feature_flags`

Type:

```text
dict
```

Required safe defaults:

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

Missing flags must default to the safest value.
Unknown flags must not enable behavior.

### `safe_mode`

Type:

```text
bool
```

Required value:

```text
true
```

If `safe_mode=false`, response must be blocked and fallback required.

### `diagnostics`

Type:

```text
bool
```

Purpose:

- requests safe-only diagnostics.

Diagnostics must never include secrets, private IDs, server paths with sensitive meaning, file contents, stack traces with secrets, token/env/config values, database/log/order content, API keys, webhook URLs, or polling commands.

## Response Fields

Required response fields:

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

### `ok`

Type:

```text
bool
```

Meaning:

- `true` only when the request is safe, dry-run, and allowed by flags;
- `false` for blocked, disabled, malformed, unsafe, or fallback responses.

### `status`

Type:

```text
string
```

Allowed values:

```text
dry_run
blocked
fallback
disabled
malformed
error
```

### `action`

Type:

```text
string
```

Must echo the requested action or return:

```text
fallback
blocked
malformed
```

### `dry_run`

Type:

```text
bool
```

Must remain:

```text
true
```

If request dry-run is false, response must not perform action and must indicate blocked/fallback.

### `blocked`

Type:

```text
bool
```

True when:

- adapter is disabled;
- safe mode is false;
- dry-run is false;
- action is unknown;
- action is forbidden;
- payload is unsafe;
- diagnostics are unsafe;
- feature flags do not allow the action;
- request is malformed.

### `fallback_required`

Type:

```text
bool
```

True when current live flow should ignore adapter output and continue existing behavior.

Required for:

- disabled adapter;
- blocked action;
- malformed request;
- unsafe diagnostics;
- any error;
- missing or unsafe feature flags.

### `reason`

Type:

```text
string
```

Must contain safe explanation only.

Forbidden in `reason`:

- token values;
- env/config values;
- private IDs;
- database/log/order content;
- API keys;
- webhook URLs;
- full server paths with sensitive context.

### `output_type`

Type:

```text
string
```

Allowed values:

```text
draft
diagnostics
blocked
fallback
disabled
malformed
error
```

### `side_effects`

Type:

```text
list
```

Required invariant:

```text
side_effects=[]
```

Any non-empty side effects list means the response is unsafe and must be blocked by future validators.

### `diagnostics_safe`

Type:

```text
bool
```

Required value for diagnostics response:

```text
true
```

If diagnostics are not safe, response must be blocked and fallback required.

## Feature Flag Rules

Future adapter must follow these rules:

- adapter behavior is disabled unless `HERMES_ADAPTER_ENABLED=true`;
- server adapter behavior is disabled unless `HERMES_SERVER_ADAPTER_ENABLED=true`;
- Telegram insertion is disabled unless `HERMES_TELEGRAM_INSERTION_ENABLED=true`;
- safe mode must be true;
- dry-run-only must be true for first stage;
- export callbacks remain blocked unless separately enabled;
- admin changes remain blocked unless separately enabled;
- engineer mode remains blocked unless separately enabled;
- assistant mode remains blocked unless separately enabled;
- missing flags default to safest value;
- unknown flags do not enable behavior.

## Dry-Run Mode

Dry-run means:

- no Telegram message is sent directly;
- no file is created or edited;
- no database is read or written;
- no log is written;
- no export is created;
- no real order file is processed;
- no network/API call is made;
- no live module is imported;
- response is only a draft, status, diagnostics-safe object, blocked response, or fallback signal.

## Blocked Response

Example shape:

```text
{
  "ok": false,
  "status": "blocked",
  "action": "blocked",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "action is forbidden in dry-run adapter",
  "output_type": "blocked",
  "side_effects": [],
  "diagnostics_safe": true
}
```

## Fallback Response

Example shape:

```text
{
  "ok": false,
  "status": "fallback",
  "action": "fallback",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "adapter disabled or unsafe; use existing Telegram flow",
  "output_type": "fallback",
  "side_effects": [],
  "diagnostics_safe": true
}
```

## Error Response

Errors must be converted to safe structured responses.

Example shape:

```text
{
  "ok": false,
  "status": "error",
  "action": "fallback",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "adapter error redacted",
  "output_type": "error",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Errors must not leak stack traces, server paths, secrets, or private values.

## Diagnostics Safe-Only

Allowed diagnostics:

- adapter enabled/disabled;
- safe mode true/false;
- dry-run true/false;
- feature flag names and boolean states;
- fallback required true/false;
- status reason codes without secrets.

Forbidden diagnostics:

- token;
- `.env`;
- `config.py` contents;
- `os.environ`;
- database paths or contents;
- log paths or contents;
- real order contents;
- private IDs;
- API keys;
- webhook URLs;
- polling/restart commands;
- production secrets.

## Fallback To Current Flow

The future adapter must never be required for the current bot to work.

If adapter is disabled, malformed, unsafe, or fails:

```text
fallback_required=true
existing Telegram flow continues
```

The adapter response is a suggestion/status object only.

## No Direct Telegram Send

The adapter must not send Telegram messages directly.

It may return only:

- draft text;
- blocked/fallback status;
- safe diagnostics;
- suggested next safe step.

Actual Telegram delivery remains outside the adapter and must be controlled by the existing flow after future validation.

## Explicit No-Touch Confirmation

For package `243-246`:

- no Python code was written;
- no tests were created;
- no server connection was made;
- no server files were read or changed;
- live Telegram was not touched;
- polling/webhook were not launched;
- token was not read;
- `.env` was not read;
- `config.py` contents were not read;
- `os.environ` was not read;
- databases/logs/real orders were not read;
- staging/production code was not changed;
- Vision/API were not touched;
- commit/push was not performed.

## Next Safe Step

```text
247-250 — план локальных contract examples для server adapter interface без реализации кода.
```
