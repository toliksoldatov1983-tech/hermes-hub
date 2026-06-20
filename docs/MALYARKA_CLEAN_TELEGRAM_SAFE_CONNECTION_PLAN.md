# Malyarka Clean — план безопасного будущего подключения Telegram

Дата: 2026-06-14

Серия:

```text
Серия 074–076 — Проверка Telegram-каркаса и план безопасного подключения
BATCH_SERIES_074_076_TELEGRAM_SKELETON_CHECK_AND_CONNECTION_PLAN
```

Пакет:

```text
Пакет 076 — план безопасного подключения Telegram
```

## Цель

Описать будущий безопасный порядок подключения Telegram без реального запуска в этой серии.

Этот документ не даёт разрешения на live Telegram, polling, чтение `.env` или работу с token.

## Текущая безопасная точка

Уже есть offline-каркас:

```text
malyarka_clean_telegram
```

Он умеет:

```text
text order
-> build_telegram_order_reply
-> existing Malyarka Clean core
-> Russian text reply
```

Он не запускает Telegram, не читает `.env`, не требует token и не создаёт Excel.

## Будущий порядок подключения

### 1. Подготовить отдельный check-режим

Перед любым live-подключением нужен отдельный check-режим.

Он должен проверять:

- модуль импортируется;
- adapter формирует ответы;
- diagnostics остаётся безопасным;
- конфигурация описана, но token не показывается.

Check-режим не должен подключаться к Telegram.

### 2. Проверить импорт без live-запуска

Нужно снова проверить:

```text
import malyarka_clean_telegram
```

Требования:

- Telegram не запускается;
- polling не запускается;
- `.env` не читается;
- token не нужен;
- старый `bot.py` не используется.

### 3. Проверить конфигурацию без показа токена

Перед реальным token нужен отдельный план конфигурации.

Проверка конфигурации должна показывать только безопасные факты:

```text
token source configured: yes/no
token value: hidden
polling enabled: false by default
live mode: false by default
```

Сам token нельзя выводить в консоль, документы, отчёты или ChatGPT.

### 4. Только после отдельного разрешения подключить token/.env

Чтение `.env` и подключение token разрешены только после отдельного прямого разрешения пользователя.

До этого:

```text
.env не читать
token не искать
token не печатать
token не вставлять в код
```

### 5. Только после отдельного разрешения запустить polling

Polling — это реальный live-запуск Telegram.

Его можно запускать только после отдельного разрешения пользователя и после успешных проверок:

- offline adapter tests;
- check-mode import;
- safe config check;
- понятный rollback/stop plan.

### 6. Не использовать старый bot.py как активный

Старый `bot.py` нельзя использовать как активную систему.

Он не должен быть:

- точкой запуска;
- источником token;
- источником polling;
- базой для нового live-бота.

Если его когда-нибудь нужно изучить, это должен быть отдельный read-only аудит с отдельным разрешением.

### 7. Первый live-этап принимает только текст заказа

Первый будущий live-бот должен принимать только текст заказа.

Минимальный сценарий:

```text
user sends text order
-> bot calls existing adapter/core
-> bot returns text reply
```

На первом live-этапе бот не должен отправлять файлы и не должен создавать Excel.

### 8. Не подключать фото/Vision/API/базу/цены

На первом Telegram-подключении нельзя подключать:

```text
photo
Vision
external API
database
order history
prices
cost
LKM
materials
production export
```

Каждый из этих слоёв требует отдельного будущего плана и отдельного разрешения.

## Минимальные будущие safety-gates

Перед live Telegram должны быть закрыты:

```text
offline adapter tests passed
safe import check passed
safe config check passed
token handling plan accepted
polling launch plan accepted
stop/rollback instruction prepared
user gave explicit permission
```

## Итог

Безопасная последовательность такая:

```text
offline skeleton
-> skeleton check
-> connection plan
-> separate token/.env permission
-> separate polling permission
-> text-only live bot
```

В этой серии Telegram не подключается и не запускается.

