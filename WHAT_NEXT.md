# WHAT NEXT — Операционный пульт Hermes Hub

Дата: 2026-06-21
Обновлять: после каждого завершённого шага.

---

## 🔴 Сейчас (ближайшие 3)

| # | Задача | Файл | Статус |
|---|--------|------|--------|
| 1 | Regression checklist | `docs/REGRESSION_CHECKLIST.md` | ✅ done |
| 2 | WHAT_NEXT.md | `WHAT_NEXT.md` | ✅ done |
| 3 | TASK_QUEUE | `TASK_QUEUE.md` | ✅ done |
| 4 | SYNC_CHECKLIST | `docs/SYNC_CHECKLIST.md` | ✅ done |
| 5 | Telegram safe commands | `docs/TELEGRAM_SAFE_COMMANDS.md` | ✅ done |
| 6 | Telegram approval flow | `docs/TELEGRAM_APPROVAL_FLOW.md` | ✅ done |
| 7 | Health check дизайн | `docs/HEALTH_CHECK_DESIGN.md` | ✅ done |
| 8 | Commit policy | `docs/COMMIT_POLICY.md` | ✅ done |
| 9 | Obsidian long memory rules | `docs/OBSIDIAN_LONG_MEMORY_RULES.md` | ✅ done |
| 10 | Obsidian short memory rules | `docs/OBSIDIAN_SHORT_MEMORY_RULES.md` | ✅ done |

---

## ✅ Все 10 операционных документов готовы

Следующий шаг — выбор пользователя:
- **GitHub** — создать repo и первый checkpoint
- **Autostart** — решить: включить или оставить ручной
- **Phase 2 retry** — план повторного dry-run

После закрытия этих трёх → **Vision**: выбрать альтернативу или оставить заблокированным.

---

## 🟢 Hermes может сам (markdown-only)

| # | Задача | Файл |
|---|--------|------|
| 4 | Telegram safe commands | `docs/TELEGRAM_SAFE_COMMANDS.md` |
| 5 | Telegram approval flow | `docs/TELEGRAM_APPROVAL_FLOW.md` |
| 6 | Health check дизайн | `docs/HEALTH_CHECK_DESIGN.md` |
| 7 | Commit policy | `docs/COMMIT_POLICY.md` |
| 8 | Obsidian long memory rules | `docs/OBSIDIAN_LONG_MEMORY_RULES.md` |
| 9 | Obsidian short memory rules | `docs/OBSIDIAN_SHORT_MEMORY_RULES.md` |

---

## 🔧 Копить для Codex (батчи)

| # | Batch | Готовность |
|---|-------|-----------|
| C1 | BATCH_014: Malyarka Clean Core (parser + dispute + area) | Ready |
| C2 | BATCH_015: Agent Implementation (4 agents) | Ready |
| C3 | BATCH_012: Export Regression Tests | Ready |
| C4 | BATCH_016: Old Archive Review | Ready |
| C5 | BATCH_010: Phase 2 Dry-Run Retry | Blocked |
| C6 | BATCH_013: GitHub Setup | Needs user decision |

---

## 👤 Решения от пользователя

| # | Вопрос |
|---|--------|
| D1 | Нужен ли GitHub? |
| D2 | Autostart или ручной controlled start? |
| D3 | Нужна ли экономика сейчас? |
| D4 | Альтернатива для Vision? |

---

## 🚫 Blocked

| Блокер | Что блокирует |
|--------|--------------|
| Phase 2 dry-run fail | BATCH_010, все Telegram-режимы |
| Нет GitHub решения | BATCH_013 |
| Нет autostart решения | BATCH_017 |

---

## 📋 Как пользоваться

1. Открыть Hermes.
2. Спросить: «Что дальше?» → Hermes читает этот файл.
3. Выбрать задачу → Hermes делает или готовит Codex-пакет.
4. После выполнения → обновить этот файл.
