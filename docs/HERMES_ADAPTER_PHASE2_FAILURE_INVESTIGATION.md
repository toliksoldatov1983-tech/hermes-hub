# HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION

Дата: 2026-06-20

Итог расследования:

```text
PHASE2_FAILURE_INVESTIGATION_READY
```

Исходный статус dry-run:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

## Scope

Это read-only / plan-only investigation.

Код не менялся. Phase 2 не запускалась повторно. Feature flag не менялся.

Прочитано локально:

- `E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_REPORT.md`;
- локальная staging-копия `malyarka_telegram/handlers.py`;
- локальная staging-копия `malyarka_telegram/router.py`;
- локальная staging-копия `malyarka_telegram/intent.py`;
- локальная staging-копия `malyarka_telegram/messages.py`;
- локальная staging-копия `malyarka_telegram/keyboards.py`;
- локальная staging-копия `malyarka_core/parsing.py`;
- локальные sandbox/fake adapter files в `E:\Hermes-Hub\local_tests`.

Сервер в этом investigation не трогался.

## Failure fact

При временно включённом Hermes adapter сообщение:

```text
700 x 500
```

получило неправильный ответ:

```text
What is 700 x 500 for?
1. Image dimensions
2. Canvas size
3. Window size
4. Other
```

Это не штатный Malyarka order flow.

Ожидаемое поведение:

- outside order mode: сообщение похоже на заказ, бот предлагает перейти в `/заказ`;
- inside order mode: строка разбирается как `700 500 1`;
- adapter не заменяет Malyarka parser и не задаёт generic English clarification.

## Вероятная точка неправильного перехвата

Вероятная точка:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
```

Причина:

Во время precheck/dry-run ранее было зафиксировано, что feature flag и Hermes hook находятся в `malyarka_core/adapters/telegram.py`:

```text
_HERMES_ADAPTER_ENABLED = False
from malyarka_core.adapters.hermes_adapter import check_hermes_safety
hermes = check_hermes_safety(text)
if hermes.get("fallback_required"): pass
elif hermes.get("blocked"): return blocked preview
```

Из этого видно, что hook вставлен в adapter boundary вокруг order preview path.

Локальная staging-копия `malyarka_core/adapters/telegram.py` отсутствует, поэтому точное положение hook в файле сейчас нельзя подтвердить локально. Но live dry-run показал, что при включённом flag именно этот путь начал влиять на обработку `700 x 500`.

Вероятная ошибка дизайна:

```text
Hermes adapter вызывается до обязательной проверки "order-like input -> Malyarka order flow fallback".
```

То есть adapter получает производственный размер как обычный свободный вопрос и возвращает/провоцирует generic assistant clarification вместо `fallback_required=true`.

## Почему появился English clarification

Штатные локальные Malyarka messages/router не содержат такого English response.

Локально найдено:

- `malyarka_telegram/router.py` содержит `looks_like_order_text(...)`;
- `malyarka_telegram/intent.py` содержит dimension detection и повышает order confidence для размеров;
- `malyarka_telegram/messages.py` содержит русские Malyarka-сообщения;
- `malyarka_core/parsing.py` разбирает `700 x 500` как height=700, width=500, quantity=1.

Следовательно, ответ:

```text
What is 700 x 500 for?
Image dimensions / Canvas size / Window size / Other
```

с высокой вероятностью пришёл не из штатного Malyarka router/messages/parser, а из Hermes adapter/assistant path или из generic clarification layer, который был вызван вместо fallback.

Inference:

```text
check_hermes_safety(text) или связанный adapter path не классифицировал `700 x 500` как protected order-like input and did not force fallback_required=true.
```

## Expected routing rule

Нужное правило routing:

1. Любой order-like input должен идти в Malyarka order flow.
2. Adapter обязан вернуть `fallback_required=true`, если сообщение похоже на размер/заказ.
3. Adapter не должен заменять штатный parser в режиме заказа.
4. Adapter не должен формировать generic English clarification для размеров.
5. В нейтральном режиме adapter может только уступить routing layer:
   - если `looks_like_order_text(text)` true, штатный Telegram router решает: suggest order mode;
   - если current mode is order, штатный parser делает preview.
6. Если adapter не уверен, безопасный ответ всегда:

```text
fallback_required=true
```

## Required contract tests before any repeat Phase 2

Нужны focused tests до повторного включения flag:

1. `700 x 500` outside order mode:
   - expected: adapter returns `fallback_required=true`;
   - existing router returns "looks like order / switch to order mode";
   - no English clarification.

2. `700 x 500` inside order mode:
   - expected: adapter returns `fallback_required=true`;
   - Malyarka parser produces confirmed row `700 500 1`;
   - export availability follows existing order preview logic.

3. `/start`:
   - expected: existing neutral menu flow remains unchanged;
   - adapter fallback or no-op.

4. `тест`:
   - expected: safe dry-run may answer only if explicitly designed;
   - no production action;
   - no parser replacement.

5. Unknown ordinary question:
   - expected: allowed generic assistant path only outside order-like detection;
   - response language should follow project UX rules, preferably Russian;
   - no Telegram send inside adapter.

6. `fallback_required=true`:
   - expected: call-site ignores adapter output completely and continues old Telegram flow.

7. English clarification guard:
   - for dimension/order-like input, adapter output must not contain generic English options like `Image dimensions`, `Canvas size`, `Window size`.

## Files likely to change later

Do not change now.

Likely future files:

- server-side `/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py`;
- server-side `/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py`;
- possibly local contract tests under `E:\Hermes-Hub\local_tests\server_adapter_sandbox`;
- possibly local fake adapter contract tests under `E:\Hermes-Hub\local_tests\hermes_adapter_fake`;
- possibly future docs for corrected Phase 2 gate.

Files that should probably not be changed first:

- `malyarka_telegram/app.py`;
- `malyarka_telegram/router.py`;
- `malyarka_telegram/handlers.py`;
- `malyarka_core/services/orders.py`.

Reason:

The failure appears to be in adapter boundary / fallback behavior, not in the existing parser/router, which already handled the same dummy input correctly before Phase 2.

## Next safe Codex batch, without implementation in this investigation

Suggested next batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX_PLAN
```

Plan-only contents:

1. Read server-side adapter files only after explicit approval.
2. Design guard: `order-like -> fallback_required=true`.
3. Design call-site invariant: adapter output ignored when fallback is required.
4. Add local contract tests for:
   - `700 x 500` outside order mode;
   - `700 x 500` inside order mode;
   - `/start`;
   - `тест`;
   - unknown question;
   - fallback path;
   - English clarification blocker.
5. Prepare patch plan for minimal adapter boundary fix.
6. Require a new controlled dry-run approval before any future flag enable.

## Blocker

Phase 2 must remain blocked until there is a corrected adapter fallback contract and tests.

Blocker:

```text
Hermes adapter currently treats production-size input `700 x 500` as generic ambiguous text instead of yielding fallback to Malyarka order flow.
```

## No-touch confirmation

Not performed:

- server access;
- SSH;
- service start/restart/stop/enable/disable;
- feature flag change;
- Phase 2 runtime;
- Telegram test;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- `.py` code change;
- adapter code change;
- production enable;
- git/commit/push.

## 2026-06-20 — Follow-up: order-like fallback fix batch result

Batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX
```

Result:

```text
ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY
```

Reason:

The safe local tree does not contain the real adapter boundary files:

```text
malyarka_core/adapters/telegram.py
malyarka_core/adapters/hermes_adapter.py
```

Only markdown plans/reports and local test doubles were found. Since the server, SSH, service, feature flag and Phase 2 runtime were forbidden for this batch, no `.py` fix was applied.

Created:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_FIX_REPORT.md
```

Next safe step:

```text
BATCH_PHASE2_FETCH_OR_CREATE_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```
