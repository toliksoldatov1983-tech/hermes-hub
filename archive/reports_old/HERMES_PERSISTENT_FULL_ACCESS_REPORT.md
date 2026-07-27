# HERMES_PERSISTENT_FULL_ACCESS_REPORT

Дата: 2026-07-04
Исполнитель: Codex

## Финальный статус

`HERMES_ACCESS_REGISTRY_READY_SERVER_BLOCKED`

Локальный постоянный контур доступа подготовлен. Серверный доступ пока заблокирован, потому что `49.13.76.163` не принимает найденные или созданный SSH public key.

## Что найдено

- `C:\Users\user\.ssh\` найден.
- `C:\Users\user\Desktop\Hermes-Clean\` найден.
- `[удалённый архив]` найден.
- `C:\Users\user\AppData\Local\hermes\` найден.
- Hermes config найден: `C:\Users\user\AppData\Local\hermes\config.yaml`.
- Hermes gateway binding plugin найден и включен:
  `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding`.
- Existing SSH keys found:
  - `hetzner_hermes`
  - `hermes_phase2_temp`
  - `hermes_temp_server_readonly`

## Что создано

- Backup:
  `C:\Users\user\Desktop\Hermes-Clean\backup_before_persistent_full_access_20260704_005041`
- Persistent SSH key:
  `C:\Users\user\.ssh\hermes_clean_full_access_ed25519`
- SSH alias:
  `hermes-server`
- SSH config:
  `C:\Users\user\.ssh\config`
- Access registry:
  `C:\Users\user\Desktop\Hermes-Clean\00_START\HERMES_ACCESS_REGISTRY.md`

## SSH Alias

```text
Host hermes-server
    HostName 49.13.76.163
    User ubuntu
    IdentityFile C:\Users\user\.ssh\hermes_clean_full_access_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
```

Public key fingerprint:

`SHA256:BtFC****b2YU`

Private key was not printed.

## Server Access Status

Status: `NEEDS_FIX`

Checks:

- `root@49.13.76.163` with existing keys: rejected by server.
- `ubuntu@49.13.76.163` with existing keys: rejected by server.
- `ssh hermes-server`: rejected by server.

Observed non-secret result:

`Permission denied (publickey)`

Required fix:

- Install public key from `C:\Users\user\.ssh\hermes_clean_full_access_ed25519.pub` into `~ubuntu/.ssh/authorized_keys` on `49.13.76.163`.

## Telegram Access Status

Status: `LOCAL_READY_SERVER_TAKEOVER_BLOCKED`

- Local gateway process is running:
  `hermes gateway run`
- Current PID chain:
  `8868 -> 4164 -> 3940 -> 24464`
- Binding plugin status:
  `binding_enabled=True`
  `binding_error=None`
  `pre_gateway_dispatch_callbacks=1`
- Live Telegram restart was not performed.
- Owner-only live tests were not performed.

Reason:

- Old server polling cannot be inspected or stopped until SSH is fixed.
- Starting/restarting local gateway takeover while old server polling may still hold the same Telegram token risks polling conflict.

## Old Server Bot Status

Status: `NOT_VERIFIED`

Documented likely service/path:

- service: `malyarka-telegram-bot.service`
- path: `/opt/malyarka-telegram-bot`
- process: `/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling`

No server process was stopped.
No server service was disabled.
No server files were changed.

## Local Gateway Status

Status: `RUNNING_OLD_PROCESS_STATE`

The plugin is enabled in config, but current live process may have started before the persistent access task. Local gateway restart was not performed in this block.

## Tests Passed

- SSH inventory completed without printing secrets.
- SSH alias created.
- Persistent key created locally.
- `ssh hermes-server` test ran and correctly reported server-side public key block.
- Hermes plugin discovery:
  - `binding_enabled=True`
  - `binding_error=None`
  - `pre_gateway_dispatch_callbacks=1`
- Local direct environment token presence check completed without printing values.

## Blocked

- Server access is blocked until the public key is installed server-side.
- Old server polling cannot be stopped until SSH works.
- Telegram gateway takeover cannot be safely completed until old server polling status is known.
- Live Telegram owner-only tests were not run.

## Revoke Access

To revoke local prepared access:

1. Remove the `hermes-server` block from `C:\Users\user\.ssh\config`.
2. Remove the matching public key from server `~ubuntu/.ssh/authorized_keys` if it has been installed.
3. Optionally archive/remove local key files only after separate explicit approval:
   - `C:\Users\user\.ssh\hermes_clean_full_access_ed25519`
   - `C:\Users\user\.ssh\hermes_clean_full_access_ed25519.pub`

No delete was performed by Codex.

## Risks Remaining

- Server may use a different user than `ubuntu`.
- Server may require console-side public key installation.
- Old server bot may still be polling Telegram.
- Local gateway may conflict with old polling if restarted before server polling is stopped.
- Token source for live local gateway is not documented in this report by value; secrets remain local and unprinted.

## Next Required Step

`SERVER_PUBLIC_KEY_INSTALL_REQUIRED`

After key installation:

1. Verify `ssh hermes-server "hostname && whoami && pwd"`.
2. Read-only inspect `malyarka-telegram-bot.service`.
3. Stop only confirmed old server polling.
4. Restart only confirmed local `hermes gateway run`.
5. Run owner-only Telegram tests.
