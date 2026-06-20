# Server Bot Staging Checklist

Дата: 2026-06-15

Назначение: проверить локальный staging перед запуском server bot read-only collector.

Локальный staging:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

## Checklist

Перед запуском collector подтвердить:

- [ ] В staging есть только whitelist-файлы.
- [ ] `.env` отсутствует.
- [ ] token/secrets отсутствуют.
- [ ] env dumps отсутствуют.
- [ ] базы данных отсутствуют.
- [ ] `orders.db` отсутствует.
- [ ] logs отсутствуют.
- [ ] `.git` отсутствует.
- [ ] JSON с секретами отсутствуют.
- [ ] приватные ключи отсутствуют.
- [ ] реальные заказы отсутствуют.
- [ ] реальные `.cdr` файлы отсутствуют.
- [ ] реальные `.art` файлы отсутствуют.
- [ ] реальные `.xlsx` файлы отсутствуют.
- [ ] папки целиком без фильтра не копировались.
- [ ] структура staging соответствует whitelist.
- [ ] `MANIFEST.md` обновлён, если копирование реально выполнялось.
- [ ] collector ещё не запускался до этой проверки.

## Разрешённая структура

```text
server_bot_read_only_copy
├─ malyarka_telegram
│  ├─ app.py
│  ├─ router.py
│  ├─ handlers.py
│  ├─ keyboards.py
│  ├─ messages.py
│  ├─ access.py
│  ├─ modes.py
│  ├─ session.py
│  ├─ intent.py
│  └─ models.py
├─ malyarka_core
│  ├─ services
│  │  ├─ orders.py
│  │  └─ archive.py
│  ├─ parsing.py
│  ├─ validation.py
│  └─ calculations.py
├─ requirements.txt
├─ MALYARKA_CURRENT_STATE.md
├─ README.md
└─ MANIFEST.md
```

## Если найден лишний файл

Если найден файл вне whitelist, collector не запускать.

Сначала остановиться и отдельно решить, что делать с этим файлом. Не читать `.env`, token, secrets, logs, database files или приватные данные.

## Следующий шаг после успешной проверки

Только после успешного checklist можно запускать collector локально:

```powershell
python E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py --source E:\Hermes-Hub\inputs\server_bot_read_only_copy --output E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```
