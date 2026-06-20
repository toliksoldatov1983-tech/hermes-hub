# Phase 2 — TTY1 Command Mode

Date: 2026-06-18 | Mode: USER EXECUTES AT tty1

## Команды (вводить по одной, в порядке)

```bash
cd /opt/malyarka-telegram-bot

# 1. PRECHECK
grep 'HERMES_ADAPTER' malyarka_core/adapters/telegram.py | head -1
systemctl is-active malyarka-telegram-bot

# 2. BACKUP
cp malyarka_core/adapters/telegram.py _hermes_backups/phase2_$(date +%Y%m%d_%H%M%S).py

# 3. ENABLE
sed -i 's/_HERMES_ADAPTER_ENABLED = False/_HERMES_ADAPTER_ENABLED = True/' malyarka_core/adapters/telegram.py
grep 'HERMES_ADAPTER' malyarka_core/adapters/telegram.py | head -1

# 4. SYNTAX CHECK
python3 -c 'import py_compile; py_compile.compile("malyarka_core/adapters/telegram.py", doraise=True); print("OK")'

# 5. RESTART BOT
systemctl restart malyarka-telegram-bot
sleep 3
systemctl status malyarka-telegram-bot --no-pager | head -5
```

**→ Теперь отправь тестовые сообщения в бота с телефона:**
- `700 x 500` (проверить ответ)
- `/start` (должен быть заблокирован)
- Ждать 2-3 минуты, наблюдать что бот не упал

```bash
# 6. REVERT
sed -i 's/_HERMES_ADAPTER_ENABLED = True/_HERMES_ADAPTER_ENABLED = False/' malyarka_core/adapters/telegram.py
grep 'HERMES_ADAPTER' malyarka_core/adapters/telegram.py | head -1
python3 -c 'import py_compile; py_compile.compile("malyarka_core/adapters/telegram.py", doraise=True); print("OK")'

# 7. RESTART BOT BACK
systemctl restart malyarka-telegram-bot
sleep 3
systemctl status malyarka-telegram-bot --no-pager | head -3
```

После выполнения — скопируй вывод команд в чат.
