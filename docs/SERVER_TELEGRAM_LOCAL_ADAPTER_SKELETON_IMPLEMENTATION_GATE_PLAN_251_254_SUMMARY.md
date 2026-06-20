# Series 251-254 summary

Created local adapter skeleton implementation gate plan.

Main document:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_GATE_PLAN_251_254.md
```

## Scope

Markdown-only gate plan.

No code.
No tests.
No server connection.
No live bot changes.
No secret reads.

## Gate Conditions

Future local skeleton implementation requires:

- separate explicit user permission;
- local-only scope;
- exact list of files allowed to create/change;
- exact list of forbidden files/zones;
- rollback plan;
- contract interface from `243-246`;
- contract examples from `247-250`;
- off by default;
- dry-run only;
- safe mode required;
- feature flags required;
- `side_effects=[]`;
- fallback to current flow;
- no direct Telegram send;
- no server/live changes.

## Future Target

Design target remains:

```text
malyarka_core/adapters/telegram.py
```

First implementation must be local-only, not server/production/staging.

## Forbidden

- server files;
- live Telegram;
- polling/webhook;
- token;
- `.env`;
- `config.py` contents;
- `os.environ`;
- databases/logs/real orders;
- staging/production code;
- Vision/API;
- commit/push.

## Gate Decision

Implementation is not allowed yet.

Next safe step:

```text
255-258 — план первого локального adapter skeleton implementation только после отдельного разрешения.
```
