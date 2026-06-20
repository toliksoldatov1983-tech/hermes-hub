# Local server adapter contract examples plan

Technical name: `BATCH_247_250_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN`

Date: 2026-06-16

## Status

This is a markdown-only examples plan for the future server adapter interface.

No Python code is written.
No tests are created.
No server connection is made.
No live bot modules are imported.
No polling/webhook is launched.
No server files are read, changed, or created.

## Sources Read

Local markdown sources:

- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md`
- `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`

## Purpose

Define local contract examples for the future server adapter interface before any implementation or tests.

These examples are not executable tests.
They are expected request/response shapes for later local validation.

Future target:

```text
malyarka_core/adapters/telegram.py
```

## Global Safety Rules For All Examples

Every example must preserve:

- no direct Telegram send from adapter;
- no file writes;
- no database writes;
- no log writes;
- no network/API calls;
- no token reads;
- no `.env` reads;
- no `config.py` contents reads;
- no `os.environ` reads;
- no real order file processing;
- no live module imports;
- `side_effects=[]`;
- safe, structured response.

## Example 1 — Adapter Off By Default

### Request Shape

```text
{
  "action": "answer_text",
  "payload": {
    "text": "Что дальше?",
    "current_mode": "chat",
    "safe_context_summary": "local safe context"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": false,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": false
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "disabled",
  "action": "fallback",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "adapter disabled by feature flag",
  "output_type": "fallback",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
disabled
```

Safety:

- adapter is off by default;
- existing flow continues;
- no action is executed;
- `side_effects=[]`.

## Example 2 — Safe Dry-Run Allowed

### Request Shape

```text
{
  "action": "explain_status",
  "payload": {
    "text": "Покажи статус безопасно",
    "current_mode": "chat",
    "safe_context_summary": "adapter dry-run local status only"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_SERVER_ADAPTER_ENABLED": true,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": false
}
```

### Expected Response Shape

```text
{
  "ok": true,
  "status": "dry_run",
  "action": "explain_status",
  "dry_run": true,
  "blocked": false,
  "fallback_required": false,
  "reason": "safe dry-run action allowed",
  "output_type": "draft",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
dry_run
```

Safety:

- safe action only;
- dry-run only;
- no Telegram send;
- `side_effects=[]`.

## Example 3 — Export Blocked

### Request Shape

```text
{
  "action": "create_export",
  "payload": {
    "order_preview_safe": "summary only"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_EXPORT_CALLBACKS_ENABLED": false,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": false
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "blocked",
  "action": "blocked",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "export action blocked by feature flags",
  "output_type": "blocked",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
blocked
```

Safety:

- export is not created;
- export callbacks are off;
- no files are written;
- fallback required.

## Example 4 — Admin Blocked

### Request Shape

```text
{
  "action": "admin_change",
  "payload": {
    "requested_change": "change rule draft only"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_ADMIN_CHANGES_ENABLED": false,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": false
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "blocked",
  "action": "blocked",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "admin changes disabled",
  "output_type": "blocked",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
blocked
```

Safety:

- no admin change;
- no rule/price/material update;
- no write operation.

## Example 5 — Write Blocked

### Request Shape

```text
{
  "action": "edit_file",
  "payload": {
    "target": "server file"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": false
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "blocked",
  "action": "blocked",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "write action forbidden",
  "output_type": "blocked",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
blocked
```

Safety:

- no files are edited;
- no server state changes;
- side effects remain empty.

## Example 6 — Unknown Action Blocked

### Request Shape

```text
{
  "action": "do_magic_live",
  "payload": {},
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": false
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "blocked",
  "action": "blocked",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "unknown action blocked",
  "output_type": "blocked",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
blocked
```

Safety:

- unknown behavior cannot execute;
- fallback preserves current flow.

## Example 7 — Malformed Request

### Request Shape

```text
{
  "payload": "not a dict",
  "dry_run": true
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "malformed",
  "action": "malformed",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "required fields missing or invalid",
  "output_type": "malformed",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
malformed
```

Safety:

- malformed input is controlled;
- no exception details leak;
- fallback required.

## Example 8 — `fallback_required=true`

### Request Shape

```text
{
  "action": "fallback",
  "payload": {
    "reason": "use existing Telegram flow"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": false
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "fallback",
  "action": "fallback",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "fallback requested",
  "output_type": "fallback",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
fallback
```

Safety:

- existing flow remains authoritative;
- adapter does not execute behavior;
- no side effects.

## Example 9 — Diagnostics Safe-Only

### Request Shape

```text
{
  "action": "diagnostics",
  "payload": {
    "include": "safe flags only"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_SERVER_ADAPTER_ENABLED": true,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": true
}
```

### Expected Response Shape

```text
{
  "ok": true,
  "status": "dry_run",
  "action": "diagnostics",
  "dry_run": true,
  "blocked": false,
  "fallback_required": false,
  "reason": "safe diagnostics only",
  "output_type": "diagnostics",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
dry_run
```

Safety:

- diagnostics contain only safe flag/status facts;
- no token/env/config/db/log/order/private data;
- no polling/restart commands.

## Example 10 — Unsafe Diagnostics Blocked

### Request Shape

```text
{
  "action": "diagnostics",
  "payload": {
    "include": "token env config db logs"
  },
  "dry_run": true,
  "feature_flags": {
    "HERMES_ADAPTER_ENABLED": true,
    "HERMES_SAFE_MODE": true,
    "HERMES_DRY_RUN_ONLY": true
  },
  "safe_mode": true,
  "diagnostics": true
}
```

### Expected Response Shape

```text
{
  "ok": false,
  "status": "blocked",
  "action": "blocked",
  "dry_run": true,
  "blocked": true,
  "fallback_required": true,
  "reason": "unsafe diagnostics request blocked",
  "output_type": "blocked",
  "side_effects": [],
  "diagnostics_safe": true
}
```

Expected status:

```text
blocked
```

Safety:

- unsafe diagnostics request is blocked;
- forbidden data is not exposed;
- reason is redacted and generic.

## Examples Safety Checklist

Every future implementation/test derived from these examples must verify:

- all responses include required response fields;
- `side_effects=[]`;
- `dry_run=true`;
- blocked actions have `blocked=true`;
- blocked/unsafe/disabled/malformed responses have `fallback_required=true`;
- diagnostics-safe flag is true;
- no response contains secrets;
- no adapter response directly sends Telegram messages;
- current flow can continue on fallback.

## Explicit No-Touch Confirmation

For package `247-250`:

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
251-254 — план локального adapter skeleton implementation gate, без реализации кода.
```
