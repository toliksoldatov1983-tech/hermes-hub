# Acceptance Criteria — Hermes-Clean Release Candidate v2

## 1. Все тесты зелёные

| Критерий | Статус |
|----------|--------|
| `pytest tests/ -q` | ✅ **278 passed, 0 failed** |
| Все модули покрыты | ✅ 12 модулей, каждый с тестами |
| Нет skipped/errored тестов | ✅ 0 skipped, 0 errors |

## 2. Изоляция сети

| Критерий | Статус |
|----------|--------|
| Нет сетевых библиотек | ✅ нет requests, httpx, aiohttp |
| Нет telebot/aiogram | ✅ только эмуляция |
| Google Drive заблокирован | ✅ 403 appNotAuthorizedToFile + freeze |
| SecretGuard не даёт включить сеть | ✅ SafetyViolation при `enable_network` |

## 3. Заглушки активны

| Заглушка | Статус |
|----------|--------|
| MockProvider | ✅ `mock-key-placeholder`, `request()` → `[MOCK]` |
| TelegramDialogFlow | ✅ 6 шагов, без Telegram API |
| GDriveStub | ✅ все операции → 403 + freeze |
| Export Gate | ✅ блокировка при disputes |

## 4. Целостность данных

| Критерий | Статус |
|----------|--------|
| State Machine: 7 состояний | ✅ все переходы тестированы |
| Task Queue: audit без нарушений | ✅ после полного цикла |
| Memory Sync: integrity consistent | ✅ |
| Preview Report: 6 блоков | ✅ confirmed, disputed, validation, pricing, export, action |
| Dispute Resolver: 7 шаблонов | ✅ все причины покрыты |

## 5. Безопасность

| Критерий | Статус |
|----------|--------|
| Нет доступа к .env | ✅ SecretGuard блокирует |
| Нет реальных ключей в коде | ✅ sanitize() → [REDACTED] |
| SafetyViolation при нарушении | ✅ 5 запретов, 5 правил |
| Pending approvals | ✅ MemorySync.approve() обязателен |

## Итог

| Критерий | Результат |
|----------|-----------|
| Общее количество тестов | 278 |
| Пройдено | 278 (100%) |
| Провалено | 0 |
| Модулей | 12 |
| Статус | ✅ **RELEASE CANDIDATE v2 — ПРИНЯТ** |
