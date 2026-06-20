# TASK.md
# BUNDLE_271_300_LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS

## Order

2

## Type

LOCAL_IMPLEMENTATION_ALLOWED

## Autonomy

AUTO_LOCAL_ONLY

## ЗАДАЧА

Реализовать только локальный sandbox adapter skeleton и focused contract tests в local_adapter_sandbox после проверки prerequisites.

## ОЖИДАЕМЫЙ РЕЗУЛЬТАТ

Локальный sandbox создан, локальные tests подготовлены/запущены только локально, сервер не тронут.

## Conveyor rule

Можно выполнять автоматически только local sandbox actions explicitly described in this bundle. No server/live/secrets/real orders.

## Previous required bundle

`BUNDLE_255_270_LOCAL_ADAPTER_SKELETON_IMPLEMENTATION_PREP`

If previous required bundle is missing or incomplete, stop and report:

`STOP_PREVIOUS_BUNDLE_MISSING_OR_INCOMPLETE`

## Next bundle

`BUNDLE_301_330_TINY_GUARDED_CALLSITE_PLAN`

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

`REPORT_BUNDLE_271_300_LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS.md`

## Status codes

Use one of:

- `LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS_COMPLETE`
- `LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS_INCOMPLETE`
- `LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS_BLOCKED_MISSING_PREREQUISITES`
- `LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS_STOPPED_REVIEW_REQUIRED`
- `LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS_STOPPED_APPROVAL_REQUIRED`
- `LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS_STOPPED_SAFETY_RISK`
- `LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS_BLOCKED_NOT_READY`

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

