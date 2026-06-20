# HERMES-RULE-CONVEYOR-001

Created: 2026-06-17
Source: `hermes_hub_accelerated_conveyor_2026-06-17.zip`
Installed: 2026-06-17 by Hermes (deepseek-v4-pro)

## Назначение

Полуавтоматический конвейер по bundle-пакетам проекта Hermes Hub / Malyarka Clean.

- Ускорить работу без ручной передачи каждого пакета через ChatGPT.
- Сохранить stop-gates на опасных местах.
- Не дать Hermes/Codex перейти в server/live/runtime/secrets без отдельного разрешения.

## Ключевой принцип

Hermes/Codex НЕ должен проходить всё вслепую. Он должен идти по MANIFEST строго по порядку, выполнять только разрешённые safe/offline/local этапы и останавливаться на gate/риске/неоднозначности.

## Порядок работы

1. Прочитать README.md, MANIFEST.md, SAFETY_RULES.md, STOP_AND_REPORT_TEMPLATE.md из архива конвейера.
2. Проверить реальную локальную папку: `E:\Hermes-Hub\task_bundles`.
3. Найти первый missing или incomplete bundle по MANIFEST.
4. Если bundle отсутствует в `E:\Hermes-Hub\task_bundles`, но есть в архиве — скопировать/создать bundle-папку с `TASK.md` и `README_FOR_CODEX.md` (markdown-only).
5. Выполнять только bundle со статусом:
   - **AUTO_MARKDOWN** — автоматически (markdown-only).
   - **AUTO_LOCAL_ONLY** — только если действие строго локальное и не трогает server/live/secrets/real orders.
6. На bundle со статусом **STOP_REVIEW** или **STOP_APPROVAL** — остановиться и вернуть отчёт.

## MANIFEST (порядок bundles)

| Order | Bundle | Type | Autonomy |
|------:|--------|------|----------|
| 1 | BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP | PACKAGE_PREP_ONLY | AUTO_MARKDOWN |
| 2 | BUNDLE_271_300_LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS | LOCAL_IMPLEMENTATION_ALLOWED | AUTO_LOCAL_ONLY |
| 3 | BUNDLE_301_330_TINY_GUARDED_CALLSITE_PLAN | PLAN_ONLY | AUTO_MARKDOWN |
| 4 | BUNDLE_331_360_SERVER_PATCH_READINESS_GATE | GATE_ONLY | **STOP_REVIEW** |
| 5 | BUNDLE_361_390_SERVER_PATCH_PLAN_ONLY | PLAN_ONLY | AUTO_MARKDOWN |
| 6 | BUNDLE_391_420_SERVER_PATCH_PREPARE_DIFF_ONLY | DIFF_PREP_ONLY | STOP_REVIEW |
| 7 | BUNDLE_421_450_SERVER_PATCH_DIFF_DRAFT_ONLY | DIFF_DRAFT_ONLY | STOP_REVIEW |
| 8 | BUNDLE_451_480_SERVER_PATCH_DRY_RUN_RECHECK_PLAN | PLAN_ONLY | AUTO_MARKDOWN |
| 9 | BUNDLE_481_510_SERVER_PATCH_FINAL_APPROVAL_GATE | GATE_ONLY | **STOP_APPROVAL** |
| 10 | BUNDLE_511_540_SERVER_PATCH_BUNDLE_PREP_ONLY | PACKAGE_PREP_ONLY | AUTO_MARKDOWN |
| 11 | BUNDLE_541_570_SERVER_PATCH_EXECUTION_PLAN_DRAFT | PLAN_DRAFT_ONLY | STOP_REVIEW |
| 12 | BUNDLE_571_600_SERVER_PATCH_APPLY_APPROVAL_GATE | GATE_ONLY | **STOP_APPROVAL** |
| 13 | BUNDLE_601_630_SERVER_PATCH_APPLY_ONLY_PREP | PACKAGE_PREP_ONLY | STOP_REVIEW |
| 14 | BUNDLE_631_660_SERVER_PATCH_APPLY_DRY_RUN_PACKAGE | DRY_RUN_PACKAGE_ONLY | STOP_REVIEW |
| 15 | BUNDLE_661_690_SERVER_PATCH_POST_DRY_RUN_REVIEW | REVIEW_ONLY | AUTO_MARKDOWN |
| 16 | BUNDLE_691_720_LIVE_ACTIVATION_READINESS_PLAN | PLAN_ONLY | STOP_REVIEW |
| 17 | BUNDLE_721_750_LIVE_ACTIVATION_GATE_ONLY | GATE_ONLY | **STOP_APPROVAL** |
| 18 | BUNDLE_751_780_LIVE_ACTIVATION_PACKAGE_PREP_ONLY | PACKAGE_PREP_ONLY | STOP_REVIEW |
| 19–44 | Диагностические и runtime bundles (см. полный MANIFEST в архиве) | various | mostly STOP_REVIEW / STOP_APPROVAL |

## Абсолютные запретные зоны

- server
- `/opt/malyarka-telegram-bot`
- live Telegram bot
- polling / webhook
- Telegram API calls
- token / `.env` / `config.py` contents / `os.environ`
- database / log / order contents
- real orders
- private IDs / API keys
- production / staging code
- Vision / API
- `.git` / commit / push
- Corel / ArtCAM / CNC
- export / admin / write actions (кроме явно разрешённых markdown-only)

## Короткие команды — не разрешения

Не считать разрешением: `+`, `ок`, `да`, `продолжай`, `делай`, `включай`, `запускай`, `подключай`, `внедряй`, любую короткую/двусмысленную фразу.

## Runtime запрещён

Ни один bundle в этом конвейере не даёт разрешения на: start bot, start polling, start webhook, Telegram API, secrets, real orders, mutation production/staging.

## Разрешённые автоматические действия

- Читать markdown в архиве конвейера.
- Читать markdown в `E:\Hermes-Hub\task_bundles`.
- Создавать отсутствующие bundle-папки из архива.
- Создавать/обновлять markdown-only project docs.
- Для AUTO_LOCAL_ONLY: локальный sandbox код/тесты, только если bundle явно разрешает и не трогает server/live/secrets/real orders.

## Обязательная остановка

Остановиться когда:
- нужен server
- нужен live/runtime
- нужен secret
- нужен real order
- нужна мутация production/staging кода
- gate говорит STOP_REVIEW или STOP_APPROVAL
- предыдущий bundle отсутствует/не завершён
- состояние неоднозначно

## Шаблон отчёта при остановке

```text
CONVEYOR STOP REPORT

bundle:
  name: <BUNDLE_NAME>
  order: <ORDER>
  autonomy: <AUTO_MARKDOWN | AUTO_LOCAL_ONLY | STOP_REVIEW | STOP_APPROVAL>

stop_reason:
  code: <STOP_CODE>
  explanation: <SAFE_SHORT_EXPLANATION>

risk:
  server: <true|false>
  live_bot: <true|false>
  polling_webhook: <true|false>
  telegram_api: <true|false>
  secrets: <true|false>
  real_orders: <true|false>
  production_code: <true|false>
  commit_push: <true|false>
  ambiguity: <true|false>

what_was_done:
  - <SAFE_LIST>

what_was_not_touched:
  - server
  - live bot
  - polling/webhook
  - Telegram API
  - token/.env/config.py/os.environ
  - db/log/order contents
  - real orders
  - production/staging code
  - .git/commit/push

proposed_options:
  1. <OPTION_A>
  2. <OPTION_B>
  3. Ask ChatGPT to prepare next safe package.

needed_user_decision:
  <CLEAR_DECISION_NEEDED>
```

## Архив-источник

Путь к архиву: `C:\Users\user\Desktop\hermes_hub_accelerated_conveyor_2026-06-17.zip`

Файлы архива:
- `README.md` — назначение, порядок, запреты
- `START_FOR_CODEX.md` — главный стартовый файл для Codex
- `MANIFEST.md` — полная таблица 44 bundles с типами и автономией
- `SAFETY_RULES.md` — детальные правила безопасности
- `APPROVAL_GATES.md` — принцип explicit approval
- `STOP_AND_REPORT_TEMPLATE.md` — шаблон отчёта остановки
- `HOW_TO_INSTALL_ON_E_DRIVE.md` — ручная установка
- `context/00_MASTER_CONTEXT.md` — контекст проекта
- `context/01_CURRENT_STATUS.md` — текущий статус
- `task_bundles/` — 44 bundle-папки с TASK.md и README_FOR_CODEX.md
