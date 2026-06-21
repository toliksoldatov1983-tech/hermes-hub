@echo off
setlocal

set "ROOT=E:\Hermes-Hub"
set "PROJECT=%ROOT%\projects\malyarka-clean"
set "INPUT_FILE=%ROOT%\inputs\ORDER_INPUT.txt"
set "EXCEL_FILE=%ROOT%\outputs\COREL_EXPORT.xlsx"
set "PYTHONPATH=%PROJECT%\src;%PROJECT%\tools"
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
echo Malyarka Clean single local order runner
echo =======================================
echo.
echo This reads ORDER_INPUT.txt, saves LAST_ORDER_RESULT.txt, and creates COREL_EXPORT.xlsx only for clean orders.
echo It does not run Telegram, Vision, API, database, prices, production or Corel itself.
echo.
echo Input file:
echo %INPUT_FILE%
echo.

python "%PROJECT%\tools\run_local_order.py" --input-file "%INPUT_FILE%" --excel-file "%EXCEL_FILE%"
set "EXIT_CODE=%ERRORLEVEL%"

if "%EXIT_CODE%"=="0" (
    echo.
    echo Done: order checked and Excel created.
) else (
    echo.
    echo Done: order checked, Excel was not created.
)

if not defined NO_PAUSE pause
exit /b %EXIT_CODE%
