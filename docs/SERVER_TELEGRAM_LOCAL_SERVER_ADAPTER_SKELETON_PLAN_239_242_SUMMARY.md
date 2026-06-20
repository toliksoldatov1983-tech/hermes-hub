# Series 239-242 summary

Created local server adapter skeleton plan.

Main document:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242.md
```

## Scope

Markdown-only plan.

No code.
No tests.
No server connection.
No live bot changes.
No secret reads.

## Skeleton Design

Future skeleton should be local first and model a safe adapter bridge before any live server integration.

Future design target:

```text
malyarka_core/adapters/telegram.py
```

Future live-adjacent path:

```text
router.py / handlers.py
-> tiny guarded call-site
-> malyarka_core/adapters/telegram.py or adjacent Hermes bridge
-> dry-run response
-> fallback if disabled/unsafe
```

## Mandatory Rules

- adapter off by default;
- first mode dry-run only;
- feature flags required;
- safe mode required;
- fallback to current flow required;
- `side_effects=[]`;
- no direct Telegram sends from adapter;
- no token/env/config/os.environ reads;
- no file/db/log writes;
- no exports/admin/write actions.

## Files Not To Touch First

- `app.py`;
- `services/orders.py`;
- live `router.py` / `handlers.py` except future tiny guarded call-site after local validation.

## Next Safe Step

```text
243-246 — план локального server adapter contract interface без реализации кода.
```
