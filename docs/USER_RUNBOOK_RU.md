# РАНБУК ПОЛЬЗОВАТЕЛЯ HERMES-CLEAN

## Minimal context для нового чата

Чтобы новый Hermes/Codex чат не открывался с перегруженным контекстом, читать только:

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

Готовые промпты:

```text
00_MEMORY\START_NEW_HERMES_CHAT_PROMPT.md
00_MEMORY\START_NEW_CODEX_CHAT_PROMPT.md
```

Не автозагружать весь `05_REPORTS`, весь `src`, весь `tests`, старые проекты, архивы, Google Drive данные и реальные заказы.

> Русская инструкция по ежедневной работе с Hermes-Clean.
> Все команды локальные. Telegram, API, Google Drive не используются.

---

## 1. ЕЖЕДНЕВНЫЙ ЗАПУСК (одна команда)

```cmd
cd C:\Users\user\Desktop\Hermes-Clean
scripts\start_local.cmd
```

Эта команда запускает полный цикл проверки:
- обновление состояния;
- панель управления;
- дымковые проверки (smoke);
- статус runtime;
- статус Malyarka;
- аудит безопасности.

После завершения открой `05_REPORTS\LOCAL_DASHBOARD.md`.

---

## 2. ПОЛНАЯ ЛОКАЛЬНАЯ ПРОВЕРКА

### Стандартная (10 проверок):

```cmd
scripts\check_local.cmd
```

### Полная (27 проверок — все команды и тесты):

```cmd
scripts\check_full.cmd
```

---

## 3. КОМАНДЫ CLI

### Состояние проекта

| Команда | Что делает |
|---------|------------|
| `hermes.cmd dashboard` | Полная панель управления |
| `hermes.cmd app-status` | Runtime: что включено/выключено |
| `hermes.cmd daily-report` | Ежедневный отчёт |
| `hermes.cmd project-audit` | Аудит безопасности и структуры (25 проверок) |
| `hermes.cmd status` | Короткий статус |
| `hermes.cmd start-summary` | Стартовая сводка |
| `hermes.cmd health` | Проверка здоровья проекта |
| `hermes.cmd help-local` | Список всех 35+ команд |

### Задачи и память

| Команда | Что делает |
|---------|------------|
| `hermes.cmd tasks` | Текущая очередь задач |
| `hermes.cmd memory` | Проектная память (решения, запреты) |
| `hermes.cmd reports` | Индекс всех отчётов |

### Telegram (ТОЛЬКО dry-run)

| Команда | Что делает |
|---------|------------|
| `hermes.cmd telegram-flow --case clean` | Чистый заказ (dry-run) |
| `hermes.cmd telegram-flow --case disputed` | Спорный заказ (dry-run) |
| `hermes.cmd telegram-scenarios` | Прогнать 18 сценариев |
| `hermes.cmd telegram-status` | Статус Telegram dry-run |
| `hermes.cmd message /status` | Сухой статус |
| `hermes.cmd message /order краска \| 2 \| ведро` | Сухой заказ |
| `hermes.cmd message /disputes` | Сухие споры |
| `hermes.cmd message /export-blocked` | Причины блокировки экспорта |

### Malyarka (ТОЛЬКО synthetic)

| Команда | Что делает |
|---------|------------|
| `hermes.cmd malyarka-status` | Статус модуля Malyarka |
| `hermes.cmd malyarka-demo` | Демо модуля |
| `hermes.cmd malyarka-fixtures` | 12 синтетических фикстур |
| `hermes.cmd malyarka-disputes` | Классификация споров (8 типов) |
| `hermes.cmd malyarka-combined` | Парсинг + споры + цены |
| `hermes.cmd malyarka-dialog --script clean` | Диалог: чистый заказ |
| `hermes.cmd malyarka-dialog --script disputed` | Диалог: спорный заказ |
| `hermes.cmd malyarka-transcript --script clean` | Протокол: чистый |
| `hermes.cmd malyarka-transcript --script disputed` | Протокол: спорный |
| `hermes.cmd malyarka-pricing` | Синтетические цены |
| `hermes.cmd malyarka-schema` | Схема экспорта |
| `hermes.cmd malyarka-workflow` | Полный workflow |

### Безопасность

| Команда | Что делает |
|---------|------------|
| `hermes.cmd safety delete` | Проверить gate (покажет BLOCKED) |
| `hermes.cmd safety-audit` | Аудит-лог безопасности |
| `hermes.cmd ai-provider` | Выбор провайдера (только mock) |
| `hermes.cmd review-provider` | Выбор review-провайдера |

### Финальные проверки

| Команда | Что делает |
|---------|------------|
| `hermes.cmd smoke` | 23 дымковые проверки |
| `scripts\run_tests.cmd` | 309+ тестов |
| `scripts\check_local.cmd` | Стандартная проверка (10 шагов) |
| `scripts\check_full.cmd` | Полная проверка (27 шагов) |
| `scripts\start_local.cmd` | Ежедневный запуск (одна команда) |

---

## 4. ГДЕ СМОТРЕТЬ

| Файл | Содержание |
|------|------------|
| `05_REPORTS\LOCAL_DASHBOARD.md` | Главная панель |
| `05_REPORTS\DAILY_LOCAL_REPORT.md` | Ежедневный отчёт |
| `05_REPORTS\LOCAL_PROJECT_AUDIT.md` | Результаты аудита |
| `05_REPORTS\LOCAL_RUNTIME_STATUS.md` | Статус подсистем |
| `05_REPORTS\MALYARKA_MODULE_STATUS.md` | Статус модуля Malyarka |
| `05_REPORTS\MALYARKA_DISPUTE_CLASSIFICATION_REPORT.md` | Отчёт по спорам |
| `05_REPORTS\REPORT_TO_USER.md` | История выполненных блоков |
| `03_TASKS\NEXT_TASK.md` | Следующая задача |
| `00_START\CURRENT_STATE.md` | Текущее состояние проекта |

---

## 5. ЗАПРЕТЫ

### НИКОГДА без отдельного разрешения:

- ❌ Читать `.env`, токены, ключи
- ❌ Запускать live Telegram (polling/webhook)
- ❌ Подключать реальные AI-провайдеры (Gemini, DeepSeek)
- ❌ Читать/менять реальные заказы
- ❌ Менять Google Drive
- ❌ Распаковывать старые архивы как рабочие проекты
- ❌ Удалять файлы
- ❌ Использовать synthetic Malyarka как реальный расчёт

### Approval gates (что нужно явно одобрить):

| Gate | Для чего |
|------|----------|
| `APPROVE_SECRET_SETUP` | Включить Gemini / DeepSeek API |
| `APPROVE_TELEGRAM_LIVE` | Запустить live Telegram бот |
| `APPROVE_REAL_ORDER_ACCESS` | Доступ к реальным заказам |
| `APPROVE_GOOGLE_DRIVE_MOVE` | Перенос файлов на Google Drive |
| `APPROVE_ARCHIVE_UNPACK` | Распаковка старых архивов |
| `APPROVE_DELETE` | Удаление файлов |

---

## 6. РЕЖИМЫ БЕЗОПАСНОСТИ

### SAFE (можно всегда)

Операции, которые безопасны всегда:
- создание локальных отчётов;
- dry-run команды;
- локальные тесты;
- чтение файлов проекта;
- аудит безопасности.

### CONFIRM_REQUIRED (нужно одобрение)

Операции, требующие gate:
- внешние API → `APPROVE_SECRET_SETUP`
- токены/ключи → `APPROVE_SECRET_SETUP`
- live Telegram → `APPROVE_TELEGRAM_LIVE`
- реальные заказы → `APPROVE_REAL_ORDER_ACCESS`
- Google Drive → `APPROVE_GOOGLE_DRIVE_MOVE`

### BLOCKED (заблокировано всегда)

Операции, которые нельзя выполнять:
- удаление файлов;
- изменение старых проектов;
- live Telegram polling/webhook;
- чтение секретов;
- изменение реальных заказов.

---

## 7. ДЕЙСТВИЯ ПРИ APPROVAL GATE

Когда Hermes говорит `BLOCKED` или `CONFIRM_REQUIRED`:

1. Прочитай причину блокировки.
2. Проверь, нужна ли тебе эта операция реально.
3. Если нужна — дай явную команду с approval phrase:
   ```
   APPROVE_SECRET_SETUP
   ```
4. Hermes выполнит ТОЛЬКО эту одобренную операцию.
5. После выполнения gate снова закрывается.

---

## 8. ЕСЛИ ЧТО-ТО СЛОМАЛОСЬ

```cmd
cd C:\Users\user\Desktop\Hermes-Clean
scripts\check_local.cmd
```

Если тесты падают — смотри `05_REPORTS\LOCAL_PROJECT_AUDIT.md` → «Actionable Findings».

---

## 9. ПОСЛЕ ПЕРЕЗАГРУЗКИ ПК

```cmd
cd C:\Users\user\Desktop\Hermes-Clean
scripts\start_local.cmd
```

Готово. Открой `05_REPORTS\LOCAL_DASHBOARD.md` и работай.

---

## 10. ЧТО ВКЛЮЧЕНО / ВЫКЛЮЧЕНО

### Включено (6 подсистем)

| Подсистема | Режим |
|-----------|-------|
| `local_cli` | Локальный CLI |
| `dashboard` | Локальный markdown |
| `smoke_tests` | Локальные тесты |
| `telegram_dry_run` | Только dry-run |
| `malyarka_synthetic` | Только synthetic |
| `mock_ai_provider` | Только mock |

### Выключено (6 подсистем)

| Подсистема | Gate для включения |
|-----------|-------------------|
| `live_telegram` | `APPROVE_TELEGRAM_LIVE` |
| `real_ai_providers` | `APPROVE_SECRET_SETUP` |
| `google_drive_write` | `APPROVE_GOOGLE_DRIVE_MOVE` |
| `real_order_access` | `APPROVE_REAL_ORDER_ACCESS` |
| `archive_import` | `APPROVE_ARCHIVE_UNPACK` |
| `delete_files` | `APPROVE_DELETE` |
