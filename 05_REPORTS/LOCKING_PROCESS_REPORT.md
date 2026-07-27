# LOCKING_PROCESS_REPORT

## Блок

BATCH_004E_FIND_LOCKING_PROCESS_FOR_MALYARKA_CODEX_WORK

## Проверяемая папка

`C:\Users\user\Desktop\malyarka_codex_work`

## Существование папки

Папка существует на рабочем столе.

Папка назначения в карантине не создана:

`C:\Users\user\Desktop\[удалён]\malyarka_codex_work`

## Использованные способы диагностики

1. Проверено существование папки через `Test-Path`.
2. Проверены процессы через `Get-CimInstance Win32_Process`.
3. Выполнен поиск процессов по точной строке `malyarka_codex_work`.
4. Выполнен поиск процессов по словам `malyarka`, `Hermes`, `python`, `code`, `powershell`, `pwsh`, `cmd`, `node`.
5. Проверено наличие `handle.exe` в PATH.
6. Создан и запущен диагностический скрипт `04_TOOLS/windows/find_locking_process.ps1`.
7. Скрипт попытался использовать Windows Restart Manager для определения процессов, связанных с путём.

## handle.exe

`handle.exe` не найден в PATH.

Скачивание и установка Sysinternals не выполнялись.

## Restart Manager

Диагностический скрипт:

`C:\Users\user\Desktop\Hermes-Clean\04_TOOLS\windows\find_locking_process.ps1`

Результат:

- метод: Restart Manager;
- папка существует;
- список процессов не получен;
- ошибка: `RmGetList failed with code 5`.

Код 5 означает отказ доступа для этого способа диагностики в текущем контексте.

## Точное совпадение malyarka_codex_work

Процессов, у которых в имени, пути или командной строке явно указано `malyarka_codex_work`, не найдено.

## Найденные кандидаты

### Кандидат 1

- Имя процесса: `cmd.exe`
- PID: `11680`
- Родительский PID: `8200`
- Путь процесса: `C:\WINDOWS\system32\cmd.exe`
- Командная строка: `C:\WINDOWS\system32\cmd.exe /c ""E:\[удалённый архив]\app\memory-gateway\Start-MemoryGateway.bat" "`
- Почему кандидат: процесс запускает старый компонент `memory-gateway` из `E:\[архив] [удалённый архив]`, то есть связан со старым Hermes-окружением.
- Можно ли безопасно закрыть вручную: возможно, но только после подтверждения пользователя. Codex не закрывал процесс.

### Кандидат 2

- Имя процесса: `node.exe`
- PID: `18920`
- Родительский PID: `11680`
- Родительский процесс: `cmd.exe`
- Путь процесса: `C:\Program Files\nodejs\node.exe`
- Командная строка: `node  server.js`
- Почему кандидат: дочерний процесс от `cmd.exe` PID 11680, который запущен из `E:\[удалённый архив]\app\memory-gateway\Start-MemoryGateway.bat`. Вероятно относится к старому Hermes memory-gateway.
- Можно ли безопасно закрыть вручную: возможно, но только после подтверждения пользователя. Codex не закрывал процесс.

### Кандидат 3

- Имя процесса: `chrome.exe`
- PID: `11236`
- Родительский PID: `8200`
- Путь процесса: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- Командная строка: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --single-argument E:\[удалённый архив]\app\hermes-dashboard\index.html`
- Почему кандидат: открыт старый Hermes dashboard из `E:\[архив] [удалённый архив]`.
- Можно ли безопасно закрыть вручную: возможно, но только после подтверждения пользователя. Codex не закрывал процесс.

## Диагностические процессы, не считать блокировщиками

Во время диагностики появлялись PowerShell-процессы с командами поиска по словам `malyarka` и `Hermes`.

Они относятся к текущей диагностике Codex и не являются устойчивыми кандидатами на блокировку папки.

## Вывод

Точный блокирующий процесс не доказан.

Вероятные кандидаты связаны со старым Hermes-окружением:

- `cmd.exe` PID 11680, запускающий `E:\[удалённый архив]\app\memory-gateway\Start-MemoryGateway.bat`;
- `node.exe` PID 18920, дочерний процесс от этого `cmd.exe`;
- `chrome.exe` PID 11236, открывший `E:\[удалённый архив]\app\hermes-dashboard\index.html`.

Никакие процессы не закрывались.

Никакие файлы не удалялись.

Содержимое `malyarka_codex_work`, `.env`, токены, ключи, базы и реальные заказы не читались.

## Что делать дальше

Пользователь должен решить, можно ли вручную закрыть найденные кандидаты:

1. `chrome.exe` PID 11236, если это старое окно Hermes dashboard.
2. `cmd.exe` PID 11680, если это старый Hermes memory-gateway.
3. `node.exe` PID 18920, если это дочерний сервер старого memory-gateway.

Следующий крупный блок: BATCH_004F_USER_APPROVES_PROCESS_CLOSE_OR_MANUAL_CLOSE.
