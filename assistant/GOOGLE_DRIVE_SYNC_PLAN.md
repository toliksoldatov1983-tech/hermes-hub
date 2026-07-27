# GOOGLE DRIVE SYNC PLAN

Дата: 2026-07-04 · Статус: **PLAN READY**

## Структура на Drive

```
Google Drive / Hermes-Clean /
  Orders/        ← архивные карточки
  Tasks/         ← список задач
  Daily/         ← daily log
  Reports/       ← отчёты
  Prices/        ← реестры цен
  LKM/           ← нормы расхода
  Backups/       ← резервные копии
```

## Правила синхронизации

- Локальная база — главная
- Google Drive — копия
- Не удалять на Drive
- Не перезаписывать молча
- Конфликт → создать conflict report
- Запись только после подтверждения пользователя
