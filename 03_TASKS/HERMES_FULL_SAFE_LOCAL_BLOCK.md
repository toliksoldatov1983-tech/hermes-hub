# HERMES_FULL_SAFE_LOCAL_BLOCK

Этот файл содержит готовое крупное задание для следующего запуска Hermes-Clean/Codex.

## Задание

Выполнить `BATCH_063_SAFE_LOCAL_MALYARKA_FULL_HARDENING_PACK`.

Работать крупными внутренними блоками и не останавливаться на мелких шагах.

Задача специально сделана большой, чтобы максимально загрузить Hermes-Clean полезной локальной работой, но без опасных действий.

## Безопасность

Разрешено:

- менять файлы внутри `C:\Users\user\Desktop\Hermes-Clean`;
- писать локальный Python-код;
- писать тесты;
- запускать локальные тесты;
- создавать локальные отчёты;
- использовать только synthetic/manual input.

Запрещено:

- читать реальные заказы;
- читать клиентские документы;
- читать `.env`, токены, ключи;
- менять Google Drive;
- запускать live Telegram;
- запускать внешние AI API;
- читать или распаковывать старые архивы;
- открывать `[удалён]`;
- удалять файлы.

## Основной фокус

1. Malyarka validation layer.
2. Synthetic fixtures expansion.
3. Dispute resolver contract.
4. Export gate hardening.
5. Telegram dry-run Malyarka scenarios.
6. Docs and command coverage.
7. Full local verification.

## Проверки

Финальный минимум:

```cmd
scripts\hermes.cmd project-audit
scripts\hermes.cmd smoke
scripts\run_tests.cmd
```

Желательно также:

```cmd
scripts\hermes.cmd help-local
scripts\hermes.cmd malyarka-fixtures
scripts\hermes.cmd malyarka-disputes
scripts\hermes.cmd malyarka-combined
scripts\hermes.cmd telegram-scenarios
```
