# GEMINI_SETUP

Gemini is not connected yet.

Future setup requires:

1. `APPROVE_SECRET_SETUP`.
2. Environment variable `GEMINI_API_KEY`.
3. Local smoke test with no real orders.

No key is stored in this repository.

## Current local gate

Hermes-Clean now has a provider factory:

```cmd
scripts\hermes.cmd ai-provider --mode mock
scripts\hermes.cmd ai-provider --mode gemini-disabled
scripts\hermes.cmd ai-provider --mode gemini
```

Current behavior:

- `mock` returns `MockProvider`.
- `gemini-disabled` returns a blocked Gemini placeholder.
- `gemini` remains blocked without `APPROVE_SECRET_SETUP`.
- even with approval flags, real Gemini client is not implemented in this local-safe block.

No real `GEMINI_API_KEY` is read by the current code.

## Risk-control plan

Detailed safe setup plan:

```text
docs\GEMINI_RISK_CONTROL_PLAN.md
```

Real Gemini setup remains blocked until `APPROVE_SECRET_SETUP`.
