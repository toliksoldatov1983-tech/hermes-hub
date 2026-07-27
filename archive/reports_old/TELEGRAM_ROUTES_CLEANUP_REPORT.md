# TELEGRAM_ROUTES_CLEANUP_REPORT

Date: 2026-07-03

Final local status: `TELEGRAM_ROUTES_CLEANUP_LOCAL_FIXED_PENDING_LIVE_RESTART`

## Backup

Primary backup:

`C:\Users\user\Desktop\Hermes-Clean\backup_before_telegram_routes_cleanup_20260703_231124`

Earlier status-routing backup also exists:

`C:\Users\user\Desktop\Hermes-Clean\backup_before_status_routing_fix_20260703_230813`

Backup exclusions respected: `.env`, token files, `.git`, `.venv`, `orders.db`, `__pycache__`, and `bot_archive_20260703.py`.

## Live Entrypoint

Visible running process:

- PID 20840: `bash.exe -lic "set +m; hermes gateway run 2>&1"`
- PID 12188: child `bash.exe`
- PID 10024: child `bash.exe`
- PID 17796: `hermes.exe gateway run`
- PID 17256: `python.exe ... hermes.exe gateway run`
- PID 10100: `python.exe ... hermes.exe gateway run`

No separate `malyarka_telegram/app.py --run-polling` or `bot.py` polling process was visible.

The active Malyarka Telegram code path fixed in this batch is:

- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`

Live gateway restart was not performed because the running gateway command does not expose the exact Malyarka Telegram polling entrypoint in the process list. Restarting an ambiguous `hermes gateway run` process would risk disturbing unrelated Hermes gateway state.

## Cause

The old generic answer lived in:

`[удалённый архив]`

Old text:

`Понял, это вопрос по задачам или проекту...`

Root causes:

- `handle_text_message_with_router()` could call `answer_free_text()` before direct Hermes-Clean routing.
- `_route_neutral_text()` kept a legacy project/task fallback that matched status-like phrases.
- safety checks were not first in the `handle_text_message_with_router()` free-chat path.
- inline order phrases such as `Есть заказ: ..., 720x400 2 шт` were weaker than plain size-line input.

## Changed Files

- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `C:\Users\user\Desktop\Hermes-Clean\05_REPORTS\TELEGRAM_ROUTE_MAP_BEFORE_CLEANUP.md`
- `C:\Users\user\Desktop\Hermes-Clean\05_REPORTS\TELEGRAM_ROUTES_CLEANUP_REPORT.md`
- `C:\Users\user\Desktop\Hermes-Clean\05_REPORTS\TELEGRAM_STATUS_ROUTING_FIX_REPORT.md`
- `C:\Users\user\Desktop\Hermes-Clean\00_START\CURRENT_STATE.md`
- `C:\Users\user\Desktop\Hermes-Clean\03_TASKS\ACTIVE_BATCH.md`
- `C:\Users\user\Desktop\Hermes-Clean\03_TASKS\DONE.md`
- `C:\Users\user\Desktop\Hermes-Clean\03_TASKS\NEXT_TASK.md`
- `C:\Users\user\Desktop\Hermes-Clean\05_REPORTS\REPORT_TO_USER.md`

## Routing After Cleanup

Implemented order:

1. owner/auth check remains upstream in Telegram app path.
2. hard safety gate in handler path.
3. Hermes-Clean direct intents:
   - status
   - next step
   - correction mode
   - price draft
   - LKM draft
   - backup request
4. order intake preview.
5. legacy router/fallback.
6. generic assistant fallback last.

Status phrases now return exactly:

```text
=== СТАТУС HERMES-CLEAN ===
Telegram: PRODUCTION SINGLE-USER ACTIVE
Malyarka: Иван фасады v2 CLOSED
Root: E:\РАБОТА connected
Цены/ЛКМ: DRAFT
Защиты: 16 active
Следующий шаг: реальный заказ или уточнение цен/ЛКМ
```

## Test Results

Local owner-path simulations:

- `Покажи статус` -> Hermes-Clean status, no old generic fallback.
- `Статус` -> Hermes-Clean status.
- `Как дела по проекту` -> Hermes-Clean status.
- `Статус Hermes` -> Hermes-Clean status.
- `Статус Малярки` -> Hermes-Clean status.
- `Что дальше?` -> Hermes-Clean next safe step.
- `Есть заказ: Тест routing, МДФ 19 мм, RAL 9005, покраска, 720x400 2 шт` -> Malyarka preview with `720 400 2`.
- `Исправь цвет на RAL 9010` -> correction mode.
- `Поставь цену 25 000 тг за м² как draft` -> price draft.
- `PGP301 + тестовый профиль = 777 г/м² как draft` -> LKM draft.
- `Удали файл` -> blocked before fallback.
- `Запусти Vision` -> blocked before fallback.

Commands run:

```text
python -m py_compile malyarka_telegram\router.py malyarka_telegram\handlers.py malyarka_hermes\safety.py
python -m pytest tests\test_malyarka_telegram_router.py tests\test_malyarka_telegram_router_integration.py tests\test_malyarka_telegram_intent.py -q
```

Result:

```text
145 passed in 0.21s
```

Live Telegram owner-only tests were not sent from this session, and the gateway was not restarted, for the live-entrypoint reason above.

## Rollback

Rollback source:

`C:\Users\user\Desktop\Hermes-Clean\backup_before_telegram_routes_cleanup_20260703_231124`

Restore only the changed files from the backup to their original paths. Do not use reset/clear/prune. Do not touch `bot_archive_20260703.py`.

Suggested rollback approach:

1. Stop only the confirmed Telegram polling/gateway process if a restart is needed.
2. Copy the changed files listed above back from the backup.
3. Run `python -m py_compile` on restored Python files.
4. Start only the same confirmed Telegram polling/gateway command.

## Final Status

`TELEGRAM_ROUTES_CLEANUP_LOCAL_FIXED_PENDING_LIVE_RESTART`

Next required large step: confirm the gateway entrypoint/cwd without reading secrets, restart only that confirmed polling process, then run owner-only live Telegram tests.
