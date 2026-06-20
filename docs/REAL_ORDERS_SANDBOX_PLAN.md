# Real Orders Sandbox Plan

Date: 2026-06-17 | Gate: YELLOW/RED

## Preconditions

- [ ] User explicitly approves sandbox
- [ ] Safe data copy created (no production)
- [ ] No secrets in sandbox data
- [ ] Offline chain verified (✅ 118 tests)

## Sandbox Rules

1. Only safe copies of orders (not live DB)
2. No token/.env/config.py in sandbox
3. No Telegram/API calls
4. No Corel/Excel export
5. Results never sent to clients

## Transition to Real

Separate RED approval required.
