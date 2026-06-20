# HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_REPORT

Дата: 2026-06-20

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

Итоговый статус:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED
```

## Approval

Live patch was explicitly approved with:

```text
APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE
```

This approval did not approve Phase 2.

## Precheck result

Precheck passed:

```text
SSH: verified
service before patch: active/running
autostart: disabled
feature flag: OFF
live target: /opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
production: OFF
Phase 2: OFF
```

## Backup

Backup created before upload:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py.20260620_021040.before_order_like_fallback_patch
```

## Patch applied

Uploaded only:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

to:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

No `telegram.py` change was made.

## Checks

Syntax/import-safe checks passed:

```text
python -m py_compile malyarka_core/adapters/hermes_adapter.py
IMPORT_SAFE_OK
```

Controlled service restart was performed to load the patched file.

Post-restart state:

```text
service: active/running
autostart: disabled
feature flag: OFF
production: OFF
Phase 2: OFF
```

Patch guard confirmed:

```text
order_like_input_fallback
```

## Sanity Telegram test

User performed ordinary sanity test:

```text
/start
700 x 500
```

User result:

```text
Everything normal.
```

The previous forbidden English clarification did not recur in the reported sanity result.

User noted:

```text
Malyarka file does not download.
```

Assessment:

This is not treated as failure of this order-like fallback patch. The patch changed only `hermes_adapter.py`, feature flag remained OFF, and the sanity scope for this patch was `/start` plus `700 x 500` without generic English clarification.

The Malyarka file download issue should be tracked as a separate export/callback blocker and investigated in a separate read-only batch.

## Rollback

Rollback was not needed.

Backup remains available:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py.20260620_021040.before_order_like_fallback_patch
```

## Final verified state

```text
service: active/running
autostart: disabled
feature flag: OFF
production: OFF
Phase 2: OFF
patch guard: present
```

## No-touch confirmation

Not performed:

- feature flag enable;
- Phase 2 launch;
- production enable;
- systemctl enable;
- systemctl stop;
- autostart change;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- `telegram.py` change;
- adapter logic beyond approved fix-candidate;
- git/commit/push;
- Codex-sent live Telegram test.

