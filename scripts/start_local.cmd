@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0.."

echo ╔══════════════════════════════════════════════╗
echo ║      Hermes-Clean — Локальный запуск        ║
echo ╚══════════════════════════════════════════════╝
echo.

echo ─── Проверка Python ───
python --version
if %errorlevel% neq 0 (
    echo [FAIL] Python не найден. Установи Python 3.10+
    pause
    exit /b 1
)
echo.

echo ─── Подготовка ───
set PYTHONPATH=%CD%\src

echo ─── Обновление состояния ───
python -m hermes_core refresh-all
echo.

echo ─── Панель управления ───
python -m hermes_core dashboard
echo.

echo ─── Дымковые проверки (smoke) ───
python -m hermes_core smoke
echo.

echo ─── Статус приложения ───
python -m hermes_core app-status
echo.

echo ─── Состояние Malyarka ───
python -m hermes_core malyarka-status
echo.

echo ─── Проверка безопасности ───
python -m hermes_core safety-audit
echo.

echo ╔══════════════════════════════════════════════╗
echo ║  Hermes-Clean ЗАПУЩЕН в safe локальном режиме║
echo ╚══════════════════════════════════════════════╝
echo.
echo Доступные команды:
echo   scripts\hermes.cmd help-local  — список всех команд
echo   scripts\hermes.cmd dashboard   — панель управления
echo   scripts\hermes.cmd smoke       — дымковые проверки
echo   scripts\check_local.cmd        — полная локальная проверка
echo   scripts\run_tests.cmd          — запуск тестов
echo.
echo Функции, отключённые в safe-mode:
echo   - Live Telegram, polling, webhook
echo   - Реальные AI-провайдеры (Gemini, DeepSeek)
echo   - Google Drive запись
echo   - Доступ к реальным заказам
echo   - Чтение .env, токенов, ключей
echo   - Удаление файлов
echo   - Импорт архивов
echo.
echo Панель управления: 05_REPORTS\LOCAL_DASHBOARD.md
echo Состояние:         00_START\CURRENT_STATE.md
echo.
pause
