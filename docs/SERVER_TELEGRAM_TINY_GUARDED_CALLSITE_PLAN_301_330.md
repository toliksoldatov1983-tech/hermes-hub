# Tiny Guarded Call-Site Plan

Technical name: `BUNDLE_301_330_TINY_GUARDED_CALLSITE_PLAN`
Date: 2026-06-17
Type: PLAN_ONLY / AUTO_MARKDOWN

## Status

Markdown-only plan. No code. No tests. No server/live/secrets/real orders.

## Purpose

Спроектировать tiny guarded call-site — минимальную точку подключения Hermes adapter в существующем серверном Telegram-боте.

Call-site должен быть:
- **tiny** — минимальный код, одна функция/декоратор, не более ~20 строк логики
- **guarded** — защищён feature flags, safe mode, dry-run, fallback
- **call-site** — точка вызова адаптера, не сам адаптер

## Context

Из предыдущих bundle:

- **Adapter skeleton** (271-300): реализован `server_adapter_skeleton.py` — локальный test-double контракта
- **Insertion design** (235-238): целевая точка `malyarka_core/adapters/telegram.py`, маршрут: `router/handlers → call-site → adapter → dry-run response → fallback`
- **Master context** (00): "preferred future tiny guarded call-site: `malyarka_telegram/handlers.py`"

## Call-Site Location

```text
malyarka_telegram/handlers.py
```

Это файл на сервере (`/opt/malyarka-telegram-bot/malyarka_telegram/handlers.py`).

**Важно:** мы не читаем и не меняем содержимое этого файла. План описывает только форму будущей вставки.

## Proposed Call-Site Shape

### Концепт

В существующий обработчик сообщений (функцию в `handlers.py`) добавляется **одна строка-вызов** перед основной логикой:

```python
# Псевдокод — не реальный код handlers.py
async def handle_message(message, ...):
    # TINY GUARDED CALL-SITE — одна строка
    adapter_result = await hermes_call_site(message, safe_context)

    if adapter_result.fallback_required:
        pass  # продолжаем существующую логику
    # существующая логика handlers.py продолжается без изменений
```

### Call-Site функция (новая, отдельная)

Создаётся **отдельный файл** (не меняем `handlers.py` на первой стадии):

```text
malyarka_telegram/hermes_call_site.py
```

Функция:

```python
async def hermes_call_site(message, safe_context) -> AdapterResult:
    """
    Tiny guarded call-site for Hermes adapter.

    RULES:
    - off by default (HERMES_TELEGRAM_INSERTION_ENABLED=false)
    - dry-run only
    - safe mode required
    - fallback to existing flow on any block
    - never sends Telegram messages directly
    """
    flags = load_feature_flags()

    if not flags.get("HERMES_TELEGRAM_INSERTION_ENABLED"):
        return AdapterResult(fallback_required=True, reason="insertion disabled")

    if not flags.get("HERMES_SAFE_MODE"):
        return AdapterResult(fallback_required=True, reason="safe mode required")

    request = build_adapter_request(message, safe_context, dry_run=True, flags=flags)
    response = process_request(request)  # вызывает server_adapter_skeleton

    return AdapterResult(
        ok=response["ok"],
        fallback_required=response["fallback_required"],
        response=response,
    )
```

### Точка вставки в handlers.py

**Только после полного approval gate (bundle 331-360 и далее):**

```python
# В начало существующей handler-функции добавляется ОДНА строка:
call_result = await hermes_call_site(message, safe_context)
if call_result.fallback_required:
    pass  # continue existing flow
```

Без этой строки существующий бот работает как раньше.

## Guard Layers

| Слой | Механизм | По умолчанию |
|---|---|---|
| Feature flag | `HERMES_TELEGRAM_INSERTION_ENABLED` | `false` |
| Safe mode | `HERMES_SAFE_MODE` | `true` |
| Dry-run | `HERMES_DRY_RUN_ONLY` | `true` |
| Adapter enabled | `HERMES_ADAPTER_ENABLED` | `false` |
| Fallback | `fallback_required=true` | всегда при disabled |
| Side effects | `side_effects=[]` | всегда |
| No Telegram send | — | всегда |

## Call-Site Contract

### Input (что call-site передаёт адаптеру)

```python
{
    "action": "answer_text",        # или explain_status, suggest_next_safe_step
    "payload": {
        "text": "...",              # текст сообщения пользователя (без secrets)
        "current_mode": "...",      # текущий режим бота
        "safe_context_summary": "", # безопасный контекст (без token/env/private IDs)
    },
    "dry_run": True,                # всегда True
    "feature_flags": {...},         # из конфига бота
    "safe_mode": True,              # всегда True
    "diagnostics": False,           # True только в диагностическом режиме
}
```

### Output (что call-site получает от адаптера)

```python
{
    "ok": bool,
    "status": "dry_run" | "blocked" | "fallback" | "disabled",
    "fallback_required": bool,      # True → игнорируем ответ, продолжаем старую логику
    "reason": str,
    "output_type": "draft" | "diagnostics" | "blocked" | "fallback",
    ...
}
```

### Правило fallback

Если `fallback_required=True` — ответ адаптера **игнорируется**, бот продолжает существующую логику `handlers.py` без изменений.

## Что НЕ делает call-site

- Не отправляет сообщения в Telegram
- Не читает token / .env / config.py
- Не читает базу данных / логи / заказы
- Не меняет production/staging код
- Не запускает polling/webhook
- Не вызывает Telegram API напрямую
- Не обрабатывает реальные заказы

## Что call-site ДЕЛАЕТ

- Принимает сообщение пользователя и безопасный контекст
- Проверяет feature flags
- Формирует безопасный request для адаптера
- Вызывает `process_request()` из adapter skeleton
- Возвращает результат с флагом `fallback_required`
- Если `fallback_required=True` — существующая логика продолжается

## Порядок внедрения (будущие этапы)

1. **BUNDLE_301_330** (этот): Plan only — описать форму call-site
2. **BUNDLE_331_360**: SERVER_PATCH_READINESS_GATE — проверить готовность к server patch
3. **BUNDLE_361_390**: SERVER_PATCH_PLAN_ONLY — описать план server patch
4. ... (server patch bundles)
5. **Когда разрешено**: создать `malyarka_telegram/hermes_call_site.py` на сервере
6. **Когда разрешено**: добавить одну строку в `handlers.py`
7. **Когда разрешено**: активировать feature flag `HERMES_TELEGRAM_INSERTION_ENABLED=true`

## Rollback

1. `HERMES_TELEGRAM_INSERTION_ENABLED=false`
2. Убрать строку вызова из `handlers.py` (если была добавлена)
3. Удалить `hermes_call_site.py` (опционально)
4. Бот продолжает работать как раньше

Rollback не требует:
- перезапуска бота (если flags читаются динамически)
- изменения других файлов
- чтения secrets

## Acceptance Criteria

Перед внедрением на сервер:
- [ ] Adapter skeleton протестирован локально (17/17 ✓)
- [ ] Call-site форма согласована
- [ ] Feature flags готовы
- [ ] Fallback проверен локально
- [ ] Rollback план документирован
- [ ] Server patch readiness gate пройден
- [ ] Explicit approval получен

## Источники

- `SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_SKELETON_PLAN_239_242.md`
- `SERVER_TELEGRAM_LOCAL_SERVER_ADAPTER_CONTRACT_INTERFACE_PLAN_243_246.md`
- `00_MASTER_CONTEXT.md` (из архива конвейера)
- `server_adapter_skeleton.py` (BUNDLE_271_300)
