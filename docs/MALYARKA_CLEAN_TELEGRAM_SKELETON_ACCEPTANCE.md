# Malyarka Clean — приёмка безопасного Telegram-каркаса

Дата: 2026-06-14

Серия:

```text
Серия 070–073 — Безопасный Telegram-каркас без live-запуска
BATCH_SERIES_070_073_SAFE_TELEGRAM_SKELETON_NO_LIVE_RUN
```

## Что создано

Создан безопасный Telegram-каркас внутри проекта Malyarka Clean:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram
```

Файлы:

```text
__init__.py
adapter.py
messages.py
diagnostics.py
```

Созданы focused tests:

```text
E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_adapter.py
```

## Что умеет adapter

Главная функция:

```text
build_telegram_order_reply(order_text: str) -> str
```

Она:

- принимает текст заказа;
- вызывает существующее ядро Malyarka Clean;
- формирует русский текст ответа для будущего Telegram;
- показывает `status`;
- показывает подтверждённые строки;
- показывает спорные строки;
- показывает `total_area_m2`;
- показывает, заблокирован ли export;
- даёт короткую подсказку.

## Важная граница

Adapter не является live Telegram.

Он не:

- запускает Telegram;
- запускает polling;
- читает `.env`;
- требует token;
- использует старый `bot.py`;
- отправляет сообщения;
- отправляет файлы;
- создаёт Excel;
- меняет локальный runner;
- меняет Excel/Corel export.

## Как adapter вызывает ядро

Текущий путь:

```text
order_text
-> malyarka_clean_telegram.build_telegram_order_reply
-> malyarka_clean_core.build_order_result
-> formatted Russian reply
```

То есть Telegram-каркас не содержит собственного парсера, расчёта площади или правил спорных строк.

## Проверки

Запущено:

```text
PYTHONPATH=E:\Hermes-Hub\projects\malyarka-clean\src
python -m pytest E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_adapter.py -q
```

Результат:

```text
7 passed
```

Проверено:

- импорт Telegram-модуля не требует token;
- импорт не читает `.env`;
- clean-текст даёт ответ `clean`;
- спорный текст даёт `has_disputes` и просьбу исправить только спорные строки;
- мусорный текст даёт `empty_or_invalid`;
- adapter не создаёт `COREL_EXPORT.xlsx`;
- adapter не запускает polling.

## Что не трогалось

```text
Telegram live launch
polling
Telegram token
.env
orders.db
.git
tokens
keys
old Malyarka as active system
old bot.py
Vision
API
database
prices
cost
LKM
materials
Docker
commits/push
folder renames
parser
area calculation
dispute rules
Excel/Corel export
production export
```

## Следующий этап

Следующий этап должен быть отдельным планом перед реальным Telegram-подключением:

```text
Серия 074–076 — Проверка Telegram-каркаса и план безопасного подключения
BATCH_SERIES_074_076_TELEGRAM_SKELETON_CHECK_AND_CONNECTION_PLAN
```

До отдельного разрешения пользователя нельзя подключать token, читать `.env`, запускать polling или отправлять сообщения в реальный Telegram.

