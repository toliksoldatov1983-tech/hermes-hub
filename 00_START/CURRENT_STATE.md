# CURRENT STATE

Дата: 2026-07-24 · Статус: **GOOGLE DRIVE МАЛЯРКИ ПЕРЕСОБРАН И ПРОВЕРЕН**

## Сервер
hermes / 178.104.95.187 · SSH ✅

## Telegram
PRODUCTION SINGLE-USER · Gateway RUNNING 24/7 on server · PHONE LIVE TEST PASSED

Server check 2026-07-04:
- `hermes-gateway.service` is active, enabled, `Restart=always`, `Linger=yes`.
- Service command: `python -m hermes_cli.main gateway run --replace`.
- Earlier Telegram polling conflicts stopped after 2026-07-04 08:20:11 UTC in checked logs.
- Owner phone test reached the server at 2026-07-04 08:29:42 UTC.
- Pairing approved for Telegram user `784990082` at 2026-07-04 13:34 +05:00.
- Repeat `/status` from phone returned `Hermes Gateway Status` in Telegram.
- Fresh server check: gateway remains `active` and `enabled`; no new journal errors in the checked window.

## Сценарий приёма заказа
1. Пользователь пишет заказ в Telegram обычным текстом
2. Hermes → preview (confirmed/disputed)
3. Disputed=0 → жду «ПИШИ ЗАКАЗ В E:\РАБОТА»
4. Export в E:\РАБОТА\01_ЗАКАЗЫ\2026\07_Июль\<заказ>\
5. Если папка есть → _v2

## Рабочие документы Малярки

- Прочитаны 17 DOCX из локальной выгрузки Google Drive.
- Создан индекс `00_START/MALYARKA_DOCUMENT_INDEX.md`.
- Добавлены 5 рабочих шаблонов и 3 эталонных заказа.
- Учебные УЧ-002 и УЧ-003 добавлены в синтетические тестовые фикстуры.
- Подтверждённые ставки маляру: модерн 6 000 тг/м², выборка 7 400 тг/м².
- По трём накладным подтверждены цены за 1 кг для 10 кодов ЛКМ; тип материалов пока не определён.
- Цены МДФ, грунта и остальных компонентов остаются неизвестными.
- Google Drive пересобран из канонических документов Hermes-Clean.
- Отчёт: `05_REPORTS/MALYARKA_DRIVE_DOCUMENTS_IMPORT_2026-07-24.md`.

## Пересборка Google Drive

- Пользователь самостоятельно очистил Google Drive аккаунта.
- OAuth восстановлен только для Drive, Docs и Sheets; Gmail, Calendar и Contacts не разрешены.
- Подготовлен локальный манифест: `00_START/GOOGLE_DRIVE_REBUILD_MANIFEST.md`.
- Комплект: 16 канонических файлов — правила, цены, нормы, шаблоны, инструкция и эталоны.
- Проверка: 16/16 файлов существуют, битых ссылок нет, секретных маркеров нет.
- Историческая базовая цена 23 600 тг/м² запрещена для новых расчётов; цены услуг берутся по типу заказа и обработки.
- Создана папка `МАЛЯРКА — УПРАВЛЕНИЕ`: https://drive.google.com/drive/folders/1vSO8OoPMnUKMVgM4O39-gb32VBMHM7j9
- Проверено: 7 папок, 16 Google-документов, пустых документов 0, дублей 0, публичных разрешений 0.
- Результат: `05_REPORTS/GOOGLE_DRIVE_REBUILD_RESULT_2026-07-24.json`.
