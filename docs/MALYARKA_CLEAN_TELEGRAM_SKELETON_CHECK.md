# Malyarka Clean — проверка Telegram-каркаса

Дата: 2026-06-14

Серия:

```text
Серия 074–076 — Проверка Telegram-каркаса и план безопасного подключения
BATCH_SERIES_074_076_TELEGRAM_SKELETON_CHECK_AND_CONNECTION_PLAN
```

Пакет:

```text
Пакет 075 — документ проверки Telegram-каркаса
```

## Что проверено

Проверен безопасный non-live пакет:

```text
E:\Hermes-Hub\projects\malyarka-clean\src\malyarka_clean_telegram
```

Проверки:

- импорт `malyarka_clean_telegram` без Telegram token;
- импорт без чтения `.env`;
- `diagnostics` возвращает безопасные флаги;
- adapter работает на `clean`;
- adapter работает на `has_disputes`;
- adapter работает на `empty_or_invalid`;
- Excel из adapter не создаётся;
- polling не запускается.

## Запущенные проверки

Focused tests:

```text
PYTHONPATH=E:\Hermes-Hub\projects\malyarka-clean\src
python -m pytest E:\Hermes-Hub\projects\malyarka-clean\tests\test_telegram_adapter.py -q
```

Результат:

```text
7 passed
```

Safe import/check:

```text
from malyarka_clean_telegram import build_telegram_order_reply, get_telegram_skeleton_diagnostics
```

Результат diagnostics:

```text
live_telegram = false
polling = false
token_required = false
reads_env_file = false
uses_old_bot_py = false
sends_files = false
creates_excel = false
```

Проверенные ответы:

```text
clean -> Статус: clean
has_disputes -> Статус: has_disputes
empty_or_invalid -> Статус: empty_or_invalid
```

## Что подтвердилось

Token не нужен для импорта и работы adapter.

`.env` не читался.

Polling не запускался.

Старый `bot.py` не использовался.

Adapter только формирует текстовый ответ:

```text
order text
-> existing Malyarka Clean core
-> Russian text reply
```

Adapter не отправляет сообщения в Telegram, не отправляет файлы, не создаёт Excel и не меняет локальный runner.

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

## Итог

Telegram-каркас прошёл безопасную проверку как offline adapter.

Он готов только для следующего планового этапа: продумать безопасное подключение. Реальное подключение Telegram, token, `.env` и polling всё ещё требуют отдельного разрешения пользователя.

