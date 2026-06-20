# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN

Дата: 2026-06-20

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN
```

Итоговый статус:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN_READY
```

## Scope

This is plan-only.

No live patch was applied.

No server, SSH, systemctl, feature flag, Phase 2, production, secrets, DB, logs or real orders were touched.

## Approval gate

Future live patch may be executed only after this exact phrase:

```text
APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE
```

This approval phrase does not approve Phase 2 retry.

Phase 2 retry still needs a separate future approval.

## Diff summary

Compared:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Changed file:

```text
hermes_adapter.py
```

Unchanged:

```text
telegram.py
```

Human-readable changes:

1. Added `import re`.
2. Added `ORDER_LIKE_PATTERNS`.
3. Added early guard in `check_hermes_safety(text)`:

```text
if input looks like Malyarka size/order:
    fallback_required = True
    blocked = False
    block_reason = order_like_input_fallback
    return result
```

4. Changed slash-command handling so commands like `/start` fallback to the existing Telegram router instead of being blocked:

```text
fallback_required = True
blocked = False
block_reason = command_fallback
```

5. Added helper:

```text
_looks_like_order_input(text)
```

## Protected inputs

The fix-candidate protects:

```text
700 x 500
700х500
700 × 500
700*500
700 x 500 x 2
700 500
700 500 2
```

For these inputs, the adapter must yield fallback to old Malyarka order flow.

## Generic paths that remain working

Safe generic text remains allowed:

```text
тест
unknown generic question
```

Unsafe patterns remain blocked:

```text
BOT_TOKEN
token=
API_KEY
secret
config.py
.env
os.environ
```

Forbidden production/server-like requests remain blocked.

## Why this is safe

- The patch does not add network/API calls.
- The patch does not read secrets.
- The patch does not write files.
- The patch does not touch DB/logs/orders.
- The patch is a guard-only change.
- For order-like input it returns control to the existing Malyarka parser/router.
- Feature flag stays OFF by default.

## Future live patch order

Documentation only. Do not execute now.

1. Read-only SSH check.
2. Confirm service current state.
3. Confirm autostart disabled.
4. Confirm feature flag OFF.
5. Backup live:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

6. Upload reviewed patched `hermes_adapter.py`.
7. Run syntax check only for the patched file.
8. Keep feature flag OFF.
9. Do not run Phase 2.
10. Restart service only if the future approved live patch plan explicitly requires it.
11. Run ordinary bot sanity check only after separate approval.
12. Record status.

## Forbidden in future live patch unless separately approved

- Phase 2 enable;
- production enable;
- autostart enable;
- reading `.env`, `config.py`, token, `os.environ`;
- reading DB/live logs/real orders;
- changing adapter logic beyond reviewed diff;
- live Telegram Phase 2 test;
- git/commit/push.

## Next live patch batch after approval

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

## 2026-06-20 — Applied

Applied by approved batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

Result:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED
```

Report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_REPORT.md
```
