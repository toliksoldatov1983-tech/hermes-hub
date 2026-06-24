# REGRESSION 2026-06-24

BATCH_023 Daily Regression

## Server
- host: root@178.104.95.187
- path: /opt/malyarka-telegram-bot
- backup: /opt/malyarka-telegram-bot/backups/batch_023_20260624_050143

## Checks
- Corel Excel: PASS
- Malyarka File: PASS
- Спорный заказ: PASS
- Экономист: PASS
- Daily note: PASS

## Daily
- Obsidian template created: E:\Hermes-General\obsidian-long-memory\01_Daily\Шаблон_дня.md
- Server cron: 0 21 * * * cd /opt/malyarka-telegram-bot && .venv/bin/python scripts/daily_summary.py >> /var/log/malyarka_daily_summary.log 2>&1

## Service
- systemctl restart malyarka-telegram-bot: PASS
- service status: active
