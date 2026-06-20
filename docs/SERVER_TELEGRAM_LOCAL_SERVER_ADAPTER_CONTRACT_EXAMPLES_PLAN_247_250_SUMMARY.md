# Series 247-250 summary

Created local server adapter contract examples plan.

Main document:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_EXAMPLES_PLAN_247_250.md
```

## Scope

Markdown-only plan.

No code.
No tests.
No server connection.
No live bot changes.
No secret reads.

## Examples Planned

- adapter off by default;
- safe dry-run allowed;
- export blocked;
- admin blocked;
- write blocked;
- unknown action blocked;
- malformed request;
- `fallback_required=true`;
- diagnostics safe-only;
- unsafe diagnostics blocked.

## Safety Rules Confirmed

Each example describes:

- request shape;
- expected response shape;
- expected status;
- blocked/fallback flag;
- `side_effects=[]`;
- why it is safe.

Global rules:

- no direct Telegram send;
- no token/env/config/os.environ reads;
- no db/log/order contents;
- no private IDs/API keys/webhook URLs;
- no file/db/log writes;
- no polling/webhook;
- fallback to current flow when blocked or unsafe.

## Next Safe Step

```text
251-254 — план локального adapter skeleton implementation gate, без реализации кода.
```
