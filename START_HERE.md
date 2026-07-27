# START_HERE

## Minimal Context For New Hermes/Codex Chat

To avoid context overload, new chats should not load the whole project.

Read only:

```text
AGENTS.md
START_HERE.md
00_START\CURRENT_STATE.md
03_TASKS\NEXT_TASK.md
05_REPORTS\REPORT_TO_USER.md
00_MEMORY\ACTIVE_CONTEXT.md
00_MEMORY\COMPACT_STATE_FOR_AGENTS.md
00_MEMORY\CONTEXT_LOAD_POLICY.md
```

Ready prompts:

```text
00_MEMORY\START_NEW_HERMES_CHAT_PROMPT.md
00_MEMORY\START_NEW_CODEX_CHAT_PROMPT.md
```

Do not autoload all reports, all source, all tests, old projects, archives, Google Drive data or real orders.

Hermes-Clean — локальная dry-run среда для ассистента Hermes (Маларка).

**Путь проекта:**
```text
C:\Users\user\Documents\«Гермес Клин»
```

## Быстрый старт (одна команда)

```cmd
scripts\start_local.cmd
```

Эта команда запускает:
- refresh-all → dashboard → smoke → app-status → malyarka-status → safety-audit

## Утренний запуск

```cmd
cd C:\Users\user\Documents\«Гермес Клин»
scripts\hermes.cmd refresh-all
scripts\hermes.cmd dashboard
scripts\hermes.cmd smoke
```

После этого открой: `05_REPORTS\LOCAL_DASHBOARD.md`

## Полная локальная проверка

Стандартная:
```cmd
scripts\check_local.cmd
```

Полная (27 проверок):
```cmd
scripts\check_full.cmd
```

## Основные команды

```cmd
scripts\hermes.cmd dashboard         - панель управления
scripts\hermes.cmd app-status        - статус runtime (вкл/выкл)
scripts\hermes.cmd daily-report      - ежедневный отчёт
scripts\hermes.cmd project-audit     - аудит безопасности (25 проверок)
scripts\hermes.cmd smoke             - дымковые проверки (23)
scripts\hermes.cmd help-local        - список всех команд
scripts\run_tests.cmd                - 309+ тестов
scripts\hermes.cmd release-checklist - чеклист релиза
```

## Текущие цифры

- **50+ CLI команд**
- **586 тестов** (все пройдены)
- **25 project-audit** (все пройдены)
- **27 smoke checks** (все пройдены)
- **8 AI провайдеров** (2 SAFE: mock + mock-review, 6 BLOCKED)
- **Runtime bridge** (21 allowed, 10 blocked actions)
- **Mobile Gateway** (11 API endpoint'ов, localhost:8514)
- **0 `.env` файлов** внутри Hermes-Clean
- **6 подсистем включено**, **6 отключено** (safe-mode)

## Malyarka (dry-run, synthetic)

```cmd
scripts\hermes.cmd malyarka-status         - статус модуля
scripts\hermes.cmd malyarka-demo           - демо модуля
scripts\hermes.cmd malyarka-fixtures       - 12 синтетических фикстур
scripts\hermes.cmd malyarka-disputes       - классификация споров
scripts\hermes.cmd malyarka-combined       - парсинг + споры + цены
scripts\hermes.cmd malyarka-dialog         - диалог оператора
scripts\hermes.cmd malyarka-transcript     - протокол диалога
scripts\hermes.cmd malyarka-pricing        - синтетические цены
scripts\hermes.cmd malyarka-schema         - схема экспорта
scripts\hermes.cmd malyarka-workflow       - полный workflow
```

## Telegram (только dry-run)

```cmd
scripts\hermes.cmd telegram-flow --case clean    - чистый заказ
scripts\hermes.cmd telegram-flow --case disputed - спорный заказ
scripts\hermes.cmd telegram-scenarios            - 18 сценариев
scripts\hermes.cmd telegram-status               - статус dry-run
scripts\hermes.cmd message /status               - сухой статус
```

Live Telegram отключён.

## Daily Assistant (ежедневный помощник)

```cmd
scripts\hermes.cmd daily-assistant    - полный снимок проекта
scripts\hermes.cmd daily-brief        - краткая сводка (один экран)
scripts\hermes.cmd what-next          - следующие шаги
scripts\hermes.cmd local-health       - быстрая проверка здоровья
scripts\hermes.cmd project-status     - быстрый статус проекта
scripts\hermes.cmd malyarka-mode-status - AI-путь Malyarka
```

```cmd
scripts\hermes.cmd bridge daily-assistant   - мост: ежедневный помощник
scripts\hermes.cmd bridge malyarka-status   - мост: статус Malyarka
scripts\hermes.cmd bridge ai-provider-list  - мост: список AI провайдеров
scripts\hermes.cmd bridge secret-gate       - мост: secret gate
scripts\hermes.cmd bridge live-telegram     - мост: ЗАБЛОКИРОВАНО (демо)
```

## Безопасность (safety gates)

| Gate | Назначение |
|------|-----------|
| `APPROVE_SECRET_SETUP` | Включить реальные AI-провайдеры |
| `APPROVE_TELEGRAM_LIVE` | Запустить live Telegram |
| `APPROVE_REAL_ORDER_ACCESS` | Доступ к реальным заказам |
| `APPROVE_GOOGLE_DRIVE_MOVE` | Google Drive запись |
| `APPROVE_ARCHIVE_UNPACK` | Распаковка архивов |
| `APPROVE_DELETE` | Удаление файлов |

## Где смотреть

| Файл | Назначение |
|------|-----------|
| `05_REPORTS\LOCAL_DASHBOARD.md` | Главная панель |
| `05_REPORTS\LOCAL_PROJECT_AUDIT.md` | Результаты аудита |
| `05_REPORTS\LOCAL_RELEASE_CHECKLIST.md` | Чеклист релиза |
| `05_REPORTS\REPORT_TO_USER.md` | История выполненных блоков |
| `docs\USER_RUNBOOK_RU.md` | Полная русская инструкция |
| `docs\SAFE_LOCAL_OPERATIONS_RU.md` | Безопасные операции |
| `00_START\CURRENT_STATE.md` | Текущее состояние |
| `03_TASKS\NEXT_TASK.md` | Следующая задача |

## Что нельзя без отдельного разрешения

- Читать `.env`, токены, ключи
- Запускать live Telegram, polling, webhook
- Подключать реальные AI-провайдеры (Gemini, DeepSeek)
- Работать с реальными заказами
- Менять Google Drive
- Импортировать архивы
- Удалять файлы
