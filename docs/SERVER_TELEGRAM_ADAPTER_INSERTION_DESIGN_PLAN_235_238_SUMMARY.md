# Series 235-238 summary

Created minimal server adapter insertion design plan.

Main document:

```text
E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md
```

## Sources

Read only local markdown:

- inventory report `231C-234C`;
- inventory summary `231C-234C`;
- server boundary plan `211-214`;
- `START_NEW_CHAT_PROMPT.md`;
- `HERMES_NAVIGATION_INDEX.md`.

No server connection.
No server file content reads.
No code.
No tests.

## Found Layers

Presence-only layers:

- `malyarka_telegram`;
- `malyarka_core`;
- `malyarka_core/services`;
- `malyarka_core/services/orders.py`;
- `malyarka_core/adapters/telegram.py`;
- `malyarka_core/exports/*`;
- `malyarka_ai`;
- `malyarka_vision`;
- `.venv`;
- `requirements.txt`.

## Candidate Boundary Points

- `malyarka_telegram/app.py`;
- `malyarka_telegram/router.py`;
- `malyarka_telegram/handlers.py`;
- `malyarka_core/adapters/telegram.py`;
- `malyarka_core/services/orders.py`.

## Minimal Safe Point

Chosen minimal design point:

```text
malyarka_core/adapters/telegram.py
```

Reason:

- adapter-shaped location already exists by filename;
- avoids direct Hermes logic in `app.py`;
- keeps `router.py` / `handlers.py` as future tiny guarded call-sites;
- avoids changing `services/orders.py` first;
- supports feature-flag rollback and dry-run-only behavior.

## Required First-Stage Rules

- off by default;
- dry-run only;
- safe mode on;
- no direct Telegram send from adapter;
- no file/database/log writes;
- no token/env/config reads;
- no exports;
- fallback to existing flow if disabled or unsafe.

## Risks

- `app.py` may be close to polling/runtime;
- `router.py` and `handlers.py` may affect live UX;
- `config.py` exists but contents were not read;
- no function/import contents are known yet;
- `malyarka_ai` and `malyarka_vision` must remain out of scope.

## Next Safe Step

```text
239-242 — план локального server adapter skeleton без подключения к live-боту.
```
