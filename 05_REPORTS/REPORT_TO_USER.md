# REPORT_TO_USER.md

## TELEGRAM_PHONE_LIVE_TEST_PASSED

Дата: 2026-07-04
Исполнитель: Codex

### Что сделано

- Получен скриншот повторного `/status` после pairing approval.
- Telegram ответил: `Hermes Gateway Status`.
- Проверено на сервере: `hermes-gateway` остается `active` и `enabled`.
- Проверено: в свежем окне `journalctl` нет новых ошибок.

### Что это значит

- Бот работает с сервера 24/7.
- ПК можно выключать; Telegram gateway остается на сервере.
- Телефонный доступ пользователя `Soldatov Anatoliy (784990082)` привязан и работает.

### Что не сделано

- Реальные заказы не открывались.
- Export в `E:\РАБОТА` не выполнялся.
- `.env`, токены и ключи не читались.
- Google Drive не менялся.

### Статус

`PHONE_LIVE_TEST_PASSED`

### Следующий шаг

Вернуться к рабочему сценарию: ждать реальный заказ или безопасную команду в Telegram. Реальный export и работа с заказами выполняются только после отдельного подтверждения.

---

## TELEGRAM_PAIRING_APPROVED

Дата: 2026-07-04
Исполнитель: Codex

### Что сделано

- Получено отдельное подтверждение пользователя: `разрешаю привязать Telegram 5MUQKKUT`.
- На сервере выполнено: `hermes pairing approve telegram 5MUQKKUT`.
- Сервер подтвердил: `Soldatov Anatoliy (784990082)` теперь может пользоваться ботом.
- Проверено: `hermes-gateway` остается `active` и `enabled`.

### Что не сделано

- Повторный `/status` после привязки еще не отправлен с телефона.
- `.env`, токены и ключи не читались.
- Live bot не перезапускался.
- Реальные заказы не открывались.

### Статус

`SERVER_GATEWAY_24_7_PAIRING_APPROVED_PENDING_REPEAT_PHONE_TEST`

### Следующий шаг

Пользователь повторно отправляет боту с телефона `статус` или `/status`, затем Codex проверяет свежие server logs и фиксирует финальный live test result.

---

## TELEGRAM_SERVER_24_7_STATUS Checked

Дата: 2026-07-04
Исполнитель: Codex

### Что сделано

- Проверен локальный проект `C:\Users\user\Documents\«Гермес Клин».`: кода Telegram-бота там нет.
- Проверена legacy-обертка `Malyarka_Bot_Service`: локальная Windows задача отключена, рабочая папка из скрипта отсутствует.
- Проверен батник `Перезапустить_бота.bat`: он управляет серверным `hermes-gateway`.
- Проверен сервер `hermes-server` по SSH.
- Подтверждено: `hermes-gateway.service` активен, включен, `Restart=always`, `Linger=yes`.
- Подтверждено: gateway работает на сервере и не зависит от включенного ПК.
- Проверены процессы на сервере: второго видимого polling/gateway процесса не найдено.

### Что найдено

- В логах были `Telegram polling conflict` до `2026-07-04 08:20:11 UTC`.
- В свежем проверенном окне новых conflict-строк не было.
- Входящий тест с телефона дошел до сервера.
- Лог сервера: `Unauthorized user: 784990082 (Soldatov Anatoliy) on telegram`.
- Telegram показал pairing flow: пользователь еще не разрешен.

### Что не сделано

- Live bot не перезапускался.
- Второй polling не запускался.
- `.env`, токены и ключи не читались.
- Реальные заказы не открывались.
- Pairing approval не выполнялся без отдельного подтверждения.

### Статус

`SERVER_GATEWAY_24_7_RUNNING_PENDING_PAIRING_APPROVAL`

### Следующий шаг

Получить отдельное подтверждение пользователя на pairing approval, выполнить серверную команду, затем повторить `статус` или `/status` с телефона и проверить свежие server logs.

---

## HERMES_PERSISTENT_FULL_ACCESS Prepared

Дата: 2026-07-04
Исполнитель: Codex

### Что сделано

- Создан backup: `backup_before_persistent_full_access_20260704_005041`.
- Создан access registry: `00_START\HERMES_ACCESS_REGISTRY.md`.
- Создан отчёт: `05_REPORTS\HERMES_PERSISTENT_FULL_ACCESS_REPORT.md`.
- Создан постоянный SSH key: `C:\Users\user\.ssh\hermes_clean_full_access_ed25519`.
- Создан SSH alias: `hermes-server`.
- Зафиксирован masked fingerprint: `SHA256:BtFC****b2YU`.

### Проверки

- Существующие ключи проверены против `root@49.13.76.163` и `ubuntu@49.13.76.163`.
- Новый alias `hermes-server` проверен.
- Результат: сервер отклоняет public key auth.
- Hermes binding plugin локально включён и виден: `pre_gateway_dispatch_callbacks=1`.

### Что не сделано

- Старый server polling не остановлен.
- Local gateway не перезапущен.
- Второй polling не запускался.
- Live Telegram tests не выполнялись.

### Статус

`HERMES_ACCESS_REGISTRY_READY_SERVER_BLOCKED`

### Следующий шаг

`SERVER_PUBLIC_KEY_INSTALL_REQUIRED`

---

## TELEGRAM_GATEWAY_BINDING Local Ready

Дата: 2026-07-03
Исполнитель: Codex

### Что сделано

- Создан backup: `backup_before_telegram_gateway_binding_20260703_234433`.
- Создан plan: `05_REPORTS\TELEGRAM_BINDING_IMPLEMENTATION_PLAN.md`.
- Реализован Hermes plugin: `hermes-clean-gateway-binding`.
- Plugin подключается к `pre_gateway_dispatch` и обрабатывает Hermes-Clean/Malyarka direct intents до generic fallback.
- Plugin включен в `C:\Users\user\AppData\Local\hermes\config.yaml`.
- Core `gateway\run.py` и Telegram `adapter.py` не изменялись.

### Проверки

- py_compile passed.
- Plugin discovery: callback `pre_gateway_dispatch` зарегистрирован.
- Hook-level fake gateway test passed.
- Required local route tests passed.
- Status aliases passed.
- Focused pytest: 145 passed.

### Live

- Gateway не остановлен.
- Gateway не перезапущен.
- Второй polling не запускался.
- Live Telegram tests не выполнялись.

### Статус

`TELEGRAM_GATEWAY_BINDING_LOCAL_READY_PENDING_RESTART`

### Следующий шаг

`APPROVE_TELEGRAM_GATEWAY_RESTART_AND_OWNER_ONLY_LIVE_TESTS`

---

## TELEGRAM_LIVE_BINDING Discovery

Дата: 2026-07-03
Исполнитель: Codex

### Что найдено

- Live runner найден: generic `hermes gateway run`.
- PID chain остался запущен: `20840 -> 12188 -> 10024 -> 17796 -> 17256 -> 10100`.
- CWD: `[удалённый архив]`.
- Telegram update path идет через:
  - `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\platforms\telegram\adapter.py`
  - `C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\run.py`
- Это generic Hermes Agent pipeline, а не Malyarka runner.

### Что не найдено

- Binding live gateway к `[удалённый архив]`.
- Hermes config hook/plugin, который импортирует `malyarka_telegram`.
- Package/PYTHONPATH binding для `[удалённый архив]` из CWD `E:\«Гермес Клин»`.

### Почему restart заблокирован

Restart `hermes gateway run` сейчас перезапустит тот же generic gateway и не докажет использование исправленного Malyarka router.

### Безопасность

- `.env` и token values не читались.
- Gateway не остановлен и не перезапущен.
- Новый polling не запускался.
- Live Telegram tests не выполнялись.

### Статус

`TELEGRAM_LIVE_BINDING_NOT_FOUND`

### Отчет

`05_REPORTS\TELEGRAM_LIVE_BINDING_DISCOVERY_REPORT.md`

### Следующий шаг

`TELEGRAM_BINDING_PLAN_DECISION_REQUIRED`

---

## BATCH_095 Completed

Дата: 2026-07-02
Исполнитель: Hermes Agent

Создан Mobile Web UI для Hermes-Clean.

### Mobile Web UI

- 8 экранов: Главная, Ассистент, Малярка, Статус, Проверки, AI Provider, Safety, Настройки
- Тёмная тема, mobile-first (max-width: 480px)
- 4 файла: index.html, app.css, app.js, api_client.js
- Подключение к Local API через 127.0.0.1:8514
- Vanilla JS, без framework'ов

### Проверки

- **543 теста** (494 + 49) — все пройдены
- 27/27 smoke, 25/25 audit
- `mobile-web-self-check` → OK
- Все CLI команды → exit 0

### Безопасность

- .env не читался
- Внешние URL отсутствуют
- 0.0.0.0 не используется
- Android-приложение не создавалось

### Следующий

BATCH_096_ANDROID_WEBVIEW_SHELL_APP

---

## BATCH_096_TELEGRAM_ROUTES_CLEANUP Local Fixed

Дата: 2026-07-03
Исполнитель: Codex

Сделана безопасная зачистка Telegram routes / handlers / fallbacks для Hermes-Clean.

### Что изменено

- Hermes-Clean direct intents поставлены перед free chat и generic fallback.
- `Покажи статус`, `Статус`, `Как дела по проекту`, `Статус Hermes`, `Статус Малярки` возвращают Hermes-Clean status.
- `Что дальше?` возвращает Hermes-Clean next safe step.
- Correction / price draft / LKM draft / backup request добавлены как прямые safe intents.
- `Удали файл`, `Перезапиши`, `Запусти Vision`, `Измени доступ`, `Сделай git push`, `Подключи Google Drive` блокируются до fallback.
- Legacy fallback не удалён, только понижен порядком routing.

### Backup

- `backup_before_telegram_routes_cleanup_20260703_231124`

### Проверки

- `python -m py_compile malyarka_telegram\router.py malyarka_telegram\handlers.py malyarka_hermes\safety.py`
- `python -m pytest tests\test_malyarka_telegram_router.py tests\test_malyarka_telegram_router_integration.py tests\test_malyarka_telegram_intent.py -q`
- Результат: 145 passed.

### Ограничение

Live gateway restart не выполнен: видимый процесс - `hermes gateway run`, но точный Malyarka Telegram entrypoint/cwd не подтверждён через process list без вмешательства в gateway state.

### Следующий шаг

Подтвердить live entrypoint/cwd без секретов, перезапустить только подтверждённый polling/gateway и выполнить owner-only live tests.

---

## TELEGRAM_LIVE_RESTART Blocked

Дата: 2026-07-03
Исполнитель: Codex

### Что подтверждено

- Активная gateway-like цепочка найдена: `hermes gateway run`.
- CWD для основной цепочки: `[удалённый архив]`.
- PID chain: `20840 -> 12188 -> 10024 -> 17796 -> 17256 -> 10100`.

### Что не подтверждено

- Не подтверждено, что live gateway импортирует `[удалённый архив]`.
- Из подтверждённой CWD `E:\«Гермес Клин»` пакет `malyarka_telegram` не импортируется той же Python-средой.
- Отдельного `malyarka_telegram.app --run-polling` или `bot.py` polling процесса не найдено.

### Решение

- Gateway не остановлен.
- Gateway не перезапущен.
- Live Telegram tests не выполнялись.

### Статус

`TELEGRAM_LIVE_RESTART_BLOCKED`

### Следующий шаг

Найти фактический Telegram polling runner или подтверждённую Hermes gateway plugin binding к `malyarka-runtime-clean` без чтения `.env` и токенов.

---

## MALYARKA DOCUMENTS LOCAL IMPORT

Дата: 2026-07-24

### Выполнено

- Прочитаны 17 документов Малярки из локальной выгрузки Google Drive.
- В Hermes-Clean добавлены один индекс, пять рабочих шаблонов и три эталонных заказа.
- Два входных шаблона объединены в один.
- Финансовый шаблон разделяет клиентскую цену, материалы и оплату маляру.
- В проект записаны ставки: модерн 6 000 тг/м², выборка 7 400 тг/м².
- Учебные УЧ-002 и УЧ-003 подключены как синтетические фикстуры.

### Проверки

- 8 обязательных файлов из 8 существуют.
- 8 ссылок индекса из 8 работают.
- Целевые тесты: 10 passed.
- Полный набор: 810 passed, 13 старых сбоев путей/CLI/окружения.

### Не выполнено

- Прямая сверка Google Drive: OAuth-токен отозван.
- Удаление и пересоздание документов на Google Drive не выполнялось.

### Следующий шаг

Восстановить доступ к Drive только для чтения, провести сверку один к одному и подготовить список удаления. Само удаление — только после отдельного подтверждения пользователя.

Подробный отчёт: `05_REPORTS\MALYARKA_DRIVE_DOCUMENTS_IMPORT_2026-07-24.md`.

---

## MALYARKA MATERIAL PRICES FROM INVOICES

Дата: 2026-07-24

- Обработаны три накладные со скриншотов.
- В существующий реестр добавлены 10 кодов материалов с ценами.
- S0500N-10 подтверждён двумя накладными по одной цене 6 600 тг.
- PGP301: 2 600 тг/кг.
- По правилу пользователя все материалы учитываются в килограммах; тип материала не назначался без данных.
- Частично видимые S1, K2, S4 не добавлены: нет цены и количества.
- Все три контрольные суммы совпали.

---

## GOOGLE DRIVE REBUILD KIT PREPARED

Дата: 2026-07-24

### Выполнено

- Подготовлен манифест нового пустого Google Drive.
- Выбраны 16 канонических файлов: правила, цены, нормы, шаблоны, инструкция и эталоны.
- Проверено наличие 16/16 файлов.
- Битых ссылок: 0.
- Секретных маркеров: 0.
- Реальные заказы и фотографии клиентов исключены.
- Старый путь проекта исправлен.
- Историческая базовая цена 23 600 тг/м² запрещена для новых расчётов.

### Не выполнено

- Google Drive не очищался Hermes.
- OAuth не восстанавливался.
- Папки и файлы на Drive не создавались.

### Следующий шаг

После сообщения пользователя об окончании ручной очистки восстановить OAuth для `drive,docs,sheets`, проверить Drive в режиме чтения и показать точный план загрузки перед отдельным подтверждением.

---

## GOOGLE DRIVE REBUILD COMPLETED

Дата: 2026-07-24

### Выполнено

- Пользователь самостоятельно очистил Google Drive.
- Hermes подтвердил через API, что активных файлов на Drive было 0.
- OAuth восстановлен только для Drive, Docs и Sheets.
- Создан корень `МАЛЯРКА — УПРАВЛЕНИЕ` и шесть разделов.
- Создано 16 Google-документов из канонических файлов Hermes-Clean.
- Главный индекс содержит ссылки на документы.

### Проверки

- Всего объектов: 23.
- Папок: 7.
- Документов: 16.
- Пустых документов: 0.
- Дублей: 0.
- Публичных и доменных разрешений: 0.
- Gmail, Calendar и Contacts не разрешены.

Корень: https://drive.google.com/drive/folders/1vSO8OoPMnUKMVgM4O39-gb32VBMHM7j9

Технический результат: `05_REPORTS\GOOGLE_DRIVE_REBUILD_RESULT_2026-07-24.json`.
