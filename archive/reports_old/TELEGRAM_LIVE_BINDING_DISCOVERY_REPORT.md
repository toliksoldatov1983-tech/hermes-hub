# TELEGRAM_LIVE_BINDING_DISCOVERY_REPORT

Дата: 2026-07-03
Исполнитель: Codex

## Итог

Фактический live runner найден, но binding `Telegram gateway -> Hermes-Clean / Malyarka router` не найден.

Финальный статус:

`TELEGRAM_LIVE_BINDING_NOT_FOUND`

## Что запущено сейчас

Найдена активная live-цепочка:

- `20840` -> `12188` -> `10024` -> `17796` -> `17256` -> `10100`
- команда верхнего процесса: `bash.exe -lic "set +m; hermes gateway run 2>&1"`
- Hermes command: `C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe gateway run`
- CWD live-цепочки: `[удалённый архив]`
- Hermes home: `C:\Users\user\AppData\Local\hermes`

Gateway не остановлен и не перезапущен.

## Где фактический Telegram runner

Live runner сейчас является generic Hermes gateway:

- `C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\run.py`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\platforms\telegram\adapter.py`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\platforms\telegram\plugin.yaml`

Фактический путь обработки Telegram text update:

1. `plugins\platforms\telegram\adapter.py`
2. `TelegramAdapter._handle_text_message`
3. `BasePlatformAdapter.handle_message`
4. `GatewayRunner._handle_message`
5. `GatewayRunner._handle_message_with_agent`
6. `GatewayRunner._run_agent`

Это generic Hermes Agent pipeline, а не `malyarka_telegram.app`.

## Где находится Malyarka Telegram runner

Исправленный Malyarka путь найден отдельно:

- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`

Документы проекта описывают Malyarka runner как:

`python -m malyarka_telegram.app --run-polling`

Но такого процесса в текущей live-цепочке не подтверждено.

## Где находится old fallback

Old generic fallback найден в:

`[удалённый архив]`

Текст fallback:

`Понял, это вопрос по задачам или проекту...`

После локального fix этот fallback должен срабатывать только после direct Hermes-Clean intents. Но live gateway сейчас не доказано использует этот файл.

## Почему `malyarka_telegram` не импортируется live gateway

Read-only import check из CWD `E:\«Гермес Клин»` тем же Hermes/Python окружением показал:

`ModuleNotFoundError: No module named 'malyarka_telegram'`

Причины:

- live gateway CWD: `[удалённый архив]`;
- project path `[удалённый архив]` отсутствует в `sys.path`;
- в `malyarka-runtime-clean` не найдено package binding через `pyproject.toml`, `setup.py` или `setup.cfg`;
- Hermes config указывает `terminal.cwd: E:\«Гермес Клин»`;
- в `C:\Users\user\AppData\Local\hermes\config.yaml` релевантный `hooks` пустой: `hooks: {}`;
- Telegram platform toolset указан как generic `hermes-telegram`;
- documented plugin binding к `malyarka-runtime-clean` в Hermes gateway config не найден.

Из CWD `[удалённый архив]` импорт `malyarka_telegram.router` работает, потому что package root попадает в `sys.path`.

## Что нужно изменить

Нужен отдельный план подключения Malyarka router к live Telegram. Без этого restart `hermes gateway run` не исправит routing фразы `Покажи статус`.

Варианты:

1. Запускать отдельный Malyarka polling runner из `[удалённый архив]`:
   `python -m malyarka_telegram.app --run-polling`
   Перед этим нужно безопасно остановить конфликтующий polling и не допустить двух polling процессов на одном Telegram token.

2. Подключить Malyarka direct router через Hermes gateway hook/plugin:
   `pre_gateway_dispatch` должен обрабатывать Hermes-Clean/Malyarka intents до generic Hermes Agent fallback.
   Для этого потребуется package binding: `PYTHONPATH`, editable install или packaging.

3. Упаковать `malyarka-runtime-clean` как importable package:
   добавить package metadata или безопасно настроить launch environment, чтобы live Hermes gateway видел `malyarka_telegram`.

На этом этапе изменения не выполнялись.

## Риски

- Текущий `hermes gateway run` является generic Telegram gateway и может продолжать отвечать generic Hermes Agent fallback.
- Запуск Malyarka polling параллельно текущему gateway может создать конфликт polling по одному Telegram bot token.
- Подключение hook/plugin в Hermes gateway затронет весь Hermes Telegram path, поэтому требует отдельного backup и focused tests.
- Для live запуска нужен token/env, но `.env` и token values на этом этапе не читались и не должны показываться.

## Проверенные места

- `C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\run.py`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\config.py`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\platforms\base.py`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\platforms\telegram\adapter.py`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\platforms\telegram\plugin.yaml`
- `C:\Users\user\AppData\Local\hermes\config.yaml` только redacted / non-secret scan
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `[удалённый архив]`
- `E:\«Гермес Клин»` project docs / task docs / handoff references

Примечание: один широкий read-only поиск был прерван после чрезмерного объема вывода. Файлы не менялись, процессы gateway не останавливались.

## Что осталось запрещено

- `.env` не читать.
- Token values не читать и не показывать.
- Gateway не останавливать до подтвержденного plan.
- Новый polling не запускать до подтвержденного plan.
- `E:\РАБОТА`, Google Drive, Vision, production database, CorelDRAW, ArtCAM, CNC не трогать.
- `bot_archive_20260703.py` не трогать.
- `git push`, delete, reset, clear, prune не делать.

## Rollback

Live changes не выполнялись, поэтому live rollback не требуется.

Локальный routing backup уже существует:

`C:\Users\user\Desktop\Hermes-Clean\backup_before_telegram_routes_cleanup_20260703_231124`

Если нужно откатить локальные routing changes, использовать этот backup вручную и только после отдельного подтверждения пользователя.

## Следующий крупный шаг

`TELEGRAM_BINDING_PLAN_DECISION_REQUIRED`

Нужно выбрать и описать безопасный способ подключения:

- отдельный Malyarka polling runner;
- Hermes `pre_gateway_dispatch` hook/plugin;
- package/PYTHONPATH binding для `malyarka-runtime-clean`.

До выбора binding plan live restart остается заблокирован.
