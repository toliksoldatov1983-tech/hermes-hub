# Перенос рабочих документов Малярки в Hermes-Clean

Дата: 2026-07-24
Статус: LOCAL_IMPORT_COMPLETE · DRIVE_UNCHANGED · DRIVE_DIRECT_COMPARE_BLOCKED

## Источник

Прочитаны 17 DOCX из локальной выгрузки Google Drive:
`C:\Users\user\Desktop\фото и видео работ\архив который надо удолить`

Прямой доступ к Google Drive не использовался: OAuth-токен отозван (`invalid_grant`). На Google Drive ничего не создано, не изменено и не удалено.

## Перенесено

### Индекс

- `00_START\MALYARKA_DOCUMENT_INDEX.md`

### Рабочие шаблоны

- `docs\malyarka_templates\ORDER_INTAKE_TEMPLATE.md`
- `docs\malyarka_templates\COREL_EXPORT_TEMPLATE.md`
- `docs\malyarka_templates\MALYARKA_MATERIAL_TEMPLATE.md`
- `docs\malyarka_templates\FINANCE_AND_COST_TEMPLATE.md`
- `docs\malyarka_templates\ARCHIVE_ORDER_CARD_TEMPLATE.md`

Два старых входных шаблона объединены в один. Финансовый шаблон исправлен: клиентская цена, материалы и оплата маляру разделены.

### Эталонные заказы

- `docs\malyarka_reference_orders\YULYA_001.md`
- `docs\malyarka_reference_orders\UCH_002.md`
- `docs\malyarka_reference_orders\UCH_003.md`
- `docs\malyarka_reference_orders\README.md`

Исторические цены внутри эталонов помечены как недействующие для новых заказов.

### Рабочие данные проекта

- В `00_START\HERMES_PRICE_STOCK_DRAFT.md` добавлены подтверждённые ставки маляру:
  - модерн — 6 000 тг/м²;
  - выборка — 7 400 тг/м².
- В `AGENTS.md` добавлено обязательное чтение индекса документов для задач Малярки.
- В `src\hermes_clean\fixtures.py` добавлены учебные фикстуры УЧ-002 и УЧ-003.
- В `tests\test_fixtures.py` добавлена проверка контрольных площадей и маршрутов.

## Не перенесено как рабочая истина

- настройки Space Agent — устаревшие модель и провайдер;
- сводные документы проекта — дубли текущих правил;
- пустые закупочные цены материалов — остаются `нет данных`;
- исторические клиентские цены эталонов — только контроль старого прогона.

## Проверки

- индекс: 8 ссылок, отсутствующих файлов 0;
- обязательные файлы: 8 из 8 существуют;
- ставки 6 000/7 400 присутствуют;
- целевые тесты: 10 passed;
- полный pytest: 810 passed, 13 failed.

13 ошибок полного набора относятся к старым тестам с жёстким путём `C:\Users\user\Desktop\Hermes-Clean`, отсутствующим старым CLI-командам и вложенному запуску Python без pytest. Изменённые фикстуры и новые документы целевые тесты проходят.

## Риск перед удалением Google Drive

Удалять Google Drive пока нельзя. Нужны:

1. восстановленный доступ только для чтения;
2. прямая сверка списка и содержимого файлов один к одному;
3. отдельное подтверждение пользователя на удаление или перенос в корзину;
4. после этого — создание новых рабочих документов на Drive из локальных шаблонов Hermes-Clean.
