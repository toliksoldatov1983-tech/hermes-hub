# Server Temp Root Key Recreate Plan

Date: 2026-06-18

## When Needed

Future server gates requiring root SSH.

## Steps

1. Create new temp key locally:
   ```
   ssh-keygen -t ed25519 -f C:\Users\user\.ssh\hermes_temp_server_readonly_v2 -C "hermes-temp-readonly-v2" -N ""
   ```
2. Get public key fingerprint
3. Add to server via Rescue:
   ```
   echo 'ssh-ed25519 AAAA... v2' >> /mnt/root/.ssh/authorized_keys
   ```
4. Test connection
5. Remove after gates complete

## WARNING

- Never reuse old temp key
- Never paste private key
- Remove key after gates
