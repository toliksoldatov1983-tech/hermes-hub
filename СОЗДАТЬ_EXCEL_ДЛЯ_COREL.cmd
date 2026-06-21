@echo off
setlocal

set "ROOT=E:\Hermes-Hub"
set "PROJECT=%ROOT%\projects\malyarka-clean"
set "INPUT_FILE=%ROOT%\inputs\ORDER_INPUT.txt"
set "OUTPUT_FILE=%ROOT%\outputs\COREL_EXPORT.xlsx"
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
echo Malyarka Clean Corel Excel export
echo =================================
echo.
echo This creates only a local .xlsx file for Corel from a clean order.
echo It does not run Telegram, Vision, API, database, prices, production or Corel itself.
echo.
echo Input file:
echo %INPUT_FILE%
echo.
echo Output file:
echo %OUTPUT_FILE%
echo.

python "%PROJECT%\tools\create_corel_excel.py" --input-file "%INPUT_FILE%" --output-file "%OUTPUT_FILE%"
set "EXIT_CODE=%ERRORLEVEL%"

if "%EXIT_CODE%"=="0" (
    echo.
    echo Done: Corel Excel file created.
) else (
    echo.
    echo Export blocked or failed with code %EXIT_CODE%.
)

if not defined NO_PAUSE pause
exit /b %EXIT_CODE%
