# Local Daily Report

## Назначение

`daily-report` создаёт короткий ежедневный локальный отчёт Hermes-Clean.

## Команда

```cmd
scripts\hermes.cmd daily-report
```

Команда создаёт:

```text
05_REPORTS\DAILY_LOCAL_REPORT.md
```

## Что входит в отчёт

- health status;
- smoke status;
- active batch;
- next task;
- runtime status;
- Malyarka combined preview;
- Telegram dry-run scenarios;
- safe commands;
- disabled subsystems;
- pending approvals.

## Безопасность

Команда не читает `.env`, токены, ключи, реальные заказы, клиентские документы, Google Drive или старые архивы.

Команда не запускает live Telegram и не отправляет сообщения.
