# MALYARKA_CURRENT_STATE

state_version: 0.8.26

Главный актуальный источник правды по проекту «Малярка». Это краткое рабочее состояние после принятых этапов Telegram-кнопок, разделителей размеров, нейтрального Vision-каркаса, отката Gemini, безопасной DeepSeek-архитектуры, DeepSeek bridge/fallback, DeepSeek diagnostic preview, локального CLI-режима diagnostics, архитектурной спецификации режимов Telegram-бота, спецификации router/state machine и первого кодового каркаса router/state machine, плана подключения router/state machine к Telegram-слою, подключения router/state machine к Telegram text-handling слою, подключения routed-функции к live Telegram app.py и успешной ручной live-проверки Telegram polling, уточнения UX-логики кнопок копирования и принятого UX-пакета кнопок копирования.

## 1. Текущий краткий статус

- Новая версия проекта собирается модульно и безопасно, отдельно от старого `bot.py`.
- Старый `bot.py` не менять без отдельного разрешения пользователя; использовать только как источник уже рабочих частей.
- `.env`, `orders.db`, `.venv`, `.git`, реальные фото, токены, ключи и личные данные не трогать без отдельного прямого разрешения.
- `git add .`, commit и push не делать без отдельного разрешения пользователя.
- Реальные внешние AI/API не подключать без отдельного разрешения пользователя.
- Polling не запускать без отдельного разрешения пользователя.
- `state_version` — рабочая версия состояния, не версия релиза программы.

## 2. Telegram UX

- Настоящая inline-кнопка ` Скопировать для Corel` работает в живом Telegram.
- Финальный чистый экспорт теперь должен быть Excel-файлом для CorelDRAW.
- Для чистого заказа основная кнопка — `Скачать Excel для Corel`.
- `Скопировать для Corel` можно оставить запасной кнопкой для чистого заказа.
- Если экспорт заблокирован из-за спорных строк, основной кнопкой должна быть `Скопировать для исправления`, а не `Скопировать для Corel`.
- В копируемом Corel-тексте нет нумерации, заголовков, площади и итогов.
- `Скопировать подтверждённые` и `Скопировать спорные` убрать из обычного рабочего UX или позже перенести в служебный режим.
- `reply_markup` подключён в `malyarka_telegram/app.py`.
- Живой тест кнопки `Скопировать для Corel` прошёл.

Логика export/copy-кнопок:

Если экспорт доступен:

- показывать основную кнопку `Скачать Excel для Corel`;
- финальный чистый экспорт должен формироваться как Excel-файл для CorelDRAW;
- `Скопировать для Corel` можно оставить запасной кнопкой;
- запасная кнопка копирует только чистые Corel-строки: высота, ширина, количество;
- без заголовков, площади, итогов, нумерации и пояснений.

Если экспорт заблокирован:

- не показывать `Скопировать для Corel` как главную финальную кнопку;
- показывать `Скопировать для исправления`;
- не показывать `Скачать Excel для Corel`, пока есть спорные строки;
- `Скопировать подтверждённые` и `Скопировать спорные` не показывать в обычном рабочем UX или позже вынести в служебный режим.

Назначение `Скопировать для исправления`:

- копирует редактируемый текст заказа, который пользователь может поправить и отправить обратно боту;
- подтверждённые строки — в нормализованном виде: высота ширина количество;
- спорные строки — как raw-текст;
- без заголовков;
- без площади;
- без итогов;
- без причины блокировки;
- без пояснений.

Пример исходного заказа со спорной строкой:

```text
1000*400
непонятная строка
1000*600
```

`Скопировать для исправления` должно копировать:

```text
1000 400 1
непонятная строка
1000 600 1
```

Пользователь может исправить и отправить обратно боту:

```text
1000 400 1
500 700 2
1000 600 1
```

UX-пакет кнопок копирования реализован и принят.

Изменённые файлы этапа:

- `malyarka_telegram/keyboards.py`
- `malyarka_telegram/handlers.py`
- `tests/test_malyarka_telegram_messages.py`
- `tests/test_malyarka_telegram_router_integration.py`
- `tests/test_malyarka_telegram_app_router_integration.py`

Рабочая логика после реализации:

Чистый заказ:

- получает основную кнопку `Скачать Excel для Corel`;
- финальный чистый экспорт — Excel-файл для CorelDRAW;
- может также получить запасную кнопку `Скопировать для Corel`;
- запасной `copy_text` для Corel содержит только строки формата `height width quantity`;
- без заголовков;
- без площади;
- без итогов;
- без нумерации;
- без пояснений.

Заказ со спорными строками:

- больше не получает `Скопировать для Corel` как финальную кнопку;
- первой кнопкой идёт `Скопировать для исправления`;
- `Скопировать для исправления` копирует редактируемый заказ в исходном порядке;
- подтверждённые строки нормализованы;
- спорные строки идут raw-текстом;
- без заголовков;
- без площади;
- без итогов;
- без причины блокировки;
- без пояснений.

Пример для спорного заказа:

```text
1000*400
непонятная строка
1000*600
```

`Скопировать для исправления` копирует:

```text
1000 400 1
непонятная строка
1000 600 1
```

Сохранённые кнопки:

- `Скопировать подтверждённые` и `Скопировать спорные` убрать из обычного рабочего UX;
- позже их можно перенести в служебный режим, если они понадобятся для диагностики.

Сценарий исправления:

- пользователь копирует текст через `Скопировать для исправления`;
- исправляет спорные строки;
- отправляет исправленный текст обратно боту;
- бот пересобирает заказ как новую версию;
- если спорных строк больше нет, экспорт становится доступен;
- появляется финальная кнопка `Скачать Excel для Corel`.

## 3. Парсер размеров

- Добавлена поддержка разделителей `*`, `x`, `х`, `X`, `Х`, `×`.
- Распознаются форматы:
  - `1000*400`
  - `1000 x 400`
  - `1000х400`
  - `1000×400`
  - `1000*400*2`
  - `1000 x 400 x 2`
  - `1000*400 2`
- Если количество не указано, `quantity=1`.
- Старый формат `1000 400` и `1000 400 2` сохранён.
- Проверка на этапе парсера прошла: `pytest 180 passed`.

## 4. Vision

- Создан безопасный нейтральный каркас `malyarka_vision`.
- Реальный внешний Vision/API не подключён.
- Фото никуда не отправляются.
- Telegram photo handler пока остаётся заглушкой.
- Сообщение `Фото-режим ещё не подключён` остаётся правильным текущим поведением.

## 5. Gemini

- Gemini/google-genai отменён как направление.
- `google-genai` убран из `requirements.txt` и не возвращался.
- Второй Gemini-слой откатан/нейтрализован.
- `malyarka_vision` оставлен только как нейтральная безопасная заглушка.
- Gemini API не вызывался.
- `GEMINI_API_KEY` не читался и не выводился.

## 6. DeepSeek

Приняты три безопасных этапа DeepSeek: внутренняя архитектура контракта/prompt/pipeline, bridge/fallback без внешнего AI и diagnostic preview без внешнего AI.

### 6.1. Внутренняя DeepSeek-архитектура

Созданы файлы:

- `malyarka_ai/contracts.py`
- `malyarka_ai/prompts.py`
- `malyarka_ai/pipeline.py`

Изменены файлы:

- `malyarka_ai/deepseek.py`
- `malyarka_ai/__init__.py`
- `tests/test_malyarka_ai_deepseek.py`

Текущие настройки и ограничения:

- Основной будущий AI-провайдер: DeepSeek.
- Переменная будущего ключа: `DEEPSEEK_API_KEY`.
- `base_url`: `https://api.deepseek.com`.
- Default model: `deepseek-v4-flash`.
- `real_ai_enabled=False` по умолчанию.
- `check_deepseek_ready(config)` возвращает безопасную диагностику без значения ключа: `provider`, `has_api_key`, `real_ai_enabled`, `base_url`, `model`, `reason`.
- `analyze_order_text_with_deepseek(text, config)` остаётся безопасной функцией без внешнего вызова.

Принят JSON-контракт будущего DeepSeek-ответа:

- Корень: `{"items": [...]}`.
- Типы строк: `row`, `disputed`, `info`, `scheme`.
- Поля item: `type`, `source`, `raw`, `size`, `note`, `reason`.
- Для `row` обязательны `size.height`, `size.width`, `size.quantity`.
- Для `disputed` обязателен непустой `reason`.

Добавлен `build_deepseek_order_prompt(text)`:

- запрещает додумывать;
- запрещает исправлять размеры от себя;
- первое число = `height`;
- второе число = `width`;
- третье число = `quantity`;
- если `quantity` нет, `quantity=1`;
- требует только JSON без пояснений вне JSON.

Добавлен `prepare_deepseek_order_analysis(text, config)`:

- `provider=deepseek`;
- `model=deepseek-v4-flash`;
- `external_api_called=False`;
- строит prompt;
- не читает ключи;
- не вызывает внешний API.

Добавлен `validate_deepseek_order_response(data)`:

- принимает корректный `row`;
- принимает `disputed` с `reason`;
- отклоняет `disputed` без `reason`;
- отклоняет `row` без `height/width/quantity`;
- проверяет положительные числовые размеры.

Добавлен `parse_deepseek_json_response(text)`:

- на битом JSON не падает;
- возвращает `valid=False`, `data=None`, `errors`;
- лишний текст вне JSON отклоняется.

### 6.2. DeepSeek bridge/fallback

Принят безопасный этап DeepSeek bridge/fallback без внешнего AI.

Созданы файлы:

- `malyarka_ai/bridge.py`
- `tests/test_malyarka_ai_bridge.py`

Изменён файл:

- `malyarka_ai/__init__.py`

Реализована функция `prepare_order_analysis_with_fallback(text, config)`:

- вызывает локальный `build_order_preview_from_text(text)`;
- отдельно вызывает `prepare_deepseek_order_analysis(text, config)` только для подготовки prompt/контракта;
- не вызывает DeepSeek API;
- возвращает `local_preview` / `local_result`;
- возвращает `prepared_ai_analysis` / `prepared_ai_prompt`;
- возвращает `export_allowed`;
- возвращает `disputed_rows`;
- всегда `external_api_called=False` на этом этапе;
- всегда `fallback_used=True` на этом этапе.

Принята fallback-логика:

- локальный парсер остаётся основным безопасным путём;
- если `real_ai_enabled=False` — fallback на локальный парсер;
- если ключ не передан — fallback на локальный парсер;
- если ключ передан и `real_ai_enabled=True` — API всё равно не подключён, fallback остаётся локальным;
- если будущий AI-ответ invalid или API недоступен — fallback должен быть локальным.

### 6.3. DeepSeek diagnostic preview и локальный CLI

Принят безопасный этап DeepSeek diagnostic preview без внешнего AI.

Созданы файлы:

- `malyarka_ai/diagnostics.py`
- `tests/test_malyarka_ai_diagnostics.py`

Изменён файл:

- `malyarka_ai/__init__.py`

Принят локальный CLI-режим проверки заказа через DeepSeek fallback diagnostics.

Изменённые файлы этапа локального CLI:

- `malyarka_ai/diagnostics.py`
- `tests/test_malyarka_ai_diagnostics.py`

Доступные CLI-режимы:

```powershell
.\.venv\Scripts\python.exe -m malyarka_ai.diagnostics --text "1000*400"
echo 1000*400 | .\.venv\Scripts\python.exe -m malyarka_ai.diagnostics --stdin
.\.venv\Scripts\python.exe -m malyarka_ai.diagnostics --text-file path\to\order.txt
.\.venv\Scripts\python.exe -m malyarka_ai.diagnostics --text "1000*400" --format summary
```

По умолчанию выводится JSON.

Summary-режим показывает человекочитаемую выжимку:

- `export_allowed`
- `local_corel_lines`
- `disputed_rows`
- `fallback_used`
- `external_api_called`

Diagnostic preview показывает:

- `provider`
- `model`
- `real_ai_enabled`
- `external_api_called`
- `fallback_used`
- `fallback_reason`
- `export_allowed`
- `disputed_rows`
- `local_preview`
- `local_corel_lines`
- `prepared_ai_prompt`
- `prepared_ai_analysis`

Для чистого заказа:

```text
1000*400
1000*600
```

ключевые поля результата:

- `external_api_called=false`
- `fallback_used=true`
- `export_allowed=true`
- `local_corel_lines`: `["1000 400 1", "1000 600 1"]`
- `disputed_rows.has_disputed=false`

Для заказа со спорной строкой:

```text
1000*400
непонятная строка
1000*600
```

ключевые поля результата:

- `external_api_called=false`
- `fallback_used=true`
- `export_allowed=false`
- `local_corel_lines`: `["1000 400 1", "1000 600 1"]`
- `disputed_rows.has_disputed=true`
- `disputed_rows.count=1`

Подтверждённый безопасный статус:

- Local parser остаётся основным безопасным путём.
- DeepSeek API не вызывался.
- `DEEPSEEK_API_KEY` не читался и не выводился.
- `GEMINI_API_KEY` не читался и не выводился.
- `BOT_TOKEN` не читался и не выводился.
- Telegram handlers не подключались к DeepSeek.
- Photo handler остался заглушкой.
- `google-genai` не возвращался в `requirements.txt`.
- `--run-polling` не запускался.
- `bot.py`, `.env`, `orders.db`, `.venv`, `.git`, реальные фото, токены, ключи и личные данные не трогались.

## 7. Последние проверки

- После этапа локального CLI-режима DeepSeek fallback diagnostics: `pytest 229 passed`.
- `py_compile malyarka_ai\diagnostics.py`: OK.
- Import check: `deepseek local diagnostics cli imports ok`.
- CLI `--sample`: OK.
- CLI `--text "1000*400"`: OK.
- CLI `--stdin`: OK.
- CLI `--text-file`: покрыт тестом.
- После этапа архитектурной спецификации режимов: `git status --short` выполнен.
- Новый файл спецификации виден как `?? TELEGRAM_MODES_SPEC.md`.
- `type TELEGRAM_MODES_SPEC.md` выполнен.
- После этапа спецификации router/state machine: `git status --short` выполнен.
- Новый файл виден как `?? TELEGRAM_ROUTER_STATE_MACHINE_SPEC.md`.
- `type TELEGRAM_ROUTER_STATE_MACHINE_SPEC.md` выполнен.
- После первого кодового каркаса router/state machine: `git status --short --ignored` выполнен.
- `pytest`: `247 passed`.
- `py_compile`: OK для `malyarka_telegram/modes.py`, `malyarka_telegram/session.py`, `malyarka_telegram/router.py`.
- Import новых модулей: `telegram mode router imports ok`.
- Import существующего Telegram: `existing telegram imports ok`.
- malyarka_telegram.app --check: OK, polling_started=false. 
- После этапа `TELEGRAM_ROUTER_INTEGRATION_PLAN.md`: `git status --short` выполнен.
- `type TELEGRAM_ROUTER_INTEGRATION_PLAN.md` выполнен.
- После этапа подключения router/state machine к Telegram text-handling слою: `git status --short` выполнен.
- `pytest`: `260 passed`.
- `py_compile`: OK для `malyarka_telegram/handlers.py`, `malyarka_telegram/modes.py`, `malyarka_telegram/session.py`, `malyarka_telegram/router.py`.
- Routed imports: `telegram routed handlers imports ok`.
- Existing Telegram imports: `existing telegram imports ok`.
- `malyarka_telegram.app --check`: OK, `polling_started=false`.
- После этапа подключения routed-функции к live Telegram `app.py`: `git status --short` выполнен.
- `pytest`: `272 passed`.
- `py_compile`: OK для `malyarka_telegram/app.py`, `malyarka_telegram/handlers.py`, `malyarka_telegram/modes.py`, `malyarka_telegram/session.py`, `malyarka_telegram/router.py`.
- Import check: `telegram live router imports ok`.
- `malyarka_telegram.app --check`: OK, `polling_started=false`.
- До live-проверки было: `pytest 272 passed`.
- До live-проверки `malyarka_telegram.app --check`: OK, `polling_started=false`.
- Ручная live-проверка команд режимов через `--run-polling` прошла успешно после отдельного прямого разрешения пользователя.
- Polling запускался только для ручной проверки.
- После UX-пакета кнопок копирования: `pytest 278 passed`.
- `py_compile`: OK для `malyarka_telegram/messages.py`, `malyarka_telegram/keyboards.py`, `malyarka_telegram/handlers.py`.
- Import check: `telegram copy ux imports ok`.
- `malyarka_telegram.app --check`: OK, `polling_started=false`.

## 8. Следующий шаг

Текущий Telegram-бот можно использовать для продолжения работы через режимы:

- свободный вход / уточнение намерения;
- `/заказ`;
- `/идеи`;
- `/инженер`;
- `/админ` только как скрытая диагностика владельца.

Следующий проектный этап выбирать отдельно:

- либо продолжить производственный путь: Файл Малярки как второй экспорт после Excel для Corel;
- либо продолжить инженерный путь: ручная передача задач из `/инженер` в Hermes без автозапуска Hermes из Telegram;
- либо доработать UX Telegram после реального использования.

Ограничения остаются:

- Hermes из Telegram не запускать автоматически;
- DeepSeek/OpenAI API из Telegram-бота не вызывать;
- DeepSeek внутрь Telegram-бота не подключать без отдельного этапа;
- `.env`, `BOT_TOKEN`, `DEEPSEEK_API_KEY`, `orders.db`, `.venv`, `.git`, `bot.py`, фото, токены, ключи и личные данные не трогать без отдельного прямого разрешения.

## 9. Короткий стартовый промпт для нового рабочего чата

Ты — рабочий coding-agent проекта «Малярка». Работай коротко и по делу. Основная рабочая папка проекта: `C:\Users\user\Desktop\malyarka_codex_work`, если пользователь явно не указал другую папку. Старый `bot.py` не трогай без отдельного разрешения. Не трогай `.env`, `orders.db`, `.venv`, `.git`, реальные фото, токены, ключи и личные данные. Не используй `git add .`; commit/push только после отдельного разрешения пользователя. Актуально: Telegram inline-кнопка ` Скопировать для Corel` работает; разделители размеров `*`, `x`, `х`, `X`, `Х`, `×` поддержаны; `malyarka_vision` — безопасная нейтральная заглушка; Gemini/google-genai отменён; принят безопасный DeepSeek diagnostic preview через `malyarka_ai/diagnostics.py`; команды `.\.venv\Scripts\python.exe -m malyarka_ai.diagnostics --sample` и `.\.venv\Scripts\python.exe -m malyarka_ai.diagnostics --text "1000*400"` печатают JSON-диагностику с local preview, `local_corel_lines`, `prepared_ai_prompt`, `fallback_used`, `external_api_called`, `export_allowed`, `disputed_rows`; API не вызывается, ключи не читаются, `external_api_called=False`, `fallback_used=True`, локальный парсер остаётся основным безопасным путём. Локальный CLI-режим DeepSeek fallback diagnostics принят: доступны `--text`, `--stdin`, `--text-file`, `--format summary`, по умолчанию JSON. Создана архитектурная спецификация режимов `TELEGRAM_MODES_SPEC.md` в корне проекта, потому что папки `docs` не было. Создана спецификация router/state machine `TELEGRAM_ROUTER_STATE_MACHINE_SPEC.md`: режимы `/заказ -> order`, `/чат -> chat`, `/инженер -> engineer`, `/выжимка -> summary`, `/правила -> rules`, recommended default после `/start` — `neutral`, хранение текущего режима на первом этапе — in-memory `user_id -> current_mode` без `orders.db`. Принят первый кодовый каркас `malyarka_telegram/modes.py`, `session.py`, `router.py` и тесты; router пока не подключён к живому Telegram, `app.py` и `handlers.py` не менялись. Принят кодовый этап подключения router/state machine к Telegram text-handling слою через `handle_text_message_with_router(...)`; затем routed-функция подключена к live Telegram `app.py` через `build_live_text_response(...)` и runtime `_RUNTIME_SESSION_STORE`. Ручная live-проверка Telegram через `--run-polling` выполнена после отдельного прямого разрешения пользователя: `/заказ`, `/чат`, `/инженер`, `/выжимка`, `/правила` работают; preview и copy-кнопка после `/заказ` работают; `/чат` не парсит `1000*400` как заказ. UX-пакет copy-кнопок реализован и принят: чистый заказ получает только `Скопировать для Corel`, спорный заказ первой кнопкой получает `Скопировать для исправления`, также сохранены `Скопировать подтверждённые` и `Скопировать спорные`. Следующий шаг — ручная live-проверка UX-кнопок через `--run-polling` только после отдельного прямого разрешения пользователя.

## 10. Три слоя / роли проекта

В проекте «Малярка» разделяются три слоя.

### 10.1. Рабочий бот

Рабочий бот — это производственный слой.

Назначение:

- принимать заказы;
- разбирать размеры;
- считать площадь;
- находить спорные строки;
- готовить Corel-строки;
- показывать preview;
- работать строго по принятым правилам.

Текущая техническая база:

- `malyarka_telegram`
- `malyarka_hermes`
- локальный парсер
- fallback через локальный parser

Ограничение:

Рабочий бот не должен превращаться в свободную болталку. Он не должен менять правила и код.

### 10.2. Инженер проекта

Инженер проекта — это слой управления изменениями.

Назначение:

- держать порядок проекта;
- принимать или отклонять этапы;
- формировать задания для Codex/Hermes;
- проверять отчёты Codex/Hermes;
- следить за `MALYARKA_CURRENT_STATE.md`;
- обновлять файл состояния после принятых этапов;
- не давать хаосу из разговоров напрямую попадать в рабочий код.

Текущая реализация:

- текущий чат инженера проекта;
- Codex/Hermes как исполнитель технических задач;
- `MALYARKA_CURRENT_STATE.md` как главный источник правды.

### 10.3. Разговорный помощник

Разговорный помощник — это будущий слой для свободного общения.

Назначение:

- обсуждать работу, бизнес, идеи и бытовые вопросы;
- помогать думать;
- объяснять расчёты и правила;
- предлагать улучшения;
- делать выжимки для инженера проекта.

Ограничение:

Разговорный помощник не меняет код и правила напрямую.

Если из разговора появилась полезная идея, путь такой:

идея → выжимка → инженер проекта → задание Codex/Hermes → проверка → принятие → обновление `MALYARKA_CURRENT_STATE.md` → рабочий бот

## 11. Планируемые режимы одного Telegram-бота

Пока это план, не реализация в живом Telegram.

Создана архитектурная спецификация режимов:

- `TELEGRAM_MODES_SPEC.md`

Папки `docs` в проекте не было, поэтому файл создан в корне проекта:

- `C:\Users\user\Desktop\malyarka_codex_work\TELEGRAM_MODES_SPEC.md`

Создана спецификация router/state machine:

- `TELEGRAM_ROUTER_STATE_MACHINE_SPEC.md`
- `C:\Users\user\Desktop\malyarka_codex_work\TELEGRAM_ROUTER_STATE_MACHINE_SPEC.md`

Принят первый кодовый каркас router/state machine.

Созданы файлы:

- `malyarka_telegram/modes.py`
- `malyarka_telegram/session.py`
- `malyarka_telegram/router.py`
- `tests/test_malyarka_telegram_modes.py`
- `tests/test_malyarka_telegram_router.py`

Реализованные режимы:

- `/заказ` → `order`
- `/чат` → `chat`
- `/инженер` → `engineer`
- `/выжимка` → `summary`
- `/правила` → `rules`
- default/no mode → `neutral`

Session store:

`InMemoryModeSessionStore`:

- хранит только `user_id -> current_mode` в памяти процесса;
- если режим не установлен, возвращает `neutral`;
- не пишет в файл;
- не пишет в `orders.db`;
- не читает `.env`;
- не использует внешние зависимости.

Router-защита:

- В `/чат` текст `1000*400` не отправляется в parser заказа: `should_parse_order=False`.
- В `neutral` похожий на заказ текст тоже не разбирается автоматически.
- Только `order` mode ставит `should_parse_order=True`.
- Во всех режимах `should_call_ai=False`.
- Local order parser остаётся рабочим путём только для `order` mode.

Создан план подключения router/state machine к Telegram-слою:

- `TELEGRAM_ROUTER_INTEGRATION_PLAN.md`
- `C:\Users\user\Desktop\malyarka_codex_work\TELEGRAM_ROUTER_INTEGRATION_PLAN.md`

Краткое содержание плана:

- команды режимов должны идти через router;
- текущий preview заказов сохраняется через старый локальный путь только при `should_parse_order=True`;
- `/чат` не должен отправлять текст в parser заказа;
- `neutral` не должен разбирать похожий на заказ текст автоматически;
- только `order` mode должен отправлять текст в parser заказа;
- DeepSeek API не вызывается;
- ключи не читаются;
- polling не запускается.

Будущие файлы для отдельного кодового этапа:

- `malyarka_telegram/handlers.py`
- `malyarka_telegram/app.py`, только если реально понадобится
- `tests/test_malyarka_telegram_router_integration.py`
- `tests/test_malyarka_telegram_safe_launch.py`
- `tests/test_malyarka_telegram_messages.py`, если нужно проверить preview

Предложенная схема подключения:

- добавить совместимую обёртку вокруг обработки текста;
- обёртка вызывает router;
- если router возвращает `should_parse_order=True`, текст идёт в текущий local preview/parser;
- если `should_parse_order=False`, возвращается сообщение режима;
- старую сигнатуру обработчика нужно сохранить или обернуть, чтобы не сломать существующие тесты и Telegram preview.

Тесты, описанные в плане:

- `/заказ` включает `order` mode;
- после `/заказ` текст `1000*400` идёт в parser заказа;
- `/чат` включает `chat` mode;
- в `/чат` текст `1000*400` НЕ идёт в parser заказа;
- `neutral` mode не разбирает похожий на заказ текст автоматически;
- `/инженер` не меняет код;
- `/выжимка` не создаёт задачу автоматически;
- `/правила` не меняет правила напрямую;
- copy-кнопки для order preview не ломаются;
- `app --check` остаётся `polling_started=false`;
- DeepSeek API не вызывается;
- ключи не читаются;
- `orders.db` не используется.

Риски и защита:

Риски:

- сломать текущий preview;
- отправить разговорный текст в parser заказа;
- изменить сигнатуру функции и сломать тесты;
- случайно подключить AI/API;
- тронуть `orders.db`.

Защита:

- тесты до подключения;
- совместимая функция-обёртка;
- `should_parse_order` только в `order` mode;
- `should_call_ai=False` во всех режимах;
- `orders.db` не использовать.

Принят кодовый этап подключения router/state machine к Telegram text-handling слою.

Изменённые файлы:

- `malyarka_telegram/handlers.py`
- `tests/test_malyarka_telegram_router_integration.py`

Добавлена функция `handle_text_message_with_router(text, user_id, session_store)`.

Она:

- вызывает `route_telegram_text(...)`;
- если router возвращает `should_parse_order=True`, использует старый локальный preview-путь через `build_text_response(...)`;
- если `should_parse_order=False`, возвращает `TelegramTextResponse` с сообщением режима без parser/copy-кнопок;
- не вызывает DeepSeek API;
- не читает ключи;
- не трогает `orders.db`;
- не запускает polling.

Старый `handle_text_message(text)` сохранён совместимым:

- работает без `user_id`;
- работает без `session_store`;
- возвращает строку;
- строит preview как раньше;
- текущий Telegram preview не сломан.

Поведение режимов в routed text-handling:

- `/заказ` включает `order`, сама команда не парсится.
- После `/заказ` текст `1000*400` идёт в local parser/preview.
- После `/заказ` copy-кнопка/preview сохраняются.
- `/чат` включает `chat`.
- В `/чат` текст `1000*400` не идёт в parser заказа, а предлагает перейти в `/заказ`.
- `neutral` не разбирает похожий на заказ текст автоматически.
- `/инженер`, `/выжимка`, `/правила` остаются безопасными placeholder-режимами.
- `should_call_ai=False` во всех режимах.

Принят этап подключения routed-функции к live Telegram `app.py`.

Изменённые файлы этапа:

- `malyarka_telegram/app.py`
- `tests/test_malyarka_telegram_app_router_integration.py`
- `tests/test_malyarka_telegram_router_integration.py`

В `app.py` live text-handling теперь идёт через `build_live_text_response(...)`, который вызывает `handle_text_message_with_router(text, user_id, session_store)`.

Runtime session store:

`_RUNTIME_SESSION_STORE = InMemoryModeSessionStore()`

Назначение:

- хранит текущий режим пользователя в памяти процесса;
- `user_id` берётся из `message.from_user.id`;
- есть безопасный fallback на `0`;
- `orders.db` не используется;
- база не создаётся;
- данные в файл не пишутся.

Поведение live Telegram text-handling:

- `/заказ` включает `order`, сама команда не парсится.
- После `/заказ` текст `1000*400` идёт в local parser/preview.
- После `/заказ` copy-кнопка сохраняется.
- `/чат` включает `chat`.
- В `/чат` текст `1000*400` не идёт в parser заказа, а предлагает перейти в `/заказ`.
- `neutral` не разбирает `1000*400` автоматически.
- `/инженер`, `/выжимка`, `/правила` остаются безопасными placeholder-режимами.
- `should_call_ai=False` во всех режимах.

Старый `handle_text_message(text)` совместим:

- работает без `user_id`;
- работает без `session_store`;
- старые тесты проходят;
- старый preview-путь сохранён.

Preview и copy-кнопки сохранены:

- если включён `order` mode, preview строится старым local parser путём;
- `copy_keyboard` передаётся в `_build_inline_copy_markup(...)` как раньше;
- кнопка `Скопировать для Corel` не сломана.

Безопасный статус этапа:

- Router/state machine подключён к live Telegram `app.py` для text-handling, но polling не запускался.
- `malyarka_telegram/handlers.py` менялся только для text-handling/router wrapper.
- Рабочее поведение Telegram preview и copy-кнопок сохранено.
- DeepSeek API не вызывался.
- `BOT_TOKEN`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY` не читались и не выводились.
- `app --check` показал только boolean `has_token=true`, без значения токена.
- `orders.db` не трогался.
- `.env` не трогался.
- `.venv` не трогалась.
- `.git` не трогался.
- `bot.py` не трогался.
- Фото, токены, ключи и личные данные не трогались.
- `--run-polling` не запускался на кодовых этапах до ручной проверки.
- `git add`, commit и push не выполнялись.

Ручная live-проверка Telegram через `--run-polling` выполнена после отдельного прямого разрешения пользователя.

Результат проверки:

- `/заказ` работает.
- После `/заказ` текст `1000*400` даёт preview заказа.
- Copy-кнопка Corel работает.
- `/чат` работает.
- После `/чат` текст `1000*400` не парсится как заказ.
- `/инженер` работает как безопасный placeholder-режим.
- `/выжимка` работает как безопасный placeholder-режим.
- `/правила` работает как безопасный placeholder-режим.

Polling был запущен только для ручной проверки и после проверки должен быть остановлен пользователем через `Ctrl+C`.

Безопасный статус после live-проверки:

- DeepSeek API не подключался.
- Внешние AI/API не вызывались.
- `BOT_TOKEN`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY` не выводились.
- `orders.db` не трогался.
- `.env` не трогался.
- `.venv` не трогалась.
- `.git` не трогался.
- `bot.py` не трогался.
- Реальные фото, токены, ключи и личные данные не трогались.
- `git add`, commit и push не выполнялись.

Безопасный статус после UX-пакета copy-кнопок:

- `/заказ` и live/routed preview не сломаны.
- `/чат` по-прежнему не парсит `1000*400` как заказ.
- Старый `handle_text_message(text)` совместим.
- `app.py` не менялся.
- DeepSeek API не вызывался.
- `BOT_TOKEN`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY` не читались и не выводились.
- `orders.db` не трогался.
- `.env` не трогался.
- `.venv` не трогалась.
- `.git` не трогался.
- `bot.py` не трогался.
- Фото, токены, ключи и личные данные не трогались.
- `--run-polling` не запускался.
- `git add`, commit и push не выполнялись.

Рабочим производственным режимом считается `/заказ`:

- строгий приём и разбор заказов;
- без свободной болталки;
- без додумывания размеров;
- без автоматического изменения правил и кода.

Цепочка изменений:

идея → выжимка → инженер → Codex/Hermes → проверка → состояние → рабочий бот

Отложенная очередь идей:

- AI audit;
- Mock-режим для AI-тестов;
- `TASKS_QUEUE.md`;
- RAG/Obsidian;
- Ollama;
- категоризатор рабочего бота;
- проверка актуальных цен DeepSeek перед реальным подключением.

Главное правило:

Разговорный режим не должен автоматически создавать или менять заказ.
Инженерный режим не должен менять код без задания и проверки.
Рабочий режим не должен свободно болтать и додумывать размеры.

## 12. Принципы гибкости

Не зашивать жёстко в код без необходимости:

- список допустимых разделителей размеров;
- форматы ввода заказов;
- тексты сообщений об ошибках;
- тексты подсказок пользователю;
- опасные слова и блокировки;
- пути к рабочим файлам;
- будущие режимы бота;
- правила, которые могут измениться в бизнесе.

Цель:

То, что часто меняется, должно постепенно выноситься в конфиг, правила или отдельные state-файлы, а не прятаться глубоко в код.

План на будущее:

- рассмотреть отдельный файл конфигурации, например `config.yaml` или `rules.json`;
- рассмотреть файл очереди идей/задач, например `TASKS_QUEUE.md`;
- не создавать эти файлы сейчас без отдельной задачи.













## UPDATE 0.8.12 — принятое Excel-ядро для CorelDRAW

Принят безопасный этап Excel-ядра для CorelDRAW.

Изменённые файлы этапа:
- `malyarka_core/exports/corel.py`
- `tests/test_corel_export.py`

Поведение Excel-ядра:
- `.xlsx` формируется без `openpyxl`, через стандартную библиотеку Python;
- данные начинаются со строки 2;
- заголовков нет;
- только 3 колонки: `height`, `width`, `quantity`;
- материал, цвет, покрытие, фрезеровка и примечания не попадают в Excel;
- спорный заказ блокируется;
- пустой заказ блокируется;
- при блокировке `.xlsx` не создаётся.

Проверки:
- сервер: `tests/test_corel_export.py` — `8 passed`;
- сервер: `py_compile` — OK;
- Windows: `tests/test_corel_export.py` — `8 passed in 0.06s`.

Безопасный статус:
- live Telegram не подключался;
- polling не запускался;
- gateway не запускался;
- внешние AI/API не вызывались;
- `.env`, `orders.db`, `.venv`, `.git`, `bot.py`, токены, ключи, фото и личные данные не трогались.

Актуальный следующий шаг:
подключить Telegram UX-кнопку `Скачать Excel для Corel` к готовому Excel-ядру.

## UPDATE 0.8.13 — принята Telegram UX-кнопка Excel для Corel

Принят безопасный этап внутреннего Telegram UX-слоя для кнопки `Скачать Excel для Corel`.

Изменённые файлы этапа:

- `malyarka_telegram/keyboards.py`
- `tests/test_malyarka_telegram_messages.py`
- `tests/test_malyarka_telegram_app_router_integration.py`

Поведение Telegram UX:

- для чистого заказа первой кнопкой появляется `Скачать Excel для Corel`;
- запасная кнопка `Скопировать для Corel` остаётся доступной;
- для спорного заказа кнопка `Скачать Excel для Corel` не появляется;
- для спорного заказа основной путь остаётся `Скопировать для исправления`;
- `/чат` и neutral-режим не создают Excel UX;
- реальный Excel-файл через Telegram на этом этапе не создаётся и не отправляется.

Проверки:

- сервер: `tests/test_malyarka_telegram_messages.py tests/test_malyarka_telegram_app_router_integration.py` — `34 passed in 0.09s`;
- сервер: `py_compile` — OK;
- Windows: `tests/test_malyarka_telegram_messages.py tests/test_malyarka_telegram_app_router_integration.py` — `34 passed in 0.17s`.

Безопасный статус:

- live Telegram не подключался;
- `malyarka_telegram/app.py` не изменялся;
- `bot.py` не трогался;
- polling не запускался;
- gateway не запускался;
- внешние AI/API не вызывались;
- `.env`, `orders.db`, `.venv`, `.git`, токены, ключи, фото и личные данные не трогались.

Актуальный следующий шаг:

подключить реальное создание и отправку Excel-файла через Telegram live-слой только после отдельного разрешения пользователя.

## UPDATE 0.8.14 — подключена кодовая подготовка Excel-файла в Telegram live-слое

Принят безопасный этап кодового live-слоя: кнопка `Скачать Excel для Corel` связана с подготовкой `.xlsx` через готовое Excel-ядро.

Изменённые файлы этапа:

- `malyarka_telegram/app.py`
- `tests/test_malyarka_telegram_app_router_integration.py`

Что реализовано:

- добавлен in-memory контекст последнего чистого заказа по `user_id`;
- добавлена подготовка Excel через `malyarka_core.exports.corel.export_corel_xlsx(...)`;
- кнопка `Скачать Excel для Corel` получает live callback/action;
- `.xlsx` создаётся во временной папке;
- реальная отправка файла в Telegram пока отключена;
- callback сообщает, что Excel подготовлен, но отправка файла пока отключена.

Проверки:

- сервер: `tests/test_malyarka_telegram_messages.py tests/test_malyarka_telegram_app_router_integration.py tests/test_corel_export.py` — `45 passed in 0.10s`;
- сервер: `py_compile` — OK;
- Windows: `tests/test_malyarka_telegram_messages.py tests/test_malyarka_telegram_app_router_integration.py tests/test_corel_export.py` — `45 passed in 0.18s`.

Безопасный статус:

- polling не запускался;
- gateway не запускался;
- внешние AI/API не вызывались;
- реальная отправка файла в Telegram не выполнялась;
- `.env`, `orders.db`, `.venv`, `.git`, `bot.py`, токены, ключи, фото и личные данные не трогались.

Актуальный следующий шаг:

подключить реальную отправку Excel-файла пользователю через Telegram callback и провести live-проверку только после отдельного разрешения пользователя.

## UPDATE 0.8.15 — подключена реальная отправка Excel-файла через Telegram callback

Принят безопасный кодовый этап реальной отправки Excel-файла через Telegram callback.

Изменённые файлы этапа:

- `malyarka_telegram/app.py`
- `tests/test_malyarka_telegram_app_router_integration.py`

Что реализовано:

- добавлена функция `handle_corel_excel_callback(callback, output_dir=None, document_factory=None)`;
- callback `download_corel_excel` теперь не только готовит `.xlsx`, но и вызывает отправку документа через `callback.message.answer_document(...)`;
- в live aiogram-режиме документ оборачивается в `FSInputFile`;
- в тестах используется `document_factory`, чтобы тест не зависел от наличия aiogram;
- если чистого заказа нет, файл не отправляется и пользователь получает alert-сообщение;
- `.xlsx` создаётся во временной папке.

Проверки:

- сервер: `tests/test_malyarka_telegram_messages.py tests/test_malyarka_telegram_app_router_integration.py tests/test_corel_export.py` — `47 passed in 0.11s`;
- сервер: `py_compile` — OK;
- Windows: `tests/test_malyarka_telegram_messages.py tests/test_malyarka_telegram_app_router_integration.py tests/test_corel_export.py` — `47 passed in 0.19s`.

Безопасный статус:

- polling не запускался;
- gateway не запускался;
- live Telegram не проверялся;
- внешние AI/API не вызывались;
- `.env` не читался и не менялся;
- `BOT_TOKEN` не читался и не выводился;
- `orders.db`, `.venv`, `.git`, `bot.py`, токены, ключи, фото и личные данные не трогались.

Актуальный следующий шаг:

провести live-проверку реальной отправки Excel-файла в Telegram через callback только после отдельного разрешения пользователя.

## UPDATE 0.8.16 — live-проверка отправки Excel-файла в Telegram прошла

Принят live-этап реальной отправки Excel-файла через Telegram callback.

Что проверено вручную:

- Windows-среда готова к polling: `aiogram_available=true`, `has_token=true`, `ready_for_polling=true`;
- бот запущен через `malyarka_telegram.app --run-polling`;
- команда `/заказ` включает режим заказа;
- чистый заказ:
  - `1000*400`
  - `1000*600*2`
  корректно разобран;
- preview заказа показал подтверждённые строки;
- спорных строк нет;
- экспорт доступен;
- кнопка `Скачать Excel для Corel` появилась;
- после нажатия кнопки бот прислал `.xlsx`;
- polling остановлен вручную через `Ctrl+C`.

Проверенный рабочий сценарий:

`/заказ` → текст заказа → preview → `Скачать Excel для Corel` → получение Excel-файла в Telegram.

Безопасный статус:

- polling запускался только для ручной live-проверки;
- после проверки polling остановлен;
- `.env` не выводился;
- `BOT_TOKEN` не выводился;
- `orders.db`, `.venv`, `.git`, `bot.py`, фото, токены, ключи и личные данные не трогались;
- DeepSeek API и другие внешние AI/API не вызывались;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

спроектировать и реализовать Файл Малярки как второй производственный экспорт после Excel для Corel.

## UPDATE 0.8.17 — принята спецификация личного Telegram-бота с тремя дверями

Принята спецификация:

- `TELEGRAM_THREE_DOORS_PRIVATE_BOT_SPEC.md`

Назначение спецификации:

- один личный Telegram-бот «Малярка»;
- три видимые двери:
  - `/заказ` — рабочий режим для заказов, Corel, Файла Малярки и будущего архива;
  - `/инженер` — управление проектом, задачами, проверками, отчётами и принятием этапов;
  - `/идеи` — свободный разговор, обсуждение идей и выжимки для инженера;
- один скрытый служебный режим:
  - `/админ` — только для владельца, не показывать в главном меню.

Главные правила спецификации:

- пользователь не обязан помнить команды;
- основной вход — кнопки главного меню и подсказки;
- команды `/заказ`, `/инженер`, `/идеи` остаются быстрым способом переключения;
- бот личный и доступен только владельцу по Telegram `owner_id`;
- чужие пользователи игнорируются или получают отказ;
- группы игнорируются;
- если текст с размерами пришёл без выбранного режима, бот спрашивает, что сделать;
- если фото/скриншот пришёл без выбранного режима, бот спрашивает, что сделать;
- пока Vision не подключён, фото не разбираются как заказ и не отправляются во внешние AI/API;
- `/заказ` не должен становиться свободной болталкой;
- `/идеи` не должен автоматически превращать размеры в заказ;
- `/инженер` не должен менять файлы без карточки задачи и подтверждения пользователя;
- `/админ` нужен только для служебной диагностики владельца.

Безопасный статус этапа:

- создан только файл спецификации;
- код проекта не менялся;
- `MALYARKA_CURRENT_STATE.md` на этапе создания спецификации не менялся;
- `.env`, `BOT_TOKEN`, `orders.db`, `.venv`, `.git`, `bot.py`, фото, токены, ключи и личные данные не трогались;
- polling не запускался;
- gateway не запускался;
- внешние AI/API не вызывались;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

вернуться к основному этапу проекта — спроектировать и реализовать Файл Малярки как второй производственный экспорт после Excel для Corel.

## UPDATE 0.8.18 — принята спецификация Файла Малярки

Принята спецификация:

- `MALYARKA_FILE_SPEC.md`

Назначение спецификации:

- Файл Малярки — второй производственный экспорт после Excel для Corel;
- это файл для работы малярки, а не для CorelDRAW;
- он не заменяет Excel для Corel;
- он не является архивом заказа;
- он не является базой данных;
- он не должен угадывать материал, цвет, цену или спорные строки.

Главные правила Файла Малярки:

- Excel для Corel остаётся чистым экспортом только `height / width / quantity`;
- Файл Малярки должен содержать производственные данные;
- минимальные колонки первого этапа:
  - номер строки;
  - высота;
  - ширина;
  - количество;
  - площадь одной детали;
  - площадь строки;
  - статус строки `confirmed / disputed`;
  - raw-текст;
  - причина спорности, если есть;
- площадь одной детали считается как `height * width / 1_000_000`;
- площадь строки считается как `item_area_m2 * quantity`;
- итоговая площадь считается только по подтверждённым строкам;
- спорные строки не включаются в чистовой итог;
- при спорных строках чистовой Файл Малярки блокируется или явно помечается как неполный;
- материал, цвет, толщина, тип работы, примечания и цена добавляются только если подтверждены;
- неподтверждённая цена не считается.

Безопасный статус этапа:

- создан только файл спецификации;
- код проекта не менялся;
- `MALYARKA_CURRENT_STATE.md` на этапе создания спецификации не менялся;
- `.env`, `BOT_TOKEN`, `orders.db`, `.venv`, `.git`, `bot.py`, фото, токены, ключи и личные данные не трогались;
- polling не запускался;
- gateway не запускался;
- внешние AI/API не вызывались;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

реализовать первый кодовый этап Файла Малярки по принятой спецификации `MALYARKA_FILE_SPEC.md`, без изменения Excel для Corel, без `orders.db`, без фото/Vision, без DeepSeek API и без старого `bot.py`.

## UPDATE 0.8.19 — принят read-only Telegram-пульт Hermes

Принят первый безопасный кодовый этап Telegram-пульта Hermes внутри бота «Малярка».

Что реализовано:

- добавлен безопасный фундамент личного пульта управления;
- добавлена owner_id-механика;
- добавлен модуль `malyarka_telegram/access.py`;
- добавлен тест `tests/test_malyarka_telegram_access.py`;
- `/инженер` работает как read-only режим управления проектом;
- `/идеи` работает как read-only режим свободного обсуждения;
- `/админ` работает как скрытый диагностический режим;
- `/заказ` сохранён и не сломан;
- Excel для Corel сохранён и не сломан;
- реальный Hermes из Telegram пока не запускается;
- команды вида `!...` получают безопасный отказ;
- импорт `malyarka_hermes` из Telegram handlers/app убран;
- `owner_id` читается только через `MALYARKA_TELEGRAM_OWNER_ID`;
- диагностика показывает только boolean `owner_id_configured=true/false`, без значения owner_id.

Проверки:

- сервер: `88 passed`;
- сервер: `py_compile` — OK;
- Windows: `88 passed`;
- Windows: `py_compile` — OK;
- Windows `app --check`:
  - `has_token=true`;
  - `owner_id_configured=true` при временной переменной PowerShell;
  - `ready_for_polling=true`;
  - `polling_started=false`.

Live-проверка Telegram:

- `/инженер` включается и показывает read-only режим;
- `/идеи` включается;
- в `/идеи` текст `1000*400` не разбирается как заказ;
- `/заказ` работает;
- заказ `1000*400` и `1000*600*2` даёт preview;
- кнопка `Скачать Excel для Corel` есть;
- кнопка `Скопировать для Corel` есть;
- `/админ` показывает безопасную диагностику:
  - `current_mode=admin`;
  - `owner_id_configured=true`;
  - `polling_started=false`;
  - `state_version=unknown` как безопасный fallback, если файл состояния не найден рядом с кодом.

Безопасный статус:

- polling запускался только для ручной live-проверки;
- после проверки polling остановлен пользователем;
- gateway не запускался;
- реальный Hermes из Telegram не запускался;
- внешние AI/API не вызывались;
- `.env` не читался и не менялся;
- `BOT_TOKEN` не выводился;
- `orders.db` не трогался;
- `.venv`, `.git`, `bot.py`, реальные фото, токены, ключи и личные данные не трогались;
- git add, commit, push не выполнялись.

Важно:

- `owner_id` пока проверялся временно через PowerShell-переменную `MALYARKA_TELEGRAM_OWNER_ID`;
- постоянная запись `MALYARKA_TELEGRAM_OWNER_ID` в `.env` ещё не выполнялась;
- без постоянной настройки owner_id пульт не будет автоматически включаться при новом запуске.

Актуальный следующий шаг:

сделать карточку задачи read-only в режиме `/инженер`:

- `/инженер` принимает текст задачи;
- формирует карточку:
  - ЗАДАЧА;
  - ОЖИДАЕМЫЙ РЕЗУЛЬТАТ;
  - МОЖНО;
  - НЕЛЬЗЯ;
  - ПРОВЕРКИ;
  - СТАТУС;
- показывает кнопки:
  - Разрешаю;
  - Отмена;
  - Исправить задачу;
- на этом этапе всё ещё не запускать Hermes автоматически;
- не менять файлы без отдельного подтверждения;
- не запускать polling/gateway/API без отдельного разрешения.

## UPDATE 0.8.20 — принята read-only карточка задачи в `/инженер`

Принят следующий безопасный этап Telegram-пульта Hermes: карточка задачи read-only в режиме `/инженер`.

Что реализовано:

- в активном режиме `/инженер` обычный текст пользователя превращается в карточку задачи;
- карточка содержит блоки:
  - `ЗАДАЧА`;
  - `ОЖИДАЕМЫЙ РЕЗУЛЬТАТ`;
  - `МОЖНО`;
  - `НЕЛЬЗЯ`;
  - `ПРОВЕРКИ`;
  - `СТАТУС`;
- карточка явно помечена как read-only;
- добавлены кнопки:
  - `Разрешаю`;
  - `Отмена`;
  - `Исправить задачу`;
- кнопки пока не запускают реальные изменения;
- реальный Hermes из Telegram не запускается;
- команды, polling, gateway и внешние API не запускаются;
- `/заказ` сохранён и не сломан;
- Excel для Corel сохранён и не сломан;
- `/идеи` сохранён как read-only режим обсуждения;
- `/админ` сохранён как скрытая безопасная диагностика.

Изменённые файлы этапа:

- `malyarka_telegram/messages.py`;
- `malyarka_telegram/keyboards.py`;
- `malyarka_telegram/router.py`;
- `malyarka_telegram/handlers.py`;
- `tests/test_malyarka_telegram_router.py`;
- `tests/test_malyarka_telegram_router_integration.py`;
- `tests/test_malyarka_telegram_app_router_integration.py`;
- `tests/test_malyarka_telegram_messages.py`.

Проверки:

- сервер: `89 passed`;
- сервер: `py_compile` — OK;
- Windows: `89 passed`;
- Windows: `py_compile` — OK;
- Windows `app --check`:
  - `has_token=true`;
  - `owner_id_configured=true` при временной переменной PowerShell;
  - `ready_for_polling=true`;
  - `polling_started=false`.

Live-проверка Telegram:

- `/инженер` включает read-only инженерный режим;
- сообщение `сделать файл малярки` создаёт карточку задачи;
- карточка содержит обязательные блоки;
- кнопки `Разрешаю`, `Отмена`, `Исправить задачу` отображаются;
- кнопка `Разрешаю` на этом этапе не нажималась и реальные изменения не запускались.

Безопасный статус:

- polling запускался только для ручной live-проверки;
- после проверки polling остановлен пользователем;
- gateway не запускался;
- реальный Hermes из Telegram не запускался;
- внешние AI/API не вызывались;
- `.env` не читался и не менялся;
- `BOT_TOKEN` не выводился;
- `orders.db` не трогался;
- `.venv`, `.git`, `bot.py`, реальные фото, токены, ключи и личные данные не трогались;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

сделать read-only обработку кнопок карточки задачи в режиме `/инженер`: `Разрешаю`, `Отмена`, `Исправить задачу`, без запуска Hermes и без изменения файлов из Telegram.

## UPDATE 0.8.21 — принята read-only обработка кнопок карточки `/инженер`

Принят следующий безопасный этап Telegram-пульта Hermes: read-only обработка кнопок карточки задачи в режиме `/инженер`.

Что реализовано:

- кнопка `Разрешаю` обрабатывается безопасно;
- кнопка `Отмена` обрабатывается безопасно;
- кнопка `Исправить задачу` обрабатывается безопасно;
- кнопки не запускают Hermes;
- кнопки не меняют файлы;
- кнопки не запускают команды;
- кнопки не запускают polling/gateway/API;
- callback-обработка подключена в `malyarka_telegram/app.py`;
- `/заказ` сохранён и не сломан;
- Excel для Corel сохранён и не сломан;
- `/идеи` сохранён как read-only режим обсуждения;
- `/админ` сохранён как скрытая безопасная диагностика.

Поведение кнопок:

- `Разрешаю`:
  - карточка отмечается как разрешённая для будущего этапа;
  - на этом шаге Hermes не запускается;
  - файлы не меняются;
  - для реального выполнения потребуется отдельное подтверждение.

- `Отмена`:
  - карточка задачи отменяется;
  - никакие действия не выполняются.

- `Исправить задачу`:
  - бот просит отправить исправленный текст задачи;
  - после исправления должна снова формироваться read-only карточка;
  - Hermes не запускается;
  - файлы не меняются.

Изменённые файлы этапа:

- `malyarka_telegram/messages.py`;
- `malyarka_telegram/keyboards.py`;
- `malyarka_telegram/app.py`;
- `tests/test_malyarka_telegram_messages.py`;
- `tests/test_malyarka_telegram_app_router_integration.py`.

Проверки:

- сервер: `94 passed`;
- сервер: `py_compile` — OK;
- Windows: `94 passed`;
- Windows: `py_compile` — OK;
- Windows `app --check`:
  - `has_token=true`;
  - `owner_id_configured=true` при временной переменной PowerShell;
  - `ready_for_polling=true`;
  - `polling_started=false`.

Live-проверка Telegram:

- карточка задачи в `/инженер` отображается;
- кнопка `Разрешаю` проверена: показывает безопасное всплывающее сообщение, Hermes не запускает и файлы не меняет;
- кнопка `Отмена` проверена пользователем и соответствует норме;
- кнопка `Исправить задачу` проверена пользователем и соответствует норме.

Безопасный статус:

- polling запускался только для ручной live-проверки;
- после проверки polling остановлен пользователем;
- gateway не запускался;
- реальный Hermes из Telegram не запускался;
- внешние AI/API не вызывались;
- `.env` не читался и не менялся;
- `BOT_TOKEN` не выводился;
- `orders.db` не трогался;
- `.venv`, `.git`, `bot.py`, реальные фото, токены, ключи и личные данные не трогались;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

сделать ручную передачу задачи из `/инженер` в Hermes без автозапуска Hermes из Telegram: бот готовит copy-ready задание, пользователь вручную переносит его в Hermes.

## UPDATE 0.8.22 — принята спецификация свободного входа, резервного AI и независимого ревью

Принята спецификация:

- `FREE_ENTRY_INTENT_ROUTER_SPEC.md`

Файл создан на сервере и перенесён на Windows:

- сервер: `/root/malyarka_codex_work/FREE_ENTRY_INTENT_ROUTER_SPEC.md`;
- Windows: `C:\Users\user\Desktop\malyarka_codex_work\FREE_ENTRY_INTENT_ROUTER_SPEC.md`.

Проверено:

- размер файла: `38678` байт;
- файл содержит `701` строку;
- первые строки файла читаются корректно после `chcp 65001` и `Get-Content -Encoding UTF8`;
- русская кодировка файла не сломана;
- первоначальные кракозябры были только проблемой отображения PowerShell.

Что зафиксировано в спецификации:

1. Свободный вход / Free Entry

Пользователь может писать обычными словами, без обязательного знания команд.

Бот должен понимать смысл фразы и направлять в нужную дверь:

- `/идеи` — свободное обсуждение, интервьюер, промпт-инженер, выжимки;
- `/заказ` — новый заказ, продолжение заказа, исправление заказа, Excel для Corel, будущий Файл Малярки;
- `/инженер` — карточка задачи, промпт для Hermes/Codex, ручная передача задачи;
- `/админ` — скрытая диагностика владельца.

Если намерение понятно, бот предлагает или включает нужный режим.

Если намерение неясно, бот обязан задать уточняющий вопрос, а не угадывать.

2. Резервный AI-провайдер для Hermes

DeepSeek настроен как резервный провайдер Hermes.

Проверено:

- провайдер: `deepseek`;
- модель: `deepseek-reasoner`;
- после пополнения баланса Hermes ответил `ok`;
- резервный контур Hermes через DeepSeek работает.

Важно:

- DeepSeek для Hermes — это настройка инструмента Hermes, а не подключение DeepSeek внутрь Telegram-бота;
- ключ DeepSeek не добавлялся в `.env` проекта «Малярка`;
- ключ DeepSeek не записывался в `MALYARKA_CURRENT_STATE.md`;
- будущий AI-слой внутри Telegram-бота — отдельный этап.

3. Независимое ревью / cross-provider QA

Зафиксирована будущая схема контроля качества:

- Codex / ChatGPT / Hermes — основной исполнитель;
- DeepSeek или другой отдельный AI-провайдер — независимый ревьюер;
- пользователь / инженер проекта — принимает решение.

Независимый ревьюер должен проверять:

- какие файлы изменены;
- не тронуты ли запрещённые зоны;
- не нарушены ли правила `MALYARKA_CURRENT_STATE.md`;
- не сломан ли `/заказ`;
- не сломан ли Excel для Corel;
- не запущены ли запрещённые API/polling/gateway;
- достаточно ли тестов;
- есть ли логические противоречия;
- можно ли принимать этап.

Безопасный статус этапа:

- создан только новый markdown-файл спецификации;
- код проекта не менялся;
- `MALYARKA_CURRENT_STATE.md` на этапе создания спецификации Hermes не менял;
- `.env` не читался и не менялся;
- `BOT_TOKEN` не читался и не выводился;
- `orders.db` не трогался;
- `.venv`, `.git`, `bot.py`, реальные фото, токены, ключи и личные данные не трогались;
- polling/gateway/API из проекта «Малярка» не запускались;
- Hermes из Telegram не запускался;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

первый безопасный кодовый этап Free Entry / Intent Dispatcher: создать локальное распознавание намерений по сигнатурам, без внешнего AI/API, без изменения рабочей логики `/заказ` и без подключения DeepSeek внутрь Telegram-бота.

## UPDATE 0.8.23 — принят первый кодовый этап Free Entry / Intent Dispatcher

Принят первый безопасный кодовый этап Free Entry / Intent Dispatcher.

Что реализовано:

- создан локальный модуль `malyarka_telegram/intent.py`;
- создана структура результата `IntentResult`;
- реализована функция `classify_intent(text)`;
- распознавание работает только локально по сигнатурам и regex;
- внешний AI/API не вызывается;
- `.env` не читается;
- `orders.db` не используется;
- Free Entry пока не подключён к live Telegram router/app.py;
- рабочая логика `/заказ` не изменялась;
- Excel для Corel не менялся и не сломан.

Распознаваемые intent:

- `order` — заказ, размеры, фасады, детали, Excel/Corel;
- `engineer` — инженерная задача, Hermes, статус, отчёт, этап;
- `ideas` — идея, обсуждение, подумать, интервью, промпт;
- `admin` — диагностика/админ, только безопасно;
- `unknown` — непонятная или двусмысленная фраза, нужен уточняющий вопрос.

Примеры поведения:

- `1000*400` → `order`;
- `1000 x 400 2` → `order`;
- `прими заказ` → `order`;
- `Excel для Corel` → `order`;
- `какой статус проекта` → `engineer`;
- `задача для Hermes` → `engineer`;
- `у меня есть идея` → `ideas`;
- `давай обсудим новую идею` → `ideas`;
- `сделай это нормально` → `unknown` + уточнение;
- `разберись с файлом малярки` → `unknown` + уточнение;
- `дай .env` → blocked.

Изменённые файлы этапа:

- `malyarka_telegram/intent.py`;
- `malyarka_telegram/__init__.py`;
- `tests/test_malyarka_telegram_intent.py`.

Проверки:

- сервер: `tests/test_malyarka_telegram_intent.py` — `97 passed`;
- сервер: общий набор Telegram/Corel тестов — `191 passed`;
- сервер: `py_compile malyarka_telegram/intent.py` — OK;
- Windows: `tests/test_malyarka_telegram_intent.py` — `97 passed in 0.16s`;
- Windows: общий набор Telegram/Corel тестов — `191 passed in 0.40s`;
- Windows: `py_compile malyarka_telegram\intent.py` — OK.

Безопасный статус:

- Free Entry пока не подключён к live Telegram;
- polling не запускался;
- gateway не запускался;
- Hermes из Telegram не запускался;
- DeepSeek/OpenAI API из проекта не вызывались;
- DeepSeek внутри Telegram-бота не подключался;
- `.env` не читался и не менялся;
- `BOT_TOKEN` не читался и не выводился;
- `DEEPSEEK_API_KEY` не читался и не выводился;
- `orders.db` не трогался;
- `.venv`, `.git`, `bot.py`, реальные фото, токены, ключи и личные данные не трогались;
- `app.py`, `handlers.py`, `router.py` не менялись;
- `MALYARKA_CURRENT_STATE.md`, `FREE_ENTRY_INTENT_ROUTER_SPEC.md`, `TELEGRAM_*_SPEC.md` на кодовом этапе Hermes не менялись;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

подключить Free Entry / Intent Dispatcher к Telegram text-handling слою: сначала только в neutral mode, через локальный `classify_intent(...)`, без внешнего AI/API, без изменения рабочей логики `/заказ`, без подключения DeepSeek внутрь Telegram-бота.

## UPDATE 0.8.24 — Free Entry подключён к neutral mode

Принят безопасный кодовый этап подключения Free Entry / Intent Dispatcher к Telegram text-handling слою.

Что реализовано:

- `classify_intent(...)` подключён в `neutral mode`;
- свободные фразы пользователя теперь обрабатываются локальным сигнатурным классификатором;
- внешний AI/API не вызывается;
- DeepSeek/OpenAI API из Telegram-бота не вызываются;
- DeepSeek внутрь Telegram-бота не подключался;
- Hermes из Telegram не запускается.

Поведение в `neutral mode`:

- `order` → бот предлагает перейти в `/заказ`;
- `engineer` → бот предлагает перейти в `/инженер`;
- `ideas` → бот предлагает перейти в `/идеи`;
- `admin` → бот не открывает скрытый режим автоматически, а уточняет действие;
- `unknown` → бот задаёт уточняющий вопрос;
- `blocked` → бот даёт безопасный отказ.

Изменённые файлы этапа:

- `malyarka_telegram/router.py`;
- `tests/test_malyarka_telegram_router.py`.

Проверки:

- сервер: общий набор Telegram/Corel/intent тестов — `196 passed`;
- сервер: `py_compile malyarka_telegram/intent.py malyarka_telegram/router.py malyarka_telegram/handlers.py` — OK;
- Windows: subset router/integration/intent — `160 passed in 0.33s`;
- Windows: общий набор Telegram/Corel/intent тестов — `196 passed in 0.43s`;
- Windows: `py_compile malyarka_telegram\intent.py malyarka_telegram\router.py malyarka_telegram\handlers.py` — OK.

Безопасный статус:

- `/заказ` сохранён;
- Excel для Corel сохранён;
- `app.py` не менялся;
- `handlers.py` не менялся;
- Excel/Corel-ядро не менялось;
- polling не запускался;
- gateway не запускался;
- Hermes из Telegram не запускался;
- DeepSeek/OpenAI API из Telegram-бота не вызывались;
- `.env` не читался и не менялся;
- `BOT_TOKEN` не читался и не выводился;
- `DEEPSEEK_API_KEY` не читался и не выводился;
- `orders.db` не трогался;
- `.venv`, `.git`, `bot.py`, реальные фото, токены, ключи и личные данные не трогались;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

добавить inline-кнопки уточнения для Free Entry в neutral mode: `Новый заказ`, `Идея / обсуждение`, `Инженер`, `Отмена`, без внешнего AI/API и без автозапуска Hermes.

## UPDATE 0.8.25 — добавлены inline-кнопки уточнения Free Entry

Принят безопасный кодовый этап inline-кнопок уточнения для Free Entry в `neutral mode`.

Реализовано:

- для `action="clarify_intent"` добавлена inline-клавиатура уточнения;
- кнопки: `Новый заказ`, `Идея / обсуждение`, `Инженер`, `Отмена`;
- `/админ` в уточняющих кнопках не показывается;
- callback-кнопки безопасно переключают режим или отменяют уточнение;
- Hermes из Telegram не запускается;
- внешний AI/API не вызывается;
- DeepSeek внутрь Telegram-бота не подключался.

Callback data:

- `free_entry_order` → включает `/заказ`;
- `free_entry_ideas` → включает `/идеи`;
- `free_entry_engineer` → включает `/инженер`;
- `free_entry_cancel` → оставляет/возвращает `neutral`.

Изменённые файлы:

- `malyarka_telegram/keyboards.py`;
- `malyarka_telegram/handlers.py`;
- `malyarka_telegram/app.py`;
- `tests/test_malyarka_telegram_router_integration.py`;
- `tests/test_malyarka_telegram_app_router_integration.py`.

Проверки:

- сервер: `203 passed`;
- сервер: `py_compile` — OK;
- Windows: `189 passed in 0.45s`;
- Windows: `203 passed in 0.40s`;
- Windows: `py_compile` — OK.

Безопасный статус:

- `/заказ` сохранён;
- Excel для Corel сохранён;
- polling на кодовом этапе не запускался;
- gateway не запускался;
- Hermes из Telegram не запускался;
- DeepSeek/OpenAI API из Telegram-бота не вызывались;
- `.env`, `BOT_TOKEN`, `DEEPSEEK_API_KEY`, `orders.db`, `.venv`, `.git`, `bot.py`, фото, токены, ключи и личные данные не трогались;
- git add, commit, push не выполнялись.

Актуальный следующий шаг:

ручная live-проверка inline-кнопок уточнения Free Entry через `--run-polling` только после отдельного прямого разрешения пользователя.

## UPDATE 0.8.26 — live-проверка inline-кнопок Free Entry прошла

Принята ручная live-проверка inline-кнопок уточнения Free Entry через Telegram polling.

Что проверено в живом Telegram:

- непонятная фраза в `neutral mode` показывает уточняющий вопрос;
- появляются кнопки:
  - `Новый заказ`;
  - `Идея / обсуждение`;
  - `Инженер`;
  - `Отмена`;
- кнопка `/админ` в уточняющих кнопках не показывается;
- кнопка `Новый заказ` работает и включает режим `/заказ`;
- после перехода в `/заказ` заказ `1000*400` даёт preview;
- кнопка `Идея / обсуждение` работает и включает режим `/идеи`;
- в `/идеи` текст не оформляется автоматически как заказ;
- кнопка `Инженер` работает и включает режим `/инженер`;
- кнопка `Отмена` работает и отменяет уточнение.

Безопасный статус live-проверки:

- polling запускался только после отдельного прямого разрешения пользователя;
- после проверки polling остановлен пользователем;
- Hermes из Telegram не запускался;
- gateway не запускался;
- DeepSeek/OpenAI API из Telegram-бота не вызывались;
- DeepSeek внутрь Telegram-бота не подключался;
- `.env` не менялся;
- `BOT_TOKEN` не выводился;
- `DEEPSEEK_API_KEY` не читался и не выводился;
- `orders.db` не трогался;
- `.venv`, `.git`, `bot.py`, реальные фото, токены, ключи и личные данные не трогались;
- git add, commit, push не выполнялись.

Итог:

Telegram-бот можно использовать для продолжения работы через свободный вход и двери `/заказ`, `/идеи`, `/инженер`. Автозапуск Hermes из Telegram всё ещё запрещён и не подключён.

Актуальный следующий шаг:

выбрать следующий проектный этап отдельно: Файл Малярки, ручная передача задач из `/инженер` в Hermes или UX-доработки Telegram после реального использования.

