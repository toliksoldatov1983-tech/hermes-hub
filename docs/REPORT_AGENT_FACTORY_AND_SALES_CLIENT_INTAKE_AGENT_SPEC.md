# REPORT — Agent Factory & Sales + Client Intake Agent Spec

Date: 2026-06-17
Executed by: Hermes (deepseek-v4-pro)
Branch: Non-server — Agent Factory spec

---

## 1. Что сделано

Создана система спецификации суб-агентов Hermes Hub и первый агент: **Sales + Client Intake Agent**.

### Agent Factory

| Файл | Назначение |
|---|---|
| `agents/AGENT_FACTORY_RULES.md` | Правила фабрики: создание, статусы, цепочка, запреты |
| `agents/AGENT_REGISTRY.md` | Реестр всех агентов (сейчас 1, запланировано 6) |

### Sales + Client Intake Agent (proposed)

| Файл | Содержание |
|---|---|
| `AGENT_SPEC.md` | Полная спецификация: роль, цель, логика, вход/выход, статусы |
| `QUESTIONS.md` | 11 вопросов в 6 блоках, порядок, что не спрашивать |
| `INTAKE_CARD_TEMPLATE.md` | YAML-шаблон карточки + пример заполнения |
| `RESPONSE_TEMPLATES.md` | 8 шаблонов: приветствие, запросы, карточка, handoff, блокировка |
| `SAFETY_RULES.md` | 10 абсолютных запретов + границы компетенции + режимы test/live |
| `HANDOFF_TO_MALYARKA.md` | Когда/как передать Intake Card → Malyarka Agent |

---

## 2. Архитектура агентов

```text
Клиент → Sales + Client Intake Agent → Malyarka Agent → Corel Export Agent
              ↓ (Intake Card)            ↓ (Order Result)   ↓ (.cdr)
         Структурирование             Расчёт площади       Файл для CNC
```

---

## 3. Статусы агента

| Статус | Применение |
|--------|-----------|
| `proposed` | Спецификация создана — **текущий** |
| `accepted` | Утверждена пользователем |
| `active` | Реализован и работает |
| `blocked` | Приостановлен |
| `archived` | Выведен |

---

## 4. Safety rules (ключевые)

- ❌ Не выдумывать цену
- ❌ Не обещать сроки
- ❌ Не принимать заказ в производство
- ❌ Не трогать сервер
- ❌ Не читать secrets
- ❌ Не писать клиенту без live-разрешения
- ❌ Не работать с реальными заказами без разрешения

---

## 5. Safety подтверждение

```
server_touched:     false
secrets_read:       false
telegram_api:       false
live_bot:           false
python_code:        false
commit_push:        false
```
Все действия: markdown-only.

---

## 6. Следующий шаг

1. Пользователь решает: `accepted` / `revise` / `rejected`
2. После `accepted`: реализация Python-модуля (отдельный проект)
3. После реализации: подключение к Telegram через безопасный adapter
4. После подключения: тестовый режим → live (с разрешением)

В реестр запланированы ещё 5 агентов (Malyarka, Corel Export, Telegram Safe, Memory, Diagnostics).

---

## 7. Revision 2026-06-17 — Safety Rules Softened

**Правило по материалам (#9):** с «запрещено давать советы» → «запрещены окончательные технические рекомендации». Разрешены уточняющие вопросы (материал есть? МДФ/шпон? фасады новые? покраска или изготовление?). Разрешены общие пояснения простыми словами.

**Правило по скидкам (#10):** с «запрещено обсуждать» → «запрещено обещать или назначать». Разрешено зафиксировать запрос клиента (`discount_request: true`) и ответить: «Итоговые условия подтвердит менеджер».

**Новые поля Intake Card:** `material_question`, `technical_advice_requested`, `discount_request`, `manager_review_required`.

**Эскалация:** добавлен механизм передачи сложных вопросов менеджеру с пометкой `manager_review_required`.

Статус агента: `proposed` (не менялся).
