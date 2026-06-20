# REPORT — Hermes Outbound IP & SSH Firewall Diagnostic

Date: 2026-06-17

## Outbound IP

```
185.13.22.202
```

## TCP 22 Status

```
OPEN — "Permission denied (publickey,password)"
```

SSH доходит до сервера, порт 22 открыт, сервер отвечает. **Это НЕ firewall issue.**

## Диагноз

```text
Firewall: ✅ TCP 22 открыт
SSH: ❌ Permission denied (publickey,password)
Причина: публичный ключ НЕ принят сервером
```

## Previous Attempts vs Now

| Attempt | IP | Result | Причина |
|---------|-----|--------|---------|
| Gate 1 original | 49.13.76.163 | Timeout | Wrong IP (server moved) |
| Gate 1 retry | 178.104.95.187 | Timeout | Firewall? Now: key issue |
| Gate 1 now | 178.104.95.187 | Permission denied | Key not in authorized_keys |

## User Action

Проверить через Hetzner Console:
```bash
cat /home/ubuntu/.ssh/authorized_keys
```

Убедиться, что туда добавлен temp public key.
Если нет — выполнить команду из `SERVER_CONSOLE_ADD_HERMES_TEMP_PUBLIC_KEY_COMMAND.md`.
