# BATCH_117 — APPROVAL WORDING

## Точная фраза для будущего controlled preflight

```
ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT
```

## Что эта фраза разрешит

- ТОЛЬКО controlled preflight (проверка плана, dry-run rehearsal)
- БЕЗ записи в реальные папки

## Что эта фраза НЕ разрешит

- ❌ Копирование файлов в E:\Заказы
- ❌ Создание папок в E:\Заказы
- ❌ Overwrite существующих файлов
- ❌ Delete файлов или папок
- ❌ CorelDRAW automation
- ❌ ArtCAM automation
- ❌ CNC
- ❌ Google Drive upload
- ❌ Telegram live / polling / webhook
- ❌ Внешние API
- ❌ Production database

## Правила approval

1. Фраза должна быть отдельным явным сообщением пользователя
2. Упоминание фразы в отчёте НЕ является approval
3. Простое «BATCH_117» без «ОДОБРЯЮ» НЕ является approval
4. Фраза разрешает только controlled preflight по отдельному плану
