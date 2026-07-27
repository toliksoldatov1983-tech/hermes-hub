# Hermes commands

Краткая памятка по командам Hermes, которые помогают работать крупными блоками и не терять контекст.

## Главные slash-команды в Hermes Desktop

`/goal <задача>` - поставить долгую цель. Hermes продолжает работу до логического конца, паузы, очистки или лимита.

`/goal draft <цель>` - попросить Hermes развернуть цель в более строгий контракт: результат, проверки, ограничения, когда остановиться.

`/goal status` - показать текущую цель.

`/goal show` - показать цель и контракт выполнения.

`/goal pause` - поставить цель на паузу.

`/goal resume` - продолжить цель.

`/goal clear` - очистить активную цель.

`/learn <что запомнить>` - превратить повторяющийся порядок работы в навык.

`/journey` - открыть карту памяти и навыков.

`/learning` - алиас для `/journey`.

`/memory-graph` - алиас для `/journey`.

`/tools` - посмотреть или переключить доступные инструменты.

`/status` - состояние текущей сессии.

`/queue <сообщение>` или `/q <сообщение>` - поставить сообщение в очередь.

`/steer <уточнение>` - направить уже запущенную работу.

`/retry` - повторить последний запрос.

`/rollback` - посмотреть или восстановить файловые чекпоинты.

`/undo` - убрать последний обмен в чате.

`/usage` - показать расход токенов.

`/compress` - сжать длинный контекст.

`/new` - новая сессия.

`/branch` - ответвить текущую работу в новую сессию.

`/resume` - вернуться к сохраненной сессии.

## Полезные CLI-команды

Запускать из терминала:

```powershell
hermes logs
hermes logs errors
hermes logs desktop
hermes logs gui
hermes logs --since 1h
```

Логи и диагностика.

```powershell
hermes doctor
hermes status
hermes status --all
```

Проверка состояния установки.

```powershell
hermes backup --quick
hermes checkpoints status
```

Быстрый бэкап состояния и проверка чекпоинтов.

```powershell
hermes sessions list
hermes sessions browse
hermes sessions rename <ID> <TITLE>
```

Работа с историями сессий.

```powershell
hermes project list
hermes project create <NAME>
hermes project use <NAME>
```

Работа с проектами.

```powershell
hermes skills list
hermes skills search <QUERY>
hermes skills install <SKILL>
hermes skills list-modified
```

Навыки.

```powershell
hermes tools --summary
hermes tools list
```

Инструменты.

```powershell
hermes cron list
hermes cron status
```

Плановые задачи.

```powershell
hermes kanban list
hermes kanban show <TASK>
hermes kanban stats
```

Доска задач для больших проектов.

```powershell
hermes config path
hermes config check
hermes config show
```

Конфигурация. Не редактировать `.env` без отдельной необходимости.

```powershell
hermes prompt-size
```

Размер системного промпта, памяти, навыков и схем инструментов.

## Опасные команды

Запускать только после отдельного подтверждения:

`hermes doctor --fix`

`hermes memory reset`

`hermes sessions delete`

`hermes sessions prune`

`hermes checkpoints clear`

`hermes kanban complete`

`hermes kanban archive`

`hermes uninstall`

Любые команды, которые меняют `.env`, токены, ключи, реальные заказы или запускают live-ботов.

## Как использовать в работе

Для большой задачи сначала писать:

```text
/goal draft <что нужно получить>
```

Для уже понятной задачи:

```text
/goal <что нужно сделать до конца>
```

После повторяющегося успешного процесса:

```text
/learn запомни этот порядок работы как навык
```

Для проверки накопленных навыков и памяти:

```text
/journey
```

Для диагностики проблем:

```powershell
hermes logs errors --since 1h
hermes logs desktop --since 1h
hermes doctor
```
