# Server Console — Remove Hermes Temp Public Key

Date: 2026-06-17

## After all read-only gates complete, run as root:

```bash
sed -i '/hermes-temp-readonly/d' /home/ubuntu/.ssh/authorized_keys && \
echo "Removed. Keys count:" && wc -l < /home/ubuntu/.ssh/authorized_keys
```

## Verify removal

```bash
ssh -i C:\Users\user\.ssh\hermes_temp_server_readonly ubuntu@49.13.76.163 pwd
```

Expected: `Permission denied`
