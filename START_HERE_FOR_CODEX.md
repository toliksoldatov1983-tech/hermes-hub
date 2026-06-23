# START HERE FOR CODEX

Проект: **Malyarka** (ранее Hermes Hub)
Папка: `E:\Hermes-Hub`

## При старте читай

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\CURRENT_SESSION_CONTEXT.md
E:\Hermes-Hub\SAFETY_RULES.md
E:\Hermes-Hub\handoff\
```

## Codex Role

- Реализует, проверяет, деплоит
- Работает внутри `E:\Hermes-Hub`
- После каждого шага обновляет `logs/WORKLOG.md`
- Не читает секреты, не делает внешние API вызовы
- Даёт пользователю полные Win+R пути

## Запрещено

```
.env, token, config.py, os.environ, API ключи
orders.db, логи с реальными данными
C:\Users\user\Desktop\malyarka_codex_work
C:\Users\user\Desktop\malyarka_memory_cleanup
Production (Phase 2)
Telegram launch
Vision без разрешения
git push без approval
```

## Стиль

Коротко, по-русски. Для папок — полный Win+R путь.
