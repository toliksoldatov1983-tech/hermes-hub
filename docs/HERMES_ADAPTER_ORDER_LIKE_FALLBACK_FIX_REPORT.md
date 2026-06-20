# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_FIX_REPORT

Дата: 2026-06-20

Batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX
```

Итоговый статус:

```text
ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY
```

## Reason for plan-only result

Безопасной локальной копии реальных boundary-файлов не найдено:

```text
malyarka_core/adapters/telegram.py
malyarka_core/adapters/hermes_adapter.py
```

Поиск по `E:\Hermes-Hub` нашёл только:

- markdown-документы с draft/plan/report mentions;
- local sandbox/test-double files;
- staging-копию Telegram router/handlers/parser без `malyarka_core/adapters/telegram.py`;
- старые plan-only документы по server adapter gates.

Так как пользователь запретил трогать сервер/SSH/service/feature flag/Phase 2/runtime, а реального локального adapter boundary кода нет, исправление `.py` не выполнялось.

## What was read

Read-only локально:

- `E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md`;
- `E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_REPORT.md`;
- local staging files:
  - `malyarka_telegram/handlers.py`;
  - `malyarka_telegram/router.py`;
  - `malyarka_telegram/intent.py`;
  - `malyarka_telegram/messages.py`;
  - `malyarka_telegram/keyboards.py`;
  - `malyarka_core/parsing.py`;
- local test-double files:
  - `E:\Hermes-Hub\local_tests\server_adapter_sandbox\server_adapter_skeleton.py`;
  - `E:\Hermes-Hub\local_tests\server_adapter_sandbox\test_server_adapter_skeleton.py`;
  - `E:\Hermes-Hub\local_tests\hermes_adapter_fake\fake_adapter.py`.

## Confirmed local finding

Existing local/staging Malyarka router/parser logic already protects order-like input:

- `malyarka_telegram/router.py` has `looks_like_order_text(...)`;
- `malyarka_telegram/intent.py` detects dimension patterns and boosts order intent;
- `malyarka_core/parsing.py` parses `700 x 500` as `height=700`, `width=500`, `quantity=1`;
- Malyarka messages are Russian, not the observed English clarification.

Therefore the failed English clarification likely came from the Hermes adapter/generic assistant path, not from the old Malyarka order parser.

## Required future fix design

Future real fix should be applied only to the real adapter boundary after explicit approval and local/staging copy is available.

Required rule:

```text
order-like input -> fallback_required=true
```

Protected input examples:

```text
700 x 500
700 500
700*500
700 x 500 x 1
```

The adapter must not produce:

```text
What is 700 x 500 for?
Image dimensions
Canvas size
Window size
Other
```

## Contract tests required before next Phase 2 attempt

Must be added against the real adapter boundary or faithful local copy:

1. `700 x 500` outside order mode -> adapter fallback / existing router suggests order mode, no English clarification.
2. `700 x 500` inside order mode -> existing parser confirms row `700 500 1`.
3. `/start` -> existing menu flow is not broken.
4. `тест` -> safe generic path or fallback, no production side effects.
5. Unknown ordinary question -> safe generic path can be allowed if not order-like.
6. `fallback_required=true` -> call-site ignores adapter output and continues old Telegram flow.
7. English clarification guard -> order-like input cannot include `Image dimensions`, `Canvas size`, `Window size`, or `What is 700 x 500 for?`.

## Files to change later, not now

Likely future files:

```text
malyarka_core/adapters/telegram.py
malyarka_core/adapters/hermes_adapter.py
local contract tests for adapter boundary
```

Do not start by changing:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_core/services/orders.py
```

Reason: existing router/parser behavior was correct when Hermes adapter flag was OFF.

## Suggested next safe batch

```text
BATCH_PHASE2_FETCH_OR_CREATE_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

Goals:

1. Get a safe local copy of the exact server adapter boundary files or reconstruct them from approved local sources.
2. Add local contract tests first.
3. Implement order-like fallback guard locally.
4. Run local tests.
5. Prepare a separate controlled server patch plan only after tests pass.

## No-touch confirmation

Not performed:

- server access;
- SSH;
- systemctl;
- service changes;
- feature flag changes;
- Phase 2 launch;
- production enable;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- real adapter `.py` change;
- Telegram live test;
- git/commit/push.

