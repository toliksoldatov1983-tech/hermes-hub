# TASK.md
# BUNDLE_451_480_SERVER_PATCH_DRY_RUN_RECHECK_PLAN

## Order

8

## Type

PLAN_ONLY

## Autonomy

AUTO_MARKDOWN

## ЗАДАЧА

Описать dry-run recheck plan. Без запуска server/live.

## ОЖИДАЕМЫЙ РЕЗУЛЬТАТ

Создан dry-run recheck plan.

## Conveyor rule

Можно выполнять автоматически только markdown/local documentation actions. No server/live/secrets/real orders.

## Previous required bundle

`BUNDLE_421_450_SERVER_PATCH_DIFF_DRAFT_ONLY`

If previous required bundle is missing or incomplete, stop and report:

`STOP_PREVIOUS_BUNDLE_MISSING_OR_INCOMPLETE`

## Next bundle

`BUNDLE_481_510_SERVER_PATCH_FINAL_APPROVAL_GATE`

## Read allowed

- this bundle `TASK.md`
- this bundle `README_FOR_CODEX.md`
- top-level `MANIFEST.md`
- top-level `SAFETY_RULES.md`
- top-level `STOP_AND_REPORT_TEMPLATE.md`
- local markdown docs already explicitly referenced by current bundle

## Absolutely do not touch

- server;
- `/opt/malyarka-telegram-bot`;
- live Telegram bot;
- polling / webhook;
- Telegram API calls;
- token;
- `.env`;
- `config.py` contents;
- `os.environ`;
- database/log/order contents;
- real orders;
- private IDs;
- API keys;
- production/staging code;
- Vision/API;
- `.git`;
- commit/push;
- Corel / ArtCAM / CNC;
- export/admin/write actions unless an individual accepted bundle explicitly allows a local no-op or markdown-only operation.


## STOP CONDITIONS

Codex/Hermes must stop and return a report if any of these appears:

- server touch is required;
- live bot touch is required;
- polling/webhook is required;
- Telegram API call is required;
- token/.env/config.py contents/os.environ must be read;
- db/log/order contents must be read;
- real order data is needed;
- production/staging code must be changed;
- commit/push is requested;
- bundle order is unclear;
- previous required bundle is missing;
- current bundle is a gate requiring approval;
- any instruction conflicts with SAFETY_RULES.md.


## Deliverables

Create/update only safe local markdown deliverables unless this bundle explicitly allows local sandbox files.

Recommended report file name:

`REPORT_BUNDLE_451_480_SERVER_PATCH_DRY_RUN_RECHECK_PLAN.md`

## Status codes

Use one of:

- `SERVER_PATCH_DRY_RUN_RECHECK_PLAN_COMPLETE`
- `SERVER_PATCH_DRY_RUN_RECHECK_PLAN_INCOMPLETE`
- `SERVER_PATCH_DRY_RUN_RECHECK_PLAN_BLOCKED_MISSING_PREREQUISITES`
- `SERVER_PATCH_DRY_RUN_RECHECK_PLAN_STOPPED_REVIEW_REQUIRED`
- `SERVER_PATCH_DRY_RUN_RECHECK_PLAN_STOPPED_APPROVAL_REQUIRED`
- `SERVER_PATCH_DRY_RUN_RECHECK_PLAN_STOPPED_SAFETY_RISK`
- `SERVER_PATCH_DRY_RUN_RECHECK_PLAN_BLOCKED_NOT_READY`

## REQUIRED REPORT

Return:

1. bundle name;
2. autonomy class;
3. what was read;
4. what was created/updated;
5. whether prerequisites were complete;
6. whether STOP condition occurred;
7. exact stop reason if stopped;
8. confirmation:
   - server_touched: false
   - live_bot_touched: false
   - polling_started: false
   - webhook_started: false
   - telegram_api_called: false
   - secrets_read: false
   - real_orders_used: false
   - ux_changed: false
   - mutation_performed: false
   - commit_push_performed: false
9. next safe bundle.

