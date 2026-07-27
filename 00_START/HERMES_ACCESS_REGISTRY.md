# HERMES_ACCESS_REGISTRY

Дата: 2026-07-04
Режим: `PERSISTENT_FULL_HERMES_ACCESS`

Этот файл фиксирует постоянный контур доступа Hermes-Clean. Секреты здесь не хранятся.

## Server Access

- server: `49.13.76.163`
- alias: `hermes-server`
- ssh user: `ubuntu`
- ssh config: `C:\Users\user\.ssh\config`
- persistent key path: `C:\Users\user\.ssh\hermes_clean_full_access_ed25519`
- public key path: `C:\Users\user\.ssh\hermes_clean_full_access_ed25519.pub`
- public key fingerprint: `SHA256:BtFC****b2YU`
- existing checked keys:
  - `C:\Users\user\.ssh\hetzner_hermes` -> found, server rejected
  - `C:\Users\user\.ssh\hermes_phase2_temp` -> found, server rejected
  - `C:\Users\user\.ssh\hermes_temp_server_readonly` -> found, server rejected
- status: `NEEDS_FIX`
- reason: `ssh hermes-server` returns `Permission denied (publickey)`
- test command: `ssh -o BatchMode=yes hermes-server "hostname && whoami && pwd"`
- required server-side fix: install public key from `C:\Users\user\.ssh\hermes_clean_full_access_ed25519.pub` into `~ubuntu/.ssh/authorized_keys` on `49.13.76.163`
- revoke method: remove the matching public key fingerprint from `~ubuntu/.ssh/authorized_keys`

## Telegram Access

- desired production mode: `TELEGRAM_PRODUCTION_SINGLE_USER_ACTIVE`
- local gateway command: `hermes gateway run`
- current local gateway process: running
- current local gateway PID chain: `8868 -> 4164 -> 3940 -> 24464`
- gateway binding plugin: `hermes-clean-gateway-binding`
- plugin status: `ENABLED_LOCAL_PENDING_RESTART`
- plugin path: `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding`
- Hermes config: `C:\Users\user\AppData\Local\hermes\config.yaml`
- token source status: not printed; local process/config must keep using existing Telegram token source
- local environment token presence checked: `MISSING` for direct process environment variables in this Codex shell
- allowed owner chat_id status: not printed; owner-only verification pending live Telegram test
- polling owner: `CONFLICT_UNKNOWN`
- reason: old server polling could not be inspected because SSH access is blocked

## Local Hermes Access

- Hermes home: `C:\Users\user\AppData\Local\hermes`
- Hermes config path: `C:\Users\user\AppData\Local\hermes\config.yaml`
- Hermes gateway runner: `C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\run.py`
- Telegram adapter: `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\platforms\telegram\adapter.py`
- binding plugin path: `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding`
- Malyarka runtime root: `[удалённый архив]`
- reports path: `C:\Users\user\Desktop\Hermes-Clean\05_REPORTS`
- status: `LOCAL_READY_PENDING_RESTART`

## Server Old Bot

- possible service: `malyarka-telegram-bot.service`
- possible runtime path: `/opt/malyarka-telegram-bot`
- possible process: `/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling`
- live status: `NOT_VERIFIED`
- reason: SSH to `49.13.76.163` is blocked by public key authorization
- planned stop method after SSH fix: `sudo systemctl stop malyarka-telegram-bot.service`
- planned autostart disable method after SSH fix: `sudo systemctl disable malyarka-telegram-bot.service`
- rollback method after SSH fix: `sudo systemctl start malyarka-telegram-bot.service`
- rollback autostart method after SSH fix: `sudo systemctl enable malyarka-telegram-bot.service`

## Forbidden To Print

- private keys
- passwords
- Telegram bot tokens
- OpenAI/API keys
- `.env` content
- full secret values
- full authorized_keys content

## Next Required Gate

`SERVER_PUBLIC_KEY_INSTALL_REQUIRED`

After server-side public key installation:

1. Run `ssh -o BatchMode=yes hermes-server "hostname && whoami && pwd"`.
2. Inspect old server polling read-only.
3. Stop only confirmed old Telegram polling.
4. Restart only confirmed local `hermes gateway run`.
5. Run owner-only live Telegram tests.
