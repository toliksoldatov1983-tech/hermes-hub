# Malyarka Export Report — Staging (Dry-Run)

## Созданные staging-файлы

| Файл | Тип |
|------|-----|
| demo_order_corel.txt | Corel TXT |
| demo_order_malyarka.xlsx | Excel XLSX |
| demo_order_export_preview.json | Preview JSON |

## Данные

- Источник: fake/dry-run демо-заказ
- Подтверждённых строк: 3
- Спорных строк: 0
- Общая площадь: 1.202 м²

## Безопасность

- Staging folder: `C:\Users\user\Desktop\Hermes-Clean\06_EXPORT_STAGING`
- E:\Заказы: НЕ трогался
- Desktop\orders: НЕ трогался
- Google Drive: НЕ трогался
- CorelDRAW: НЕ запускался
- ArtCAM: НЕ запускался
- Overwrite: НЕ использовался
- Delete: НЕ использовался

## Проверка

- TXT: первая строка пустая, без заголовков, tab delimiter, H/W/Qty ✓
- XLSX: 9 колонок, м² правильные, лицо только ✓
- JSON: metadata + hashes ✓

## Следующий шаг

Оператор должен вручную проверить TXT и XLSX.
Затем: BATCH_115 — controlled real order folder write plan.
