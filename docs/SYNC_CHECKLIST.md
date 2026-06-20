# SYNC CHECKLIST — Как не потерять синхронизацию

Дата: 2026-06-21
Использовать: после каждого батча / важного решения.

---

## 📡 Что обновлять после каждого батча

| Файл | Что писать | Пример |
|------|-----------|--------|
| `HERMES_HUB_STATE.md` | Новый статус, новые файлы, изменения runtime | `BATCH_NNN: implemented X` |
| `tasks/NEXT_TASKS.md` | Обновлённый список задач | Убрать сделанное, добавить следующее |
| `logs/WORKLOG.md` | Запись: дата, что сделано, результат, след. шаг | `2026-06-21 — BATCH_NNN — done — next: ...` |
| `handoff/REPORT_TO_CHATGPT.md` | После серии батчей: сводка для ChatGPT | Что сделано, что дальше |
| `patches/LATEST_STATE_PATCH.md` | Какие файлы изменены, что нового | Список изменённых файлов |
| `patches/PATCH_LOG.md` | Запись в лог патчей | `BATCH_NNN: applied, files: ...` |

---

## 🧭 Где source of truth

| Что | Где | Приоритет |
|-----|-----|-----------|
| **Текущий state проекта** | `HERMES_HUB_STATE.md` | 🥇 Главный |
| **Runtime (сервер, бот, флаги)** | `sync/SHARED_CURRENT_STATUS.md` | 🥇 Главный |
| **Задачи** | `tasks/NEXT_TASKS.md` + `TASK_QUEUE.md` | 🥇 Главный |
| **Мастер-карта** | `PROJECT_MASTER_MAP_MALYARKA_HERMES.md` | 🥇 Главный |
| **Решения** | `decisions/DECISIONS.md` | 🥇 Главный |
| **Worklog** | `logs/WORKLOG.md` | 🥇 Главный |

**Правило:** Hermes Hub — единственный источник правды.

---

## 🚫 Что НЕ дублировать в Obsidian

| Не дублировать | Почему | Где должно быть |
|---------------|--------|-----------------|
| Текущий state проекта | Противоречия | `HERMES_HUB_STATE.md` |
| Runtime статус (сервер, бот) | Устаревает быстро | `sync/SHARED_CURRENT_STATUS.md` |
| Список задач | Расходится с Hub | `tasks/NEXT_TASKS.md` |
| Approval gates | Должны быть в одном месте | `sync/APPROVAL_GATES.md` |
| Блокеры | Расходятся | `sync/BLOCKERS.md` |
| Worklog | Дублирование | `logs/WORKLOG.md` |

**Obsidian — для знаний, заметок, шаблонов. Не для state.**

---

## 🔍 Как проверять противоречия (еженедельно)

| # | Проверка | Как |
|---|---------|-----|
| 1 | State vs Runtime | Сравнить `HERMES_HUB_STATE.md` с `SHARED_CURRENT_STATUS.md` |
| 2 | Hub vs Obsidian | Presence-only: есть ли факты в Obsidian, которых нет в Hub |
| 3 | Задачи vs Блокеры | `TASK_QUEUE.md`: нет ли задач с активными блокерами |
| 4 | Deprecated | Не ссылается ли кто-то на устаревшие файлы |
| 5 | Решения | Все ли решения за неделю записаны в `DECISIONS.md` |

---

## 🔄 Порядок после каждого батча

1. Обновить `HERMES_HUB_STATE.md`.
2. Обновить `tasks/NEXT_TASKS.md`.
3. Записать в `logs/WORKLOG.md`.
4. Записать в `patches/PATCH_LOG.md`.
5. Обновить `patches/LATEST_STATE_PATCH.md`.
6. Обновить `handoff/REPORT_TO_CHATGPT.md` (если серия батчей).
7. Запустить `Update-ChatGPTContextBundle.ps1` (если есть Codex).
8. Обновить `WHAT_NEXT.md`.

---

## 🟢 Что обновляется само (Hermes следит)

| Файл | Триггер |
|------|---------|
| `WHAT_NEXT.md` | После каждого шага |
| `TASK_QUEUE.md` | После каждого шага |
| `sync/BLOCKERS.md` | При появлении/снятии блокера |
| `sync/DONE_LOG.md` | После каждого батча |
