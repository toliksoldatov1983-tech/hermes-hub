# DONE — Полный реестр выполненных BATCH'ей

## 2026-07-04 - BATCH_097_TELEGRAM_SERVER_24_7_STATUS

Completed safe server status check and first owner phone reachability test for Telegram/Hermes 24/7 operation.

Created:
- `05_REPORTS\TELEGRAM_SERVER_24_7_STATUS_2026-07-04.md`

Updated:
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\DONE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`

Confirmed:
- SSH alias `hermes-server` works.
- `hermes-gateway.service` is active and enabled.
- `Restart=always`, `Linger=yes`.
- Main command: `python -m hermes_cli.main gateway run --replace`.
- No second visible server polling/gateway process found.
- Latest checked Telegram polling conflict line was `2026-07-04 08:20:11 UTC`.
- Owner phone `/status` reached the server at `2026-07-04 08:29:42 UTC`.
- Gateway returned pairing flow because the Telegram user is not authorized yet.

Pending:
- repeat owner-only live test from Telegram phone after pairing.

Update 2026-07-04 13:34 +05:00:
- User explicitly approved pairing code `5MUQKKUT`.
- Server command completed successfully.
- Telegram user `Soldatov Anatoliy (784990082)` can now use the bot on next message.

Update 2026-07-04:
- Repeat `/status` from phone returned `Hermes Gateway Status`.
- Server gateway remained `active` and `enabled`.
- No new journal errors appeared in the checked window.
- Result: `PHONE_LIVE_TEST_PASSED`.

Safety:
- no `.env` reading;
- no token or key reading;
- no live bot restart;
- no second polling;
- no real orders;
- no Google Drive change;
- no delete operations.

## Финальный: BATCH_081_SAFE_LOCAL_RELEASE_CANDIDATE_V2

Сформирован пакет релизной документации и метаданных.

### Созданные артефакты (docs/)

| Файл | Описание |
|------|----------|
| `docs/release_checklist_v2.md` | 5 этапов, 20 пунктов проверки |
| `docs/acceptance_criteria.md` | 5 групп критериев, матрица |
| `docs/known_limitations.md` | 7 известных ограничений с решениями |
| `docs/disabled_subsystem_matrix.md` | 18 подсистем: 6🔴 3🟡 9🟢 |
| `docs/command_matrix.md` | 30+ CLI команд по всем модулям |
| `docs/final_test_report.md` | 278/278, сводка, история сборки |

### Полная история (10 шагов)

| Шаг | Код | Название | Тестов |
|-----|-----|----------|-------|
| 1 | BATCH_063C | Базовый перенос компонентов | 48 |
| 2 | BATCH_073 | Ревизия и документирование | 48 |
| 3 | BATCH_074 | Машина состояний | 76 |
| 4 | BATCH_075 | Preview Report | 111 |
| 5 | BATCH_076 | Telegram Dialog Flow | 137 |
| 6 | BATCH_077 | Task Queue + Audit | 176 |
| 7 | BATCH_078 | Memory Sync | 219 |
| 8 | BATCH_079 | Secret Guard | 255 |
| 9 | BATCH_080 | GDrive Freeze | 278 |
| **10** | **BATCH_081** | **Release Candidate v2** | **278** |
## 2026-07-01 - BATCH_082_SAFE_LOCAL_RELEASE_READINESS_SUMMARY

Completed local release/readiness summary.

Created:
- `docs/RELEASE_READINESS_SUMMARY.md`
- `05_REPORTS/BATCH_082_RELEASE_READINESS_SUMMARY.md`

Updated:
- `00_START/CURRENT_STATE.md`
- `03_TASKS/ACTIVE_BATCH.md`
- `03_TASKS/NEXT_TASK.md`
- `05_REPORTS/REPORT_TO_USER.md`

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.

Completed Telegram live binding discovery by Codex.

Created:
- `05_REPORTS\TELEGRAM_LIVE_BINDING_DISCOVERY_REPORT.md`

Confirmed:
- live runner is generic `hermes gateway run`;
- PID chain remained active: `20840 -> 12188 -> 10024 -> 17796 -> 17256 -> 10100`;
- CWD is `[удалённый архив]`;
- Telegram adapter/gateway files are under `C:\Users\user\AppData\Local\hermes\hermes-agent`;
- no confirmed binding from live gateway to `[удалённый архив]`.

Result:
- `TELEGRAM_LIVE_BINDING_NOT_FOUND`

Safety:
- no `.env` reading;
- no token or key reading;
- no gateway stop/restart;
- no new polling;
- no live Telegram tests;
- no Google Drive, Vision, production database, E:\РАБОТА, CorelDRAW, ArtCAM, CNC;
- no git push, delete, reset, clear or prune.

Completed local Hermes generic Telegram gateway binding by Codex.

Created:
- `05_REPORTS\TELEGRAM_BINDING_IMPLEMENTATION_PLAN.md`
- `05_REPORTS\TELEGRAM_GATEWAY_BINDING_REPORT.md`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding\plugin.yaml`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding\__init__.py`

Updated:
- `C:\Users\user\AppData\Local\hermes\config.yaml`

Result:
- `TELEGRAM_GATEWAY_BINDING_LOCAL_READY_PENDING_RESTART`

Checks:
- py_compile passed;
- plugin discovery registered `pre_gateway_dispatch`;
- local required route tests passed;
- status aliases passed;
- hook-level fake gateway skip/allow test passed;
- focused pytest: 145 passed.

Safety:
- no `.env` reading;
- no token or key display;
- no gateway stop/restart;
- no second polling;
- no live Telegram tests;
- no Google Drive, Vision, production database, E:\РАБОТА, CorelDRAW, ArtCAM, CNC;
- no `bot_archive_20260703.py` changes;
- no git push, delete, reset, clear or prune.

Completed persistent Hermes access preparation by Codex.

Created:
- `00_START\HERMES_ACCESS_REGISTRY.md`
- `05_REPORTS\HERMES_PERSISTENT_FULL_ACCESS_REPORT.md`
- `C:\Users\user\.ssh\hermes_clean_full_access_ed25519`
- `C:\Users\user\.ssh\hermes_clean_full_access_ed25519.pub`
- `C:\Users\user\.ssh\config`

Backup:
- `backup_before_persistent_full_access_20260704_005041`

Result:
- `HERMES_ACCESS_REGISTRY_READY_SERVER_BLOCKED`

Checks:
- existing SSH keys tested against `root@49.13.76.163` and `ubuntu@49.13.76.163`;
- new alias `hermes-server` tested;
- result: server rejects public key auth;
- Hermes binding plugin discovery still passes: one `pre_gateway_dispatch` callback.

Safety:
- no private key printed;
- no token printed;
- no `.env` content printed;
- no server service stopped;
- no local gateway restart;
- no second polling;
- no Google Drive, Vision, production database, E:\РАБОТА, CorelDRAW, ArtCAM, CNC;
- no delete, reset, clear, prune or git push.

---

Completed local Telegram routes cleanup by Codex.

Created:
- `05_REPORTS\TELEGRAM_ROUTE_MAP_BEFORE_CLEANUP.md`
- `05_REPORTS\TELEGRAM_ROUTES_CLEANUP_REPORT.md`
- `05_REPORTS\TELEGRAM_STATUS_ROUTING_FIX_REPORT.md`

Updated:
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\DONE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`

Backup:
- `backup_before_telegram_routes_cleanup_20260703_231124`

Verification:
- py_compile OK;
- focused Telegram pytest: 145 passed.

Safety:
- no `.env` reading;
- no token or key reading;
- no Google Drive changes;
- no Vision enablement;
- no production database;
- no git push;
- no E:\РАБОТА changes;
- no CorelDRAW / ArtCAM / CNC launch;
- no `bot_archive_20260703.py` changes;
- no reset / clear / prune / delete.

Pending:
- confirmed live gateway restart;
- owner-only Telegram live tests.

---

Blocked live Telegram restart by Codex.

Created:
- `05_REPORTS\TELEGRAM_LIVE_RESTART_AND_TEST_REPORT.md`

Confirmed:
- active process chain: `hermes gateway run`;
- PID chain: `20840 -> 12188 -> 10024 -> 17796 -> 17256 -> 10100`;
- CWD for main chain: `[удалённый архив]`;
- command: `set +m; hermes gateway run 2>&1`.

Not confirmed:
- live gateway import/use of `[удалённый архив]`;
- direct `malyarka_telegram.app --run-polling` process.

Result:
- no process stopped;
- no gateway restarted;
- no live Telegram tests run;
- status `TELEGRAM_LIVE_RESTART_BLOCKED`.

Safety:
- no `.env` reading;
- no token or key reading;
- no Google Drive changes;
- no Vision enablement;
- no production database;
- no git push;
- no E:\РАБОТА changes;
- no CorelDRAW / ArtCAM / CNC launch;
- no `bot_archive_20260703.py` changes;
- no reset / clear / prune / delete.

## 2026-07-02 - BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER

Completed local safe-memory and context-control layer.

Created:
- `00_MEMORY\ACTIVE_CONTEXT.md`
- `00_MEMORY\PROJECT_MEMORY_INDEX.md`
- `00_MEMORY\CONTEXT_LOAD_POLICY.md`
- `00_MEMORY\START_NEW_HERMES_CHAT_PROMPT.md`
- `00_MEMORY\START_NEW_CODEX_CHAT_PROMPT.md`
- `00_MEMORY\COMPACT_STATE_FOR_AGENTS.md`
- `00_MEMORY\DO_NOT_AUTOLOAD.md`
- `00_MEMORY\CONTEXT_REFRESH_RULES.md`
- `05_REPORTS\BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER_REPORT.md`

Updated:
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\DONE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`
- `START_HERE.md`
- `docs\USER_RUNBOOK_RU.md`
- `scripts\check_local.cmd`

Main result:
- new Hermes/Codex chats should read only minimal context;
- `05_REPORTS`, `src`, `tests`, old projects, old archives and real/gated data must not autoload;
- BATCH_092 remains next, but must start through `00_MEMORY`.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no polling/webhook;
- no real orders;
- no Google Drive change;
- no old project scan;
- no archive change;
- no delete operations;
- no Malyarka logic changes.

Checks:
- help-local: OK;
- app-status: OK;
- dashboard: OK;
- project-audit: 25 checks, 0 failed;
- smoke: 27 checks, 0 failed;
- tests: 336 passed;
- check_local: OK after ASCII repair.
## 2026-07-01 - BATCH_083_SAFE_LOCAL_USER_DOCS_REFRESH

Completed user-facing documentation refresh.

Updated:
- `README.md`
- `START_HERE.md`
- `docs/WINDOWS_COMMANDS.md`
- `docs/USER_GUIDE_RU.md`
- `docs/WHAT_IS_DONE.md`
- `00_START/CURRENT_STATE.md`
- `03_TASKS/ACTIVE_BATCH.md`
- `03_TASKS/NEXT_TASK.md`
- `05_REPORTS/REPORT_TO_USER.md`

Created:
- `05_REPORTS/BATCH_083_USER_DOCS_REFRESH.md`

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.
## 2026-07-01 - END_OF_PIPELINE

Hermes-Clean Release Candidate v2 closed locally.

Created:
- `05_REPORTS/FINAL_RELEASE_CANDIDATE_V2_REPORT.md`

Updated:
- `00_START/CURRENT_STATE.md`
- `03_TASKS/ACTIVE_BATCH.md`
- `03_TASKS/NEXT_TASK.md`
- `05_REPORTS/REPORT_TO_USER.md`

Final verified state:
- tests: 278 passed;
- project audit: 25 checks, 0 failed;
- smoke: 23 checks, 0 failed;
- release checklist: OK;
- CLI commands: 35.
- END_OF_PIPELINE accepted by local task, audit and smoke checks.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.
## 2026-07-01 - BATCH_085_SAFE_LOCAL_ARCHIVE_PLAN_ONLY

Created archive plan only.

Created:
- `docs/ARCHIVE_PLAN.md`
- `05_REPORTS/ARCHIVE_PLAN_REPORT.md`

Updated:
- `00_START/CURRENT_STATE.md`
- `03_TASKS/ACTIVE_BATCH.md`
- `03_TASKS/NEXT_TASK.md`
- `05_REPORTS/REPORT_TO_USER.md`

Safety:
- no archive was created;
- no files were moved;
- no files were deleted;
- no `.env`, tokens or keys were read;
- no external APIs;
- no live Telegram;
- no real orders;
- no Google Drive change.
## 2026-07-02 - BATCH_086_CREATE_HERMES_CLEAN_ARCHIVE

Created archive after explicit user command.

Archive:
- `C:\Users\user\Desktop\Hermes-Clean-RC2-2026-07-01.zip`

Archive metadata:
- size: 776805 bytes / 0.74 MB;
- modified: 2026-07-02 01:29:03.

Created:
- `05_REPORTS/ARCHIVE_CREATION_REPORT.md`

Updated:
- `00_START/CURRENT_STATE.md`
- `03_TASKS/ACTIVE_BATCH.md`
- `03_TASKS/NEXT_TASK.md`
- `05_REPORTS/REPORT_TO_USER.md`

Safety:
- archived only Hermes-Clean;
- no files deleted;
- no files moved;
- no `.env`, tokens or keys read;
- no external APIs;
- no live Telegram;
- no real orders;
- no Google Drive change;
- no old project change.

## 2026-07-02 - BATCH_088_MACRO_MALYARKA_CORE_RECONCILIATION

Completed safe local Malyarka core reconciliation by Codex.

Created:
- `src\hermes_modules\malyarka\validation_contract.py`
- `src\hermes_modules\malyarka\dispute_questions.py`
- `src\hermes_modules\malyarka\export_source_policy.py`
- `tests\test_malyarka_validation_contract.py`
- `tests\test_malyarka_dispute_questions.py`
- `tests\test_malyarka_export_source_policy.py`
- `tests\test_malyarka_fixture_expansion.py`
- `05_REPORTS\BATCH_088_MALYARKA_CORE_RECONCILIATION_REPORT.md`

Updated:
- `src\hermes_modules\malyarka\export_contract.py`
- `src\hermes_modules\malyarka\export_preview.py`
- `src\hermes_modules\malyarka\fixtures.py`
- `src\hermes_modules\malyarka\status.py`
- `src\hermes_modules\malyarka\__init__.py`
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`

Checks:
- tests: 299 passed;
- project audit: 25 checks, 0 failed;
- smoke: 23 checks, 0 failed;
- malyarka fixtures: 12.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no polling/webhook;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.

## 2026-07-02 - BATCH_089B_PROMPT_FOR_OLD_HERMES_CHATGPT

Completed prompt preparation for opening a new Hermes / ChatGPT chat.

Created:
- `05_REPORTS\PROMPT_FOR_OLD_HERMES_CHATGPT.md`

Updated:
- `05_REPORTS\HERMES_OLD_HANDOFF_2026-07-02.md`
- `05_REPORTS\REPORT_TO_USER.md`
- `03_TASKS\DONE.md`

Confirmed in prompt:
- source of truth is `C:\Users\user\Desktop\Hermes-Clean`;
- tasks will come from ChatGPT / the user;
- old Hermes must not invent new major tasks outside `03_TASKS\NEXT_TASK.md`;
- unsafe tasks require separate user confirmation.

Checks:
- read `AGENTS.md`;
- read current handoff and report;
- no test run was needed for documentation-only prompt preparation.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no polling/webhook;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.

## 2026-07-02 - BATCH_089A_HANDOFF_TO_OLD_HERMES

Completed documentation-only handoff package for continuing work in old Hermes / ChatGPT context.

Created:
- `05_REPORTS\HERMES_OLD_HANDOFF_2026-07-02.md`

Updated:
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\DONE.md`
- `05_REPORTS\REPORT_TO_USER.md`

Confirmed:
- real source of truth is `C:\Users\user\Desktop\Hermes-Clean`;
- active Codex workspace folder with the Russian Hermes Clean name and trailing dot exists but is empty;
- the next planned big block remains `BATCH_090_PROJECT_PACKAGING_AND_ONE_COMMAND_LAUNCH`.

Checks:
- read `AGENTS.md`;
- read `START_HERE.md`;
- read current state, active batch, next task and report to user;
- no test run was needed for documentation-only handoff.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no polling/webhook;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.

## 2026-07-02 - BATCH_091_AI_PROVIDER_SECRET_GATE_SETUP

Completed universal AI Provider layer by Hermes Agent.

Created:
- `src/hermes_core/ai_provider/contract.py`
- `src/hermes_core/ai_provider/registry.py`
- `src/hermes_core/ai_provider/router.py`
- `src/hermes_core/ai_provider/__init__.py`
- `src/hermes_core/ai_provider/adapters/base.py`
- `src/hermes_core/ai_provider/adapters/mock_adapter.py`
- `src/hermes_core/ai_provider/adapters/gemini_adapter.py`
- `src/hermes_core/ai_provider/adapters/deepseek_adapter.py`
- `src/hermes_core/ai_provider/adapters/local_disabled_adapter.py`
- `src/hermes_core/ai_provider/adapters/ollama_disabled_adapter.py`
- `src/hermes_core/ai_provider/adapters/custom_disabled_adapter.py`
- `src/hermes_core/ai_provider/adapters/__init__.py`
- `tests/test_ai_provider_universal.py`
- `docs/AI_PROVIDER_ARCHITECTURE.md`
- `05_REPORTS/BATCH_091_AI_PROVIDER_SECRET_GATE_SETUP_REPORT.md`

Updated:
- `src/hermes_core/cli.py` — 8 new universal AI provider commands
- `src/hermes_core/smoke.py` — 4 new smoke checks (27 total)
- `00_START/CURRENT_STATE.md`
- `03_TASKS/ACTIVE_BATCH.md`
- `03_TASKS/DONE.md`
- `03_TASKS/NEXT_TASK.md`
- `05_REPORTS/REPORT_TO_USER.md`

Verification:
- tests: 336 passed (309 old + 27 new);
- project audit: 25 checks, 0 failed;
- smoke: 27 checks, 0 failed;
- all 8 new CLI commands verified;
- new provider can be registered without core changes.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no polling/webhook;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.

Completed full packaging, one-command launch and check scripts by Hermes Agent.

Created:
- `pyproject.toml`
- `requirements.txt`
- `scripts\start_local.cmd`
- `scripts\check_local.cmd`
- `scripts\check_full.cmd`
- `05_REPORTS\BATCH_090_PROJECT_PACKAGING_AND_ONE_COMMAND_LAUNCH_REPORT.md`

Updated:
- `START_HERE.md`
- `docs\USER_RUNBOOK_RU.md`
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\DONE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`

Verification:
- tests: 309 passed;
- project audit: 25 checks, 0 failed;
- smoke: 23 checks, 0 failed;
- malyarka fixtures: 12/12;
- malyarka-dialog, malyarka-transcript, telegram-flow — all OK.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no polling/webhook;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.

Completed safe local Malyarka dialog and compatibility reconciliation by Codex.

Created:
- `src\hermes_modules\malyarka\dialog_bridge.py`
- `tests\test_malyarka_dialog_bridge.py`
- `tests\test_malyarka_compatibility_layer.py`
- `tests\test_telegram_dry_run_safety_bridge.py`
- `05_REPORTS\BATCH_089_MACRO_MALYARKA_DIALOG_AND_COMPATIBILITY_RECONCILIATION_REPORT.md`

Updated:
- `src\hermes_clean\malyarka_dialog_commands.py`
- `src\hermes_clean\malyarka_transcript_report.py`
- `src\hermes_clean\telegram_flow_runner.py`
- `src\hermes_core\cli.py`
- `src\hermes_core\smoke.py`
- `src\hermes_modules\malyarka\__init__.py`
- dialog / transcript / telegram-flow tests
- `00_START\CURRENT_STATE.md`
- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`

Checks:
- tests: 309 passed;
- project audit: 25 checks, 0 failed;
- smoke: 23 checks, 0 failed;
- required Malyarka and report commands passed.

Safety:
- no `.env` reading;
- no token or key reading;
- no external APIs;
- no live Telegram;
- no polling/webhook;
- no real orders;
- no Google Drive change;
- no old project or archive change;
- no delete operations.

---

## 2026-07-24 - MALYARKA_DRIVE_DOCUMENTS_LOCAL_IMPORT

Completed Malyarka working-document migration from the verified local Google Drive export.

Created:
- `00_START\MALYARKA_DOCUMENT_INDEX.md`
- five normalized templates in `docs\malyarka_templates\`
- `docs\malyarka_reference_orders\README.md`
- three reference orders in `docs\malyarka_reference_orders\`
- `05_REPORTS\MALYARKA_DRIVE_DOCUMENTS_IMPORT_2026-07-24.md`

Updated:
- `AGENTS.md`
- `00_START\HERMES_PRICE_STOCK_DRAFT.md`
- `src\hermes_clean\fixtures.py`
- `tests\test_fixtures.py`
- project state, active batch, next task and user report.

Checks:
- 17 source DOCX read;
- 8/8 required working files present;
- 8 index links valid;
- targeted tests: 10 passed;
- full suite: 810 passed, 13 unrelated old path/CLI/environment failures.

Safety:
- Google Drive unchanged;
- no deletes;
- no `.env`, tokens or secrets read;
- no live gateway changes;
- no real export.

---

## 2026-07-24 - MALYARKA_MATERIAL_PRICES_FROM_INVOICES

- Распознаны три накладные со скриншотов.
- В `00_START\HERMES_PRICE_STOCK_DRAFT.md` добавлены 10 уникальных кодов материалов и подтверждённые цены.
- PGP301 удалён из списка материалов с неизвестной ценой.
- По правилу пользователя все материалы и цены приведены к килограммам; тип материалов не выдумывался.
- Контрольные суммы: 129 700 тг, 65 000 тг, 63 780 тг.
- Google Drive и реальные заказы не изменялись.

---

## 2026-07-24 - GOOGLE_DRIVE_REBUILD_MANIFEST_PREPARED

- Подготовлен `00_START\GOOGLE_DRIVE_REBUILD_MANIFEST.md`.
- Зафиксирована структура `МАЛЯРКА — УПРАВЛЕНИЕ` с категориями `00`–`05`.
- Выбраны 16 канонических файлов Hermes-Clean.
- Проверено: 16/16 существуют, битых ссылок нет, секретных маркеров нет.
- Реальные заказы и клиентские исходники исключены.
- Исправлен текущий путь Hermes-Clean в `PROJECT_RULES.md`.
- Историческая цена 23 600 тг/м² явно запрещена для новых расчётов.
- Google Drive не изменялся; пользователь очищает его самостоятельно.

---

## 2026-07-24 - GOOGLE_DRIVE_REBUILD_COMPLETED

- OAuth восстановлен только для Drive, Docs и Sheets.
- Пользователь самостоятельно очистил Drive; Hermes подтвердил `0` активных объектов перед записью.
- Создана структура `МАЛЯРКА — УПРАВЛЕНИЕ`: 7 папок и 16 Google-документов.
- После временной ошибки Google `HTTP 500` загрузка безопасно продолжена без дублей.
- Проверено чтением через API: 23 объекта, 7 папок, 16 документов.
- Пустых документов: 0; дублей: 0; публичных и доменных разрешений: 0.
- Результат сохранён в `05_REPORTS\GOOGLE_DRIVE_REBUILD_RESULT_2026-07-24.json`.
