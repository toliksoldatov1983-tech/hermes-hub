# Local App Runtime Status

## Назначение

`app-status` показывает безопасное локальное состояние Hermes-Clean как приложения.

## Команда

```cmd
scripts\hermes.cmd app-status
```

Команда создаёт:

```text
05_REPORTS\LOCAL_RUNTIME_STATUS.md
```

## Что считается включённым

- local CLI;
- dashboard;
- smoke tests;
- Telegram dry-run;
- Malyarka synthetic/manual test;
- mock AI provider.

## Что считается отключённым

- live Telegram;
- реальные AI providers;
- Google Drive write;
- real order access;
- archive import;
- delete files.

## Безопасность

Команда не читает `.env`, токены, ключи, реальные заказы, Google Drive документы или старые архивы.
