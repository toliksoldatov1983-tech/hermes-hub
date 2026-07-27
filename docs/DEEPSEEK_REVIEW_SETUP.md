# DEEPSEEK_REVIEW_SETUP

DeepSeek / DeepSig is not connected yet.

Future setup requires `APPROVE_SECRET_SETUP` and a key provided outside the project files.

Review provider never edits files directly.

## Current local gate

Hermes-Clean now has a review provider factory:

```cmd
scripts\hermes.cmd review-provider --mode mock-review
scripts\hermes.cmd review-provider --mode deepseek-disabled
scripts\hermes.cmd review-provider --mode deepsig-disabled
scripts\hermes.cmd review-provider --mode mock-review --cycles-used 2
```

Current behavior:

- `mock-review` performs local mock review only.
- `deepseek-disabled` is blocked until `APPROVE_SECRET_SETUP`.
- `deepsig-disabled` is blocked until `APPROVE_SECRET_SETUP`.
- `deepseek` / `deepsig` are blocked without approval and key availability.
- Review providers cannot edit project files directly.
- Review/fix loop stops after 2 cycles.

No real review API is called by the current code.

## Risk control plan

Detailed future rules are recorded in:

`docs\DEEPSEEK_REVIEW_RISK_CONTROL_PLAN.md`

Current hard rules:

- Codex writes code.
- DeepSeek / DeepSig only reviews.
- Review output never edits files directly.
- Real review provider setup requires `APPROVE_SECRET_SETUP`.
- `.env`, tokens and keys are not read by the current local flow.
- Real orders, client documents, Google Drive files and old archives are not review context.
- The review/fix loop stops after 2 cycles.
- If a risk appears, Hermes-Clean stays in `mock-review` or disabled review mode.
