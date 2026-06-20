# Server Access Known Good Commands

Date: 2026-06-18

```bash
# Clear old host key
ssh-keygen -R 178.104.95.187

# Rescue connect
ssh -i C:\Users\user\.ssh\hetzner_hermes -o IdentitiesOnly=yes root@178.104.95.187

# Find disk
lsblk -f

# Mount
mount /dev/sda1 /mnt

# Flush
sync

# Unmount
umount /mnt

# Reboot
reboot
```
