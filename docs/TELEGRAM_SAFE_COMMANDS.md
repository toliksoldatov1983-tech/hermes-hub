# TELEGRAM SAFE COMMANDS — Безопасные команды для Hermes-режима

Дата: 2026-06-21
Статус: PLAN-ONLY. Не реализовано. Ждёт Phase 2.
Применение: будущий Telegram-интерфейс Hermes Hub.

---

## Принцип

Все команды делятся на 4 уровня. Ни одна команда не выполняет опасное действие без approval.
**Правило:** лучше stop, чем риск.

---

## 🟢 READ-ONLY — Безопасно всегда

Эти команды только читают state, не меняют ничего.

| Команда | Что делает | Откуда берёт данные |
|---------|-----------|-------------------|
| `/status` | Текущий статус проекта | `HERMES_HUB_STATE.md` |
| `/bot` | Статус бота: работает/нет, флаги | `sync/SHARED_CURRENT_STATUS.md` |
| `/next` | Что делать дальше (top-3) | `WHAT_NEXT.md` |
| `/tasks` | Список текущих задач | `TASK_QUEUE.md` |
| `/blockers` | Открытые блокеры | `sync/BLOCKERS.md` |
| `/report` | Последний отчёт о работе | `handoff/REPORT_TO_CHATGPT.md` (кратко) |
| `/regression` | Regression checklist (без выполнения) | `docs/REGRESSION_CHECKLIST.md` |
| `/sync` | Статус синхронизации state | `docs/SYNC_CHECKLIST.md` (проверка) |
| `/health` | Health check (read-only) | `docs/HEALTH_CHECK_DESIGN.md` |

---

## 🟡 PLAN-ONLY — Только планы, без исполнения

Эти команды создают планы, но ничего не меняют на сервере.

| Команда | Что делает |
|---------|-----------|
| `/plan batch <название>` | Подготовить Codex batch-пакет |
| `/plan next` | Предложить следующий безопасный шаг |
| `/plan review` | Проверить мастер-карту на устаревшее |

---

## 🔴 APPROVAL-REQUIRED — Требует точной approval-фразы

Эти команды предлагают действие, но НЕ выполняют без approval.

| Команда | Что предлагает | Approval |
|---------|---------------|----------|
| `/approve start` | Запросить controlled start бота | `APPROVE_SERVER_BOT_CONTROLLED_START_ONCE` |
| `/approve restart` | Запросить controlled restart | `APPROVE_CONTROLLED_RESTART_ONCE` |
| `/approve phase2` | Запросить Phase 2 dry-run | `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE` |
| `/approve patch` | Запросить live patch | `APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE` |
| `/approve production` | Запросить production enable | `APPROVE_PRODUCTION_ENABLE` |
| `/approve autostart` | Запросить autostart enable | `APPROVE_ENABLE_AUTOSTART` |
| `/approve git push` | Запросить git push | `РАЗРЕШАЮ_GIT_PUSH` |

**Важно:** команда `/approve ...` только **предлагает** действие. Реальное выполнение — только после того, как пользователь пришлёт точную approval-фразу.

---

## 🚫 FORBIDDEN — Никогда через Telegram

| Действие | Причина |
|----------|---------|
| Чтение `.env` / token / `config.py` | Секреты |
| Чтение `orders.db` | Клиентские данные |
| Чтение live logs | Приватность |
| Чтение реальных заказов | Клиентские данные |
| Включение Vision API | Внешний сервис |
| Включение AI API | Внешний сервис |
| `git push` без approval | Утечка секретов |
| `systemctl stop` без approval | Остановка бота |

---

## 📋 Сводка по уровням

| Уровень | Команд | Риск | Пример |
|---------|--------|------|--------|
| 🟢 READ-ONLY | 9 | Нулевой | `/status`, `/next`, `/tasks` |
| 🟡 PLAN-ONLY | 3 | Нулевой | `/plan batch` |
| 🔴 APPROVAL | 7 | Высокий (только с фразой) | `/approve phase2` |
| 🚫 FORBIDDEN | 8 | Недопустимый | Чтение .env |

---

## Правила для Hermes в Telegram-режиме

1. **Read-only first.** Сначала `/status`, потом решение.
2. **Ничего не выполнять без approval.** Даже если кажется безопасным.
3. **Сомневаешься → stop.** Лучше спросить пользователя.
4. **Одна approval-фраза = одно действие.** Не выполнять цепочку по одной фразе.
5. **После approval-действия → regression check.**
