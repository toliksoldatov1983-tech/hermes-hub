# Series 243-246 summary

Created local server adapter contract interface plan.

Main document:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246.md
```

## Scope

Markdown-only plan.

No code.
No tests.
No server connection.
No live bot changes.
No secret reads.

## Future Contract Target

Future target:

```text
malyarka_core/adapters/telegram.py
```

Adapter must be local-first, off by default, dry-run only, feature-flag gated, fallback-safe, no-side-effects, and diagnostics safe-only.

## Request Fields

Proposed request fields:

- `action`
- `payload`
- `dry_run`
- `feature_flags`
- `safe_mode`
- `diagnostics`

## Response Fields

Proposed response fields:

- `ok`
- `status`
- `action`
- `dry_run`
- `blocked`
- `fallback_required`
- `reason`
- `output_type`
- `side_effects`
- `diagnostics_safe`

## Required Behavior

- adapter does not send Telegram messages directly;
- `side_effects=[]`;
- `dry_run=true` required;
- safe mode required;
- missing/unknown flags default safe;
- blocked/fallback/error responses are structured and redacted;
- diagnostics never expose secrets;
- existing Telegram flow continues when adapter is disabled or unsafe.

## Forbidden

- token/env/config/os.environ reads;
- database/log/order content reads;
- private IDs/API keys/webhook URLs;
- polling/webhook;
- live module imports;
- file/db/log writes;
- exports/admin/write actions.

## Next Safe Step

```text
247-250 — план локальных contract examples для server adapter interface без реализации кода.
```
