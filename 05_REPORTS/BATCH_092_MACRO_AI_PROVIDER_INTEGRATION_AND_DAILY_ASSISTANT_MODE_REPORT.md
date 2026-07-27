# BATCH_092 — AI Provider Integration & Daily Assistant Mode

Дата: 2026-07-02
Исполнитель: Hermes Agent
Статус: **COMPLETED**

---

## Что сделано

### 1. Review Provider Unification

Review provider слой переведён на универсальный AI Provider Router:

- Создан `src/hermes_core/ai_provider/adapters/review_adapter.py` — `MockReviewAdapter` (SAFE) и `DeepSeekReviewDisabledAdapter` (BLOCKED)
- Оба адаптера зарегистрированы в `ProviderRegistry` (всего 8 провайдеров: 2 SAFE, 6 BLOCKED)
- Старый `review_provider_factory.py` сохранён как compatibility bridge — делегирует вызовы в новый `AIProviderRouter`
- Mock review работает через `BaseProviderAdapter.generate_review()`

### 2. Malyarka → AI Provider Router

Создан `src/hermes_modules/malyarka/ai_review.py` — единый путь Malyarka к AI:

- `review_disputed_row(raw_text)` — ревью спорной строки через router (всегда mock в safe-local)
- `review_disputed_rows(rows)` — батчевое ревью
- `ai_explain_dispute_category(category, text)` — объяснение категории спора
- Тесты **доказывают**: `direct_gemini_call=False`, `direct_deepseek_call=False`, `network_called=False`
- AST-тест проверяет отсутствие импортов `gemini`/`deepseek` в `ai_review.py`

### 3. Daily Assistant Mode

Создан `src/hermes_core/daily_assistant.py` с тремя отчётами:

| Команда | Вывод |
|---------|-------|
| `daily-assistant` | Полный снимок: проект, Malyarka, AI Provider, safety gates, блокировки |
| `daily-brief` | Краткая сводка на один экран |
| `what-next` | Следующие шаги и безопасные команды |

Дополнительные CLI команды: `local-health`, `project-status`, `malyarka-mode-status`.

### 4. CLI обновления

- 6 новых ежедневных команд зарегистрированы в `build_parser()`
- `command_help.py` обновлён: +16 записей (universal commands + daily assistant)
- Все новые команды возвращают `exit_code=0`

### 5. Тесты

- `tests/test_batch_092_integration.py` — **44 новых теста**
- Покрытие: Review unification, Malyarka AI router, Daily assistant, Safety, Blocking, Registry, CLI, Regression
- Исправлены 2 старых теста (registry count: 6→8, custom adapter count: 7→9)
- **380 passed total** (336 старых + 44 новых)

### 6. Документация

Обновлено:
- `START_HERE.md` — цифры 50+/380/27, секция Daily Assistant
- `docs/AI_PROVIDER_ARCHITECTURE.md` — 8 провайдеров, review адаптеры, daily commands, Malyarka→Router
- `docs/USER_RUNBOOK_RU.md` — (существующий контент актуален, новые команды в START_HERE)

---

## Изменённые файлы

```
NEW:
  src/hermes_core/ai_provider/adapters/review_adapter.py
  src/hermes_modules/malyarka/ai_review.py
  src/hermes_core/daily_assistant.py
  tests/test_batch_092_integration.py

MODIFIED:
  src/hermes_core/ai_provider/registry.py          (+2 review adapters)
  src/hermes_core/review/review_provider_factory.py (bridge to router)
  src/hermes_core/review/__init__.py
  src/hermes_core/cli.py                             (+6 commands)
  src/hermes_core/command_help.py                    (+16 entries)
  tests/test_ai_provider_universal.py                (count fixes)
  START_HERE.md
  docs/AI_PROVIDER_ARCHITECTURE.md
```

---

## Результаты проверок

| Проверка | Результат |
|----------|-----------|
| `pytest tests/` | **380 passed** |
| `daily-assistant` | OK |
| `daily-brief` | OK |
| `what-next` | OK |
| `local-health` | OK (OK, 0 missing, 0 env) |
| `project-status` | OK |
| `malyarka-mode-status` | OK (router, не прямой) |
| `ai-provider-list` | OK (8 провайдеров) |
| `ai-provider-mock` | OK |
| `review-provider-mock` | OK |
| `review-provider-disabled` | OK (blocked) |
| `secret-gate` | OK (4 провайдера требуют secret) |

---

## Безопасность

- `.env` не читался
- Токены/ключи не читались
- Google Drive не трогался
- Live Telegram не запускался
- Внешние API не вызывались
- Gemini/DeepSeek не вызывались (ни прямо, ни через router — всегда mock)
- Malyarka → только router (доказано тестами)
- Файлы не удалялись
- Архивы не трогались

---

## Риски / Хвосты

- `review_provider_factory.py` — compatibility bridge; при следующем крупном рефакторинге можно удалить старый `deepseek_review_loop.py`
- Старый `hermes_core/ai/` — остаётся для обратной совместимости CLI команд `ai-provider`, `review-provider`
- `PROJECT_ROOT` в `daily_assistant.py` — использует `parents[2]`, что корректно для текущей структуры

---

## Следующий крупный шаг

```
BATCH_093_OLD_HERMES_TO_HERMES_CLEAN_RUNTIME_BRIDGE
```

---

## Что передать ChatGPT

BATCH_092 выполнен. AI Provider интегрирован с review и Malyarka. Daily assistant собран. 380 тестов пройдены. Следующий: BATCH_093.
