# Отчет: настройка SOUL.md для Hermes Desktop

ВЫПОЛНЕНО:
- Найден фактический конфиг Hermes: `C:\Users\user\AppData\Local\hermes\config.yaml`.
- Найден файл постоянной личности Hermes Desktop: `C:\Users\user\AppData\Local\hermes\SOUL.md`.
- Создана резервная копия старого `SOUL.md`: `C:\Users\user\AppData\Local\hermes\SOUL.md.bak.codex_20260704_daily_assistant`.
- `SOUL.md` заменен на промпт повседневного помощника Anatoliy: сухой стиль, запрет выдумок, крупные блоки, учет дня, заказы, дом, личное, календарь через черновик и подтверждение.

НЕ ВЫПОЛНЕНО:
- `config.yaml` не изменялся.
- `.env`, токены, Google credentials и live-настройки не трогались.
- `USER.md` и `MEMORY.md` не изменялись, потому что там уже есть накопленная память пользователя и проекта.
- Календарь не подключался и не изменялся.

ИЗМЕНЕННЫЕ ФАЙЛЫ:
- `C:\Users\user\AppData\Local\hermes\SOUL.md`
- `C:\Users\user\AppData\Local\hermes\SOUL.md.bak.codex_20260704_daily_assistant`
- `01_reports/2026-07-04-hermes-desktop-soul-prompt.md`

ПРОВЕРКИ:
- Выполнено `hermes config path`: подтвержден путь `C:\Users\user\AppData\Local\hermes\config.yaml`.
- Выполнено `hermes config show`: проверены активные параметры personality, memory и display.
- Прочитан старый `SOUL.md`.
- Проверено наличие `USER.md` и `MEMORY.md`.
- Новый `SOUL.md` прочитан после записи.
- Проверена резервная копия `SOUL.md`.
- Выполнено `hermes prompt-size`: системный промпт читается, размер около 38 KB.

РИСКИ:
- В `USER.md` уже есть старые жесткие правила вроде запрета уточняющих вопросов и немедленного действия. Они могут конфликтовать с новым более безопасным `SOUL.md`.
- Если Hermes Desktop держит старую сессию в памяти, новую личность может потребоваться подхватить через новую сессию или перезапуск Desktop.

СЛЕДУЮЩИЙ КРУПНЫЙ БЛОК:
- Очистить и привести `USER.md` к той же логике: сухой помощник, без выдумок, но с безопасными подтверждениями для опасных действий и календаря.
