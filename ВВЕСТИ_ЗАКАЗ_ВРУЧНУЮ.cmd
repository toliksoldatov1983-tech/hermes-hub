@echo off
setlocal

set "ROOT=E:\Hermes-Hub"
set "PROJECT=%ROOT%\projects\malyarka-clean"
set "PYTHONPATH=%PROJECT%\src"
set "NO_PAUSE="
set "PY_ARGS="

:parse_args
if "%~1"=="" goto run
if /I "%~1"=="--no-pause" (
    set "NO_PAUSE=1"
    shift
    goto parse_args
)
set PY_ARGS=%PY_ARGS% %1
shift
goto parse_args

:run
echo Malyarka Clean user order input
echo =================================
echo.
echo This does not run Telegram, Vision, API, database, Excel or Corel export.
echo.

cd /d "%PROJECT%"
python "%PROJECT%\tools\user_order_input.py" %PY_ARGS%

set "EXIT_CODE=%ERRORLEVEL%"
echo.
if "%EXIT_CODE%"=="0" (
    echo Done: user order input finished successfully.
) else (
    echo Error: user order input finished with code %EXIT_CODE%.
)

if not defined NO_PAUSE pause
exit /b %EXIT_CODE%
