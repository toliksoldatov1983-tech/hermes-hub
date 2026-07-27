@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0.."
set PYTHONPATH=%CD%\src

echo ╔══════════════════════════════════════════════╗
echo ║  Hermes-Clean — ПОЛНАЯ локальная проверка   ║
echo ╚══════════════════════════════════════════════╝
echo.

set ALL_OK=1

echo ─── 1. Project Audit ───
python -m hermes_core project-audit
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 2. Smoke tests ───
python -m hermes_core smoke
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 3. Malyarka Status ───
python -m hermes_core malyarka-status
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 4. Malyarka Demo ───
python -m hermes_core malyarka-demo
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 5. Malyarka Fixtures ───
python -m hermes_core malyarka-fixtures
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 6. Malyarka Disputes ───
python -m hermes_core malyarka-disputes
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 7. Malyarka Combined (default) ───
python -m hermes_core malyarka-combined
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 8. Malyarka Combined (sample text) ───
python -m hermes_core malyarka-combined "краска | 2 | ведро"
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 9. Malyarka Dialog (clean) ───
python -m hermes_core malyarka-dialog --script clean
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 10. Malyarka Dialog (disputed) ───
python -m hermes_core malyarka-dialog --script disputed
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 11. Malyarka Transcript (clean) ───
python -m hermes_core malyarka-transcript --script clean
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 12. Malyarka Transcript (disputed) ───
python -m hermes_core malyarka-transcript --script disputed
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 13. Telegram Flow (clean) ───
python -m hermes_core telegram-flow --case clean
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 14. Telegram Flow (disputed) ───
python -m hermes_core telegram-flow --case disputed
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 15. Telegram Scenarios ───
python -m hermes_core telegram-scenarios
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 16. Telegram Status ───
python -m hermes_core telegram-status
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 17. Malyarka Pricing ───
python -m hermes_core malyarka-pricing
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 18. Malyarka Schema ───
python -m hermes_core malyarka-schema
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 19. Malyarka Workflow ───
python -m hermes_core malyarka-workflow
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 20. Help (all commands) ───
python -m hermes_core help-local
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 21. Dashboard ───
python -m hermes_core dashboard
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 22. Daily Report ───
python -m hermes_core daily-report
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 23. App Status ───
python -m hermes_core app-status
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 24. Safety Audit ───
python -m hermes_core safety-audit
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 25. Health Check ───
python -m hermes_core health
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 26. Status ───
python -m hermes_core status
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ─── 27. Тесты (единые) ───
python -m pytest tests -v
if %errorlevel% neq 0 set ALL_OK=0
echo.

echo ════════════════════════════════════════════════
if %ALL_OK% equ 1 (
    echo [OK] Все 27 проверок пройдены успешно!
) else (
    echo [WARNING] Некоторые проверки завершились с ошибками.
    echo Смотри вывод выше для деталей.
)
echo ════════════════════════════════════════════════
pause
