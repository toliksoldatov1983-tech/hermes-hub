# BATCH_118 — NEXT APPROVAL GATE

## Current Gate

Следующий опасный переход (real-folder preflight) возможен только если пользователь отдельным явным сообщением даст точную фразу:

```
ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT
```

## What This Phrase Allows

- ТОЛЬКО controlled preflight (проверка плана, rehearsal)

## What This Phrase Does NOT Allow

- ❌ Copy files to E:\Заказы
- ❌ Create folders in E:\Заказы
- ❌ Overwrite existing files
- ❌ Delete files/folders
- ❌ CorelDRAW launch
- ❌ ArtCAM launch
- ❌ Google Drive upload
- ❌ Telegram live / polling / webhook
- ❌ External API calls
- ❌ Production database
- ❌ Network changes

## Rules

1. Фраза должна быть отдельным сообщением пользователя
2. Упоминание в отчёте НЕ является approval
3. «BATCH_117» без «ОДОБРЯЮ» НЕ является approval
4. Фраза разрешает только preflight, не execution
