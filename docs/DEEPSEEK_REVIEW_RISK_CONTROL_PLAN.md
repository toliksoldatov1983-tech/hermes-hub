# DEEPSEEK_REVIEW_RISK_CONTROL_PLAN

## Purpose

This document fixes the safe future path for DeepSeek / DeepSig review.

Current status: review is local-only. Real DeepSeek / DeepSig API calls are disabled.

## Source Of Truth

Codex writes and changes project files.

DeepSeek / DeepSig may be used later only as a review provider. It must not edit Hermes-Clean directly.

Hermes-Clean remains the source of truth. Review output is advisory until Codex accepts or rejects it.

## Required Gate

Real review provider setup requires:

`APPROVE_SECRET_SETUP`

Without this gate:

- no real API key may be read;
- no `.env` may be created or opened;
- no code may be sent to an external review provider;
- no external API may be called.

## Allowed Now

Safe local actions:

- use `mock-review`;
- use `deepseek-disabled` and `deepsig-disabled` blocked modes;
- document future rules;
- run local tests and smoke checks;
- update local reports inside Hermes-Clean.

## Blocked Now

Blocked without a separate future gate:

- real DeepSeek API call;
- real DeepSig API call;
- reading `DEEPSEEK_API_KEY`;
- reading `.env`;
- sending code, reports, order data, client documents or archive content outside the machine;
- changing project files from review output automatically;
- reading real orders;
- reading old archives as review context;
- using Google Drive documents as review context.

## Future Review Flow

1. Codex prepares a local code change.
2. Safety gate checks whether the proposed review context is safe.
3. Only synthetic or explicitly approved project-local context may be sent.
4. DeepSeek / DeepSig returns review comments only.
5. Codex decides which comments to accept.
6. Codex applies accepted changes locally.
7. Maximum review/fix cycles: 2.
8. After 2 cycles, Codex reports remaining risk to the user.

## Context Rules

Allowed future review context after approval:

- selected Hermes-Clean source files;
- selected Hermes-Clean tests;
- synthetic examples;
- generated local reports that do not contain secrets or real orders.

Forbidden review context:

- `.env`;
- tokens, keys, passwords;
- real orders;
- client documents;
- Google Drive files unless separately approved;
- old archives;
- `[удалён]`;
- live Telegram data;
- server folders;
- [удалённый проект] / Malyarka project files unless separately approved.

## Rollback Rule

If any risk appears, review provider mode returns to:

`mock-review`

or:

`deepseek-disabled`

No external provider is required for normal local development.

## Verification Commands

Safe local checks:

```cmd
scripts\hermes.cmd review-provider --mode mock-review
scripts\hermes.cmd review-provider --mode deepseek-disabled
scripts\hermes.cmd review-provider --mode deepsig-disabled
scripts\hermes.cmd review-provider --mode deepseek
scripts\hermes.cmd review-provider --mode deepsig
scripts\hermes.cmd smoke
scripts\run_tests.cmd
```

Expected result: real providers stay blocked unless secret setup is explicitly approved and configured later.
