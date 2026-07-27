# Local Dashboard Command Center

## Назначение

`05_REPORTS\LOCAL_DASHBOARD.md` теперь является короткой локальной стартовой панелью Hermes-Clean.

## Что показывает dashboard

- состояние core;
- next task;
- список безопасных локальных команд;
- Malyarka synthetic status;
- Malyarka combined preview;
- Telegram dry-run aliases;
- Telegram dry-run scenarios;
- pending approvals;
- safety locks.

## Команда

```cmd
scripts\hermes.cmd dashboard
```

## Безопасность

Dashboard только собирает локальный Markdown-отчёт.

Он не читает:

- реальные заказы;
- клиентские документы;
- `.env`;
- токены;
- ключи;
- старые архивы;
- Google Drive документы.

Он не запускает live Telegram и не отправляет сообщения.
