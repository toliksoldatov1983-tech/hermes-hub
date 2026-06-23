param(
    [string]$Server = "root@178.104.95.187",
    [string]$SshKey = "C:\Users\user\.ssh\hetzner_hermes"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SshKey)) {
    throw "SSH key not found: $SshKey"
}

$script = @'
set -u
echo "=== HOST ==="
hostname
date -u
uname -a

echo "=== DISK_MEMORY ==="
df -h /
free -h

echo "=== SERVICE ==="
systemctl is-enabled malyarka-telegram-bot.service 2>/dev/null || true
systemctl is-active malyarka-telegram-bot.service 2>/dev/null || true
systemctl --no-pager --full status malyarka-telegram-bot.service | sed -n '1,35p' || true

echo "=== ENV_KEYS_ONLY ==="
python3 - <<'PY'
from pathlib import Path
p = Path("/etc/malyarka-telegram-bot.env")
print("exists=" + str(p.exists()))
if p.exists():
    for line in p.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        print(s.split("=", 1)[0].strip())
PY

echo "=== RECENT_ERRORS ==="
journalctl -u malyarka-telegram-bot.service --since "30 minutes ago" --no-pager -n 80 |
  sed -E 's@[0-9]{8,}:[A-Za-z0-9_-]{20,}@[TELEGRAM_TOKEN_REDACTED]@g' || true

echo "=== ERROR_COUNTS_2H ==="
echo -n "Unauthorized: "
journalctl -u malyarka-telegram-bot.service --since "2 hours ago" --no-pager 2>/dev/null | grep -c "TelegramUnauthorizedError" || true
echo -n "Conflict: "
journalctl -u malyarka-telegram-bot.service --since "2 hours ago" --no-pager 2>/dev/null | grep -c "TelegramConflictError" || true
echo -n "Traceback: "
journalctl -u malyarka-telegram-bot.service --since "2 hours ago" --no-pager 2>/dev/null | grep -c "Traceback" || true

echo "=== PATHS ==="
for d in /opt/malyarka-telegram-bot /opt/hermes-hub /opt/malyarka-stt /root/.hermes; do
  if [ -e "$d" ]; then
    printf "%s\t" "$d"
    du -sh "$d" 2>/dev/null | awk '{print $1}'
  else
    echo "$d missing"
  fi
done

echo "=== GIT ==="
if [ -d /opt/hermes-hub/.git ]; then
  git -C /opt/hermes-hub status --short
  git -C /opt/hermes-hub rev-parse --short HEAD
fi
'@

$script = $script -replace "`r`n", "`n"
$script | ssh -i $SshKey -o BatchMode=yes -o IdentitiesOnly=yes $Server "bash -s"
