@echo off
cd /d "%~dp0.."
echo Checking Hermes-Clean local files
if not exist AGENTS.md exit /b 1
if not exist src\hermes_core\app.py exit /b 1
if not exist docs\ARCHITECTURE.md exit /b 1
echo OK
