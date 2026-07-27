# HERMES USER ANSWERS — FINAL ROADMAP INPUT

Дата: 2026-07-02

---

## Приоритеты (Блок 1)

1. Backup/GitHub
2. UI/команды
3. Malyarka цены/склад
4. Ежедневник
5. Vision dry-run
6. Telegram
7. Голос/Джарвис

Запретные зоны: .env/токены, E:\РАБОТА без разрешения, live Telegram, Vision API, Google Drive, git push, production DB, Corel/ArtCAM/CNC, delete/reset.

Цель через неделю: безопасный Hermes с backup, статусом, командами /order /status /next и работающим Malyarka.

## Malyarka (Блок 2)

- Устраивает: staging, Corel TXT, Excel, controlled copy
- Ошибки: не указаны — ждать реальных инцидентов
- Типы фасадов/работ: добавить по мере поступления заказов
- Цена: да, нужна
- ЛКМ (краска): да, нужен расчёт
- Клиенты/история: да, нужна

## Ежедневник / UI / Голос (Блок 3)

- Утро: план дня, заказы, риски
- Вечер: отчёт дня, что сделано/не сделано, следующий шаг
- Главный экран: статус, /order, /next, /status, /errors, /backup
- Джарвис: да, безопасный режим
- Голос разрешён: статус, заказ, исправление, запомнить
- Голос запрещён: delete, reset, live Telegram, export без подтверждения

## Backup / GitHub / Obsidian (Блок 4)

- GitHub: не подтверждён, сначала локальный backup
- Коммитить: код, md-доки, task-файлы, rules, templates, tests
- НЕ коммитить: .env, токены, реальные заказы, фото клиентов, E:\РАБОТА
- Backup: обязателен перед крупными изменениями
- Obsidian: vault не подключён, уточнить путь
- Писать: решения, правила, ошибки, roadmap, статусы
- НЕ писать: токены, личные данные, мусор, логи

## Vision / Telegram / Mobile / Drive (Блок 5)

- Vision: сначала тестовые скриншоты, потом dry-run реальных
- Фото клиентов: пока нет
- Telegram: дополнительный интерфейс, не главный. Сначала single-user
- Мобильный: да, позже — статус, заказ, preview
- Google Drive: HOLD до отдельного safe plan

## Что внедрять первым (MVP недели)

1. Локальный backup перед изменениями
2. UI: /order, /status, /next
3. Malyarka: intake реальных заказов (уже работает)
4. План цен/склада (черновой)
5. Ежедневник: morning briefing
