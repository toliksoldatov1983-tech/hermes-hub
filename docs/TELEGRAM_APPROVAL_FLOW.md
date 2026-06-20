# TELEGRAM APPROVAL FLOW — Модель подтверждения опасных действий

Дата: 2026-06-21
Статус: PLAN-ONLY. Не реализовано. Ждёт Phase 2.
Применение: будущий Telegram-интерфейс Hermes Hub.

---

## Главное правило

```
Лучше stop и спросить, чем выполнить опасное действие без разрешения.
```

---

## 🎯 Какие действия требуют точной approval-фразы

| Действие | Approval-фраза | Формат |
|----------|---------------|--------|
| Чтение .env / token / config.py | `РАЗРЕШАЮ_ЧИТАТЬ_SECRETS` | Точная фраза |
| Чтение orders.db / логов / заказов | `РАЗРЕШАЮ_ЧИТАТЬ_DATA` | Точная фраза |
| SSH read-only доступ | `РАЗРЕШАЮ_SSH_READ_ONLY` | Точная фраза |
| Чтение старого архива | `РАЗРЕШАЮ_ЧИТАТЬ_ARCHIVE` | Точная фраза |
| systemctl start (controlled) | `APPROVE_SERVER_BOT_CONTROLLED_START_ONCE` | Точная фраза |
| systemctl restart (controlled) | `APPROVE_CONTROLLED_RESTART_ONCE` | Точная фраза |
| systemctl enable (autostart) | `APPROVE_ENABLE_AUTOSTART` | Точная фраза |
| Phase 2 dry-run | `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE` | Точная фраза |
| Live adapter patch | `APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE` | Точная фраза |
| Production enable | `APPROVE_PRODUCTION_ENABLE` | Точная фраза |
| git push | `РАЗРЕШАЮ_GIT_PUSH` | Точная фраза |
| git commit | `РАЗРЕШАЮ_GIT_COMMIT` | Точная фраза |

---

## 🚫 Какие фразы НЕ считаются approval

| Фраза | Почему нет |
|--------|-----------|
| «да» | Слишком размыто |
| «ок» | Не указывает, что именно разрешено |
| «+» | Непонятно |
| «продолжай» | Нет границ |
| «делай дальше» | Непонятно что |
| «посмотри сервер» | Не даёт права на действия |
| «проверь бота» | Не даёт права на restart/patch |
| «давай» | Размыто |
| «можно» | Не указывает scope |
| Любая фраза, не совпадающая с точной approval-фразой | — |

---

## 🔄 Процесс approval

### Шаг 1: Hermes обнаруживает опасное действие

```
Hermes: «Для этого действия требуется approval.
         Отправьте точную фразу: APPROVE_...»
```

### Шаг 2: Пользователь отправляет approval-фразу

```
User: «APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE»
```

### Шаг 3: Hermes проверяет фразу

- Совпадает с реестром `sync/APPROVAL_GATES.md`? → ✅
- Не совпадает? → ❌ «Фраза не распознана. Ожидается: APPROVE_...»

### Шаг 4: Hermes выполняет действие

- Только одно действие на одну фразу.
- Перед выполнением: precheck.
- После выполнения: regression check.

### Шаг 5: Hermes докладывает

```
Hermes: «Выполнено: Phase 2 dry-run.
         Результат: 700x500 → Malyarka flow ✓.
         Feature flag возвращён в OFF.»
```

---

## 🛑 Когда остановиться (STOP conditions)

| Ситуация | Действие |
|----------|----------|
| Пользователь дал размытую фразу | **STOP.** Запросить точную. |
| Approval-фраза не совпадает с реестром | **STOP.** Показать ожидаемую. |
| Действие выходит за границы approval | **STOP.** Запросить новый approval. |
| Precheck не прошёл | **STOP.** Сообщить причину. |
| Обнаружен секрет в выводе | **STOP.** Не показывать. |
| Неясно, safe или unsafe | **STOP.** Спросить пользователя. |

---

## 🔐 Особые зоны

### Server / Service

- `systemctl start` — только controlled, с backup и rollback-планом.
- `systemctl stop` — только controlled, с подтверждением пользователя.
- `systemctl enable` — только после отдельного approval.
- Никаких `systemctl` без approval.

### Phase 2 / Production

- Phase 2 — только dry-run сначала.
- Production — только после успешного Phase 2.
- Feature flag — OFF по умолчанию, временный ON только для dry-run.

### Git

- `git commit` — только локально, с проверкой diff.
- `git push` — только с approval.
- Никаких `git reset --hard` / `git checkout`.

### Secrets

- **Никогда не читать без approval.**
- Даже с approval — не показывать значения в чате.
- Presence-only: «файл существует».

---

## 📋 Памятка для Hermes

```
1. Видишь опасное действие → STOP.
2. Запрашиваешь точную approval-фразу.
3. Проверяешь по реестру APPROVAL_GATES.md.
4. Выполняешь ОДНО действие.
5. Докладываешь результат.
6. Делаешь regression check.
```
