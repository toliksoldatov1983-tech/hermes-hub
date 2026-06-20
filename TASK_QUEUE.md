# TASK QUEUE — Единая очередь задач Hermes Hub

Дата: 2026-06-21
Обновлять: после каждого выполненного батча / решения.

---

## 🟢 Hermes NOW (markdown-only, безопасно)

| # | Задача | Файл | Статус |
|---|--------|------|--------|
| H1 | Regression checklist | `docs/REGRESSION_CHECKLIST.md` | ✅ done |
| H2 | WHAT_NEXT.md | `WHAT_NEXT.md` | ✅ done |
| H3 | TASK_QUEUE.md | `TASK_QUEUE.md` | ✅ done |
| H4 | SYNC_CHECKLIST | `docs/SYNC_CHECKLIST.md` | ✅ done |
| H5 | Telegram safe commands | `docs/TELEGRAM_SAFE_COMMANDS.md` | ✅ done |
| H6 | Telegram approval flow | `docs/TELEGRAM_APPROVAL_FLOW.md` | ✅ done |
| H7 | Health check дизайн | `docs/HEALTH_CHECK_DESIGN.md` | ✅ done |
| H8 | Commit policy | `docs/COMMIT_POLICY.md` | ✅ done |
| H9 | Obsidian long memory rules | `docs/OBSIDIAN_LONG_MEMORY_RULES.md` | ✅ done |
| H10 | Obsidian short memory rules | `docs/OBSIDIAN_SHORT_MEMORY_RULES.md` | ✅ done |

---

## ✅ Hermes NOW — ВСЕ ВЫПОЛНЕНЫ (10/10)

Следующий шаг: Codex-батчи или решение пользователя.

---

## 🔧 Codex BATCH LATER (код / сервер / тесты)

| # | Batch | Что делает | Статус |
|---|-------|-----------|--------|
| C1 | BATCH_014 | Malyarka Clean: parser + dispute + area | Ready |
| C2 | BATCH_015 | Agent implementation: Corel, Adapter, Memory, Diagnostics | Ready |
| C3 | BATCH_012 | Export regression tests (Corel Excel + Файл) | Ready |
| C4 | BATCH_016 | Read-only аудит старого архива | Ready |
| C5 | BATCH_011 | Telegram Hermes interface дизайн | Ready |
| C6 | BATCH_013 | GitHub repo setup | Needs D1 |
| C7 | BATCH_017 | Autostart enable plan | Needs D2 |
| C8 | BATCH_018 | Economy/pricing module plan | Needs D3 |
| C9 | BATCH_010 | Phase 2 dry-run retry | 🚫 Blocked |

---

## 👤 USER DECISION (ждём ответа)

| # | Вопрос | Статус |
|---|--------|--------|
| D1 | Нужен ли GitHub? | ⬜ ждёт |
| D2 | Autostart или ручной controlled start? | ⬜ ждёт |
| D3 | Нужна ли экономика сейчас? | ⬜ ждёт |
| D4 | Альтернатива для Vision? | ⬜ ждёт |

---

## 🚫 BLOCKED

| # | Что | Блокер | Статус |
|---|-----|--------|--------|
| B1 | Phase 2 dry-run | Adapter перехватывает order-like | 🚫 |
| B2 | Production enable | Phase 2 не готов | 🚫 |
| B3 | Autostart enable | Ждёт D2 | 🚫 |
| B4 | Vision API | Нет альтернативы | 🚫 |

---

## 🔵 LATER (не сейчас)

| # | Что | Когда |
|---|-----|-------|
| L1 | Materials / colors / coatings | После core |
| L2 | Milling / ArtCAM / CNC | После production |
| L3 | Warehouse | После экономики |
| L4 | 1С integration | Далеко |
| L5 | Vision alternative | После решения пользователя |

---

## 📋 Правила очереди

1. Одна задача in_progress одновременно.
2. После завершения → обновить статус + WORKLOG.
3. Codex-батчи исполняются только с approval пользователя.
4. Blocked-задачи не начинать без снятия блокера.
