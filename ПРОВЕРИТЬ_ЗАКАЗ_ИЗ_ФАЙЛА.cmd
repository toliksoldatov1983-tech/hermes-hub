@echo off
setlocal

set "ROOT=E:\Hermes-Hub"
set "PROJECT=%ROOT%\projects\malyarka-clean"
set "INPUT_FILE=%ROOT%\inputs\ORDER_INPUT.txt"
set "PYTHONPATH=%PROJECT%\src"
set "NO_PAUSE="

:parse_args
if "%~1"=="" goto run
if /I "%~1"=="--no-pause" (
    set "NO_PAUSE=1"
    shift
    goto parse_args
)
shift
goto parse_args

:run
echo Malyarka Clean file order check
echo ===============================
echo.
echo This reads only a local txt file. It does not run Telegram, Vision, API, database, Excel or Corel export.
echo.
echo Input file:
echo %INPUT_FILE%
echo.

python "%PROJECT%\tools\user_order_input.py" --input-file "%INPUT_FILE%"
set "EXIT_CODE=%ERRORLEVEL%"

if "%EXIT_CODE%"=="0" (
    echo.
    echo Done: file order check finished successfully.
) else (
    echo.
    echo ERROR: file order check failed with code %EXIT_CODE%.
)

if not defined NO_PAUSE pause
exit /b %EXIT_CODE%
