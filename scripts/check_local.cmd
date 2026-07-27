@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0.."
set PYTHONPATH=%CD%\src

echo ==================================================
echo Hermes-Clean - standard local check
echo ==================================================
echo.

set ALL_OK=1

echo --- 1. Project Audit ---
python -m hermes_core project-audit
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 2. Smoke tests ---
python -m hermes_core smoke
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 3. Malyarka Status ---
python -m hermes_core malyarka-status
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 4. Malyarka Fixtures ---
python -m hermes_core malyarka-fixtures
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 5. Malyarka Disputes ---
python -m hermes_core malyarka-disputes
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 6. Malyarka Combined ---
python -m hermes_core malyarka-combined
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 7. Malyarka Dialog ---
python -m hermes_core malyarka-dialog --script clean
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 8. Malyarka Transcript ---
python -m hermes_core malyarka-transcript --script clean
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 9. Telegram Flow ---
python -m hermes_core telegram-flow --case clean
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo --- 10. Unit Tests ---
python -m pytest tests -q
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ==================================================
if %ALL_OK% equ 1 (
    echo [OK] All standard local checks passed.
    set EXIT_CODE=0
) else (
    echo [WARNING] Some checks failed. Review output above.
    echo Run scripts\check_full.cmd for deeper analysis if needed.
    set EXIT_CODE=1
)
echo ==================================================

exit /b %EXIT_CODE%
