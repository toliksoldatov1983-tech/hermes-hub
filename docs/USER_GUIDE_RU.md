# Руководство пользователя Hermes-Clean

Hermes-Clean - новый чистый локальный проект помощника Hermes.

Главная папка:

```text
C:\Users\user\Desktop\Hermes-Clean
```

Старые архивы, старые папки, Google Drive и карантин не являются текущей правдой проекта.

## Быстрый запуск

```cmd
scripts\hermes.cmd refresh-all
scripts\hermes.cmd dashboard
scripts\hermes.cmd smoke
```

Открой:

```text
05_REPORTS\LOCAL_DASHBOARD.md
```

## Проверка проекта

```cmd
scripts\run_tests.cmd
scripts\hermes.cmd project-audit
scripts\hermes.cmd release-checklist
```

Текущее состояние:

- 278 тестов проходят;
- 25 проверок project-audit проходят;
- 23 smoke-проверки проходят;
- 35 локальных CLI-команд доступны.

## Malyarka

Malyarka сейчас работает только безопасно и локально:

```cmd
scripts\hermes.cmd malyarka-demo
scripts\hermes.cmd malyarka-fixtures
scripts\hermes.cmd malyarka-dialog --script disputed
scripts\hermes.cmd malyarka-transcript --script disputed
```

Реальные заказы не подключены.

## Telegram

Telegram сейчас только dry-run:

```cmd
scripts\hermes.cmd message /status
scripts\hermes.cmd telegram-scenarios
scripts\hermes.cmd telegram-flow --case disputed
```

Live-бот не запускается, токен не читается, сообщения наружу не отправляются.

## AI

Gemini, DeepSeek и DeepSig сейчас не подключены к реальным API.

Работают только:

- mock provider;
- disabled provider checks;
- локальные отчёты.

Реальные ключи требуют отдельного шага `APPROVE_SECRET_SETUP`.

## Нельзя без отдельного разрешения

- читать реальные `.env`, токены, ключи;
- запускать live Telegram;
- работать с реальными заказами;
- менять Google Drive;
- импортировать старые архивы как рабочий проект;
- удалять файлы.

## Главные отчёты

- `05_REPORTS\LOCAL_DASHBOARD.md`
- `05_REPORTS\LOCAL_PROJECT_AUDIT.md`
- `05_REPORTS\LOCAL_RELEASE_CHECKLIST.md`
- `docs\RELEASE_READINESS_SUMMARY.md`
- `05_REPORTS\REPORT_TO_USER.md`

## Следующий шаг

Смотри:

```text
03_TASKS\NEXT_TASK.md
```
