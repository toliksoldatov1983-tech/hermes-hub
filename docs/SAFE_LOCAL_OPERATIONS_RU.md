# БЕЗОПАСНЫЕ ЛОКАЛЬНЫЕ ОПЕРАЦИИ HERMES-CLEAN

> Что можно делать всегда, что требует одобрения, и как работают gates.

---

## 1. SAFE ПО УМОЛЧАНИЮ

Эти операции можно выполнять в любой момент без разрешения:

| Операция | Пример |
|----------|--------|
| Создать локальный отчёт | `hermes.cmd dashboard` |
| Обновить состояние | `hermes.cmd refresh-all` |
| Сухой запуск (dry-run) | `hermes.cmd message /status` |
| Локальный тест | `scripts\run_tests.cmd` |
| Чтение проектных файлов | `hermes.cmd tasks` |
| Аудит безопасности | `hermes.cmd project-audit` |

---

## 2. CONFIRM_REQUIRED (требуется одобрение)

Эти операции требуют явного разрешения:

| Операция | Gate |
|----------|------|
| Чтение внешней папки | Подтверждение пользователя |
| Чтение старого архива | `APPROVE_ARCHIVE_UNPACK` |
| Чтение Google Drive документа | `APPROVE_GOOGLE_DRIVE_MOVE` |
| Внешний API | `APPROVE_SECRET_SETUP` |
| Работа с токенами | `APPROVE_SECRET_SETUP` |
| Подключение Telegram | `APPROVE_TELEGRAM_LIVE` |

### Как одобрить:

1. Hermes скажет: `CONFIRM_REQUIRED`
2. Ты говоришь: `APPROVE_SECRET_SETUP` (или другой gate)
3. Hermes выполняет одобренную операцию
4. Gate автоматически закрывается после операции

---

## 3. BLOCKED (заблокировано)

Эти операции заблокированы всегда без отдельного risk-control плана:

| Операция | Почему |
|----------|--------|
| Удаление файлов | Необратимо |
| Изменение старых проектов | Архив |
| Изменение реальных заказов | Клиентские данные |
| Live Telegram | Внешний сервис |
| Чтение секретов | Безопасность |
| Изменение прав доступа | Безопасность |
| Отправка файлов наружу | Безопасность |

---

## 4. ПОДСИСТЕМЫ: ЧТО ВКЛЮЧЕНО / ВЫКЛЮЧЕНО

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

---

## 5. КАК ПРОВЕРИТЬ БЕЗОПАСНОСТЬ

```cmd
rem Проверить конкретное действие через safety gate
scripts\hermes.cmd safety delete          → BLOCKED
scripts\hermes.cmd safety create_local_report → SAFE
scripts\hermes.cmd safety connect_telegram → CONFIRM_REQUIRED

rem Посмотреть аудит-лог
scripts\hermes.cmd safety-audit

rem Полный аудит
scripts\hermes.cmd project-audit
```

---

## 6. БЛОКИРОВАННЫЕ ДЕЙСТВИЯ (18)

| Категория | Кол-во | Примеры |
|-----------|--------|---------|
| telegram | 4 | live_polling, live_webhook, send_message, live_bot_start |
| secrets | 4 | token_read, env_read, key_access, secret_storage |
| orders | 3 | real_order_read, real_order_modify, client_data_access |
| export | 3 | file_export, real_excel_create, external_send |
| external | 4 | external_api, google_drive_write, google_drive_move, archives_access |

---

## 7. ПРОВЕРКА ПЕРЕД ЗАПУСКОМ НОВОГО БЛОКА

```cmd
scripts\hermes.cmd health          ← нет .env
scripts\hermes.cmd smoke           ← 20/20 OK
scripts\run_tests.cmd              ← 187+ passed
scripts\hermes.cmd project-audit   ← 25/25 OK
```

Если всё OK — можно работать. Если FAIL — смотри `LOCAL_PROJECT_AUDIT.md` → Actionable Findings.
