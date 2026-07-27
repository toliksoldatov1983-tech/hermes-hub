# Архитектура AI Provider Layer (Универсальный слой)

> Hermes-Clean не привязан жёстко к Gemini или DeepSeek.
> Все AI-провайдеры — сменные адаптеры через единый контракт.

---

## 1. Философия

Hermes-Clean использует **provider-neutral архитектуру**:
- **Ядро не знает** о конкретных провайдерах
- Каждый провайдер — отдельный adapter-файл
- Добавление нового провайдера = создать adapter + зарегистрировать в registry
- **Никаких изменений ядра** для добавления провайдера

Gemini и DeepSeek — **первые два поддерживаемых adapter'а**.
Позже можно добавить: Ollama, OpenAI-compatible, Anthropic, local LLM и др.

---

## 2. Структура модуля

```
src/hermes_core/ai_provider/
├── __init__.py          # Экспорт ключевых типов
├── contract.py          # AIProviderContract, Capability, SecretPolicy
├── registry.py          # ProviderRegistry — реестр адаптеров
├── router.py            # AIProviderRouter — безопасный выбор провайдера
└── adapters/
    ├── __init__.py
    ├── base.py          # BaseProviderAdapter (ABC)
    ├── mock_adapter.py  # Mock (всегда доступен)
    ├── gemini_adapter.py  # Gemini (disabled в safe-mode)
    ├── deepseek_adapter.py # DeepSeek (disabled в safe-mode)
    ├── local_disabled_adapter.py  # Local LLM placeholder
    ├── ollama_disabled_adapter.py # Ollama placeholder
    ├── custom_disabled_adapter.py # Custom provider placeholder
    └── review_adapter.py          # Review adapters (mock + deepseek disabled)
```

---

## 3. AI Provider Contract

Единый контракт для любого провайдера:

```python
@dataclass(frozen=True)
class AIProviderMetadata:
    provider_id: str          # Уникальный ID (mock, gemini-disabled, ...)
    provider_name: str        # Человеческое имя (Mock Provider, Gemini, ...)
    model_id: str             # Модель по умолчанию
    mode: str                 # Режим работы
    capabilities: tuple       # Список возможностей (см. ниже)
    secret_policy: SecretPolicy  # Политика секретности
    requires_secret: bool     # Нужен ли API-ключ
    requires_network: bool    # Нужен ли доступ в сеть
    approval_required: str    # Какой gate нужен для активации
    is_enabled: bool          # Включён ли сейчас
    blocked_reason: str       # Причина блокировки (если заблокирован)
```

### Request / Response

```python
@dataclass
class AIProviderRequest:
    prompt: str               # Текст запроса
    system_prompt: str = ""   # Системный промпт
    temperature: float = 0.7  # Температура
    max_tokens: int = 1024    # Макс. токенов
    capabilities: tuple = ()  # Запрошенные возможности

@dataclass(frozen=True)
class AIProviderResponse:
    text: str                 # Текст ответа
    provider_id: str          # Какой провайдер ответил
    is_mock: bool             # Это mock или реальный API
    is_blocked: bool          # Заблокировано ли
    blocked_reason: str       # Причина блокировки
    safety: dict              # Метаданные безопасности
```

---

## 4. Provider Capabilities (Возможности)

Каждый провайдер заявляет свои возможности:

| Capability | Описание | Mock | Gemini | DeepSeek |
|------------|----------|------|--------|----------|
| TEXT_GENERATION | Генерация текста | ✅ | ✅ (disabled) | ✅ (disabled) |
| REVIEW | Ревью кода | ✅ | ❌ | ✅ (disabled) |
| VISION | Распознавание изображений | ❌ | ✅ (disabled) | ❌ |
| EMBEDDINGS | Векторные эмбеддинги | ❌ | ✅ (disabled) | ✅ (disabled) |
| TOOL_CALLING | Вызов инструментов | ❌ | ✅ (disabled) | ✅ (disabled) |
| JSON_MODE | Структурированный JSON | ✅ | ✅ (disabled) | ✅ (disabled) |
| LONG_CONTEXT | Длинный контекст | ❌ | ✅ (disabled) | ✅ (disabled) |
| LOCAL_ONLY | Работает только локально | ❌ | ❌ | ❌ |
| NETWORK_REQUIRED | Требует сеть | ❌ | ✅ | ✅ |

---

## 5. Provider Registry

Registry — единая точка регистрации провайдеров:

```python
from hermes_core.ai_provider import get_default_registry

reg = get_default_registry()
reg.register(MyNewAdapter())  # Никаких изменений ядра!
```

Сейчас зарегистрировано **8 провайдеров**:
1. `mock` — ✅ SAFE, всегда доступен
2. `gemini-disabled` — 🔴 BLOCKED, требует APPROVE_SECRET_SETUP
3. `deepseek-disabled` — 🔴 BLOCKED, требует APPROVE_SECRET_SETUP
4. `local-disabled` — 🔴 BLOCKED, не реализован
5. `ollama-disabled` — 🔴 BLOCKED, не реализован
6. `custom-disabled` — 🔴 BLOCKED, требует adapter + approval
7. `mock-review` — ✅ SAFE, mock review через универсальный router
8. `deepseek-review-disabled` — 🔴 BLOCKED, требует APPROVE_SECRET_SETUP

---

## 6. Provider Router (Безопасный выбор)

Router — это gate перед любым провайдером:

| Условие | Результат |
|---------|-----------|
| provider_id = "mock" | ✅ Разрешён (SAFE) |
| provider_id = "gemini-disabled" | 🔴 BLOCKED |
| provider_id = "deepseek-disabled" | 🔴 BLOCKED |
| provider_id = "local-disabled" | 🔴 BLOCKED (не реализован) |
| provider_id = "unknown" | 🔴 BLOCKED (неизвестный) |
| provider требует secret, approval=False | 🔴 BLOCKED |
| provider требует network, mode=safe_local | 🔴 BLOCKED |

---

## 7. Secret Policy

У каждого провайдера есть secret_policy:

| Политика | Описание |
|----------|----------|
| `NO_SECRET_REQUIRED` | Не требует ключа (mock, local LLM) |
| `SECRET_REQUIRED` | Требует ключ (custom provider) |
| `SECRET_NOT_LOADED` | Ключ нужен, но не загружен |
| `APPROVAL_REQUIRED` | Требует approval gate |
| `BLOCKED_UNTIL_APPROVE_SECRET_SETUP` | Заблокирован до APPROVE_SECRET_SETUP |

---

## 8. Как добавить нового провайдера (без изменения ядра)

1. Создать файл `src/hermes_core/ai_provider/adapters/my_adapter.py`
2. Наследовать `BaseProviderAdapter`
3. Определить `metadata` (провайдер-нейтральные поля)
4. Реализовать `generate()`
5. Зарегистрировать в `registry.py` → `get_default_registry()`

```python
class MyNewAdapter(BaseProviderAdapter):
    @property
    def metadata(self) -> AIProviderMetadata:
        return AIProviderMetadata(
            provider_id="my-provider",
            provider_name="My Custom Provider",
            model_id="my-model",
            mode="my-mode",
            capabilities=(ProviderCapability.TEXT_GENERATION,),
            secret_policy=SecretPolicy.SECRET_REQUIRED,
            requires_secret=True,
            requires_network=True,
            approval_required="APPROVE_SECRET_SETUP",
            is_enabled=False,
            blocked_reason="Not ready yet.",
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse.blocked("Not implemented.", provider_id="my-provider")
```

**Никаких изменений в core, router, CLI, smoke, tests не требуется.**

---

## 9. CLI команды (новые, универсальные)

| Команда | Назначение |
|---------|-----------|
| `ai-provider-list` | Список всех провайдеров и их статус |
| `ai-provider-status [id]` | Статус конкретного провайдера |
| `ai-provider-mock` | Выбрать mock (явно) |
| `ai-provider-router [id]` | Проверить решение router'а |
| `ai-provider-capabilities` | Возможности всех провайдеров |
| `secret-gate` | Статус secret gate |
| `review-provider-mock` | Выбрать mock review |
| `review-provider-disabled` | Статус disabled review |
| `daily-assistant` | Ежедневный снимок проекта |
| `daily-brief` | Краткая сводка на один экран |
| `what-next` | Следующие шаги |
| `local-health` | Быстрая проверка здоровья |
| `project-status` | Быстрый статус проекта |
| `malyarka-mode-status` | AI-путь Malyarka (router vs direct) |

Старые команды (`ai-provider`, `review-provider`) сохранены для обратной совместимости.

---

## 10. Безопасность

- **`.env` не читается** — ни один adapter не читает .env
- **Ключи не хранятся** — registry не содержит ключей
- **API не вызываются** — все методы блокируют вызов до approval
- **Можно зарегистрировать нового провайдера без core-изменений**

---

## 11. Malyarka → AI Provider Router

Malyarka всегда обращается только к **AI Provider Router** через модуль `hermes_modules/malyarka/ai_review.py`, никогда напрямую к Gemini, DeepSeek или другому провайдеру.

```python
from hermes_modules.malyarka.ai_review import review_disputed_row

result = review_disputed_row("broken row without pipe")
# result.provider_id == "mock"
# result.safety["direct_gemini_call"] == False
# result.safety["direct_deepseek_call"] == False
```

Это гарантирует:
- Единая точка блокировки (Router)
- Замена провайдера без изменения Malyarka
- Безопасность: Router блокирует любые real вызовы
- Доказуемо: тесты проверяют отсутствие прямых импортов Gemini/DeepSeek
