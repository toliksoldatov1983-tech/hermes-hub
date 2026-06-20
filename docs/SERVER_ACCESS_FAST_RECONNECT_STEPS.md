# Server Access Fast Reconnect Steps

Date: 2026-06-18

## When root key is gone, reconnect via Hetzner Rescue:

1. Hetzner Cloud → server `hermes` → Rescue → linux64
2. SSH Key: `hetzner-hermes`
3. Enable rescue & power cycle
4. PowerShell:
   ```
   ssh-keygen -R 178.104.95.187
   ssh -i C:\Users\user\.ssh\hetzner_hermes -o IdentitiesOnly=yes root@178.104.95.187
   ```
5. Mount:
   ```
   lsblk -f
   mount /dev/sda1 /mnt
   ```
6. Add new temp public key:
   ```
   echo 'ssh-ed25519 AAAA... new-temp-key' >> /mnt/root/.ssh/authorized_keys
   ```
7. ```
   sync
   umount /mnt
   reboot
   ```
8. Connect with new temp key.
