# BATCH_091_AI_PROVIDER_SECRET_GATE_SETUP — Отчёт

Дата: 2026-07-02
Исполнитель: Hermes Agent

## Краткий вывод

BATCH_091 выполнен полностью. Создан универсальный AI Provider слой с provider-neutral архитектурой. Gemini и DeepSeek — первые adapter'ы, НЕ жёсткие зависимости ядра. Добавление нового провайдера не требует изменения ядра. 336 тестов, 27/27 smoke, 25/25 audit — все пройдены.

---

## Что сделано

### 1. Архитектура AI Provider Contract
Создан единый контракт (`ai_provider/contract.py`):
- `AIProviderMetadata` — метаданные провайдера (provider_id, name, model, mode, capabilities, secret_policy, requires_secret, requires_network, approval_required)
- `AIProviderRequest` — запрос (prompt, system_prompt, temperature, max_tokens, capabilities)
- `AIProviderResponse` — ответ (text, provider_id, is_mock, is_blocked, blocked_reason, safety)
- `ProviderCapability` — 9 возможностей (TEXT_GENERATION, REVIEW, VISION, EMBEDDINGS, TOOL_CALLING, JSON_MODE, LONG_CONTEXT, LOCAL_ONLY, NETWORK_REQUIRED)
- `SecretPolicy` — 5 политик (NO_SECRET_REQUIRED, SECRET_REQUIRED, SECRET_NOT_LOADED, APPROVAL_REQUIRED, BLOCKED_UNTIL_APPROVE_SECRET_SETUP)

### 2. Provider Registry
Создан `ai_provider/registry.py`:
- `ProviderRegistry` — регистрация, получение, список всех/enabled/disabled
- `get_default_registry()` — глобальный реестр с 6 провайдерами
- Добавление нового провайдера: `registry.register(MyAdapter())` — без изменения ядра

### 3. Provider Router
Создан `ai_provider/router.py`:
- `AIProviderRouter` — безопасный выбор провайдера с enforcement:
  - mock — всегда разрешён
  - неизвестный провайдер — BLOCKED
  - провайдер с requires_secret без approval — BLOCKED
  - провайдер с requires_network в safe_local — BLOCKED

### 4. Шесть Provider Adapters
| Adapter | ID | Статус |
|---------|-----|--------|
| MockProviderAdapter | `mock` | ✅ SAFE |
| GeminiProviderAdapter | `gemini-disabled` | 🔴 BLOCKED |
| DeepSeekProviderAdapter | `deepseek-disabled` | 🔴 BLOCKED |
| LocalDisabledProviderAdapter | `local-disabled` | 🔴 BLOCKED |
| OllamaDisabledProviderAdapter | `ollama-disabled` | 🔴 BLOCKED |
| CustomDisabledProviderAdapter | `custom-disabled` | 🔴 BLOCKED |

### 5. Восемь новых CLI команд
| Команда | Назначение |
|---------|-----------|
| `ai-provider-list` | Список всех провайдеров и их статус |
| `ai-provider-status` | Статус конкретного провайдера |
| `ai-provider-mock` | Явный выбор mock |
| `ai-provider-router` | Проверка решения роутера |
| `ai-provider-capabilities` | Возможности всех провайдеров |
| `secret-gate` | Статус secret gate |
| `review-provider-mock` | Выбор mock review |
| `review-provider-disabled` | Выбор disabled review |

### 6. 27 новых тестов
- Реестр: 6 провайдеров, get, unknown, новый провайдер без core change
- Роутер: mock работает, unknown blocked, gemini disabled, deepseek disabled
- Secret policy: mock не требует, gemini требует
- Capabilities: mock, gemini
- Безопасность: нет env read, нет token used, нет API call, registry без ключей

### 7. Документация
Создана `docs/AI_PROVIDER_ARCHITECTURE.md` — полная документация:
- Философия provider-neutral архитектуры
- Структура модуля
- Contract, Registry, Router
- Capabilities таблица
- Secret policy
- Как добавить нового провайдера
- CLI команды
- Безопасность

---

## Результаты проверок

| Проверка | Результат |
|----------|-----------|
| Универсальные тесты | 27/27 passed |
| Все тесты | 336/336 passed |
| Smoke | 27/27 (23 + 4 новых) |
| Project audit | 25/25 |
| ai-provider-list | 6 providers, mock=SAFE |
| ai-provider-mock | is_blocked=False |
| ai-provider-router gemini-disabled | is_blocked=True |
| ai-provider-capabilities | 6 providers with capabilities |
| secret-gate | 3 providers requiring secret |
| review-provider-mock | approved=True |
| Новый провайдер без core change | ✅ (tested) |

---

## Изменённые файлы

**Созданные (14 файлов):**
- `src/hermes_core/ai_provider/__init__.py`
- `src/hermes_core/ai_provider/contract.py`
- `src/hermes_core/ai_provider/registry.py`
- `src/hermes_core/ai_provider/router.py`
- `src/hermes_core/ai_provider/adapters/__init__.py`
- `src/hermes_core/ai_provider/adapters/base.py`
- `src/hermes_core/ai_provider/adapters/mock_adapter.py`
- `src/hermes_core/ai_provider/adapters/gemini_adapter.py`
- `src/hermes_core/ai_provider/adapters/deepseek_adapter.py`
- `src/hermes_core/ai_provider/adapters/local_disabled_adapter.py`
- `src/hermes_core/ai_provider/adapters/ollama_disabled_adapter.py`
- `src/hermes_core/ai_provider/adapters/custom_disabled_adapter.py`
- `tests/test_ai_provider_universal.py` (27 тестов)
- `docs/AI_PROVIDER_ARCHITECTURE.md`

**Обновлённые (4 файла):**
- `src/hermes_core/cli.py` — 8 новых команд
- `src/hermes_core/smoke.py` — 4 новых smoke check (23→27)
- `00_START/CURRENT_STATE.md`
- `03_TASKS/ACTIVE_BATCH.md`
- `03_TASKS/DONE.md`
- `03_TASKS/NEXT_TASK.md`
- `05_REPORTS/REPORT_TO_USER.md`
- `05_REPORTS/BATCH_091_AI_PROVIDER_SECRET_GATE_SETUP_REPORT.md`

---

## Безопасность

Подтверждаю:
- `.env` не читался
- Реальный `.env` не создавался
- Токены не читались
- Ключи не читались
- Google Drive не трогался
- Live Telegram не запускался
- Polling/webhook не запускались
- Реальные заказы не использовались
- Внешние API не вызывались
- Registry не содержит реальных ключей
- Удаления не было
- `src/hermes_modules/malyarka` не сломан
- `src/hermes_clean` не удалён

---

## Ключевые архитектурные решения

1. **Gemini и DeepSeek — первые adapter'ы, не жёсткие зависимости ядра**
2. **Новый провайдер = создать adapter + регистрация в registry (core не менять)**
3. **Malyarka должна обращаться только к Router, не к провайдерам напрямую**
4. **Старые provider_factory оставлены для обратной совместимости**

---

## Риски / Хвосты

- Review Provider Factory пока не перенесён на новую архитектуру — будет в BATCH_092
- Старые provider_factory и ai-provider (старый) команды сохранены для compat
- Malyarka пока не подключена к новому Router — будет в BATCH_092

---

## Следующий крупный шаг

```
BATCH_092_AI_PROVIDER_INTEGRATION_AND_REVIEW_LAYER_UNIFICATION
```

Интеграция универсального AI Provider слоя с review провайдерами, Malyarka и сквозные тесты.

---

## Что передать ChatGPT

BATCH_091 выполнен. Создан универсальный AI Provider слой:
- `src/hermes_core/ai_provider/` — contract, registry, router, 6 adapters
- 8 новых CLI команд (ai-provider-list, ai-provider-status, ai-provider-mock, ai-provider-router, ai-provider-capabilities, secret-gate, review-provider-mock, review-provider-disabled)
- 27 новых тестов (всего 336)
- Smoke: 27/27
- Architecture docs: `docs/AI_PROVIDER_ARCHITECTURE.md`

Gemini и DeepSeek — adapter'ы, не ядро. Новый провайдер добавляется без изменения core.
Следующий блок: BATCH_092 (интеграция review слоя и Malyarka с Router'ом).
