# PROJECT_MEMORY_INDEX

Единая точка входа в память проекта «Гермес Клин».

## Read First

| File | Purpose |
|---|---|
| `AGENTS.md` | Working rules and safety gates for Codex/Hermes. |
| `START_HERE.md` | Fast local startup and main command guide. |
| `00_MEMORY\USER_PROFILE.md` | Постоянные предпочтения и ограничения пользователя. |
| `00_START\CURRENT_STATE.md` | Current project state and latest completed batches. |
| `03_TASKS\NEXT_TASK.md` | The next approved large task. |
| `05_REPORTS\REPORT_TO_USER.md` | Latest user-facing status report. |
| `00_MEMORY\ACTIVE_CONTEXT.md` | Short active memory for new chats. |
| `00_MEMORY\COMPACT_STATE_FOR_AGENTS.md` | Compressed handoff for agents. |
| `00_MEMORY\CONTEXT_LOAD_POLICY.md` | What to load and what not to load. |
| `00_MEMORY\INBOX.md` | Временные мысли и незавершённые входящие. |

## Read Only When Needed

| Area | When to read |
|---|---|
| `docs\USER_RUNBOOK_RU.md` | When user needs operating instructions. |
| `docs\AI_PROVIDER_ARCHITECTURE.md` | When working on AI Provider architecture. |
| `src\hermes_core\ai_provider\` | Only during AI Provider implementation tasks. |
| `src\hermes_modules\malyarka\` | Only during approved Malyarka tasks. |
| `src\hermes_clean\` | Only for compatibility/reference layer checks. |
| `tests\` | Only when implementing or diagnosing tests. |
| `05_REPORTS\LOCAL_DASHBOARD.md` | When current dashboard is needed. |
| `05_REPORTS\LOCAL_PROJECT_AUDIT.md` | When audit findings are needed. |
| `00_MEMORY\ENVIRONMENT.md` | Когда нужны характеристики ПК и установленный CAD/CAM-софт. |
| `00_MEMORY\CNC_FREECAD_CONTEXT.md` | Когда задача относится к станку, оси Z, FreeCAD или шестерням. |
| `00_MEMORY\CORELDRAW_CDR_READONLY_PROCESS.md` | Когда нужно безопасно прочитать размеры и площадь из `.cdr`. |
| `00_START\MALYARKA_DOCUMENT_INDEX.md` | Когда задача относится к Малярке, материалам, ценам или заказам. |
| Skill `hermes-clean-google-drive-sync` | Когда нужно проверить, пересобрать или синхронизировать Google Drive Малярки. |

## Do Not Autoload

| Area | Reason |
|---|---|
| all `05_REPORTS` | Too large; ask for a specific report. |
| all `src` | Too large; read only relevant modules. |
| all `tests` | Too large; read only relevant tests. |
| old archives | Requires approval and is not current truth. |
| old projects | Not current truth. |
| `[удалён]` | Read-only quarantine; do not use as source of decisions. |
| `E:\«Гермес Клин»` | Old/external project, not autoloaded. |
| `E:\[архив] [удалённый архив]` | Данные удалены; пустой путь ожидает удаления при следующей перезагрузке. Не читать и не использовать. |
| Google Drive Малярки | Read-only аудит разрешён. Запись, удаление и общий доступ — только после отдельного подтверждения; содержимое ограничено правилами, ценами, нормами, шаблонами, инструкциями и эталонами. |
| real orders | Gated; do not touch. |
| `.env`, keys, tokens | Forbidden without explicit approval. |

## Main Truth

The source of truth is:

```text
C:\Users\user\Documents\«Гермес Клин»
```

Старые Hermes-Hub, Hermes-General, Hermes-Clean и внешние архивы не являются рабочей памятью и не могут переопределять данные проекта «Гермес Клин».

