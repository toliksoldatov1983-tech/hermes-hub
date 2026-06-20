# Server Adapter Sandbox

BUNDLE_271_300: Local implementation of the Hermes server adapter skeleton.

## Что это

Локальный test-double/skeleton, моделирующий будущий server adapter contract.

**Не серверный код.** Не копировать в `/opt/malyarka-telegram-bot`.

## Файлы

| Файл | Назначение |
|---|---|
| `server_adapter_skeleton.py` | Основной модуль: валидация, feature flags, обработка запросов |
| `test_server_adapter_skeleton.py` | Focused contract tests (pytest) — 10 примеров из BUNDLE_247_250 |
| `README.md` | Этот файл |

## Запуск тестов

```bash
cd E:\Hermes-Hub
pytest local_tests\server_adapter_sandbox\test_server_adapter_skeleton.py -v
```

## Контракт

### Request
```python
{
    "action": str,          # answer_text | explain_status | suggest_next_safe_step | diagnostics | fallback
    "payload": dict,        # безопасные данные (без token/env/secrets)
    "dry_run": bool,        # должен быть True
    "feature_flags": dict,  # см. SAFE_DEFAULT_FEATURE_FLAGS
    "safe_mode": bool,      # должен быть True
    "diagnostics": bool,    # запрос безопасной диагностики
}
```

### Response
```python
{
    "ok": bool,
    "status": str,           # dry_run | blocked | fallback | disabled | malformed | error
    "action": str,
    "dry_run": bool,
    "blocked": bool,
    "fallback_required": bool,
    "reason": str,
    "output_type": str,      # draft | diagnostics | blocked | fallback | disabled | malformed | error
    "side_effects": [],      # всегда []
    "diagnostics_safe": bool,
}
```

## Правила безопасности

- off by default
- dry-run only
- safe mode required
- feature flags required
- side_effects = []
- fallback to current flow
- no direct Telegram send
- no server/live changes
- no secret reads
