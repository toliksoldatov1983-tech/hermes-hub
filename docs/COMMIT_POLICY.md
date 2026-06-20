# COMMIT POLICY — Правила Git для Hermes Hub

Дата: 2026-06-21
Статус: PLAN-ONLY. GitHub не настроен. Ждёт решения пользователя (D1).

---

## Главное правило

```
Git — для checkpoint и backup, не для хаотичного dump.
По умолчанию git не используется. Каждый commit — осознанное решение.
```

---

## 🚫 Что НЕЛЬЗЯ коммитить (никогда)

| Категория | Примеры | Причина |
|-----------|---------|---------|
| Секреты | `.env`, `config.py`, token, ключи | Утечка необратима |
| Базы данных | `orders.db`, `*.sqlite`, `*.db` | Клиентские данные |
| Логи | `*.log`, live logs | Приватность |
| Реальные заказы | Любые файлы с заказами клиентов | Клиентские данные |
| Временные файлы | `__pycache__/`, `.pytest_cache/`, `.venv/` | Мусор |
| Скриншоты | `*.png`, `*.jpg` | Не код |
| PDF / бинарные | `*.pdf`, `*.exe` | Не код |
| Obsidian vault | `.obsidian/` | Локальные настройки |

---

## ✅ Что МОЖНО коммитить

| Категория | Примеры |
|-----------|---------|
| State-файлы | `HERMES_HUB_STATE.md`, `sync/*.md` |
| Задачи | `tasks/*.md` |
| Handoff | `handoff/*.md` |
| Документация | `docs/*.md` |
| Мастер-карта | `PROJECT_MASTER_MAP_*.md` |
| Операционные доки | `WHAT_NEXT.md`, `TASK_QUEUE.md`, `REGRESSION_CHECKLIST.md` |
| Патчи | `patches/*.md` |
| Локальный код | `projects/malyarka-clean/**/*.py` (без secrets) |
| Тесты | `local_tests/**/*.py`, `tests/**/*.py` |
| Agent specs | `agents/**/*.md` |
| Правила | `rules/*.md` |

---

## 🔒 Когда можно commit

| Условие | Статус |
|---------|--------|
| Батч завершён и проверен | ✅ Можно |
| Все тесты пройдены | ✅ Можно |
| Regression checklist пройден | ✅ Можно |
| Rollback point зафиксирован | ✅ Можно |
| `git diff --staged` проверен — нет секретов | ✅ Можно |
| Пользователь дал approval `РАЗРЕШАЮ_GIT_COMMIT` | ✅ Можно |

---

## 🔒 Когда можно push

| Условие | Статус |
|---------|--------|
| Commit сделан и проверен | ✅ |
| Пользователь дал approval `РАЗРЕШАЮ_GIT_PUSH` | ✅ Можно |
| Remote настроен | [уточнить] |

---

## 📝 Как писать commit message

```
BATCH_NNN: краткое описание (до 72 символов)

- Что сделано.
- Какие файлы изменены.
- Результат проверки.

Rollback point: <sha или описание как откатить>
```

### Пример

```
BATCH_014: Implement Malyarka Clean parser + dispute + area

- size_parser.py: extract size rows from order text
- dispute_detector.py: separate confirmed/disputed rows
- area_calculator.py: calculate area for confirmed rows
- tests: 15 passed

Rollback point: git revert HEAD
```

---

## 🛑 Git-команды: что можно без approval

| Команда | Разрешено? |
|---------|-----------|
| `git status` | ✅ |
| `git diff` | ✅ |
| `git diff --staged` | ✅ |
| `git log` | ✅ |
| `git add *.md` | ✅ (если нет секретов) |

---

## 🔴 Git-команды: только с approval

| Команда | Approval |
|---------|----------|
| `git commit` | `РАЗРЕШАЮ_GIT_COMMIT` |
| `git push` | `РАЗРЕШАЮ_GIT_PUSH` |

---

## 🚫 Git-команды: никогда без backup

| Команда | Почему |
|---------|--------|
| `git reset --hard` | Потеря незакоммиченного |
| `git checkout -- .` | Потеря изменений |
| `git rebase` | Сложный откат |
| `git push --force` | Разрушение remote |

---

## 📦 Branches

```
main          — стабильный state (только проверенные батчи)
batches/NNN   — рабочая ветка для текущего батча
```

После завершения батча: `batches/NNN` → `main`.

---

## 🔄 Rollback point

Перед каждым commit:
1. Записать текущий SHA: `git rev-parse HEAD`.
2. Если commit ломает что-то: `git revert <sha>`.
3. Если revert невозможен: восстановить из `patches/PATCH_LOG.md`.

---

## 📋 Сводка

| Действие | Статус |
|----------|--------|
| Git использовать по умолчанию | ❌ Нет |
| Commit без approval | ❌ Нет |
| Push без approval | ❌ Нет |
| Commit после чистого батча + tests + checks | ✅ Да |
| Commit secrets / DB / logs / orders | ❌ Никогда |
| Git init / repo setup | [ждёт D1] |
