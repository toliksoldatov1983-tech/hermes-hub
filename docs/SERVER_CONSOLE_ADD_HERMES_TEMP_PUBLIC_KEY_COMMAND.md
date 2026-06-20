# Server Console — Add Hermes Temp Public Key

Date: 2026-06-17

## Run as root on server console:

```bash
mkdir -p /home/ubuntu/.ssh && \
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHrWmcFi/MgZkvAiZBZIBo6Pn1rPhnz49mHLoWCxlCFl hermes-temp-readonly' >> /home/ubuntu/.ssh/authorized_keys && \
sort -u -o /home/ubuntu/.ssh/authorized_keys /home/ubuntu/.ssh/authorized_keys && \
chown -R ubuntu:ubuntu /home/ubuntu/.ssh && \
chmod 700 /home/ubuntu/.ssh && \
chmod 600 /home/ubuntu/.ssh/authorized_keys && \
echo "Added. Keys count:" && wc -l < /home/ubuntu/.ssh/authorized_keys
```

## Verify

```bash
ssh -i C:\Users\user\.ssh\hermes_temp_server_readonly ubuntu@49.13.76.163 pwd
```

Expected: `/home/ubuntu`
