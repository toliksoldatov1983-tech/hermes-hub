# NO_SECRET_POLICY

Do not store real secrets in Hermes-Clean.

Allowed:

- `config/env.example`
- `config/providers.example.json`

Forbidden:

- real `.env`;
- API keys;
- Telegram tokens;
- passwords;
- client credentials.
