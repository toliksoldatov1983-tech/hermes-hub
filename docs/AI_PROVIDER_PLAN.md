# AI_PROVIDER_PLAN

Gemini is the future primary provider.

DeepSeek / DeepSig are fallback or review providers.

Until `APPROVE_SECRET_SETUP`, Hermes-Clean uses `MockProvider`.

Keys are environment variables only and are never committed.

## Provider factory

`ProviderFactory` supports:

- `mock`
- `gemini-disabled`
- `gemini`
- `fallback`
- `deepseek-disabled`
- `deepsig-disabled`

The factory blocks Gemini until:

1. `APPROVE_SECRET_SETUP` is granted;
2. key availability is confirmed without storing the key;
3. a future real client implementation is added.

The current implementation performs no external API calls.
