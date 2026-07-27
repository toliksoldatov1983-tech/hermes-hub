# BATCH_118 — OPERATOR DECISION MATRIX

## Вариант A: Продолжить safe-hold (default)

- Разрешено БЕЗ опасной approval-фразы
- Работа только внутри Hermes-Clean
- Без доступа к E:\Заказы
- Staging/export/tests/dry-run

## Вариант B: Дать approval на controlled real-folder preflight

**Точная фраза:**
```
ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT
```

**Разрешит ТОЛЬКО:**
- Controlled preflight (проверка плана, dry-run rehearsal)

**НЕ разрешит:**
- ❌ Создание папок в E:\Заказы
- ❌ Копирование файлов в E:\Заказы
- ❌ Overwrite
- ❌ Delete
- ❌ CorelDRAW
- ❌ ArtCAM
- ❌ Google Drive
- ❌ Telegram live

## Вариант C: Остановить real-folder линию

- Вернуться к staging/export tests
- Безопасно, если работа внутри Hermes-Clean
- Без доступа к E:\Заказы

## Правила approval

1. Фраза должна быть отдельным явным сообщением пользователя
2. Упоминание фразы в отчёте НЕ является approval
3. «BATCH_117» без «ОДОБРЯЮ» НЕ является approval
