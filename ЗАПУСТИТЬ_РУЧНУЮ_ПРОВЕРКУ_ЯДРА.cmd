@echo off
setlocal

set "ROOT=E:\Hermes-Hub"
set "PROJECT=%ROOT%\projects\malyarka-clean"
set "PYTHONPATH=%PROJECT%\src"

echo Malyarka Clean manual core check
echo =================================
echo.
echo This does not run Telegram, Vision, API, database, Excel or Corel export.
echo.

cd /d "%PROJECT%"
python "%PROJECT%\tools\manual_core_check.py"

set "EXIT_CODE=%ERRORLEVEL%"
echo.
if "%EXIT_CODE%"=="0" (
    echo Done: manual check finished successfully.
) else (
    echo Error: manual check finished with code %EXIT_CODE%.
)

if /I not "%~1"=="--no-pause" pause
exit /b %EXIT_CODE%
