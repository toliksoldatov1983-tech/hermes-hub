@echo off
setlocal

cd /d "%~dp0"
set "PYTHONPATH=%~dp0"

if "%MALYARKA_TELEGRAM_BOT_TOKEN%"=="" (
    echo ERROR: MALYARKA_TELEGRAM_BOT_TOKEN is not set.
    echo Do not store the token in this file.
    echo Set the token outside this script before running the bot.
    exit /b 2
)

if "%MALYARKA_TELEGRAM_OWNER_ID%"=="" (
    echo ERROR: MALYARKA_TELEGRAM_OWNER_ID is not set.
    echo Set the owner id outside this script before running the bot.
    exit /b 2
)

python -m malyarka_telegram.app --run-polling

endlocal
