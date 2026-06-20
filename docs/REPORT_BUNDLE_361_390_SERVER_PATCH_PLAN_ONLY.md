# REPORT — BUNDLE_361_390_SERVER_PATCH_PLAN_ONLY

Date: 2026-06-17
Executed by: Hermes (deepseek-v4-pro)
Prerequisites: BUNDLE_331_360 Readiness Gate (PARTIALLY READY ✓)

## Autonomy

`AUTO_MARKDOWN` — plan only, no server touch.

## Что прочитано

- `TASK.md` (bundle 361-390)
- `README_FOR_CODEX.md` (bundle 361-390)
- `MANIFEST.md`
- `SAFETY_RULES.md`
- `REPORT_BUNDLE_331_360_SERVER_PATCH_READINESS_GATE.md`
- `SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`
- `SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `SERVER_TELEGRAM_TINY_GUARDED_CALLSITE_PLAN_301_330.md`

## Что создано

| Файл | Размер |
|---|---|
| `task_bundles\BUNDLE_361_390_...\TASK.md` | Из архива |
| `task_bundles\BUNDLE_361_390_...\README_FOR_CODEX.md` | Из архива |
| `docs\SERVER_TELEGRAM_SERVER_PATCH_PLAN_361_390.md` | 10 671 B — полный план |

## Server Patch Plan — кратко

**Цель:** создать `hermes_call_site.py` + добавить 1 строку в `handlers.py`.

**Целевые файлы:** 1 новый (`hermes_call_site.py`), 1 изменение (`handlers.py`, +3 строки).

**Этапы:** 0 (план) → 1 (readiness) → 2 (diff prep) → 3 (dry-run) → 4 (activation).

**Feature flags:** отдельный `hermes_flags.py`, все false по умолчанию.

**Rollback:** флаги в false → мгновенный эффект без перезапуска.

## Blocker'ы учтены

Все 10 missing prerequisites из BUNDLE_331_360 отражены в pre-patch requirements:
- SSH write-доступ
- Read-only копия handlers.py
- Feature-flags инфраструктура (→ `hermes_flags.py`)
- Backup процедура
- Staging/dry-run план
- Bot runtime state

## Действия остаются запрещёнными

- ❌ Чтение config.py / token / .env
- ❌ Изменение app.py / router.py / services/orders.py
- ❌ Запуск polling/webhook
- ❌ Telegram API calls
- ❌ Обработка реальных заказов

## Safety

```
server_touched:          false
live_bot_touched:        false
secrets_read:            false
production_code_changed: false
commit_push_performed:   false
```

## Статус

`SERVER_PATCH_PLAN_ONLY_COMPLETE`

## Следующий bundle

```text
#6: BUNDLE_391_420_SERVER_PATCH_PREPARE_DIFF_ONLY
Type: DIFF_PREP_ONLY
Autonomy: STOP_REVIEW
```

**СТОП.** STOP_REVIEW — требуется решение пользователя перед подготовкой diff. Автоматическое выполнение невозможно.
