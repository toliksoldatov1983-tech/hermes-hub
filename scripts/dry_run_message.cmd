@echo off
cd /d "%~dp0.."
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%CD%\src
python scripts\dry_run_message.py %*
