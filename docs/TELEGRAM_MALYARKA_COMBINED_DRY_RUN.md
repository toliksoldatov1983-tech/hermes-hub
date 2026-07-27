# Telegram Malyarka Combined Dry-Run

## Назначение

Telegram dry-run теперь умеет показывать безопасный combined preview для Malyarka без live Telegram.

## Команда

```cmd
scripts\hermes.cmd message /malyarka-combined
```

Команда использует встроенный synthetic пример.

## Команда с ручным тестовым вводом

```cmd
scripts\hermes.cmd message /malyarka-combined paint ^| 2 ^| bucket
```

Переданный текст считается ручным тестовым вводом. Это не реальный заказ.

## Что возвращается

- source mode;
- confirmed rows;
- disputed rows;
- final ready;
- synthetic pricing total;
- запрет записи файла;
- запрет использовать результат как реальный заказ.

## Запреты

- live Telegram не запускается;
- токен не читается;
- сообщения наружу не отправляются;
- реальные заказы не читаются;
- файлы заказов не открываются;
- старые архивы не распаковываются;
- Google Drive не меняется.
