# Server Bot Staging Ready For Manual Copy

Дата: 2026-06-15

Серия:

```text
Серия 147-150 - Подготовка staging к ручному копированию whitelist-файлов
```

## Что подготовлено

Локальная staging-папка подготовлена для будущего ручного помещения whitelist-файлов серверного Telegram-бота.

Путь:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

Созданы пустые папки:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\malyarka_telegram
E:\Hermes-Hub\inputs\server_bot_read_only_copy\malyarka_core
E:\Hermes-Hub\inputs\server_bot_read_only_copy\malyarka_core\services
```

## Текущий статус

```text
staging folder structure prepared
server files not copied yet
collector not run yet
token not read
.env not read
```

## Whitelist будущих файлов

Копировать позже можно только эти файлы:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_telegram/models.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

## После ручного копирования

После будущего ручного копирования нужно пройти checklist:

```text
E:\Hermes-Hub\docs\SERVER_BOT_STAGING_CHECKLIST.md
```

Проверить:

- есть только whitelist-файлы;
- нет `.env`;
- нет token/secrets;
- нет баз;
- нет logs;
- нет `.git`;
- нет реальных заказов;
- нет реальных `.cdr/.art/.xlsx`;
- `MANIFEST.md` обновлён;
- collector ещё не запускался до проверки.

## Когда запускать collector

Collector можно запускать только после:

1. отдельного разрешения пользователя;
2. ручного копирования только whitelist-файлов;
3. успешной проверки checklist;
4. обновления `MANIFEST.md`.

Запуск только локально:

```powershell
python E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py --source E:\Hermes-Hub\inputs\server_bot_read_only_copy --output E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

## Что не делалось

- сервер не трогался;
- live-бот не трогался;
- polling/webhook не трогались;
- token не читался;
- `.env` не читался;
- переменные окружения не читались;
- серверные файлы не копировались;
- collector не запускался;
- код бота не менялся.
