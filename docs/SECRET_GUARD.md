# SECRET_GUARD

## Purpose

Secret Guard is the local safety layer that prevents Hermes-Clean from treating real secrets as normal project data.

It exists to keep this project safe while real providers such as Gemini, DeepSeek, Telegram or other external systems are not connected.

## What It Protects

Secret Guard is designed around these rules:

- do not use real API keys in code;
- do not use real tokens in code;
- do not treat `.env` as project memory;
- use mock providers until secret setup is explicitly approved;
- redact secret-like strings before they appear in reports;
- raise `SecretAccessError` when a mock provider receives a real-looking key.

## Main Local Objects

- `SecretGuard`
- `SecretAccessError`
- `MockProvider`
- `sanitize_text`
- `is_safe_string`

## Allowed Local Use

Allowed:

- create mock providers;
- sanitize text;
- validate that test strings do not look like secrets;
- run tests against synthetic keys;
- document secret policy.

Not allowed without a separate approval gate:

- read real `.env`;
- use real Gemini keys;
- use real DeepSeek or DeepSig keys;
- use real Telegram tokens;
- call external APIs;
- store real secrets in Hermes-Clean.

## Approval Gate

Real secret setup requires:

```text
APPROVE_SECRET_SETUP
```

Until that gate is reached, Hermes-Clean must stay in mock/dry-run mode.

## Tests

Covered by:

```text
tests/test_secret_guard.py
```

The tests cover sanitizing secret-like strings, mock providers, blocked real-looking keys, `.env` detection in temporary test folders, and report rendering.
