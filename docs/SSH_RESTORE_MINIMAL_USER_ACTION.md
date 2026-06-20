# SSH Restore — Minimal User Action

Date: 2026-06-17

## Step 1: Find Public Key

```
C:\Users\user\.ssh\hetzner_hermes.pub
```

## Step 2: NEVER Open Private Key

`hetzner_hermes` (private key) — never open, never send.

## Step 3: Add Public Key to Server

Via Hetzner console (root), run:

```bash
mkdir -p /home/ubuntu/.ssh
cat >> /home/ubuntu/.ssh/authorized_keys << 'EOF'
ssh-ed25519 AAAA...  # PASTE PUBLIC KEY HERE
EOF
chmod 700 /home/ubuntu/.ssh
chmod 600 /home/ubuntu/.ssh/authorized_keys
chown -R ubuntu:ubuntu /home/ubuntu/.ssh
```

## Step 4: Test

```bash
ssh -i C:\Users\user\.ssh\hetzner_hermes ubuntu@49.13.76.163 pwd
```

Expected: `/home/ubuntu`

## Step 5: Tell Hermes

«SSH доступ восстановлен, продолжай SERVER_READ_ONLY_GATE_1»
