@echo off
setlocal

set "ROOT=E:\Hermes-Hub"
set "PROJECT=%ROOT%\projects\malyarka-clean"
set "PYTHONPATH=%PROJECT%\src"

echo Malyarka Clean focused core tests
echo =================================
echo.
echo This does not run Telegram, Vision, API, database, Excel or Corel export.
echo.

cd /d "%PROJECT%"
python -m pytest ^
  "%PROJECT%\tests\test_order_result.py" ^
  "%PROJECT%\tests\test_order_pipeline_smoke.py" ^
  "%PROJECT%\tests\test_corel_export_model.py" ^
  "%PROJECT%\tests\test_area_calculator.py" ^
  "%PROJECT%\tests\test_first_local_parser.py" ^
  -q

set "EXIT_CODE=%ERRORLEVEL%"
echo.
if "%EXIT_CODE%"=="0" (
    echo Done: focused tests passed.
) else (
    echo Error: focused tests finished with code %EXIT_CODE%.
)

if /I not "%~1"=="--no-pause" pause
exit /b %EXIT_CODE%
