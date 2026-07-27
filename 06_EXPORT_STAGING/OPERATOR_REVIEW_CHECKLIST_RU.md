# OPERATOR REVIEW CHECKLIST — Malyarka Staging

## Файлы для проверки

Откройте папку: `06_EXPORT_STAGING`

| Файл | Что проверить |
|------|--------------|
| `demo_order_corel.txt` | Corel TXT preview |
| `demo_order_malyarka.xlsx` | Excel preview |
| `demo_order_export_preview.json` | Preview JSON |
| `demo_order_export_report.md` | Отчёт |

## Проверка Corel TXT

- [ ] Открыть demo_order_corel.txt в Notepad
- [ ] Первая строка пустая
- [ ] Нет заголовков (height, width)
- [ ] Колонки разделены табуляцией
- [ ] Порядок: Высота → Ширина → Количество
- [ ] Только подтверждённые строки (3 строки)
- [ ] Нет спорных строк

## Проверка Excel XLSX

- [ ] Открыть demo_order_malyarka.xlsx
- [ ] 9 колонок: №, H, W, Qty, м², Материал, Цвет, Фрезеровка, Примечание
- [ ] Площадь = H × W × Qty / 1 000 000 (только лицо)
- [ ] Торцы НЕ считаются
- [ ] 3 строки данных + итого
- [ ] Нет спорных строк

## Важно

- Это fake/dry-run демо-заказ, НЕ реальный заказ
- Файлы созданы ТОЛЬКО внутри Hermes-Clean\06_EXPORT_STAGING
- E:\Заказы НЕ трогался
- CorelDRAW НЕ запускался
- ArtCAM НЕ запускался
- Реальные папки заказов НЕ трогались
- Для записи в реальные папки нужен отдельный approval

## Результат

- [ ] Все проверки пройдены
- [ ] Staging файлы приняты
