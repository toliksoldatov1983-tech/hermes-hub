# Local Project Audit

## Назначение

`project-audit` проверяет локальную структуру Hermes-Clean и ключевые safety guarantees.

## Команда

```cmd
scripts\hermes.cmd project-audit
```

Команда создаёт:

```text
05_REPORTS\LOCAL_PROJECT_AUDIT.md
```

## Что проверяется

- наличие ключевых файлов и папок;
- отсутствие `.env` в известных локальных местах;
- наличие dashboard;
- наличие daily report;
- наличие runtime status;
- live services disabled;
- secrets disabled;
- real orders disabled;
- Google Drive write disabled;
- live Telegram disabled;
- real AI providers disabled.
- наличие документации по локальным командам;
- command coverage в dashboard / daily report / пользовательской документации.

## Безопасность

Команда не читает `.env`, токены, ключи, реальные заказы, клиентские документы, Google Drive или старые архивы.
