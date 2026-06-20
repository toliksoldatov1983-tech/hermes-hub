# Local server adapter skeleton plan

Technical name: `BATCH_239_242_LOCAL_SERVER_ADAPTER_SKELETON_PLAN`

Date: 2026-06-16

## Status

This is a markdown-only plan for a future local server adapter skeleton.

No Python code is written.
No tests are created.
No server connection is made.
No live bot modules are imported.
No polling/webhook is launched.
No collector is launched.
No server files are read, changed, or created.

The skeleton described here is not an implementation.
It is only a local project plan for a later package.

## Sources Read

Local markdown sources:

- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_ADAPTER_INSERTION_DESIGN_PLAN_235_238_SUMMARY.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231C_234C.md`
- `E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md`
- `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`

## Purpose

The future local server adapter skeleton should define a safe bridge shape before touching any live server bot code.

It should let Hermes Hub validate:

- adapter request/response shape;
- off-by-default behavior;
- dry-run-only behavior;
- feature flag gates;
- fallback behavior;
- no-side-effects invariant;
- no direct Telegram sending;
- no secrets access.

The skeleton must be local first.
It must not connect to the live bot.
It must not import production Telegram modules.

## Future Skeleton Location

Design target from package `235-238`:

```text
malyarka_core/adapters/telegram.py
```

Recommended local skeleton planning path for future implementation:

```text
E:\Hermes-Hub\local_tests\server_adapter_skeleton\
```

or a similarly local-only safe zone.

The future skeleton may model a server adapter contract without being copied into the server project.

No file is created in this package.

## Future Adapter Position

Intended future architecture:

```text
Telegram live flow
-> malyarka_telegram/router.py or handlers.py
-> tiny future guarded call-site
-> malyarka_core/adapters/telegram.py or adjacent Hermes server adapter bridge
-> Hermes adapter contract validation
-> dry-run response only
-> fallback to existing Telegram behavior if disabled/unsafe
```

Important:

- `router.py` and `handlers.py` are only future tiny guarded call-sites;
- `app.py` is not touched first;
- `services/orders.py` is not changed first;
- live bot behavior must continue unchanged when the adapter is disabled.

## Skeleton Responsibilities

The future skeleton should model:

- receiving safe input dictionary;
- validating required fields;
- checking feature flags;
- returning a structured dry-run response;
- marking unsafe/unknown actions as blocked;
- requiring fallback when disabled, malformed, or unsafe;
- exposing diagnostics only in safe-only form;
- preserving `side_effects=[]`;
- never sending Telegram messages itself.

## Skeleton Non-Responsibilities

The skeleton must not:

- read token;
- read `.env`;
- read `config.py` contents;
- read `os.environ`;
- read databases;
- read logs;
- read real orders;
- import live bot modules;
- import Telegram/aiogram runtime;
- call network/API;
- launch polling/webhook;
- create exports;
- write files;
- write logs;
- write databases;
- change prices, rules, materials, or production state.

## Proposed Local Contract Shape

Future skeleton input, design only:

```text
{
  "text": "...",
  "user_id_safe": "redacted-or-test-id",
  "current_mode": "order|chat|engineer|admin|neutral",
  "route_result": {...},
  "order_preview": {...},
  "owner_access_status": "allowed|blocked|unknown",
  "feature_flags": {...},
  "safe_context_summary": "...",
  "dry_run": true,
  "diagnostics_requested": false
}
```

Future skeleton output, design only:

```text
{
  "ok": true|false,
  "status": "dry_run|blocked|fallback|disabled|malformed",
  "action": "answer_text|explain_status|suggest_next_safe_step|fallback",
  "dry_run": true,
  "blocked": true|false,
  "fallback_required": true|false,
  "reason": "...",
  "diagnostics_safe": true,
  "side_effects": [],
  "output_type": "draft|diagnostics|fallback|blocked",
  "response_text": "...",
  "warnings": [],
  "suggested_next_step": "..."
}
```

The future implementation may refine names, but must preserve the safety ideas.

## Required Feature Flags

Future skeleton must assume these safe defaults:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SERVER_ADAPTER_ENABLED=false
HERMES_TELEGRAM_INSERTION_ENABLED=false
HERMES_SAFE_MODE=true
HERMES_DRY_RUN_ONLY=true
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_ADMIN_CHANGES_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false
HERMES_ASSISTANT_MODE_ENABLED=false
```

Rules:

- adapter disabled means fallback required;
- safe mode must be true;
- dry-run must be true;
- export/admin/write actions stay blocked;
- unknown flags must not enable behavior;
- missing flags should default to safest value.

## Off By Default Requirement

The future skeleton must return a safe disabled/fallback response when the adapter flag is off.

Required behavior:

```text
HERMES_ADAPTER_ENABLED=false
-> no adapter action
-> fallback_required=true
-> side_effects=[]
-> existing flow should continue
```

## Dry-Run Only Requirement

The future skeleton must never execute a real Telegram or server action.

Required behavior:

```text
dry_run=true
side_effects=[]
output is a draft or diagnostic only
```

If `dry_run=false`, the skeleton must block and require fallback.

## Fallback Requirement

Fallback is mandatory when:

- adapter disabled;
- safe mode missing/false;
- dry-run missing/false;
- request malformed;
- action unknown;
- action forbidden;
- diagnostics unsafe;
- feature flag missing for requested behavior;
- exception occurs.

Fallback response must be structured and predictable.

## No Direct Telegram Send

The adapter must not send Telegram messages directly.

It may only return:

- response draft;
- status explanation;
- warnings;
- diagnostics-safe state;
- suggested next safe step;
- fallback signal.

Existing Telegram flow decides what to do later, after validation and future approvals.

## Future Tiny Call-Site Rule

Future `router.py` or `handlers.py` integration may be considered only after local skeleton and contract checks exist.

The future call-site must be:

- tiny;
- feature-flagged;
- dry-run first;
- fallback-safe;
- no token/config reads;
- no polling changes;
- no direct server lifecycle changes.

`app.py` should not be touched in the first live-adjacent stage.
`services/orders.py` should not be changed in the first live-adjacent stage.

## Future Local Tests To Plan Later

No tests are created now.

Future local tests should cover:

- adapter off by default;
- dry-run only;
- safe mode required;
- fallback required on malformed input;
- forbidden actions blocked;
- export/admin/write blocked;
- diagnostics safe-only;
- side_effects always empty;
- no live imports;
- no network/API calls;
- no file/db/log writes.

## Risks

Risks:

- exact contents of `malyarka_core/adapters/telegram.py` are still unknown;
- exact router/handler call points are unknown;
- `config.py` exists and must remain unread unless a separate redacted review is approved;
- `malyarka_ai` and `malyarka_vision` exist and must stay out of this path;
- future implementation could accidentally drift into live bot behavior if not flag-gated.

## Explicit Prohibitions

This skeleton plan does not allow:

- Python implementation;
- test creation;
- server connection;
- reading server files;
- reading secrets;
- touching live bot;
- touching polling/webhook;
- importing live modules;
- changing staging/production code;
- commit/push.

## No-Touch Confirmation

For package `239-242`:

- server files were not touched;
- live Telegram was not touched;
- polling/webhook were not launched;
- token was not read;
- `.env` was not read;
- `config.py` contents were not read;
- `os.environ` was not read;
- databases/logs/real orders were not read;
- staging/production code was not changed;
- Vision/API were not touched;
- code/tests were not created.

## Next Safe Step

```text
243-246 — план локального server adapter contract interface без реализации кода.
```
