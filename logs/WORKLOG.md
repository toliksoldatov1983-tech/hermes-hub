
```text
E:\Hermes-General\HERMES_OPERATING_SYSTEM.md
E:\Hermes-General\START_HERE_FOR_HERMES_HUB_MALYARKA.md
E:\Hermes-Hub\PROJECT_MASTER_MAP_MALYARKA_HERMES.md
E:\Hermes-Hub\docs\HERMES_MASTER_MAP_LEVELS_AND_PROMPTS.md
```

No-touch:
- no server/service actions;
- no secrets/DB/logs/orders;
- no `.py` code changes;
- no git;
- no Phase 2;
- no production.
## 2026-06-23 — Telegram order preview loop and extra buttons fixed

Status:

```text
TELEGRAM_ORDER_PREVIEW_LOOP_AND_BUTTONS_FIX_CONFIRMED
```

Work performed:

- Stopped the bot when the user reported that an order caused a loop.
- Found that neutral-mode order-like text was routed to `suggest_order_mode` instead of parsing immediately.
- Found that the aiogram app attached the persistent three-button main keyboard when no inline result keyboard was present.
- Changed `malyarka_telegram/router.py` so size-like text in neutral mode immediately switches to order mode and parses.
- Changed `malyarka_telegram/app.py` so the persistent three-button keyboard is removed instead of being used as fallback.
- Updated router/app integration tests.
- Ran local tests: `441 passed`.
- Deployed clean runtime to `/opt/malyarka-telegram-bot`.
- Verified service is `active`.
- Verified server-side `1000*400` gives order preview, no `/заказ` hint, and only result buttons.
- User confirmed in Telegram: the bot gave the preview and works correctly.

Report:

```text
E:\Hermes-Hub\docs\TELEGRAM_ORDER_PREVIEW_LOOP_AND_BUTTONS_FIX_2026-06-23.md
```

No-touch:

- no token values documented;
- no `.env` values documented;
- no database/order history read;
- Hermes adapter Phase 2 was not enabled;
- production flag was not changed.
