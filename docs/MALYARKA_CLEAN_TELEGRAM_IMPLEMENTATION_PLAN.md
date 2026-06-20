# Malyarka Clean — безопасный план будущей реализации Telegram

Дата: 2026-06-14

Серия:

```text
Серия 067–069 — План безопасного Telegram-слоя
BATCH_SERIES_067_069_SAFE_TELEGRAM_LAYER_PLANNING
```

Пакет:

```text
Пакет 069 — план будущей реализации Telegram
```

## Цель

Описать будущий безопасный порядок реализации Telegram-слоя без написания кода в этой серии.

Эта серия не реализует Telegram. Она только фиксирует, как потом делать это безопасно.

## Главная архитектурная идея

Нужен отдельный новый Telegram-слой.

Он должен быть новым адаптером вокруг существующего ядра Malyarka Clean:

```text
Telegram message text
-> Telegram adapter
-> existing Malyarka Clean core
-> formatted Telegram response
```

Telegram adapter не должен содержать собственный парсер, собственный расчёт площади или собственные правила спорных строк.

## Что не использовать

Не использовать старый `bot.py` как активную систему.

Не брать из старой системы:

- точку запуска;
- polling;
- токен;
- скрытые правила;
- работу с базой;
- Vision/API логику;
- production-поведение.

Если старый `bot.py` когда-нибудь понадобится изучить, это должен быть отдельный read-only аудит с отдельным разрешением.

## Этап 1 — import/check каркас без live-запуска

Первый будущий технический пакет должен создать только безопасный каркас.

Разрешённая идея:

```text
python module or small adapter
check mode
sample text input
formatted response output
no Telegram network connection
```

На этом этапе нельзя:

- читать `.env`;
- трогать token;
- запускать polling;
- отправлять сообщения в Telegram;
- создавать `.cmd` live-запуска;
- менять parser/area/dispute rules;
- создавать production export.

## Этап 2 — тесты

После каркаса нужны focused tests.

Тесты должны проверить:

- clean order -> ответ показывает `clean`, подтверждённые строки, площадь и подсказку про Excel;
- has_disputes -> ответ показывает спорные строки и блокировку Excel;
- empty_or_invalid -> ответ просит отправить понятные размеры;
- adapter вызывает существующее ядро, а не дублирует правила;
- формат ответа не раскрывает секреты.

Тесты не должны подключаться к Telegram.

## Этап 3 — dry-run пользовательская проверка

После тестов можно сделать только dry-run проверку:

```text
sample text
-> Telegram formatter
-> printed response
```

Это всё ещё не live Telegram.

## Этап 4 — отдельное разрешение на token/polling

Только после успешного каркаса, тестов и dry-run пользователь может отдельно разрешить:

- как хранить token;
- можно ли читать `.env`;
- можно ли запускать polling;
- какие ограничения live-бота действуют;
- можно ли отправлять ответы в реальный Telegram.

Без такого отдельного разрешения token и polling остаются запретными.

## Как Telegram должен вызывать ядро

Будущий слой должен использовать тот же смысл, что локальный запуск:

```text
raw_text
-> existing order processing core
-> order result
-> formatted response
```

Результат должен опираться на существующие поля:

```text
status
confirmed_rows
disputed_rows
total_area_m2
export_blocked
short_summary
next_action
```

Если `status = clean`, Telegram может сказать, что Excel можно создать.

Если `status = has_disputes` или `empty_or_invalid`, Telegram должен показать блокировку и попросить исправить входной текст.

## Что вынести в будущие отдельные планы

Отдельные будущие планы нужны для:

- live Telegram polling;
- хранения и чтения token;
- отправки файлов через Telegram;
- автоматического создания Excel из Telegram;
- Vision/photo;
- базы заказов;
- истории заказов;
- цен, стоимости, ЛКМ и материалов;
- production workflow.

## Итог

Безопасная реализация Telegram должна идти так:

```text
план
-> новый отдельный adapter
-> check mode без сети
-> focused tests
-> dry-run
-> отдельное разрешение пользователя
-> только потом token/polling
```

В этой серии код не пишется и Telegram не запускается.

