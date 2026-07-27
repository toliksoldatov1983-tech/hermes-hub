# Gemini Risk-Control Plan

## Purpose

This plan describes how Gemini can be connected later without weakening Hermes-Clean safety rules.

Current state:

- Gemini is not connected.
- Real API keys are not read.
- Real `.env` is not created.
- External API calls are not executed.
- Hermes-Clean uses mock/disabled provider modes only.

## Required Approval Gate

Real Gemini setup requires:

```text
APPROVE_SECRET_SETUP
```

Without this approval, Hermes-Clean must stay in mock or disabled provider mode.

## Secret Rules

- Do not store real keys in the repository.
- Do not write real keys into markdown files.
- Do not create a real `.env` automatically.
- Use environment variables only.
- Allowed placeholder files: `config\env.example`, `config\providers.example.json`.
- Never print `GEMINI_API_KEY`.
- Never include real keys in reports.

## Future Safe Sequence

1. User explicitly approves `APPROVE_SECRET_SETUP`.
2. User sets `GEMINI_API_KEY` outside the repository.
3. Codex verifies only that a key is available, not its value.
4. Hermes-Clean runs a local provider-selection smoke test.
5. First real Gemini request uses synthetic text only.
6. No real orders, client documents, Google Drive files or old archives are sent.
7. After the test, Codex writes a local report.

## Blocked Until Separate Approval

- Sending real order data to Gemini.
- Sending client documents to Gemini.
- Reading `.env`.
- Reading tokens or keys.
- Using Google Drive documents as Gemini input.
- Importing old archives as Gemini context.

## Rollback Rule

If Gemini setup fails, Hermes-Clean returns to:

```text
mock provider
gemini-disabled
```

No files are deleted and no secrets are printed.
