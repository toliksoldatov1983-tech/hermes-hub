# TELEGRAM_STATUS_ROUTING_FIX_REPORT

Date: 2026-07-03

Status: `TELEGRAM_STATUS_INTENT_ROUTING_LOCAL_FIXED_PENDING_LIVE_RESTART`

Primary detailed report:

`05_REPORTS\TELEGRAM_ROUTES_CLEANUP_REPORT.md`

## Summary

The old generic response for status-like Telegram text was found in:

`[удалённый архив]`

The handler path also allowed free chat / generic fallback before Hermes-Clean direct intents.

Fixed locally:

- `Покажи статус`
- `Статус`
- `Как дела по проекту`
- `Статус Hermes`
- `Статус Малярки`

All route to Hermes-Clean status before generic fallback.

Expected response:

```text
=== СТАТУС HERMES-CLEAN ===
Telegram: PRODUCTION SINGLE-USER ACTIVE
Malyarka: Иван фасады v2 CLOSED
Root: E:\РАБОТА connected
Цены/ЛКМ: DRAFT
Защиты: 16 active
Следующий шаг: реальный заказ или уточнение цен/ЛКМ
```

## Backup

`C:\Users\user\Desktop\Hermes-Clean\backup_before_telegram_routes_cleanup_20260703_231124`

## Verification

```text
python -m py_compile malyarka_telegram\router.py malyarka_telegram\handlers.py malyarka_hermes\safety.py
python -m pytest tests\test_malyarka_telegram_router.py tests\test_malyarka_telegram_router_integration.py tests\test_malyarka_telegram_intent.py -q
```

Result:

```text
145 passed in 0.21s
```

## Live Status

Visible gateway process is `hermes gateway run`; no separate Malyarka polling process was visible. Live restart and live Telegram owner-only messages were not performed until the exact gateway entrypoint/cwd can be confirmed without reading secrets.
