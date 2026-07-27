# Отчет: очистка USER.md для Hermes Desktop

ВЫПОЛНЕНО:
- Создан backup старого профиля пользователя Hermes: `C:\Users\user\AppData\Local\hermes\memories\USER.md.bak.codex_20260704_clean_profile`.
- `USER.md` заменен на короткую согласованную выжимку.
- Сохранены полезные старые правила: русский язык, быстрый сухой стиль, `+` как продолжение, `не понял` как упрощение, Hermes-Clean, BATCH-режим, live Telegram только после `ОДОБРЯЮ BATCH_NNN`, минимизация консолей/SSH/панелей.
- Убраны опасные формулировки: "никогда не уточнять" и "действовать без разрешения всегда".

НЕ ВЫПОЛНЕНО:
- `config.yaml`, `.env`, токены, Google credentials и live-настройки не изменялись.
- `MEMORY.md` не изменялся.
- Календарь не подключался и не изменялся.

ИЗМЕНЕННЫЕ ФАЙЛЫ:
- `C:\Users\user\AppData\Local\hermes\memories\USER.md`
- `C:\Users\user\AppData\Local\hermes\memories\USER.md.bak.codex_20260704_clean_profile`
- `01_reports/2026-07-04-hermes-user-profile-cleanup.md`

ПРОВЕРКИ:
- Новый `USER.md` прочитан после записи.
- Backup старого `USER.md` существует.
- Выполнено `hermes prompt-size`: профиль пользователя подхватывается, user profile около 3.4 KB.

РИСКИ:
- Уже открытые сессии Hermes могут держать старый контекст. Для надежного применения нужна новая сессия или перезапуск Hermes Desktop.

СЛЕДУЮЩИЙ КРУПНЫЙ БЛОК:
- Перезапустить Hermes Desktop и проверить в новой сессии, что стиль стал коротким, сухим и без лишних уточнений.
