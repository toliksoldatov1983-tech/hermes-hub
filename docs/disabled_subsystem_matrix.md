# Disabled Subsystem Matrix — Hermes-Clean

## Легенда

| Символ | Значение |
|--------|----------|
| 🔴 | Полностью отключено / заблокировано |
| 🟡 | Эмуляция / заглушка |
| 🟢 | Работает на 100% |

---

## Матрица

| Подсистема | Статус | Замена | Механизм блокировки |
|-----------|--------|--------|---------------------|
| **Telegram API** | 🔴 | `TelegramDialogFlow` — эмулятор 6 шагов | `no_live_telegram` prohibition |
| **Google Drive** | 🔴 | `gdrive_manual/` — ручное размещение | `GDriveStub` → 403 + freeze |
| **Сеть / HTTP** | 🔴 | Нет, весь код локальный | `no_external_network` prohibition |
| **Реальные API-ключи** | 🔴 | `MockProvider` с mock-key-placeholder | `no_real_api_keys` prohibition + SafetyViolation |
| **Токены аутентификации** | 🔴 | Не используются | `no_real_tokens` prohibition |
| **База заказов (orders.db)** | 🔴 | Синтетические фикстуры | `no_database_write` prohibition |
| **CorelDraw экспорт (.xlsx)** | 🟡 | `build_export_model()` → dict | Export Gate — блокировка при disputes |
| **Excel-генерация (openpyxl)** | 🟡 | Не портирована | Убрана при адаптации |
| **AI/LLM провайдеры** | 🟡 | `MockProvider.request()` → `[MOCK]` | `validate_key()` → SecretAccessError |
| **Валидация заказов** | 🟢 | `validation.py` — 8 проверок | — |
| **Dispute Resolver** | 🟢 | 7 шаблонов, 4 действия | — |
| **State Machine** | 🟢 | 7 состояний, 10+ переходов | — |
| **Task Queue** | 🟢 | 7 задач, audit, dashboard | — |
| **Memory Sync** | 🟢 | 5 запретов, 5 правил, approvals | — |
| **Secret Guard** | 🟢 | 7 SECRET_PATTERNS, sanitize | — |
| **Preview Report** | 🟢 | 6 блоков, markdown | — |
| **Фикстуры** | 🟢 | 11 синтетических | — |
| **Парсинг заказов** | 🟢 | Built-in (2-3 числа → confirmed) | — |

---

## Сводка

| Статус | Количество |
|--------|-----------|
| 🔴 Полностью отключено | 6 |
| 🟡 Эмуляция / заглушка | 3 |
| 🟢 Работает | 9 |
| **Всего** | **18 подсистем** |
