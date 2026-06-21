@echo off
setlocal
set "ROOT=E:\Hermes-Hub"
set "PROJECT=%ROOT%\projects\malyarka-clean"
set "INPUT_FILE=%ROOT%\examples\EMPTY_OR_INVALID_ORDER.txt"
set "PYTHONPATH=%PROJECT%\src"
set "NO_PAUSE="
if /I "%~1"=="--no-pause" set "NO_PAUSE=1"
echo Checking empty or invalid example...
python "%PROJECT%\tools\user_order_input.py" --input-file "%INPUT_FILE%"
set "EXIT_CODE=%ERRORLEVEL%"
if not defined NO_PAUSE pause
exit /b %EXIT_CODE%

