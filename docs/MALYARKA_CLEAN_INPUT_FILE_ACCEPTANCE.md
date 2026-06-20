# Malyarka Clean: приёмка режима входного файла заказа

Дата: 2026-06-13

Пакет:

```text
BATCH_037_INPUT_FILE_ACCEPTANCE_AND_USER_SHORTCUTS_PLANNING
```

## Что принято

Режим входного файла заказа принят.

Рабочий порядок:

1. Открыть файл заказа:

```text
notepad E:\Hermes-Hub\inputs\ORDER_INPUT.txt
```

2. Вставить или изменить текст заказа.
3. Сохранить файл.
4. Запустить проверку:

```text
E:\Hermes-Hub\ПРОВЕРИТЬ_ЗАКАЗ_ИЗ_ФАЙЛА.cmd
```

5. Посмотреть результат:

```text
notepad E:\Hermes-Hub\outputs\LAST_ORDER_RESULT.txt
```

## Что уже работает

- `ORDER_INPUT.txt` существует.
- Проверка читает заказ из файла.
- Результат показывается на экране.
- Результат сохраняется в `LAST_ORDER_RESULT.txt`.
- Это обычные `.txt`-файлы, без Excel/Corel export.

## Что не входит

- Telegram;
- Vision;
- API;
- база данных;
- Excel/Corel export;
- цены;
- стоимость;
- ЛКМ;
- материалы;
- производство;
- CNC.

