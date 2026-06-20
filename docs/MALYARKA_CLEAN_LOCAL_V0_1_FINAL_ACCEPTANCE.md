# Malyarka Clean: финальная приёмка локальной v0.1

Дата: 2026-06-13

Серия:

```text
BATCH_SERIES_045_047_LOCAL_V01_ACCEPTANCE_AND_ROADMAP
```

## Что принято

`Malyarka Clean v0.1` принята как локальная рабочая точка.

Это безопасная локальная версия, которая работает без Telegram, Vision, API, базы данных и Excel/Corel export.

## Что входит в v0.1

В v0.1 есть:

- ввод заказа через `ORDER_INPUT.txt`;
- проверка заказа через `.cmd`;
- сохранение результата в `LAST_ORDER_RESULT.txt`;
- читаемый результат в Блокноте;
- примеры заказов;
- быстрые проверки примеров;
- статусы `clean`, `has_disputes`, `empty_or_invalid`;
- подтверждённые и спорные строки;
- расчёт площади подтверждённых строк;
- внутренние Corel-строки без реального Corel export.

## Главные файлы v0.1

```text
E:\Hermes-Hub\inputs\ORDER_INPUT.txt
E:\Hermes-Hub\ПРОВЕРИТЬ_ЗАКАЗ_ИЗ_ФАЙЛА.cmd
E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
E:\Hermes-Hub\README_КАК_ПОЛЬЗОВАТЬСЯ.md
```

## Что не входит в v0.1

- Excel/Corel export;
- Excel-файлы;
- Corel-файлы;
- Telegram;
- Vision;
- API;
- база данных;
- цены;
- стоимость;
- ЛКМ;
- материалы;
- производство;
- CNC.

## Итог

v0.1 можно считать завершённой локальной основой для ручной проверки текстового заказа.

