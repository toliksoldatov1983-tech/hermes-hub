# REPORT — BUNDLE_301_330_TINY_GUARDED_CALLSITE_PLAN

Date: 2026-06-17
Executed by: Hermes (deepseek-v4-pro)
Prerequisites: BUNDLE_271_300 (COMPLETE ✓)

## Autonomy

`AUTO_MARKDOWN` — plan only, without code.

## Что прочитано

- `TASK.md` (bundle 301-330 из архива)
- `README_FOR_CODEX.md` (bundle 301-330)
- `MANIFEST.md`
- `SAFETY_RULES.md`
- `SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `00_MASTER_CONTEXT.md` (архив конвейера)
- `server_adapter_skeleton.py` (результат BUNDLE_271_300)

## Что создано

| Файл | Описание |
|---|---|
| `task_bundles\BUNDLE_301_330_...\TASK.md` | Скопирован из архива |
| `task_bundles\BUNDLE_301_330_...\README_FOR_CODEX.md` | Скопирован из архива |
| `docs\SERVER_TELEGRAM_TINY_GUARDED_CALLSITE_PLAN_301_330.md` | План call-site (8 773 B) |

## Содержание плана

- **Локация:** `malyarka_telegram/handlers.py` + новый `malyarka_telegram/hermes_call_site.py`
- **Форма:** одна строка-вызов в существующий handler
- **Guards:** feature flags, safe mode, dry-run, fallback
- **Контракт:** input/output совместим с `server_adapter_skeleton.process_request()`
- **Rollback:** флаги в false → бот работает как раньше
- **Без кода:** только план, не реализация

## Safety

| Зона | Статус |
|---|---|
| server_touched | false |
| live_bot_touched | false |
| polling_started | false |
| webhook_started | false |
| telegram_api_called | false |
| secrets_read | false |
| real_orders_used | false |
| production_code_changed | false |
| commit_push_performed | false |

## Статус

`TINY_GUARDED_CALLSITE_PLAN_COMPLETE`

## Следующий bundle

```text
#4: BUNDLE_331_360_SERVER_PATCH_READINESS_GATE
Type: GATE_ONLY
Autonomy: STOP_REVIEW
```

**СТОП:** следующий bundle — STOP_REVIEW. Конвейер останавливается.
