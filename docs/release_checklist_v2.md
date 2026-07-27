# Release Checklist v2 — Hermes-Clean

**Версия:** Local Safe Release Candidate v2
**Дата:** 2026-06-30
**Путь:** `C:\Users\user\Desktop\Hermes-Clean`

---

## Этап 1. Проверка изоляции

- [x] **1.1** .env файлы отсутствуют в контуре
  - `SecretGuard().check_env_files()` → `found: false`
- [x] **1.2** os.environ не содержит секретов контура
  - `SecretGuard().check_os_environ()` → `has_secrets: false`
- [x] **1.3** Код не содержит реальных секретов
  - `SecretGuard().validate_no_real_secrets()` → empty
- [x] **1.4** Mock-провайдеры изолированы
  - `MockProvider.validate_key(real_key)` → `SecretAccessError`

---

## Этап 2. Проверка блокировок

- [x] **2.1** Google Drive заблокирован
  - `GDriveStub().read_file(path)` → `403 appNotAuthorizedToFile`
  - После первой попытки — freeze (retry невозможен)
- [x] **2.2** Сеть не используется
  - Никаких import telebot, aiogram, requests, httpx
- [x] **2.3** Экспорт блокируется при disputes
  - `build_export_model()` → `export_blocked=True`
- [x] **2.4** SafetyViolation при нарушении запретов
  - `add_decision("enable_network", True)` → `SafetyViolation`

---

## Этап 3. Проверка целостности

- [x] **3.1** Все 278 тестов проходят
  - `python -m pytest tests/ -q` → `278 passed`
- [x] **3.2** Task Queue аудит чист
  - `create_default_queue().audit()` → `is_consistent=True` (после полного цикла)
- [x] **3.3** Memory Sync integrity
  - `MemorySync().check_integrity()` → `is_consistent=True`
- [x] **3.4** State Machine переходы валидны
  - Все разрешённые переходы тестированы

---

## Этап 4. Проверка документации

- [x] **4.1** README.md в корне (если применимо)
- [x] **4.2** docs/ содержит 6 артефактов
- [x] **4.3** Статус-файлы (00_START, 03_TASKS, 05_REPORTS) обновлены

---

## Этап 5. Проверка готовности к передаче

- [x] **5.1** Память и актуальные правила находятся внутри Hermes-Clean; перенос в [архив] [удалённый архив] запрещён как устаревший маршрут
- [ ] **5.2** Интеграция с Telegram Gateway (если требуется)
- [ ] **5.3** Подключение реального экспорта (требует approval)
- [ ] **5.4** Разблокировка GDrive (требует approval администратора)
