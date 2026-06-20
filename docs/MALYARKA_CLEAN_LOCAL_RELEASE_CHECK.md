# Malyarka Clean — контрольная проверка локальной версии

Дата: 2026-06-14

Серия:

```text
Серия 061–063 — Упрощение пользовательской инструкции и контрольная проверка локальной версии
BATCH_SERIES_061_063_USER_GUIDE_AND_LOCAL_RELEASE_CHECK
```

## Что проверялось

Проверялся текущий главный локальный запускатель:

```text
E:\Hermes-Hub\ЗАПУСТИТЬ_ЗАКАЗ.cmd
```

Он читает заказ из:

```text
E:\Hermes-Hub\inputs\ORDER_INPUT.txt
```

Всегда сохраняет текстовый результат:

```text
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

И создаёт или обновляет Excel для Corel только для чистого заказа:

```text
E:\Hermes-Hub\outputs\COREL_EXPORT.xlsx
```

## Проверка 1 — чистый заказ

Вход:

```text
1000 400 2
700 300
```

Результат:

```text
exit code: 0
status: clean
LAST_ORDER_RESULT.txt сохранён
COREL_EXPORT.xlsx создан или обновлён
```

## Проверка 2 — заказ со спорной строкой

Вход:

```text
1000 400 2
мусор
700 300
```

Результат:

```text
exit code: 2
status: has_disputes
LAST_ORDER_RESULT.txt сохранён
COREL_EXPORT.xlsx не обновлён
```

## Проверка 3 — пустой или мусорный заказ

Вход:

```text
привет
ничего непонятно
```

Результат:

```text
exit code: 2
status: empty_or_invalid
LAST_ORDER_RESULT.txt сохранён
COREL_EXPORT.xlsx не обновлён
```

## Focused tests

Запущены focused tests текущего минимального ядра и локального запускателя.

Результат:

```text
37 passed
```

## Итог проверки

Контрольная проверка локальной версии пройдена.

Текущий локальный режим работает так:

- чистый заказ создаёт Excel для Corel;
- заказ со спорными строками блокирует Excel;
- пустой или мусорный заказ блокирует Excel;
- текстовый результат сохраняется всегда;
- parser, area calculation и dispute rules не менялись.

## Что не трогалось

```text
parser
area calculation
dispute rules
Telegram
Vision
API
database
prices
cost
LKM
materials
.env
orders.db
.git
tokens
keys
old Malyarka
bot.py
Docker
commits/push
folder renames
Corel files
production export
```
