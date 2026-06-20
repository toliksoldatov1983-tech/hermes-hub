# REPORT — SSH Access Recovery & Recheck Autonomous

Date: 2026-06-17

## Attempt

| # | Action | Result |
|---|--------|--------|
| 1 | chmod 600 private key | No effect (Windows NTFS) |
| 2 | SSH ubuntu@49.13.76.163 | Permission denied (publickey) |

## Analysis

- Key exists locally ✅
- Fingerprint match ✅
- Permissions fix not possible on Windows NTFS
- SSH authentication rejected at server
- **Most likely: public key NOT in server authorized_keys**

## Verdict

```text
Автоматически восстановить SSH невозможно:
нет доступа к server console/root.
Нужна ручная вставка public key пользователем.
```

## User Action

1. Открыть Hetzner console для сервера 49.13.76.163
2. Войти как root
3. Проверить: `cat /home/ubuntu/.ssh/authorized_keys`
4. Если ключ отсутствует — добавить:
   ```bash
   ssh-ed25519 AAAA...добавить публичный ключ из hetzner_hermes.pub
   ```

5. После этого: повторить SERVER_READ_ONLY_GATE_1

## Safety

```
private key: NOT read | token/env/config: NOT read | server: NO writes
```
