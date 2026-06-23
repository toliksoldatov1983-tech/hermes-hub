# PROJECT MASTER MAP — MALYARKA / HERMES

Status: bootstrap map.
Date: 2026-06-21.

## Purpose

This file is the single project map for:

```text
Hermes Hub / Malyarka Clean / existing server Telegram bot
```

It separates:

- what is live now;
- what exists locally;
- what is archive-only;
- what is planned;
- what needs Codex;
- what Hermes can manage.

## Current Live State

```text
server bot: running
service: active/running
autostart: disabled
Hermes adapter feature flag: OFF
Phase 2: OFF
production: OFF
```

Live confirmed:

- `/start` answers.
- Order-like input `700 x 500` works in Malyarka flow.
- `Excel для Corel` works.
- `Файл Малярки` downloads.
- `Файл Малярки` has Russian headers/statuses.

## Active Project Roots

Hermes Desktop operating shell:

```text
E:\Hermes-General
```

Active project:

```text
E:\Hermes-Hub
```

Local clean Malyarka code:

```text
E:\Hermes-Hub\projects\malyarka-clean
```

Server bot staging/read-only copies:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
E:\Hermes-Hub\server_staging
```

## Main Blocks

### 1. Live Server Telegram Bot

Purpose:

- current working bot;
- accepts Telegram text;
- parses Malyarka orders;
- sends Corel Excel and Malyarka File.

Status:

```text
working, but Hermes adapter remains OFF
```

Do not:

- enable Phase 2;
- enable production;
- enable autostart;
- read secrets;
- change runtime without approval.

### 2. Malyarka Clean Local Core

Path:

```text
E:\Hermes-Hub\projects\malyarka-clean
```

Contains:

- size parser;
- area calculator;
- dispute detector;
- order result;
- Corel export model;
- Excel export;
- Telegram skeleton/readiness/config checks.

Status:

```text
local tested components, not fully merged into live server bot
```

### 3. Agents

Path:

```text
E:\Hermes-Hub\agents
```

Known agents:

- Sales + Client Intake Agent;
- Malyarka Agent;
- Corel Export Agent;
- Telegram Safe Adapter Agent;
- Memory Agent;
- Diagnostics Agent.

Status:

```text
local/spec/simulation layer, not live Telegram
```

### 4. Real Orders Sandbox

Path:

```text
E:\Hermes-Hub\real_orders_sandbox
```

Status:

```text
safe-copy review layer, closed gates 1-5A, not live order processing
```

Purpose:

- test real-like scenarios safely;
- preserve NCS raw values;
- classify disputed rows;
- prevent real order mutation.

### 5. Old Malyarka Archive

Status:

```text
archive-only / source of ideas
```

Rules:

- do not treat old rules/prices/materials as current truth;
- do not run old Telegram;
- do not read secrets/DB without approval;
- use only through separate read-only review.

### 6. GitHub

Status:

```text
not active in current workflow
```

Needs future decision:

- whether to reconnect repository workflow;
- branch/checkpoint strategy;
- what may be committed;
- approval phrase for commit/push.

### 7. Obsidian

Known:

- Hermes-General has short/long Obsidian memory.
- Server bot has Obsidian hooks/hints.

Status:

```text
present but not fully reconciled with Hermes Hub
```

Needs:

- read-only Obsidian workflow review;
- decide what should be saved;
- define memory rules for project facts vs drafts.

## Open Strategic Work

1. Reconcile Hermes-General with Hermes-Hub.
2. Maintain this master map.
3. Decide GitHub workflow.
4. Decide Obsidian memory workflow.
5. Stabilize export/callback context.
6. Prepare safe regression checks for live bot.
7. Plan next Hermes adapter Phase 2 only after approval.
8. Decide autostart/production later.
9. Review old Malyarka archive by blocks.
10. Convert selected local Malyarka Clean parts into live-safe future work.

## Level 1 — Inventory Sources (COMPLETED 2026-06-21)

Inventory executed: read-only scan of `E:\Hermes-Hub` and `E:\Hermes-General`.

### LIVE — Active state and runtime

**Hermes-Hub (мозг):**
- `HERMES_HUB_STATE.md` — главный state-файл проекта
- `sync/SHARED_CURRENT_STATUS.md` — сводка runtime (сервер, бот, флаги)
- `sync/APPROVAL_GATES.md` — реестр approval-фраз
- `sync/BLOCKERS.md` — открытые блокеры
- `sync/CHATGPT_DECISIONS.md` — решения ChatGPT
- `sync/CODEX_TO_HERMES.md` — Codex→Hermes
- `sync/HERMES_TO_CODEX.md` — Hermes→Codex
- `sync/MICRO_TASK_QUEUE.md` — микро-задачи
- `sync/NEXT_BATCH_QUEUE.md` — очередь батчей
- `sync/DONE_LOG.md` — лог сделанного
- `tasks/NEXT_TASKS.md` — следующие задачи
- `handoff/ACTIVE_BATCH.md` — активный батч
- `handoff/REPORT_TO_CHATGPT.md` — отчёт для ChatGPT
- `handoff/START_NEW_CHAT_PROMPT.md` — prompt для нового чата
- `handoff/CHATGPT_CONTEXT_BUNDLE.md` — полный контекст-бандл
- `handoff/HERMES_NAVIGATION_INDEX.md` — навигационный индекс
- `patches/LATEST_STATE_PATCH.md` — последний патч состояния
- `patches/PATCH_LOG.md` — лог всех патчей
- `logs/WORKLOG.md` — рабочий журнал
- `PROJECT_MASTER_MAP_MALYARKA_HERMES.md` — эта карта
- `PROJECT_HINTS.md` — подсказки
- `SAFETY_RULES.md` — правила безопасности
- `CLEANUP_RULES.md` — правила очистки

**Hermes-General (Desktop-оболочка):**
- `HERMES_CURRENT_STATUS.md` — статус Desktop
- `HERMES_OPERATING_SYSTEM.md` — правила работы Hermes
- `START_HERE_FOR_HERMES.md` — главный вход для Hermes
- `START_HERE_FOR_HERMES_HUB_MALYARKA.md` — мост к Hermes Hub
- `SYNC_PROTOCOL.md` — протокол синхронизации
- `MALYARKA_CURRENT_STATUS.md` — статус Малярки (помечен как исторический)
- `AGENTS.md` — standing rules для агентов
- `tasks/HERMES_NEXT_TASKS.md` — задачи Hermes
- `logs/HERMES_SHARED_WORKLOG.md` — общий worklog

### LOCAL — Код и компоненты (не на сервере)

**Hermes-Hub:**
- `projects/malyarka-clean/` — чистый локальный core Малярки:
  - `src/malyarka_clean_core/` — модули: order_input, size_parser, dispute_detector, area_calculator, corel_export_model, order_result (scaffold)
  - `src/malyarka_clean_telegram/` — Telegram-скелет
  - `tests/` — тесты
  - `tools/` — утилиты
- `local_tests/hermes_adapter_fake/` — fake adapter + 6 test files (166 passed)
- `local_tests/server_adapter_sandbox/` — серверный адаптер-песочница
- `tests/test_server_bot_read_only_collector.py` — read-only коллектор
- `server_staging/` — серверные копии кода:
  - `adapter_boundary_snapshot/` — telegram.py, hermes_adapter.py (read-only копии)
  - `adapter_boundary_fix_candidate/` — исправленные версии
  - `adapter_boundary_tests/` — test_order_like_fallback.py (10 passed)
  - `malyarka_file_russian_export_fix/` — malyarka_file.py + тест русских заголовков
- `inputs/server_bot_read_only_copy/` — read-only копия серверного бота
- `examples/` — CLEAN_ORDER.txt, DISPUTED_ORDER.txt, EMPTY_OR_INVALID_ORDER.txt, MIXED_SEPARATORS_ORDER.txt
- `outputs/` — COREL_EXPORT.xlsx, LAST_ORDER_RESULT.txt

**Hermes-General:**
- `app/` — hermes-dashboard, hooks, launcher, malyarka, memory-gateway, memory-hook, open-webui-data, review
- `obsidian-long-memory/` — 00_Profile … 10_Sessions
- `obsidian-short-memory/` — 00_Inbox, 01_Daily, 02_Ideas, 03_Tasks, 04_Drafts, 05_To_Process
- `projects/malyarka-future/` — MALYARKA_PROJECT_MAP.md, интеграционный план, аудит

### ARCHIVE — Историческое, не активное

**Hermes-Hub:**
- `_archive/` — архив проекта (пустой, только README)
- `_quarantine/` — карантин (пустой, только README)
- `_reports/` — старые отчёты (пусто)
- `_scratch/` — черновики (пусто)

**Hermes-General:**
- `backups/` — бэкапы hermes-desktop, openwebui, open-webui, openwebui-db
- `files/archive/` — файловый архив
- `tmp/` — скриншоты Hermes Desktop (3 PNG), PDF-извлечение хода проекта

### PLANS — Планы, документация, спецификации

**Hermes-Hub docs/ (~100+ файлов):**
- `AGENT_*` — acceptance criteria, ecosystem reports, handoff map, integration summary, routing rules
- `APPROVAL_GATE_REGISTRY.md`, `APPROVAL_TEMPLATES.md`
- `BATCH_WORKFLOW.md`, `BATCH_VS_MICRO_TASK_RULES.md`
- `CHATGPT_CHAT_ROLES.md`
- `CODEX_*` — sync protocol, prompts ready index, start here, task queue
- `COREL_EXCEL_PRODUCTION_EXPORT_PREPLAN.md`
- `DECISION_GATE_ROLLUP.md`, `DOCUMENTATION_INDEX.md`
- `EXISTING_TELEGRAM_BOT_SERVER_INVENTORY.md`
- `HERMES_ADAPTER_*` — 20+ файлов: Phase 2 dry-run, failure investigation, order-like fallback fix, live patch планы
- `HERMES_MASTER_MAP_LEVELS_AND_PROMPTS.md`
- `MALYARKA_FILE_*` — download fix, investigation, Russian export headers
- `SERVER_*` — SSH access, bot startup (7 файлов controlled start), adapter insertion design, inventory, post-start stabilization
- `FINAL_CHECKPOINT_*`, `FINAL_NO_ACCESS_WAITING_STATE.md`, `FULL_CHAIN_REGRESSION_DOCS.md`
- `decisions/DECISIONS.md`
- `progress/PROGRESS_CARD.md`
- `rules/HERMES_AUTOPILOT_WITH_APPROVAL_GATES.md`
- `rules/HERMES_RULE_CONVEYOR_001.md`

**Hermes-Hub handoff (батч-пакеты):**
- `BATCH_001` … `BATCH_005` — контекст, архитектура, scaffold, handoff, one-command workflow
- `BATCH_PACKET_TEMPLATE.md`, `TASK_PACKET_TEMPLATE.md`
- `PROMPT_TO_PASTE_IN_*.md` — prompt-шаблоны для ChatGPT/Codex/Hermes
- `REPORT_TO_CHATGPT_SERVER_ADAPTER_FINAL.md`
- `START_NEXT_*` — стартовые prompt-ы

**Hermes-Hub task_bundles:**
- `BUNDLE_255_270` … `BUNDLE_481_510` — 8 батч-бандлов adapter implementation

**Hermes-General:**
- `future-integrations/` — deepseek, github, malyarka, openai-codex, telegram (пустые заглушки)
- `config/INSTALL_PLAN.md`, `config/SAFETY_RULES.md`
- `MALYARKA_START_HERE_FOR_HERMES.md` — интеграционный план Малярки

### AGENTS — Спецификации агентов

**Hermes-Hub agents/:**
- `AGENT_FACTORY_RULES.md` — правила фабрики агентов
- `AGENT_REGISTRY.md` — реестр (6 агентов)
- `sales_client_intake_agent/` — AGENT_SPEC, ACCEPTANCE_CRITERIA, GOLDEN_CASES, HANDOFF_CONTRACT, INTAKE_CARD, SAFETY_RULES, TEST_SCENARIOS, src/
- `malyarka_agent/` — AGENT_SPEC, ACCEPTANCE_CRITERIA, INTAKE_CONTRACT, OUTPUT_CONTRACT, GOLDEN_CASES, SAFETY_RULES, TEST_SCENARIOS, src/, tests/, demo/
- `corel_export_agent/` — AGENT_SPEC, ACCEPTANCE_CRITERIA, EXPORT_CONTRACT, TEST_SCENARIOS, src/, tests/, dry_run/
- `telegram_safe_adapter_agent/` — AGENT_SPEC, ADAPTER_CONTRACT, SAFETY_RULES, BLOCK_REASONS, FAILURE_MATRIX, HANDOFF_RULES, SCENARIOS
- `memory_agent/` — AGENT_SPEC, SAFETY_RULES, READ_WORKFLOW, WRITE_WORKFLOW, MEMORY_SNAPSHOT
- `diagnostics_agent/` — AGENT_SPEC, SAFE_REPORT_TEMPLATE, SAFE_STATUS_REPORT, WORKFLOW
- `local_simulation/` — full_chain_sales_malyarka_corel, sales_to_malyarka

**Hermes-General agents/:**
- `hermes-general/`, `hermes-local/`, `hermes-memorykeeper/`, `hermes-orchestrator/` — SYSTEM_PROMPT.md каждый
- `hermes-orders-future/` — README.md (заглушка)

### SANDBOX — Песочница для безопасного тестирования

**Hermes-Hub:**
- `real_orders_sandbox/` — safe-copy review layer (gates 1-5A закрыты):
  - `DO_NOT_READ_REAL_ORDER_FOLDERS.md`, `SAFE_COPY_RULES.md`
  - `input_safe_copies/`, `output_results/`, `review_reports/`
  - `PROCESSING_PLAN.md`, `REVIEW_CHECKLIST.md`

### TOOLS — Инструменты и скрипты

**Hermes-Hub:**
- `tools/Update-ChatGPTContextBundle.ps1` — генератор контекст-бандла
- `tools/Update-ChatGPTContextBundle.cmd` — лаунчер
- `tools/server_bot/collect_server_bot_read_only.py` — read-only коллектор сервера
- `*.cmd` лаунчеры: ВВЕСТИ_ЗАКАЗ_ВРУЧНУЮ, ЗАПУСТИТЬ_ЗАКАЗ, ЗАПУСТИТЬ_ТЕСТЫ_ЯДРА, СОЗДАТЬ_EXCEL_ДЛЯ_COREL, ПРОВЕРИТЬ_ПРИМЕР_*

**Hermes-General:**
- `installers/Hermes-Setup-official-nousresearch.exe` (7.6 MB)
- `app/Save-HermesMemory.bat`, `app/Start-Hermes.bat`

### UNKNOWN / NEEDS REVIEW

- `E:\Hermes-Hub\docs\` — 100+ файлов: часть может быть устаревшей после батчей 2026-06-20. Нужен review на дубликаты и противоречия.
- `E:\Hermes-Hub\task_bundles\` — 8 бандлов adapter implementation. Статус выполнения неясен без чтения содержимого.
- `E:\Hermes-General\MALYARKA_CURRENT_STATUS.md` — помечен как исторический, но всё ещё в корне. Решить: перенести в архив или удалить.
- `E:\Hermes-General\future-integrations\` — все 5 папок пусты. Заглушки или забытый план?
- `E:\Hermes-General\github\`, `repos\` — пусты. GitHub workflow не активирован.
- `E:\Hermes-General\notes\`, `docs\`, `handoff\`, `inputs\`, `patches\`, `server_staging\`, `shared_contracts\`, `sync\`, `templates\` — все пусты. Структура создана, но не заполнена.
- `E:\Hermes-General\agents\hermes-orders-future\` — только README, без SYSTEM_PROMPT.

### Что выглядит устаревшим

1. **Hermes-General/MALYARKA_CURRENT_STATUS.md** (12 июн) — источник истины теперь Hermes-Hub.
2. **Hermes-General/logs/CODEX_AUDIT_2026-06-12.md** — аудит 9-дневной давности.
3. **Hermes-General/logs/MALYARKA_GIT_DIFF_REVIEW_2026-06-12.md** — git diff review той же давности.
4. **Hermes-Hub/docs/** — множество AGENT_* и CODEX_* файлов от 12-17 июня с пометкой «Codex not available», которые могли устареть.
5. **Hermes-Hub/handoff/CODEX_HANDOFF_PROMPT_READY.md** — помечен 18 июн, статус «Codex not available» — [уточнить].
6. **Hermes-Hub/handoff/FINAL_NO_ACCESS_WAITING_STATE.md** (ссылка из доков) — [уточнить] актуален ли.

## Level 2 — Separate Live / Local / Archive / Plans (COMPLETED 2026-06-21)

Статусы: 🟢 LIVE · 🟡 LOCAL · ⬜ ARCHIVE · 📋 PLANS · 🔍 NEEDS REVIEW · ❌ DEPRECATED

---

### 🟢 LIVE — Актуально сейчас, источник правды

**Единый источник правды — Hermes-Hub.** Hermes-General используется только как Desktop-оболочка.

| Файл | Роль |
|---|---|
| `HERMES_HUB_STATE.md` | Главный state-файл всего проекта |
| `PROJECT_MASTER_MAP_MALYARKA_HERMES.md` | Эта карта |
| `PROJECT_HINTS.md` | Подсказки для Hermes |
| `SAFETY_RULES.md` | Правила безопасности |
| `CLEANUP_RULES.md` | Правила очистки |
| `sync/SHARED_CURRENT_STATUS.md` | Runtime-сводка: сервер, бот, флаги |
| `sync/APPROVAL_GATES.md` | Реестр approval-фраз |
| `sync/BLOCKERS.md` | Открытые блокеры |
| `sync/CHATGPT_DECISIONS.md` | Решения, принятые через ChatGPT |
| `sync/CODEX_TO_HERMES.md` | Handoff Codex → Hermes |
| `sync/HERMES_TO_CODEX.md` | Handoff Hermes → Codex |
| `sync/MICRO_TASK_QUEUE.md` | Очередь микро-задач |
| `sync/NEXT_BATCH_QUEUE.md` | Очередь батчей |
| `sync/DONE_LOG.md` | Лог завершённого |
| `tasks/NEXT_TASKS.md` | Следующие задачи |
| `handoff/ACTIVE_BATCH.md` | Активный батч |
| `handoff/REPORT_TO_CHATGPT.md` | Отчёт для ChatGPT |
| `handoff/START_NEW_CHAT_PROMPT.md` | Prompt для нового чата |
| `handoff/CHATGPT_CONTEXT_BUNDLE.md` | Полный контекст-бандл |
| `handoff/HERMES_NAVIGATION_INDEX.md` | Навигационный индекс |
| `patches/LATEST_STATE_PATCH.md` | Последний патч состояния |
| `patches/PATCH_LOG.md` | Лог патчей |
| `logs/WORKLOG.md` | Рабочий журнал |

**Hermes-General (только Desktop OS):**

| Файл | Роль |
|---|---|
| `HERMES_OPERATING_SYSTEM.md` | Правила работы Hermes Desktop |
| `START_HERE_FOR_HERMES.md` | Главный вход для Hermes |
| `START_HERE_FOR_HERMES_HUB_MALYARKA.md` | Мост к Hermes Hub |
| `SYNC_PROTOCOL.md` | Протокол синхронизации |
| `HERMES_CURRENT_STATUS.md` | Статус Desktop-оболочки |
| `AGENTS.md` | Standing rules для агентов |
| `tasks/HERMES_NEXT_TASKS.md` | Задачи Hermes Desktop |
| `logs/HERMES_SHARED_WORKLOG.md` | Общий worklog |

**Итого LIVE:** 22 файла Hermes-Hub + 8 файлов Hermes-General = **30 файлов.**

---

### 🟡 LOCAL — Рабочие локальные компоненты (код, тесты, данные)

**Hermes-Hub:**

| Компонент | Что внутри |
|---|---|
| `projects/malyarka-clean/` | Чистый локальный core: order_input, size_parser, dispute_detector, area_calculator, corel_export_model, order_result (scaffold), Telegram-скелет, тесты |
| `local_tests/hermes_adapter_fake/` | Fake adapter + 6 test-файлов (166 passed) |
| `local_tests/server_adapter_sandbox/` | Серверный адаптер-песочница |
| `tests/test_server_bot_read_only_collector.py` | Read-only коллектор сервера |
| `server_staging/` | Рабочие копии серверного кода: snapshot, fix-candidate, тесты, Russian export fix |
| `inputs/server_bot_read_only_copy/` | Read-only копия серверного бота |
| `examples/` | Тестовые примеры заказов |
| `outputs/` | Результаты: COREL_EXPORT.xlsx, LAST_ORDER_RESULT.txt |
| `tools/` | Скрипты: Update-ChatGPTContextBundle, collect_server_bot_read_only |
| `*.cmd` (11 шт.) | Лаунчеры: заказы, тесты, Corel, проверки |

**Hermes-General:**

| Компонент | Что внутри |
|---|---|
| `app/` | hermes-dashboard, hooks, launcher, malyarka, memory-gateway, memory-hook, open-webui-data, review |
| `obsidian-long-memory/` | 10 папок: Profile, Rules, Knowledge, Orders, Clients, Projects, Processes, Analytics, Templates, Environment, Sessions |
| `obsidian-short-memory/` | 6 папок: Inbox, Daily, Ideas, Tasks, Drafts, To_Process |
| `projects/malyarka-future/` | Карта проекта Малярки, интеграционный план, аудит |
| `installers/` | Hermes-Setup-official-nousresearch.exe |

**Итого LOCAL:** 10 компонентов Hermes-Hub + 5 компонентов Hermes-General = **15 компонентов.**

---

### ⬜ ARCHIVE — Историческое, не источник правды

Всё в этой категории **не должно использоваться для принятия решений.**

| Файл/папка | Причина |
|---|---|
| `Hermes-Hub/_archive/` | Пустой архив (только README) |
| `Hermes-Hub/_quarantine/` | Карантин (пуст) |
| `Hermes-Hub/_reports/` | Старые отчёты (пуст) |
| `Hermes-Hub/_scratch/` | Черновики (пуст) |
| `Hermes-General/backups/` | Бэкапы hermes-desktop, openwebui |
| `Hermes-General/files/archive/` | Файловый архив |
| `Hermes-General/tmp/` | Скриншоты Hermes Desktop, PDF-извлечение |
| `Hermes-General/logs/CODEX_AUDIT_2026-06-12.md` | Аудит 9-дневной давности |
| `Hermes-General/logs/MALYARKA_GIT_DIFF_REVIEW_2026-06-12.md` | Git diff review 9-дневной давности |

**Итого ARCHIVE: 9 позиций.**

---

### 📋 PLANS — Планы, спецификации, не реализовано

**Hermes-Hub docs/ (основной массив планов):**

| Группа | Кол-во | Тема |
|---|---|---|
| `AGENT_*` | 8 файлов | Acceptance criteria, ecosystem reports, handoff map, routing rules |
| `BATCH_WORKFLOW.md` + `BATCH_VS_MICRO_TASK_RULES.md` | 2 | Правила батчей |
| `CODEX_*` | 4 файла | Sync protocol, prompts index, start here, task queue |
| `HERMES_ADAPTER_*` | 20+ файлов | Phase 2 dry-run, failure investigation, order-like fallback fix, live patch планы |
| `MALYARKA_FILE_*` | 6+ файлов | Download fix, investigation, Russian export headers |
| `SERVER_*` | 15+ файлов | SSH access, bot startup (7 controlled-start), adapter insertion, inventory, post-start stabilization |
| `HERMES_MASTER_MAP_LEVELS_AND_PROMPTS.md` | 1 | Уровни мастер-карты |
| `APPROVAL_*`, `DECISION_*`, `DOCUMENTATION_INDEX.md` | 4 | Гейты, решения, индекс |
| `COREL_EXCEL_PRODUCTION_EXPORT_PREPLAN.md` | 1 | Preplan Corel/Excel |
| `FINAL_CHECKPOINT_*`, `FINAL_NO_ACCESS_*`, `FULL_CHAIN_*` | 3 | Чекпоинты |

**Hermes-Hub handoff/ (батч-пакеты):**

| Файл | Роль |
|---|---|
| `BATCH_001` … `BATCH_005` | 5 батчей: контекст, архитектура, scaffold, handoff, one-command |
| `BATCH_PACKET_TEMPLATE.md` | Шаблон батч-пакета |
| `TASK_PACKET_TEMPLATE.md` | Шаблон таск-пакета |
| `PROMPT_TO_PASTE_IN_*.md` (4 шт.) | Prompt-шаблоны для ChatGPT/Codex/Hermes |

**Hermes-Hub прочее:**

| Файл/папка | Роль |
|---|---|
| `task_bundles/` (8 бандлов) | BUNDLE_255_270 … BUNDLE_481_510 — adapter implementation |
| `decisions/DECISIONS.md` | Журнал решений |
| `progress/PROGRESS_CARD.md` | Карта прогресса |
| `rules/` (2 файла) | Autopilot approval gates, rule conveyor |

**Hermes-General:**

| Файл/папка | Роль |
|---|---|
| `future-integrations/` (5 папок) | Заглушки: deepseek, github, malyarka, openai-codex, telegram |
| `config/INSTALL_PLAN.md` | План установки |
| `config/SAFETY_RULES.md` | Правила безопасности (пульт) |
| `PROMPT_TO_PASTE_IN_*.txt` (3 шт.) | Prompt-шаблоны |

**Итого PLANS:** ~70+ файлов docs + 15 handoff + 8 бандлов + ~10 прочих = **~100+ единиц.**

---

### 🔍 NEEDS REVIEW — Требует проверки

**Дубликаты между Hermes-General и Hermes-Hub:**

| Hermes-General | Hermes-Hub | Статус |
|---|---|---|
| `AGENTS.md` | `AGENTS.md` | Разные файлы с одним именем. [уточнить] какой приоритетнее |
| `MALYARKA_CURRENT_STATUS.md` | `HERMES_HUB_STATE.md` | Фактический дубликат по смыслу. MALYARKA_CURRENT_STATUS — исторический |
| `MALYARKA_START_HERE_FOR_HERMES.md` | `START_HERE_FOR_HERMES.md` + `START_HERE_FOR_HERMES_HUB_MALYARKA.md` | Три входных точки — [уточнить] нужны ли все |

**Файлы с неясным статусом:**

| Файл | Почему |
|---|---|
| `Hermes-Hub/handoff/CODEX_HANDOFF_PROMPT_READY.md` | 18 июн, «Codex not available» — актуально? |
| `Hermes-Hub/handoff/START_NEXT_WORK_SESSION_PROMPT.md` | 18 июн — [уточнить] |
| `Hermes-Hub/handoff/START_NEXT_CHAT_PROMPT_SERVER_ADAPTER_CLOSED.md` | 19 июн — [уточнить] |
| `Hermes-Hub/handoff/REPORT_TO_CHATGPT_SERVER_ADAPTER_FINAL.md` | 19 июн — [уточнить] |
| `Hermes-Hub/docs/FINAL_NO_ACCESS_WAITING_STATE.md` | Упоминается в индексе — [уточнить] актуален ли |
| `Hermes-Hub/task_bundles/` (8 бандлов) | Статус выполнения неясен без чтения содержимого |

**Пустые структуры в Hermes-General (созданы, но не заполнены):**

| Папка | Статус |
|---|---|
| `docs/` | Пусто |
| `handoff/` | Пусто |
| `inputs/` | Пусто |
| `notes/` | Пусто |
| `patches/` | Пусто |
| `server_staging/` | Пусто |
| `shared_contracts/` | Пусто |
| `sync/` | Пусто |
| `templates/` | Пусто |
| `github/` | Пусто |
| `repos/` | Пусто |
| `files/inbox/`, `files/outputs/` | Пусто |

**Агенты без полной спецификации:**

| Агент | Чего не хватает |
|---|---|
| `Hermes-General/agents/hermes-orders-future/` | Только README, нет SYSTEM_PROMPT |
| `Hermes-General/agents/hermes-general/` | Только SYSTEM_PROMPT, нет AGENT_SPEC |
| `Hermes-General/agents/hermes-local/` | Только SYSTEM_PROMPT |
| `Hermes-General/agents/hermes-memorykeeper/` | Только SYSTEM_PROMPT |
| `Hermes-General/agents/hermes-orchestrator/` | Только SYSTEM_PROMPT |

**Итого NEEDS REVIEW: 28 позиций.**

---

### ❌ DEPRECATED — Устарело, но не удалять

| Файл | Причина | Что использовать вместо |
|---|---|---|
| `Hermes-General/MALYARKA_CURRENT_STATUS.md` | Источник правды теперь Hermes-Hub | `HERMES_HUB_STATE.md` |
| `Hermes-General/MALYARKA_START_HERE_FOR_HERMES.md` | Заменён мостом к Hub | `START_HERE_FOR_HERMES_HUB_MALYARKA.md` |
| `Hermes-General/logs/CODEX_AUDIT_2026-06-12.md` | 9 дней, проект ушёл вперёд | `logs/WORKLOG.md` (Hermes-Hub) |
| `Hermes-General/logs/MALYARKA_GIT_DIFF_REVIEW_2026-06-12.md` | 9 дней | — |
| `Hermes-Hub/docs/CODEX_PROMPTS_READY_INDEX.md` | «Codex not available» — устарело | — |
| `Hermes-Hub/docs/CODEX_START_HERE_WHEN_AVAILABLE.md` | «Codex not available» — устарело | `START_HERE_FOR_CODEX.md` |
| `Hermes-Hub/docs/CODEX_TASK_QUEUE_WHEN_AVAILABLE.md` | «Codex not available» — устарело | `sync/NEXT_BATCH_QUEUE.md` |
| `Hermes-Hub/handoff/CODEX_HANDOFF_PROMPT_READY.md` | 18 июн, «Codex not available» | — |

**Итого DEPRECATED: 8 файлов.** Ничего не удалено.

---

### 🔴 Документы, которые НЕЛЬЗЯ использовать как актуальные

1. `Hermes-General/MALYARKA_CURRENT_STATUS.md` — исторический, противоречит Hermes-Hub.
2. `Hermes-General/MALYARKA_START_HERE_FOR_HERMES.md` — ведёт в старую структуру.
3. `Hermes-General/logs/CODEX_AUDIT_*` и `MALYARKA_GIT_DIFF_REVIEW_*` — устаревшие аудиты.
4. Все файлы с пометкой «Codex not available» в `docs/` и `handoff/`.
5. `Hermes-General/backups/` — бэкапы, не рабочие данные.

---

### 📊 Сводка Level 2

| Статус | Кол-во |
|---|---|
| 🟢 LIVE | 30 |
| 🟡 LOCAL | 15 компонентов |
| ⬜ ARCHIVE | 9 |
| 📋 PLANS | ~100+ |
| 🔍 NEEDS REVIEW | 28 |
| ❌ DEPRECATED | 8 |

---

## Level 3 — Current Architecture Map (COMPLETED 2026-06-21)

Три системы. Одна цель: Hermes Hub — мозг, Telegram — будущий интерфейс с телефона.

---

### 🏗️ Система A: Telegram-бот Малярки (LIVE · сервер)

```
                            СЕРВЕР: 178.104.95.187
                 /opt/malyarka-telegram-bot (.venv)
                              |
                         ┌────┴────┐
                         | app.py  |  ← entrypoint: --run-polling
                         └────┬────┘
                              |
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
               router.py  handlers.py  keyboards.py
                    │         │
                    │    ┌────┴─────────────┐
                    │    │ messages.py       │
                    │    │ access.py         │
                    │    │ session.py        │
                    │    │ intent.py         │
                    │    │ engineer_tasks.py │
                    │    │ obsidian_inbox.py │
                    │    │ voice.py          │
                    │    └──────────────────┘
                    │
         ┌──────────┼──────────┐
         ▼                     ▼
   ┌───────────┐       ┌──────────────┐
   │ malyarka_ │       │ malyarka_    │
   │ core/     │       │ ai/          │  ← AI-слой
   └─────┬─────┘       └──────────────┘
         │
    ┌────┴────────────────────────┐
    │                             │
    ▼                             ▼
┌─────────────┐            ┌───────────┐
│ adapters/   │            │ parsing.py│
│ ├─telegram  │            │ validation│
│ └─hermes★   │            │ models.py │
└──────┬──────┘            │ calculat. │
       │                   └─────┬─────┘
       │                         │
       │              ┌──────────┼──────────┐
       │              ▼          ▼          ▼
       │         services/   storage/   security/
       │         ├─orders    ├─repo     └─permissions
       │         └─archive   └─schema
       │
       └──── order flow ────► exports/
                              ├─ corel.py        → Excel для Corel ✓
                              ├─ malyarka.py      → Файл Малярки ✓
                              └─ malyarka_file.py → (русские заголовки ✓)
```

**Ключевые факты:**
- Сервис: `malyarka-telegram-bot.service` → **active/running**, autostart **disabled**
- Feature flag: `_HERMES_ADAPTER_ENABLED = False`
- Phase 2: OFF | Production: OFF
- Hermes adapter: **установлен, но выключен** (`adapters/hermes_adapter.py`)
- Order-like fallback fix: применён (20.06), sanity passed
- Работает: `/start`, парсинг `700 x 500`, Excel для Corel, Файл Малярки (русские заголовки)

**Граница адаптера (design point):**
```
Telegram → router.py/handlers.py
              → [будущий tiny guarded call-site]
                  → adapters/telegram.py / adapters/hermes_adapter.py
                      → dry-run response / fallback_required=true
                          → существующий order flow
```

---

### 🏗️ Система B: Hermes Hub (LIVE · центральный мозг)

```
                       E:\Hermes-Hub
                            │
              ┌─────────────┼─────────────┐
              │             │             │
         📡 STATE       🧠 BRAIN      📦 LOCAL
              │             │             │
    ┌─────────┤      ┌──────┤      ┌─────┤
    │         │      │      │      │     │
    ▼         ▼      ▼      ▼      ▼     ▼
  sync/    tasks/  MASTER  docs/  agents/ projects/
  ├─SHARED ├─NEXT  _MAP    (~100  (6 шт)  ├─malyarka-
  │ _STATUS│ _TASKS  │     планов)  │     │ clean/
  ├─GATES  │         │              │     │ (scaffold)
  ├─BLOCK  │    ┌────┴────┐    ┌────┴───┐ local_
  │ _ERS   │    │         │    │        │ tests/
  ├─DECIS. │    ▼         ▼    ▼        ▼ server_
  ├─CODEX  │ handoff/  patches/ logs/  sandbox/ staging/
  ├─HERMES │ ├─ACTIVE  ├─LATEST └─WORK  ├─fake    ├─snap
  ├─MICRO  │ │ _BATCH  │ _STATE  _LOG   │ _adapt   │ shot
  ├─QUEUE  │ ├─REPORT  └─PATCH          │ (166✓)   ├─fix
  └─DONE   │ │ _TO_     _LOG           │ server_  │ cand
           │ │ CHATGPT                 │ adapt_   ├─tests
           │ ├─BATCH_                                          │ sandbox  └─rus_
           │ │ 001-005                                         │           export
           │ ├─CHATGPT_
           │ │ CONTEXT_
           │ │ BUNDLE
           │ └─NAV_
           │   INDEX
           │
      real_orders_
      sandbox/
      (gates 1-5A ✓)
```

**Поток работы Hermes Hub:**
```
state/sync → master map → docs/plans → agents → sandbox → Codex batches → future work
      ↑                                                        │
      └────────── handoff/REPORT_TO_CHATGPT ←──────────────────┘
```

**Ключевые факты:**
- Единый источник правды
- 6 агентов: Sales Intake, Malyarka, Corel Export, Telegram Safe Adapter, Memory, Diagnostics
- Fake adapter: 166 contract tests passed (локально)
- Malyarka Clean: scaffold (order_input → size_parser → dispute_detector → area_calculator → corel_export_model → order_result)
- Порядок работы: ChatGPT обсуждает → Codex исполняет → Hermes читает state

---

### 🏗️ Система C: Hermes-General / Hermes Desktop (LIVE · оболочка)

```
                    E:\Hermes-General
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    📋 RULES          🧠 MEMORY       🔧 APP
          │               │               │
    ┌─────┤          ┌────┴────┐     ┌────┴──────┐
    │     │          │         │     │           │
    ▼     ▼          ▼         ▼     ▼           ▼
  HERMES START    obsidian-  obsidian-  app/
  _OS    _HERE    long-      short-     ├─dashboard
         _FOR_    memory     memory     ├─hooks
         HERMES   (10 папок) (6 папок)  ├─launcher
         _HUB_                          ├─malyarka
         _MALYARKA                      ├─memory-
         (МОСТ)                         │ gateway
         │                              ├─memory-
         │                              │ hook
         ▼                              ├─open-
    E:\Hermes-Hub                       │ webui
    (центральный                        ├─review
     мозг)                              │
                                        ▼
                                  Start-Hermes.bat
                                  Save-HermesMemory.bat
```

**Поток Hermes-General:**
```
Hermes Desktop → OS rules → Obsidian memory → prompts → pult/launcher → МОСТ → Hermes Hub
```

**Ключевые факты:**
- Оболочка, не мозг
- Obsidian: long-memory (структура знаний), short-memory (inbox/ежедневник)
- Prompt-шаблоны для ChatGPT/Codex/Hermes
- Пустые структуры: 12 папок созданы, но не заполнены (docs, sync, handoff, inputs, ...)

---

### 🔗 Точки интеграции (current + future)

| # | Точка | Где | Статус |
|---|-------|-----|--------|
| 1 | `adapters/telegram.py` | Сервер | **LIVE** — существующий adapter boundary |
| 2 | `adapters/hermes_adapter.py` | Сервер | **Установлен, OFF** — feature flag выключен |
| 3 | `adapter_boundary_snapshot/` | Hermes-Hub local | **Готово** — read-only копии для анализа |
| 4 | `adapter_boundary_fix_candidate/` | Hermes-Hub local | **Готово** — order-like fallback fix |
| 5 | `hermes_adapter_fake/` | Hermes-Hub local | **166 тестов passed** — contract tests |
| 6 | `projects/malyarka-clean/` | Hermes-Hub local | **Scaffold** — будущий чистый core |
| 7 | `START_HERE_FOR_HERMES_HUB_MALYARKA.md` | Hermes-General | **LIVE** — мост General→Hub |
| 8 | `router.py / handlers.py` | Сервер | **Будущее** — tiny guarded call-site для Hermes |
| 9 | `malyarka_ai/` | Сервер | **Запретная зона** — не трогать |
| 10 | `malyarka_vision/` | Сервер | **Запретная зона** — не трогать |

---

### 📐 Где что находится

| Что | Где | Статус |
|-----|-----|--------|
| 🤖 **Telegram-бот** | Сервер 178.104.95.187 | 🟢 LIVE · active/running |
| 🧠 **Центральный мозг** | `E:\Hermes-Hub` | 🟢 LIVE · источник правды |
| 💻 **Desktop-оболочка** | `E:\Hermes-General` | 🟢 LIVE · OS + Obsidian |
| 📦 **Локальный код** | `E:\Hermes-Hub\projects\malyarka-clean\` | 🟡 LOCAL · scaffold |
| 🧪 **Тесты адаптера** | `E:\Hermes-Hub\local_tests\` | 🟡 LOCAL · 166 passed |
| 📋 **Планы** | `E:\Hermes-Hub\docs\` | 📋 PLANS · ~100+ файлов |
| 🗄️ **Архив** | `E:\Hermes-Hub\_archive\`, `Hermes-General\backups\` | ⬜ ARCHIVE |
| 🔮 **Будущий Telegram-интерфейс** | `adapters/hermes_adapter.py` → router → handlers | 🔮 FUTURE · Phase 2 blocked |

---

### 🎯 Где Telegram сейчас vs где должен быть

| | Сейчас | Будущее |
|---|--------|---------|
| **Роль** | Рабочий канал для заказов | Главный интерфейс с телефона |
| **Hermes-связь** | Отсутствует (adapter OFF) | Hermes через adapter → Phase 2 |
| **Мозг** | Собственный (app/router/handlers) | Hermes Hub управляет, бот — интерфейс |
| **Управление** | Прямые команды боту | Hermes принимает решения → бот исполняет |

---

## Level 4 — Find Missing Blocks (COMPLETED 2026-06-21)

Главный вопрос: **чего не хватает, чтобы Hermes Hub стал центральным мозгом, а Telegram — удобным интерфейсом?**

Ответ: 23 missing blocks в 7 категориях.

---

### A. Hermes OS / Управление (4 блока)

| # | Блок | Статус | Риск | Кто | Следующий шаг |
|---|------|--------|------|-----|---------------|
| A1 | **Единая команда «что дальше?»** | Частично: `NEXT_TASKS.md` есть, но нет авто-сборки из 6 источников | Hermes теряет контекст между сессиями | Hermes | Создать `WHAT_NEXT.md` — авто-сборка из sync/tasks/handoff одним вызовом |
| A2 | **Очередь задач с routing-тегами** | Частично: `NEXT_TASKS.md` + `MICRO_TASK_QUEUE.md` + `NEXT_BATCH_QUEUE.md` — три файла, нет единого view | Дублирование, противоречия, потеря задач | Hermes | Объединить в единый `TASK_QUEUE.md` с тегами `[Hermes]` / `[Codex]` / `[User]` |
| A3 | **Авто-sync после каждого этапа** | Нет автоматизации. `Update-ChatGPTContextBundle.ps1` есть, но ручной | ChatGPT/Codex/Hermes видят разный state | Hermes | Добавить `SYNC_CHECKLIST.md`: что обновлять после каждого батча |
| A4 | **Routing-матрица Hermes/Codex/ChatGPT** | Задокументирована в `HERMES_OPERATING_SYSTEM.md`, но не верифицирована на практике | Micro-задачи уходят в Codex, risky — в Hermes | User | Провести день с routing-таблицей: «это → Hermes, это → Codex» и записать реальные кейсы |

---

### B. Telegram как будущий интерфейс (6 блоков)

| # | Блок | Статус | Риск | Кто | Следующий шаг |
|---|------|--------|------|-----|---------------|
| B1 | **Safe command set** | ❌ Отсутствует. Нет списка разрешённых команд для Hermes-режима | Hermes может выполнить опасную операцию через Telegram | Hermes + User | Составить `TELEGRAM_SAFE_COMMANDS.md`: `/status`, `/orders`, `/tasks`, `/approve`, `/block` |
| B2 | **User approval flow** | Частично: `APPROVAL_GATES.md` описывает фразы, но нет Telegram-сценария | Пользователь случайно approve-ит опасное действие | Hermes | Спроектировать `TELEGRAM_APPROVAL_FLOW.md`: кнопка [✓ Approve] / [✗ Reject] с таймаутом |
| B3 | **Режим Hermes chat** | ❌ Отсутствует. Сейчас бот — только заказы | Нельзя общаться с Hermes через Telegram | Codex | После Phase 2: `HERMES_CHAT_MODE` — свободный текст → Hermes → ответ |
| B4 | **Режим orders** | 🟢 Работает. `700 x 500` → парсинг → Excel/Файл | Риск: adapter перехватывает order-like (Phase 2 bug) | Codex | Уже исправлен order-like fallback. Проверить при следующем Phase 2 dry-run |
| B5 | **Режим admin/engineer** | ❌ Отсутствует. `engineer_tasks.py` есть на сервере, но роль не подключена к Hermes | Инженерные команды без approval | Codex | После Phase 2: `HERMES_ENGINEER_MODE` + feature flag + approval gate |
| B6 | **Fallback если Hermes недоступен** | ❌ Отсутствует | Бот перестаёт отвечать на заказы если adapter включён, а Hermes упал | Codex | `HERMES_FALLBACK_MODE`: если Hermes не ответил за N секунд → старый flow |

---

### C. Live Bot Stability (4 блока)

| # | Блок | Статус | Риск | Кто | Следующий шаг |
|---|------|--------|------|-----|---------------|
| C1 | **Regression checklist** | ❌ Отсутствует. Нет списка «что проверить после каждого изменения» | Патч ломает незамеченную функцию | Hermes | Составить `REGRESSION_CHECKLIST.md`: /start, 700x500, Excel, Файл, callback, кнопки |
| C2 | **Export callback robustness** | 🟡 Хрупкое. `openpyxl` добавлен (20.06), русские заголовки исправлены — но нет теста на callback timeout | Файл не скачивается, пользователь не понимает почему | Codex | Добавить `test_export_callback_timeout.py` + мониторинг callback-ошибок |
| C3 | **Runtime context after restart** | 🔴 Критичное. Сервис active/running, но autostart disabled. После перезагрузки сервера бот не поднимется | Бот молчит после ребута сервера | User | Решить: включить autostart или оставить ручной controlled start |
| C4 | **Monitoring / status check** | ❌ Отсутствует. Нет команды «бот жив?» без Telegram-теста | Неизвестно, работает ли бот, пока пользователь не напишет | Hermes | Создать `health_check.sh` на сервере: systemctl status + /start test |

---

### D. GitHub (3 блока)

| # | Блок | Статус | Риск | Кто | Следующий шаг |
|---|------|--------|------|-----|---------------|
| D1 | **Repo / remote / branch** | ❌ Отсутствует. Папки `github/` и `repos/` пусты | Нет бэкапа кода, нет истории изменений | User | Решить: нужен ли GitHub. Если да — создать repo, связать с Hermes-Hub |
| D2 | **Commit policy** | ❌ Отсутствует. Нет правил: что коммитить, когда, кто | Случайный коммит секретов, потеря истории | Hermes + User | `COMMIT_POLICY.md`: только .md + .py без секретов, approval перед push |
| D3 | **Backup / checkpoint workflow** | 🟡 Частично. `patches/` и `LATEST_STATE_PATCH.md` есть, server-бэкапы создаются перед патчами | Потеря состояния между версиями | Hermes | Добавить `CHECKPOINT.md`: авто-бэкап перед каждым Codex-батчем |

---

### E. Obsidian (3 блока)

| # | Блок | Статус | Риск | Кто | Следующий шаг |
|---|------|--------|------|-----|---------------|
| E1 | **Что сохранять в long memory** | 🟡 Неясно. 10 папок созданы, но правила наполнения отсутствуют | Дублирование с Hermes-Hub state, мусор | User + Hermes | `OBSIDIAN_LONG_MEMORY_RULES.md`: проекты, клиенты, знания, НЕ state/задачи |
| E2 | **Что сохранять в short memory** | 🟡 Неясно. 6 папок, нет критериев | Inbox забивается, ежедневник теряется | User | `OBSIDIAN_SHORT_MEMORY_RULES.md`: inbox → daily → tasks, авто-очистка |
| E3 | **Как не дублировать state** | 🔴 Критичное. Obsidian и Hermes-Hub могут хранить одно и то же | Противоречия: Obsidian говорит одно, Hub — другое | Hermes | Правило: **state только в Hermes-Hub**. Obsidian — knowledge/notes, не state |

---

### F. Старый архив Малярки (3 блока)

| # | Блок | Статус | Риск | Кто | Следующий шаг |
|---|------|--------|------|-----|---------------|
| F1 | **Price tables / материалы** | ❌ Не разобраны. Цены/ЛКМ/материалы в старом архиве | Использование устаревших цен в новых заказах | Codex (read-only) | Read-only аудит: найти price-файлы, пометить дату, НЕ применять |
| F2 | **Salary / economics / warehouse** | ❌ Не разобраны. Экономические блоки старой Малярки | Потеря бизнес-логики при полном отказе от архива | User + Codex | Решить: нужна ли экономика сейчас. Если да — read-only извлечение формул |
| F3 | **Что нельзя принимать как истину** | 🟡 Задокументировано в MASTER_MAP: «do not treat old rules/prices as current truth» | Случайное применение старых правил к новым заказам | Hermes | Явный `DEPRECATED_RULES.md`: список всего, что из архива НЕ применять |

---

### G. Agents / Local Malyarka Clean (3 блока)

| # | Блок | Статус | Риск | Кто | Следующий шаг |
|---|------|--------|------|-----|---------------|
| G1 | **Агенты: спецификации есть, реализации нет** | 🟡 6 agents со spec-документами, но только `sales_client_intake` и `malyarka` имеют `src/` + `tests/` | Агенты остаются «бумажными» — нельзя использовать | Codex | Реализовать минимальные working-модули для 4 оставшихся агентов |
| G2 | **Malyarka Clean: scaffold, не код** | 🟡 6 модулей с docstrings, без рабочей логики. Core contracts задокументированы | Нельзя использовать как replacement для старого кода | Codex | Реализовать parser + dispute_detector + area_calculator по контрактам |
| G3 | **Локальные тесты не подключены к live** | 🟡 166 тестов fake adapter, 10 тестов order-like fallback — все локальные | Тесты проходят локально, но не гарантируют live-поведение | Codex | После Phase 2: адаптировать тесты под live adapter contract |

---

### 📊 Сводка: 23 missing blocks

| Группа | Блоков | 🔴 Крит. | 🟡 Сред. | 🟢 Есть | Hermes | Codex | User |
|--------|--------|----------|----------|---------|--------|-------|------|
| A. Hermes OS | 4 | 0 | 4 | 0 | 4 | 0 | 1 |
| B. Telegram интерфейс | 6 | 0 | 4 | 1 | 2 | 4 | 1 |
| C. Live bot stability | 4 | 1 | 1 | 0 | 2 | 1 | 1 |
| D. GitHub | 3 | 0 | 3 | 0 | 2 | 0 | 1 |
| E. Obsidian | 3 | 1 | 2 | 0 | 2 | 0 | 2 |
| F. Архив Малярки | 3 | 0 | 3 | 0 | 1 | 2 | 1 |
| G. Agents / Clean | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| **Итого** | **23** | **2** | **20** | **1** | **13** | **10** | **7** |

---

### 🔴 Самое важное (critical)

1. **C3 — Runtime context after restart** — бот не поднимется после ребута сервера (autostart disabled). Риск: молчащий бот.
2. **E3 — Дублирование state между Obsidian и Hub** — два источника «правды». Риск: противоречия.

---

### 🟡 Что можно делать Hermes (read-only, markdown)

- A1, A2, A3, A4 — навести порядок в управлении
- C1, C4 — regression checklist, health check
- D2, D3 — commit policy, checkpoint workflow
- E1, E2, E3 — Obsidian rules
- F3 — deprecated rules list
- B1, B2 — safe command set, approval flow design

**13 блоков — Hermes может сделать сейчас без Codex.**

---

### 🔧 Что только Codex (код, сервер, тесты)

- B3, B5, B6 — режимы Telegram (chat/admin/fallback)
- C2 — export callback robustness
- F1, F2 — read-only аудит архива
- G1, G2, G3 — реализация агентов и Malyarka Clean
- B4 — проверка order-like при следующем Phase 2

**10 блоков — требуют Codex.**

---

### 👤 Что требует решения пользователя

- A4 — подтвердить routing-матрицу на практике
- C3 — решить: autostart или ручной controlled start
- D1 — решить: нужен ли GitHub
- E1, E2 — утвердить Obsidian-правила
- F2 — решить: нужна ли экономика сейчас
- B1, B2 — утвердить safe commands и approval flow

**7 блоков — ждут решения пользователя.**

---

## Level 5 — Risks And Forbidden Zones (COMPLETED 2026-06-21)

**Ключевой принцип:** безопасность не в том, чтобы ничего не делать. Безопасность — в том, чтобы каждый знал, что можно, что нельзя, и что делать при сомнении.

---

### 🔴 A. Secrets — НИКОГДА без явного разрешения

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| `.env` | Все секреты в одном файле: token, API keys, пароли | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_ENV` | Presence-only: «`.env` существует» | **СТОП. Не читать.** |
| `token` (Telegram) | Компрометация бота, перехват сообщений | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_TOKEN` | Использовать dev-бота через @BotFather для тестов | **СТОП.** |
| `config.py` secret values | Может содержать token, ключи, пароли | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_CONFIG` | Presence-only: «`config.py` существует» | **СТОП. Не читать содержимое.** |
| `os.environ` | Runtime secrets в памяти процесса | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_ENVIRON` | Не импортировать live-модули | **СТОП.** |
| Private SSH keys | Доступ к серверу 178.104.95.187 | **Никто** без approval | `РАЗРЕШАЮ_SSH_READ_ONLY` | SSH read-only с явным ключом `hetzner_hermes` | **СТОП.** |

---

### 🔴 B. Data — Защита данных пользователя

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| `orders.db` | Реальные заказы клиентов | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_ORDERS_DB` | Тестовые примеры из `examples/` | **СТОП.** |
| Live logs | Могут содержать заказы, имена, телефоны | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_LOGS` | `WORKLOG.md` — только project-логи | **СТОП.** |
| Реальные заказы | Клиентские данные, цены, размеры | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_REAL_ORDERS` | `real_orders_sandbox/safe_copies` | **СТОП.** |
| Клиентские данные | Имена, контакты, адреса | **Никто** без approval | `РАЗРЕШАЮ_ЧИТАТЬ_CLIENT_DATA` | — | **СТОП.** |

---

### 🔴 / 🟡 C. Server/Runtime — Живой сервер

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| **SSH доступ** | Полный контроль над сервером | Codex (read-only) | `РАЗРЕШАЮ_SSH_READ_ONLY` | `server_staging/` — локальные копии | **СТОП.** |
| **systemctl stop** | Бот перестанет отвечать | Codex | `APPROVE_CONTROLLED_STOP_ONCE` | Проверить `systemctl status` сначала | **НЕ ОСТАНАВЛИВАТЬ.** |
| **systemctl restart** | Кратковременный downtime, потеря контекста | Codex | `APPROVE_CONTROLLED_RESTART_ONCE` | Создать backup перед restart | **Только controlled.** |
| **systemctl enable** | Бот запустится после ребута сервера | User + Codex | `APPROVE_ENABLE_AUTOSTART` | Оставить disabled, использовать ручной start | **НЕ ВКЛЮЧАТЬ без решения.** |
| **Polling процесс** | Если упадёт — бот молчит | Codex | `APPROVE_RESTART_POLLING_ONCE` | `systemctl status` + health check | **Не убивать процесс.** |
| **Webhook** | Может конфликтовать с polling | **Никто** | Не настроен | Polling работает, webhook не трогать | **Не настраивать.** |

---

### 🔴 D. Production / Phase 2 — Граница между тестом и боем

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| **Production enable** | Все изменения сразу в live | **Никто** без approval | `APPROVE_PRODUCTION_ENABLE` | Dry-run на сервере с feature flag OFF | **НЕ ВКЛЮЧАТЬ.** |
| **Phase 2 enable** | Hermes adapter начинает обрабатывать сообщения | Codex | `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE` | Локальный fake adapter (166 тестов) | **НЕ ВКЛЮЧАТЬ без dry-run.** |
| **Feature flag ON** | `_HERMES_ADAPTER_ENABLED = True` — adapter активен | Codex | `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE` | Тесты на `adapter_boundary_fix_candidate` | **OFF по умолчанию.** |
| **Live adapter code change** | Может сломать весь order flow | Codex | `APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE` | `server_staging/` — копия → fix → тест → патч | **Backup перед каждым патчем.** |
| **Live Telegram test** | Отправка сообщений реальным пользователям | User | Пользователь сам тестирует | Локальные contract tests | **Только пользователь тестирует Telegram.** |

---

### 🟡 E. Old Malyarka — Архив, не истина

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| **Старый `bot.py`** | Древний код, может содержать старые токены | Codex (read-only) | `РАЗРЕШАЮ_ЧИТАТЬ_ARCHIVE` | `projects/malyarka-clean/` — новый код | **Не запускать. Не импортировать.** |
| **Старые JSON** | Могут содержать реальные заказы | Codex (read-only) | `РАЗРЕШАЮ_ЧИТАТЬ_ARCHIVE` | `examples/*.txt` — тестовые данные | **Считать историческим.** |
| **Старые токены** | В `start_bot.bat` ранее был hardcoded token | **Никто** | — | Токен удалён из .bat | **Проверить: не осталось ли копий.** |
| **Старые цены/правила** | Устаревшие расценки, материалы, нормы | Codex (read-only) | `РАЗРЕШАЮ_ЧИТАТЬ_ARCHIVE` | `DEPRECATED_RULES.md` — явный список | **НЕ применять к новым заказам.** |

---

### 🔴 F. External — Внешние сервисы

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| **Vision API** | `malyarka_vision/` — отправка фото вовне | **Никто** без approval | `РАЗРЕШАЮ_VISION` | Пользователь отверг OpenAI для Vision | **НЕ включать.** |
| **AI API (DeepSeek, Gemini)** | `malyarka_ai/` — внешние вызовы, стоимость | **Никто** без approval | `РАЗРЕШАЮ_AI_API` | Hermes сам — AI, внешние не нужны | **НЕ вызывать.** |
| **Network calls** | Любые внешние HTTP-запросы из бота | **Никто** без approval | `РАЗРЕШАЮ_NETWORK` | Локальная обработка | **НЕ делать.** |

---

### 🔴 G. Git — История и безопасность

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| **git push** | Отправка кода (возможно с секретами) на remote | **Никто** без approval | `РАЗРЕШАЮ_GIT_PUSH` | Локальные бэкапы (`patches/`, `_archive/`) | **НЕ пушить.** |
| **git commit** | Фиксация изменений — может зафиксировать секреты | Codex | `РАЗРЕШАЮ_GIT_COMMIT` | `.md`-файлы в `handoff/` и `patches/` | **Проверить diff перед commit.** |
| **git reset / checkout** | Потеря незакоммиченных изменений | **Никто** без approval | `РАЗРЕШАЮ_GIT_RESET` | `patches/LATEST_STATE_PATCH.md` | **НЕ делать без backup.** |
| **.git директория** | Содержит всю историю, включая удалённые секреты | **Никто** | — | Не читать .git напрямую | **Обходить.** |

---

### 🟡 H. State Sync — Единый источник правды

| Риск | Почему опасно | Кто может | Approval | Safe alternative | При сомнении |
|------|--------------|-----------|----------|------------------|-------------|
| **Obsidian vs Hub state** | Два источника «правды» противоречат друг другу | Hermes | Правило: state → Hub, knowledge → Obsidian | `OBSIDIAN_LONG_MEMORY_RULES.md` | **Hub — главный.** |
| **ChatGPT vs Codex vs Hermes** | Разные агенты видят разный контекст | Hermes + ChatGPT | `Update-ChatGPTContextBundle.ps1` после каждого батча | `CHATGPT_CONTEXT_BUNDLE.md` | **Обновить бандл.** |
| **Old status files vs new** | `MALYARKA_CURRENT_STATUS.md` vs `HERMES_HUB_STATE.md` | Hermes | Пометить старые как DEPRECATED | Только Hub-файлы — источник правды | **Hub — главный.** |
| **Ручное обновление state** | Человек забыл обновить state → агенты работают с устаревшим | Hermes | `SYNC_CHECKLIST.md` — авто-проверка | `WHAT_NEXT.md` — единый entry point | **Обновить state после каждого шага.** |

---

### 🚦 Сводка гейтов

#### 🔴 RED GATES — Не трогать без явного approval

| # | Зона | Approval phrase |
|---|------|----------------|
| R1 | `.env`, `token`, `config.py`, `os.environ` | `РАЗРЕШАЮ_ЧИТАТЬ_SECRETS` |
| R2 | `orders.db`, live logs, реальные заказы | `РАЗРЕШАЮ_ЧИТАТЬ_DATA` |
| R3 | `systemctl stop/restart/enable` | `APPROVE_CONTROLLED_*_ONCE` |
| R4 | Production enable | `APPROVE_PRODUCTION_ENABLE` |
| R5 | Phase 2 enable / feature flag ON | `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE` |
| R6 | Vision API, AI API, network calls | `РАЗРЕШАЮ_EXTERNAL_API` |
| R7 | `git push` | `РАЗРЕШАЮ_GIT_PUSH` |
| R8 | Private SSH keys | `РАЗРЕШАЮ_SSH_READ_ONLY` |
| R9 | Старые токены / секреты | **НИКОГДА** |

---

#### 🟡 YELLOW GATES — Можно с approval, только controlled

| # | Зона | Approval | Условие |
|---|------|----------|---------|
| Y1 | SSH read-only | `РАЗРЕШАЮ_SSH_READ_ONLY` | Только `ls`, `systemctl status`, presence-only |
| Y2 | `systemctl start` (controlled) | `APPROVE_SERVER_BOT_CONTROLLED_START_ONCE` | Backup, precheck, rollback plan |
| Y3 | Live adapter patch | `APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE` | Backup, local test, dry-run |
| Y4 | Чтение старого архива | `РАЗРЕШАЮ_ЧИТАТЬ_ARCHIVE` | Read-only, presence-first, не применять правила |
| Y5 | `git commit` (local) | `РАЗРЕШАЮ_GIT_COMMIT` | Проверить diff, нет секретов |
| Y6 | Обновление state-файлов | Без approval (Hermes) | Только `.md`, только Hub |
| Y7 | Изменение feature flag (dry-run) | `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE` | Временный флаг, rollback после теста |

---

#### 🟢 GREEN — Безопасно без approval

| # | Действие | Кто |
|---|---------|-----|
| G1 | Читать `.md` файлы (state, sync, tasks, docs) | Hermes, ChatGPT, Codex |
| G2 | Создавать/редактировать `.md` файлы в Hub | Hermes |
| G3 | Читать тесты (`tests/`, `local_tests/`) | Hermes, Codex |
| G4 | Читать agent specs | Hermes, Codex |
| G5 | Обновлять Master Map | Hermes |
| G6 | Читать локальные копии кода (`server_staging/`) | Hermes, Codex |
| G7 | Enumeration файлов (presence-only) | Hermes, Codex |
| G8 | Обновлять WORKLOG, NEXT_TASKS, REPORT | Hermes |
| G9 | Запускать локальные тесты (`pytest`) | Hermes, Codex |
| G10 | Читать `examples/` (тестовые заказы) | Hermes, Codex |
| G11 | Запускать `Update-ChatGPTContextBundle.ps1` | Codex |
| G12 | Создавать планы в `docs/` | Hermes |

---

### 🛑 Зоны, которые вообще нельзя трогать (даже read-only)

| Зона | Причина |
|------|---------|
| Старые токены (любые копии) | Компрометация необратима |
| `orders.db` содержимое | Клиентские данные |
| Live Telegram чаты/пользователи | Приватность |
| `malyarka_vision/` | Отправка фото вовне |
| `malyarka_ai/` содержимое | Внешние API-ключи |

---

## Level 6 — Future Feature Map (COMPLETED 2026-06-21)

Карта будущих функций проекта. Что уже есть, чего нет, кто делает.

---

### A. Telegram как главный интерфейс

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| Бот работает: `/start`, заказы, Excel, Файл | Hermes-интеграция через adapter | Codex (Phase 2) |
| Adapter установлен, feature flag OFF | Phase 2 dry-run (блокирован) | Codex |
| Order-like fallback fix применён | Safe command set для Hermes-режима | Hermes + User |
| 166 contract tests (fake adapter) | Режимы: chat, orders, admin, engineer | Codex |
| Approval gate registry | Telegram approval flow (кнопки) | Hermes (дизайн) |
| — | Fallback если Hermes недоступен | Codex |

**Риски:** Phase 2 bug (перехват order-like), отсутствие fallback, нет мониторинга.

---

### B. Malyarka Order Flow

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| Серверный бот: парсинг, расчёт, export | Чистый локальный core (scaffold only) | Codex |
| Corel Excel export ✓ | Parser implementation | Codex |
| Файл Малярки (русские заголовки) ✓ | Dispute detector implementation | Codex |
| Примеры заказов в `examples/` | Area calculator implementation | Codex |
| Core contracts задокументированы | Интеграция clean core → live bot | Codex |
| Order statuses: clean/has_disputes/empty | — | — |

**Риски:** scaffold без логики не заменяет старый код; миграция рискованна.

---

### C. Производство

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| Размеры парсятся | Материалы (ЛКМ, плёнка, пластик) | Codex |
| Corel Excel для раскроя | Цвета / покрытия | User + Codex |
| — | Фрезеровка (ArtCAM/CNC) | Later |
| — | Склад запчастей/материалов | Later |

**Риски:** старые данные в архиве — нельзя вслепую применять.

---

### D. Экономика

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| Расчёт площади (area) | Цены за м² | User |
| — | Себестоимость материалов | User |
| — | Зарплата / маржа | User |
| — | Отчёты (месяц, клиент, тип) | Codex (later) |
| — | Интеграция с 1С / Excel | Later |

**Риски:** экономика без пользователя невозможна — только пользователь знает цены.

---

### E. Память

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| `HERMES_HUB_STATE.md` — главный state | Rules: что в Obsidian vs Hub | Hermes |
| Obsidian long-memory (10 папок) | Авто-сохранение decisions в Hub | Hermes |
| Obsidian short-memory (6 папок) | Дедупликация Hub ↔ Obsidian | Hermes |
| `WORKLOG.md`, `DECISIONS.md` | Weekly snapshot | Hermes |

**Риски:** дублирование state = противоречия.

---

### F. GitHub / Checkpoints

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| Папки `github/`, `repos/` (пустые) | Repo, remote, branch | User + Codex |
| `patches/LATEST_STATE_PATCH.md` | Commit policy | Hermes |
| Server-бэкапы перед патчами | Push workflow | Codex |
| — | Checkpoint automation | Hermes (design) |

**Риски:** git push без проверки = утечка секретов.

---

### G. Agents / Orchestration

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| 6 agent specs (полные) | Реализация 4 агентов | Codex |
| Sales + Malyarka имеют `src/` + `tests/` | Corel export agent implementation | Codex |
| 166 fake adapter tests | Agent orchestration (routing) | Codex |
| `AGENT_FACTORY_RULES.md` | Multi-agent workflow | Codex |

**Риски:** «бумажные» агенты без кода.

---

### H. Vision / API (later)

| Что есть | Чего нет | Кто |
|----------|----------|-----|
| `malyarka_vision/` на сервере | Запретная зона — не трогать | Никто |
| `malyarka_ai/` на сервере | Запретная зона — не трогать | Никто |
| Пользователь отверг OpenAI | Альтернатива для Vision | User (решение) |

**Риски:** внешние API = стоимость + приватность.

---

## Level 7 — GitHub / Obsidian Workflow (COMPLETED 2026-06-21)

Правила, чтобы GitHub и Obsidian помогали, а не мешали.

---

### 🔷 GitHub Workflow

**Назначение:** checkpoint / release / backup. Не хаотичный dump.

#### Commit policy

| Правило | Детали |
|---------|--------|
| **Что коммитить** | `.md` файлы (state, sync, tasks, docs, handoff, master map) |
| **Что НЕ коммитить** | `.env`, `config.py`, `token`, `orders.db`, `.git`, `__pycache__/`, `.venv/`, скриншоты, PDF |
| **Когда коммитить** | После каждого завершённого батча (BATCH_NNN_DONE) |
| **Commit message** | `BATCH_NNN: краткое описание` |
| **Кто коммитит** | Codex, после approval пользователя |
| **Перед commit** | `git diff --staged` — проверить, нет ли секретов |

#### Push policy

| Правило | Детали |
|---------|--------|
| **Когда пушить** | Только после commit + approval |
| **Approval** | `РАЗРЕШАЮ_GIT_PUSH` |
| **Remote** | [уточнить у пользователя] |

#### Branches

```
main        — стабильный state (только проверенные батчи)
batches/NNN — рабочая ветка для текущего батча
```

#### Git-команды: что можно без approval

- `git status`, `git diff`, `git log` — ✅
- `git add *.md` — ✅ (если нет секретов)
- `git commit` — 🟡 (с approval `РАЗРЕШАЮ_GIT_COMMIT`)
- `git push` — 🔴 (только `РАЗРЕШАЮ_GIT_PUSH`)
- `git reset`, `git checkout` — 🔴 (никогда без backup)

---

### 🔷 Obsidian Workflow

**Назначение:** память, заметки, объяснения. **Не** runtime-state.

#### Что хранить в Obsidian Long Memory

| Папка | Что | Пример |
|-------|-----|--------|
| `00_Profile` | О себе, контакты, роли | Имя, Telegram, сервер |
| `01_Rules` | Бизнес-правила, стандарты | Как считать площадь, нормы расхода |
| `02_Knowledge` | Технические знания | Типы пластика, технология покраски |
| `03_Orders` | **НЕ реальные заказы.** Шаблоны, типовые примеры | Типовой заказ: 700×500 |
| `04_Clients` | Информация о клиентах (если нужно) | — |
| `05_Projects` | Описание проектов | Hermes Hub, Malyarka Clean |
| `06_Processes` | Бизнес-процессы | Как принять заказ → произвести → отдать |
| `07_Analytics` | Аналитика, выводы | Средний чек, популярные размеры |
| `08_Templates` | Шаблоны документов | Договор, счёт, КП |
| `09_Environment` | Окружение | Список инструментов, сервер, софт |
| `10_Sessions` | Итоги сессий | Что сделано за неделю |

#### Что хранить в Obsidian Short Memory

| Папка | Что |
|-------|-----|
| `00_Inbox` | Быстрые заметки, идеи |
| `01_Daily` | Ежедневник |
| `02_Ideas` | Идеи для будущего |
| `03_Tasks` | **НЕ дублировать `NEXT_TASKS.md`.** Личные задачи. |
| `04_Drafts` | Черновики писем, сообщений |
| `05_To_Process` | На обработку |

#### Главное правило

```
STATE → Hermes Hub (.md файлы: HERMES_HUB_STATE.md, sync/*, tasks/*)
KNOWLEDGE → Obsidian (заметки, правила, объяснения, шаблоны)
DECISIONS → Hub (decisions/DECISIONS.md)
WORKLOG → Hub (logs/WORKLOG.md)
```

**НИКОГДА не дублировать state в Obsidian.** Hub — единственный источник правды.

#### Как избежать конфликтов

1. Если факт есть в Hub — НЕ записывать в Obsidian.
2. Если факт только в Obsidian — перенести в Hub при ревью.
3. Раз в неделю: `OBSIDIAN_SYNC_CHECK.md` — сверить Hub и Obsidian.
4. Все решения → `decisions/DECISIONS.md` в Hub.

---

## Level 8 — Priorities (COMPLETED 2026-06-21)

Приоритеты на основе найденных missing blocks и рисков.

---

### 🔴 URGENT — Нельзя откладывать

| # | Задача | Кто | Почему |
|---|--------|-----|--------|
| P1 | C3: Решить autostart (бот не поднимется после ребута) | User | Риск: молчащий бот |
| P2 | E3: Правило «state → Hub, knowledge → Obsidian» | Hermes | Риск: противоречия |
| P3 | C1: Regression checklist | Hermes | Риск: патч ломает незамеченное |

---

### 🟡 NEXT — Следующие безопасные шаги

| # | Задача | Кто |
|---|--------|-----|
| P4 | A1: `WHAT_NEXT.md` — единый entry point | Hermes |
| P5 | A2: Единый `TASK_QUEUE.md` с routing-тегами | Hermes |
| P6 | A3: `SYNC_CHECKLIST.md` | Hermes |
| P7 | B1: `TELEGRAM_SAFE_COMMANDS.md` | Hermes |
| P8 | B2: `TELEGRAM_APPROVAL_FLOW.md` | Hermes |
| P9 | C4: Health check дизайн | Hermes |
| P10 | D2: `COMMIT_POLICY.md` | Hermes |
| P11 | E1: `OBSIDIAN_LONG_MEMORY_RULES.md` | Hermes |
| P12 | E2: `OBSIDIAN_SHORT_MEMORY_RULES.md` | Hermes |

---

### 🔵 LATER — Копить для Codex

| # | Задача | Кто |
|---|--------|-----|
| P13 | G2: Malyarka Clean parser + dispute + area | Codex |
| P14 | G1: Agent implementation (4 agents) | Codex |
| P15 | B3-B6: Telegram режимы (chat/admin/fallback) | Codex |
| P16 | C2: Export callback tests | Codex |
| P17 | F1-F2: Read-only аудит архива | Codex |
| P18 | GitHub repo setup | User + Codex |

---

### 🚫 BLOCKED

| # | Задача | Блокер |
|---|--------|--------|
| P19 | Phase 2 dry-run retry | Adapter перехватывает order-like |
| P20 | Production enable | Phase 2 не готов |
| P21 | Autostart enable | User decision needed |
| P22 | Vision API | User отверг, альтернативы нет |

---

### 👤 User Decision Needed

| # | Вопрос |
|---|--------|
| D1 | Нужен ли GitHub? |
| D2 | Autostart или ручной controlled start? |
| D3 | Нужна ли экономика сейчас? |
| D4 | Какая альтернатива Vision (если нужна)? |

---

### 🟢 TOP-10 ближайших задач (Hermes может сам)

| # | Задача | Файл |
|---|--------|------|
| 1 | Regression checklist | `docs/REGRESSION_CHECKLIST.md` |
| 2 | Единый WHAT_NEXT | `WHAT_NEXT.md` |
| 3 | Единый TASK_QUEUE | `TASK_QUEUE.md` |
| 4 | SYNC_CHECKLIST | `docs/SYNC_CHECKLIST.md` |
| 5 | Telegram safe commands | `docs/TELEGRAM_SAFE_COMMANDS.md` |
| 6 | Telegram approval flow | `docs/TELEGRAM_APPROVAL_FLOW.md` |
| 7 | Health check дизайн | `docs/HEALTH_CHECK_DESIGN.md` |
| 8 | Commit policy | `docs/COMMIT_POLICY.md` |
| 9 | Obsidian long memory rules | `docs/OBSIDIAN_LONG_MEMORY_RULES.md` |
| 10 | Obsidian short memory rules | `docs/OBSIDIAN_SHORT_MEMORY_RULES.md` |

---

## Level 9 — Codex Batch Packets (COMPLETED 2026-06-21)

Готовые batch-пакеты для будущих Codex-сессий. Hermes готовит → Codex исполняет.

---

### BATCH_010: Phase 2 Dry-Run Retry

| Поле | Значение |
|------|----------|
| **Цель** | Повторный Phase 2 dry-run с order-like fallback fix |
| **Входные документы** | `adapter_boundary_fix_candidate/`, `HERMES_ADAPTER_PHASE2_DRY_RUN_REPORT.md`, `HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md` |
| **Разрешено** | SSH read-only, backup, feature flag ON (временно), restart, Telegram test, rollback |
| **Запрещено** | Production, autostart, secrets, DB, git push |
| **Expected result** | `700 x 500` → Malyarka flow (не English clarification) |
| **Approval** | `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE` |

---

### BATCH_011: Telegram Hermes Interface Design

| Поле | Значение |
|------|----------|
| **Цель** | Спроектировать safe command set + approval flow + режимы |
| **Входные документы** | `TELEGRAM_SAFE_COMMANDS.md`, `TELEGRAM_APPROVAL_FLOW.md`, Level 9 docs |
| **Разрешено** | Создание `.md` планов, дизайн команд |
| **Запрещено** | Изменение серверного кода, включение adapter |
| **Expected result** | Полный дизайн Telegram-интерфейса для Hermes |
| **Approval** | Не требуется (planning only) |

---

### BATCH_012: Export Regression Tests

| Поле | Значение |
|------|----------|
| **Цель** | Создать тесты для Corel Excel + Файл Малярки export |
| **Входные документы** | `REGRESSION_CHECKLIST.md`, `examples/`, `server_staging/malyarka_file_russian_export_fix/` |
| **Разрешено** | Создание локальных тестов, pytest |
| **Запрещено** | Сервер, live bot, secrets |
| **Expected result** | `pytest` проходит для export flow |
| **Approval** | Не требуется (локально) |

---

### BATCH_013: GitHub Workflow Setup

| Поле | Значение |
|------|----------|
| **Цель** | Создать repo, настроить branches, первый commit |
| **Входные документы** | `COMMIT_POLICY.md`, `CHECKPOINT.md` |
| **Разрешено** | `git init`, `git add *.md`, `git commit` |
| **Запрещено** | `git push` без approval, коммит секретов |
| **Expected result** | Локальный git repo с master-map и state |
| **Approval** | `РАЗРЕШАЮ_GIT_COMMIT` |

---

### BATCH_014: Malyarka Clean Core Implementation

| Поле | Значение |
|------|----------|
| **Цель** | Реализовать parser + dispute_detector + area_calculator |
| **Входные документы** | `MALYARKA_CLEAN_CORE_CONTRACTS.md`, `BATCH_002_MALYARKA_CLEAN_ARCHITECTURE.md` |
| **Разрешено** | `projects/malyarka-clean/`, pytest |
| **Запрещено** | Сервер, live bot, secrets, старый код |
| **Expected result** | `order_input → parser → dispute → area → result` с тестами |
| **Approval** | Требуется для записи `.py` файлов |

---

### BATCH_015: Agent Implementation (4 agents)

| Поле | Значение |
|------|----------|
| **Цель** | Реализовать Corel Export, Telegram Adapter, Memory, Diagnostics agents |
| **Входные документы** | Agent specs в `agents/*/AGENT_SPEC.md` |
| **Разрешено** | `agents/*/src/`, pytest |
| **Запрещено** | Сервер, live bot, secrets |
| **Expected result** | Минимальные working-модули + тесты |
| **Approval** | Требуется для записи `.py` файлов |

---

### BATCH_016: Old Malyarka Archive Review

| Поле | Значение |
|------|----------|
| **Цель** | Read-only аудит архива: цены, материалы, правила |
| **Входные документы** | `DEPRECATED_RULES.md` |
| **Разрешено** | `ls`, presence-only, чтение `.md` и `.json` без секретов |
| **Запрещено** | Старые токены, `orders.db`, применение старых правил |
| **Expected result** | Инвентаризация архива + список извлечённых данных |
| **Approval** | `РАЗРЕШАЮ_ЧИТАТЬ_ARCHIVE` |

---

### BATCH_017: Autostart / Production Decision Plan

| Поле | Значение |
|------|----------|
| **Цель** | Подготовить план controlled autostart enable |
| **Входные документы** | `SERVER_BOT_CONTROLLED_STARTUP_BATCH_PLAN.md` |
| **Разрешено** | Planning only |
| **Запрещено** | `systemctl enable` без approval |
| **Expected result** | План с precheck, approval gate, rollback |
| **Approval** | `APPROVE_ENABLE_AUTOSTART` |

---

### BATCH_018: Economy / Pricing Module Plan

| Поле | Значение |
|------|----------|
| **Цель** | Спроектировать модуль цен и себестоимости |
| **Входные данные** | Цены от пользователя |
| **Разрешено** | Planning only |
| **Запрещено** | Применять старые цены |
| **Expected result** | `docs/ECONOMY_PRICING_MODULE_PLAN.md` |
| **Approval** | Требуется (пользователь даёт цены) |

---

## Level 10 — Maintenance (COMPLETED 2026-06-21)

Как Hermes поддерживает проект после завершения мастер-карты.

---

### 🔄 Как обновлять Master Map

1. После каждого завершённого батча → новый раздел в Master Map.
2. После каждого нового уровня → обновить «Current Safe Next Level».
3. Раз в неделю → ревью на устаревшее, пометить `[reviewed YYYY-MM-DD]`.

---

### 📡 Как обновлять State / Sync / Handoff

| Файл | Когда обновлять | Что писать |
|------|----------------|------------|
| `HERMES_HUB_STATE.md` | После каждого батча / важного решения | Новый статус, новые файлы, изменения runtime |
| `sync/SHARED_CURRENT_STATUS.md` | При изменении runtime (сервер, бот, флаги) | Таблица runtime |
| `sync/BLOCKERS.md` | При появлении / снятии блокера | Блокер + причина + след. шаг |
| `sync/DONE_LOG.md` | После каждого завершённого батча | BATCH_NNN + результат |
| `tasks/NEXT_TASKS.md` | После каждого батча | Обновлённый список задач |
| `handoff/REPORT_TO_CHATGPT.md` | После каждой серии батчей | Что сделано, что дальше |
| `handoff/CHATGPT_CONTEXT_BUNDLE.md` | `Update-ChatGPTContextBundle.ps1` | Авто-сборка |

---

### 📝 Как вести WORKLOG

```
Формат записи:
### YYYY-MM-DD — BATCH_NNN / LEVEL_N / DECISION
- Что сделано.
- Какие файлы созданы/изменены.
- Результат проверки.
- Следующий шаг.
```

---

### 🧠 Как фиксировать Decisions

```
Файл: decisions/DECISIONS.md

Формат:
### YYYY-MM-DD — Решение: <кратко>
- Контекст.
- Варианты.
- Выбрано.
- Почему.
- Кто принял.
```

---

### 📦 Как готовить Codex Tasks

1. Взять задачу из `TASK_QUEUE.md` (тег `[Codex]`).
2. Создать batch-пакет в `handoff/BATCH_NNN_*.md`.
3. Заполнить: цель, входные документы, разрешено, запрещено, expected result, approval.
4. Передать Codex с approval пользователя.

---

### ❌ Как отмечать Deprecated

1. Файл → добавить в `### ❌ DEPRECATED` секцию Master Map.
2. Указать причину и замену.
3. **Не удалять файл.**
4. В WORKLOG: `DEPRECATED: <файл> → <причина>`.

---

### 🔍 Как проверять противоречия

**Еженедельно (Hermes):**
1. Сравнить `HERMES_HUB_STATE.md` с `SHARED_CURRENT_STATUS.md`.
2. Сравнить Hub state с Obsidian (presence-only).
3. Проверить `NEXT_TASKS.md` vs `BLOCKERS.md` — нет ли задач с открытыми блокерами.
4. Проверить `DEPRECATED` — не ссылается ли кто на устаревшее.

**При каждом батче (Codex):**
1. `APPROVAL_GATES.md` — не нарушен ли approval.
2. `BLOCKERS.md` — не активен ли блокер для этой задачи.

---

### 📸 Как делать Weekly Snapshot

**Раз в неделю (Hermes):**
1. Создать `patches/WEEKLY_SNAPSHOT_YYYY-MM-DD.md`.
2. Записать:
   - Текущий runtime (сервер, бот, флаги).
   - Активные батчи.
   - Открытые блокеры.
   - Решения за неделю.
   - Top-5 задач на следующую неделю.

---

### 👤 Как пользователь работает через Hermes

**Ежедневно:**
1. Открыть Hermes Desktop.
2. Спросить: «Что дальше?»
3. Hermes читает `WHAT_NEXT.md` → выдаёт top-3 задачи.
4. Пользователь выбирает → Hermes исполняет или готовит Codex-пакет.

**Еженедельно:**
1. «Сделай weekly snapshot.»
2. «Проверь противоречия.»
3. «Что устарело?»

**При проблеме:**
1. «Проверь бота» → health check.
2. «Что сломалось?» → regression checklist.
3. «Верни как было» → rollback по `PATCH_LOG.md`.

---

## 📊 Финальная сводка мастер-карты

| Уровень | Название | Статус |
|---------|----------|--------|
| LEVEL 1 | Inventory Sources | ✅ COMPLETED |
| LEVEL 2 | Separate Live / Local / Archive / Plans | ✅ COMPLETED |
| LEVEL 3 | Current Architecture Map | ✅ COMPLETED |
| LEVEL 4 | Find Missing Blocks (23 блока) | ✅ COMPLETED |
| LEVEL 5 | Risks And Forbidden Zones (29 рисков) | ✅ COMPLETED |
| LEVEL 6 | Future Feature Map (8 групп) | ✅ COMPLETED |
| LEVEL 7 | GitHub / Obsidian Workflow | ✅ COMPLETED |
| LEVEL 8 | Priorities (22 задачи) | ✅ COMPLETED |
| LEVEL 9 | Codex Batch Packets (9 батчей) | ✅ COMPLETED |
| LEVEL 10 | Maintenance | ✅ COMPLETED |

**Статус: `MASTER_MAP_LEVELS_1_10_COMPLETED`**

---

### Что есть (итог)

- Полная инвентаризация 2 проектов (Hermes-Hub + Hermes-General)
- Архитектурная карта 3 систем (Telegram, Hub, Desktop)
- 23 missing blocks с владельцами
- 29 рисков с approval-фразами
- RED/YELLOW/GREEN гейты
- Карта будущих фич (8 групп)
- GitHub + Obsidian workflow rules
- Приоритеты: 22 задачи (3 urgent, 10 Hermes, 6 Codex, 4 blocked)
- 9 готовых Codex batch-пакетов
- Процедура maintenance (weekly snapshot, противоречия, deprecated)

---

### Что готово

- Hermes может работать автономно: 13 задач markdown-only
- Codex-пакеты готовы к исполнению (после approval)
- Все approval-фразы задокументированы
- Правила безопасности видимы и проверяемы

---

### Что не готово

- Malyarka Clean core: scaffold, не код
- 4 агента: specs, не реализация
- Phase 2: блокирован
- GitHub: не настроен
- Autostart: не решён
- Экономика: не спроектирована

---

### Что делать дальше (TOP-10)

| # | Задача | Кто | Файл |
|---|--------|-----|------|
| 1 | Regression checklist | Hermes | `docs/REGRESSION_CHECKLIST.md` |
| 2 | WHAT_NEXT.md | Hermes | `WHAT_NEXT.md` |
| 3 | Единый TASK_QUEUE.md | Hermes | `TASK_QUEUE.md` |
| 4 | SYNC_CHECKLIST.md | Hermes | `docs/SYNC_CHECKLIST.md` |
| 5 | Telegram safe commands | Hermes | `docs/TELEGRAM_SAFE_COMMANDS.md` |
| 6 | Telegram approval flow | Hermes | `docs/TELEGRAM_APPROVAL_FLOW.md` |
| 7 | Health check дизайн | Hermes | `docs/HEALTH_CHECK_DESIGN.md` |
| 8 | Commit policy | Hermes | `docs/COMMIT_POLICY.md` |
| 9 | Obsidian long memory rules | Hermes | `docs/OBSIDIAN_LONG_MEMORY_RULES.md` |
| 10 | Obsidian short memory rules | Hermes | `docs/OBSIDIAN_SHORT_MEMORY_RULES.md` |

---

### Кто делает

| Исполнитель | Задач |
|-------------|-------|
| 🟢 **Hermes** (read-only, markdown) | **13** (TOP-10 + A4, E3, D3) |
| 🔧 **Codex** (код, сервер, тесты) | **6** (P13-P18) |
| 👤 **User** (решения) | **4** (D1-D4) |
| 🚫 **Blocked** | **4** (P19-P22) |

---

### Что требует решения пользователя

1. D1 — Нужен ли GitHub?
2. D2 — Autostart или ручной controlled start?
3. D3 — Нужна ли экономика сейчас?
4. D4 — Альтернатива для Vision?

---

### Как вести дальше

1. Hermes читает `WHAT_NEXT.md` → выдаёт top-3 задачи.
2. Hermes делает markdown-задачи сам.
3. Для Codex-задач → готовит batch-пакет → пользователь approve → Codex исполняет.
4. Раз в неделю: weekly snapshot + проверка противоречий.
5. После каждого батча: обновить state/sync/worklog/master map.
## 2026-06-23 — Live Telegram order preview update

Live confirmed:

- neutral order-like input such as `1000*400` opens order preview immediately;
- `/заказ` is no longer required for obvious size input;
- the unwanted persistent three-button mode keyboard is removed from order fallback responses;
- order result buttons remain: Excel for Corel, Malyarka File, copy for Corel.

Reference:

```text
E:\Hermes-Hub\docs\TELEGRAM_ORDER_PREVIEW_LOOP_AND_BUTTONS_FIX_2026-06-23.md
```

