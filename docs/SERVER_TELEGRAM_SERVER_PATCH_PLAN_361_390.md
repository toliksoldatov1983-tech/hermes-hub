# Server Patch Plan (PLAN ONLY)

Technical name: `BUNDLE_361_390_SERVER_PATCH_PLAN_ONLY`
Date: 2026-06-17
Type: PLAN_ONLY / AUTO_MARKDOWN
Based on: BUNDLE_331_360 Readiness Gate (PARTIALLY READY)

## Status

Это markdown-only проектный план. Никакие server действия не выполняются. Никакой код не пишется. Никакой diff не готовится.

---

## 1. Что такое Server Patch в контексте Hermes Hub

**Цель:** Безопасно подключить существующий серверный Telegram-бот к Hermes Hub через adapter layer.

**Суть patch:** Добавить на сервер минимальный код, который:
1. Создаёт `malyarka_telegram/hermes_call_site.py` — tiny guarded call-site (новый файл)
2. Добавляет **одну строку** в `malyarka_telegram/handlers.py` — вызов call-site
3. Не меняет остальную логику бота
4. Off by default, dry-run only, feature-flag gated
5. При любых проблемах — fallback к существующему поведению

### Что НЕ делает patch

- Не меняет `app.py` (entry point, polling)
- Не меняет `router.py` (маршрутизация)
- Не меняет `config.py` (содержит token — запрещено читать)
- Не меняет `services/orders.py` (ядро заказов)
- Не читает token / .env / secrets
- Не запускает/останавливает бот
- Не меняет polling/webhook

---

## 2. Целевые файлы на сервере

По данным presence-only inventory (231C-234C):

### Создать (новый файл)

| Файл | Назначение |
|---|---|
| `/opt/malyarka-telegram-bot/malyarka_telegram/hermes_call_site.py` | Tiny guarded call-site |

Содержание (проект, не реальный код):
- `hermes_call_site(message, safe_context)` — асинхронная функция
- Проверка feature flags (`HERMES_TELEGRAM_INSERTION_ENABLED`)
- Формирование request для adapter skeleton
- Вызов `process_request()`
- Возврат `AdapterResult(fallback_required, response)`
- ~30 строк

### Изменить (существующий файл)

| Файл | Изменение | Строк |
|---|---|---|
| `/opt/malyarka-telegram-bot/malyarka_telegram/handlers.py` | Добавить import + 1 строка вызова в начало handler-функции | +3 |

**Важно:** содержимое `handlers.py` неизвестно. Перед внесением изменений необходимо:
1. Получить safe read-only копию `handlers.py` (с разрешением пользователя)
2. Найти точную handler-функцию для вставки
3. Идентифицировать точную строку для вставки
4. Подготовить patch с контекстом ±3 строки

### Не трогать

| Файл | Причина |
|---|---|
| `app.py` | Entry point, polling — высокий риск |
| `router.py` | Маршрутизация — высокий риск |
| `config.py` | **Token/secrets — КРИТИЧЕСКИЙ ЗАПРЕТ** |
| `services/orders.py` | Ядро заказов |
| `.env` | Secrets |
| `keyboards.py`, `messages.py`, `access.py` и др. | Не нужны для call-site |

---

## 3. Pre-Patch Requirements (blockers из BUNDLE_331_360)

Перед любыми server действиями необходимо:

| # | Requirement | Статус | Кто решает |
|---|------------|--------|------------|
| 1 | SSH write-доступ подтверждён | ❌ | Пользователь |
| 2 | Safe read-only копия `handlers.py` получена | ❌ | Пользователь + Codex |
| 3 | Точная handler-функция идентифицирована | ❌ | После чтения handlers.py |
| 4 | Feature-flags инфраструктура проверена | ❌ | После чтения config.py (safe parts) |
| 5 | Backup процедура документирована | ❌ | Пользователь |
| 6 | Staging environment (или dry-run план) | ❌ | Архитектурное решение |
| 7 | Bot runtime state известен | ❌ | Пользователь |
| 8 | Rollback протестирован локально | ❌ | Codex (локально) |

---

## 4. Этапы Server Patch (проектный план)

### Этап 0 — Подготовка (этот bundle: 361-390)

- [x] Server patch plan создан (этот документ)
- [ ] Утверждение плана пользователем
- [ ] Решение о staging vs production-first подходе

### Этап 1 — Server Readiness (будущие bundle 391-420)

**STOP_REVIEW gate** — только после разрешения пользователя:

1. Подтвердить SSH write-доступ
2. Получить safe read-only копию `handlers.py`
3. Идентифицировать точную handler-функцию
4. Проверить feature-flags инфраструктуру
5. Документировать backup процедуру
6. Создать dry-run план

### Этап 2 — Diff Preparation (будущие bundle 421-450)

**STOP_REVIEW gate** — только после readiness:

1. Написать `hermes_call_site.py` (на основе skeleton из 271-300 + call-site plan 301-330)
2. Подготовить diff для `handlers.py` (добавление 3 строк)
3. Проверить diff локально (на safe копии handlers.py)
4. Убедиться: diff не затрагивает config.py, token, secrets
5. Подготовить rollback diff (обратный patch)

### Этап 3 — Dry-Run (будущие bundle 451-480)

**STOP_APPROVAL gate** — только после утверждения diff:

1. Применить patch на сервере в dry-run режиме (feature flags все false)
2. Проверить: бот продолжает работать
3. Проверить: call-site возвращает fallback
4. Проверить: логи чистые, без ошибок
5. Если сухо — откатить и доложить

### Этап 4 — Activation (будущие bundle 481-510+)

**STOP_APPROVAL gate** — финальное разрешение:

1. Применить patch
2. Включить feature flags поэтапно:
   - `HERMES_TELEGRAM_INSERTION_ENABLED=true`
   - `HERMES_ADAPTER_ENABLED=true`
   - Остальные safe defaults остаются
3. Мониторить логи 24 часа
4. При проблемах — rollback (флаги в false)

---

## 5. Feature Flags для Server-Side

Флаги, которые должны быть на сервере:

```python
# Все по умолчанию FALSE/SAFE
HERMES_ADAPTER_ENABLED = False
HERMES_SERVER_ADAPTER_ENABLED = False
HERMES_TELEGRAM_INSERTION_ENABLED = False
HERMES_SAFE_MODE = True
HERMES_DRY_RUN_ONLY = True
HERMES_EXPORT_CALLBACKS_ENABLED = False
HERMES_ADMIN_CHANGES_ENABLED = False
```

**Проблема:** неизвестно, где и как серверный бот хранит конфигурацию. `config.py` содержит token — читать нельзя. Нужно:
- Либо отдельный `hermes_flags.py` (новый файл, без secrets)
- Либо переменные окружения (добавить в `.env` — тоже secrets)

**Рекомендация:** создать отдельный `malyarka_telegram/hermes_flags.py` с безопасными значениями по умолчанию.

---

## 6. Rollback Plan

### Мгновенный rollback (без перезапуска бота)

```python
# В hermes_flags.py или эквиваленте:
HERMES_TELEGRAM_INSERTION_ENABLED = False
HERMES_ADAPTER_ENABLED = False
```

Call-site читает флаги при каждом вызове → мгновенный эффект.

### Полный rollback (если нужно убрать код)

1. Убрать строку вызова из `handlers.py`
2. Удалить `hermes_call_site.py`
3. Удалить `hermes_flags.py` (опционально)
4. Перезапустить бота (если требуется)

### Что rollback НЕ делает

- Не удаляет существующие файлы бота
- Не меняет `app.py`, `router.py`, `config.py`
- Не трогает базу данных, заказы, логи
- Не требует чтения secrets

---

## 7. Риски и Mitigation

| Риск | Mitigation |
|------|-----------|
| config.py leak | `hermes_flags.py` — отдельный файл без secrets |
| Бот падает при patch | Dry-run + мониторинг + мгновенный rollback |
| Неизвестная структура handlers.py | Read-only копия перед patch |
| Нет staging | Dry-run на production с флагами false |
| SSH нестабилен | Подготовить offline-пакет для ручной установки |
| Нарушение безопасности | Все флаги false по умолчанию, side_effects=[], fallback required |

---

## 8. Что остаётся запрещённым (на всех этапах)

- ❌ Чтение `config.py` contents
- ❌ Чтение token / `.env` / `os.environ`
- ❌ Чтение database / log / order contents
- ❌ Изменение `app.py`, `router.py`, `services/orders.py`
- ❌ Запуск/остановка polling/webhook
- ❌ Telegram API calls из adapter
- ❌ Обработка реальных заказов через adapter
- ❌ Commit/push без отдельного разрешения

---

## 9. Следующий шаг

```text
BUNDLE_391_420_SERVER_PATCH_PREPARE_DIFF_ONLY
Autonomy: STOP_REVIEW
```

Требуется решение пользователя — готовить ли diff на основе этого плана.

---

## Источники

- `REPORT_BUNDLE_331_360_SERVER_PATCH_READINESS_GATE.md`
- `SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`
- `SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `SERVER_TELEGRAM_TINY_GUARDED_CALLSITE_PLAN_301_330.md`
- `server_adapter_skeleton.py` (BUNDLE_271_300)
- `SAFETY_RULES.md`
- `MANIFEST.md`
