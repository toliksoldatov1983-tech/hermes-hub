# Server Bot Leave Running Monitoring Plan

Date: 2026-06-20

Mode: plan only.

## Meaning Of Leave Running

Leave the service in the current observed state:

```text
active/running
autostart disabled
feature flag OFF
production not enabled
Phase 2 not continued
```

## Allowed Read-Only Checks

Allowed if user asks for status:

```text
systemctl show malyarka-telegram-bot.service --property=ActiveState,SubState,MainPID --no-pager
systemctl is-enabled malyarka-telegram-bot.service
pgrep -af 'malyarka_telegram.app --run-polling'
```

Feature flag check may use safe grep on adapter/telegram file only:

```text
grep -n '^_HERMES_ADAPTER_ENABLED[[:space:]]*=' /opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
```

## Forbidden

Do not:

- restart;
- stop;
- enable;
- disable;
- change feature flag;
- read `.env`;
- read `config.py`;
- read token;
- read `os.environ`;
- read DB/logs/orders;
- change `.py` code;
- use git/commit/push;
- enable production;
- continue Phase 2.

## Reasons To Consider Controlled Stop

Consider controlled stop if:

- bot behaves unexpectedly;
- user sees repeated unwanted messages;
- service starts multiple processes;
- CPU/memory appears abnormal by safe checks;
- Telegram test reveals unsafe behavior;
- user wants bot offline.

Stop still requires:

```text
APPROVE_SERVER_BOT_CONTROLLED_STOP_ONCE
```

