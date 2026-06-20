# Safe SSH access recovery plan

Technical name: `BATCH_SERIES_231B_234B_HERMES_ADAPTER_SAFE_SSH_ACCESS_RECOVERY_PLAN`

## Status

This is a local SSH access recovery and diagnostic plan.

Server inventory was not executed.
Server files were not read.
Token, `.env`, `config.py`, `os.environ`, databases, live logs, and real orders were not read.
Bot code was not launched.
Polling/webhook were not launched.
Server files were not changed.

## Context

Previous package `231-234` attempted a read-only presence-only server inventory after valid approval.

The attempt stopped before collecting server structure:

```text
Permission denied (publickey,password).
```

No server filenames or folder names were collected in that run.

## Local Documents Read

Read local markdown documents:

- `E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md`
- `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231_234.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_READ_ONLY_SERVER_INVENTORY_REPORT_231_234_SUMMARY.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_SAFE_SERVER_INVENTORY_APPROVAL_GATE_PLAN_223_226.md`
- `E:\Hermes-Hub\docs\SERVER_TELEGRAM_SERVER_INVENTORY_READINESS_FINAL_CHECK_227_230.md`

## Local SSH Client Check

SSH client is installed.

Version observed:

```text
OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2
```

Note: `ssh -V` writes version text to stderr on Windows, so PowerShell reported a non-zero/native-command style output, but the version was visible.

## Local `.ssh` Zone Presence-Only Check

Local `.ssh` directory:

```text
present
```

Presence-only SSH files found:

```text
hetzner_hermes
hetzner_hermes.pub
known_hosts
known_hosts.old
```

SSH config file:

```text
not present
```

Known hosts file:

```text
present
```

Public key files:

```text
hetzner_hermes.pub
```

Private key candidate names only:

```text
hetzner_hermes
```

Private key contents were not read.
Public key contents were not read.
Known hosts contents were not read.

## Host / Alias Check

No local SSH config file was found, so no `Host` alias was confirmed from local SSH config.

The previous attempted command used direct target:

```text
root@178.104.95.187
```

Because no SSH config alias is present and the previous command did not specify an identity file, the likely cause is:

```text
the required key was not selected automatically, or the server does not accept the attempted user/key combination.
```

This is a diagnosis from local presence-only data and the previous error text.
No server-side authentication logs were read.

## Safe Recovery Options

Recommended safe next options:

1. User confirms the SSH user and key name without sharing password, passphrase, or private key contents.
2. User explicitly permits a new non-interactive read-only connection test using an explicit identity file, for example `hetzner_hermes`, without running inventory commands yet.
3. If connection works, a separate approval can authorize the read-only presence-only inventory command.
4. If connection still fails, user can manually provide a safe presence-only listing instead.

Potential future connection shape, not executed in this package:

```text
ssh -i <local-private-key-path> <ssh-user>@178.104.95.187
```

Do not paste the private key, passphrase, or password into chat.

## Data Needed From User

To safely recover access, the user should provide only non-secret connection metadata:

- SSH user, for example `root` or another server user;
- whether the key file name `hetzner_hermes` is the correct key;
- whether the key requires a passphrase, without sharing the passphrase;
- whether a different host alias should be used;
- whether the user prefers to manually provide a presence-only listing instead.

Do not provide:

- password;
- passphrase;
- private key contents;
- token;
- `.env`;
- `config.py` values;
- server file contents.

## Stop Conditions

Stop if any next step requires:

- password or passphrase in chat;
- showing or reading private key contents;
- changing `authorized_keys`;
- connecting to the server and running commands without a new explicit scope;
- reading server files;
- reading `.env`, `config.py`, databases, logs, or real orders;
- unclear host/user/key;
- risk of secret exposure.

## What Was Not Done

Not done:

- no server inventory;
- no server file read;
- no SSH command that executed a remote inventory command in this package;
- no scp/rsync/sftp;
- no private key read;
- no public key content read;
- no known_hosts content read;
- no `.env` read;
- no `config.py` read;
- no `os.environ` read;
- no database/log/order content read;
- no polling/webhook;
- no bot code launched;
- no server file changed;
- no `authorized_keys` change;
- no commit/push.

## Next Safe Step

Either:

```text
User provides safe SSH metadata only: SSH user + confirmation that hetzner_hermes is the intended key, without password/passphrase/private key contents.
```

Or:

```text
User manually provides a safe presence-only list of server files/folders.
```

Repeat read-only inventory only after access is safely recovered and after a separate explicit approval.
