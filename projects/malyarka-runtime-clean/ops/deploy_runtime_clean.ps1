param(
    [string]$Server = "root@178.104.95.187",
    [string]$SshKey = "C:\Users\user\.ssh\hetzner_hermes",
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [switch]$Apply
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SshKey)) {
    throw "SSH key not found: $SshKey"
}

Write-Host "Running local tests before deploy package..."
Push-Location $ProjectRoot
try {
    $env:PYTHONIOENCODING = "utf-8"
    python -m pytest -q
}
finally {
    Pop-Location
}

$packageInfo = & (Join-Path $PSScriptRoot "package_runtime_clean.ps1") -ProjectRoot $ProjectRoot
$package = $packageInfo.Package
$remoteZip = "/tmp/malyarka-runtime-clean.zip"
$remoteStage = "/opt/malyarka-telegram-bot.next"
$live = "/opt/malyarka-telegram-bot"

Write-Host "Uploading package to ${Server}:$remoteZip"
scp -i $SshKey -o BatchMode=yes -o IdentitiesOnly=yes $package "${Server}:$remoteZip"

$mode = if ($Apply) { "APPLY" } else { "DRY_RUN" }

$remoteScript = @"
set -euo pipefail
MODE="$mode"
LIVE="$live"
STAGE="$remoteStage"
ZIP="$remoteZip"
BACKUP_DIR="/opt/malyarka-backups"
STAMP=`$(date -u +%Y%m%d_%H%M%S)

echo "=== DEPLOY MODE: `$MODE ==="
echo "Live: `$LIVE"
echo "Stage: `$STAGE"

rm -rf "`$STAGE"
mkdir -p "`$STAGE"
python3 -m zipfile -e "`$ZIP" "`$STAGE"

echo "=== STAGE COMPILE CHECK ==="
cd "`$STAGE"
python3 -m compileall -q .

echo "=== STAGE FILES ==="
find "`$STAGE" -maxdepth 2 -type f | sed "s#`$STAGE/##" | sort | head -120

echo "=== CURRENT SERVICE ==="
systemctl is-active malyarka-telegram-bot.service || true

if [ "`$MODE" != "APPLY" ]; then
  echo "DRY RUN ONLY. No live files changed and service was not restarted."
  exit 0
fi

mkdir -p "`$BACKUP_DIR"
BACKUP="`$BACKUP_DIR/malyarka-telegram-bot_before_runtime_clean_`$STAMP.tgz"
echo "=== BACKUP LIVE TO `$BACKUP ==="
tar --exclude="./.venv" --exclude="./__pycache__" --exclude="*/__pycache__" -C "`$LIVE" -czf "`$BACKUP" .

echo "=== STOP SERVICE ==="
systemctl stop malyarka-telegram-bot.service

echo "=== SYNC STAGE TO LIVE ==="
rsync -a --delete \
  --exclude ".venv/" \
  --exclude ".env" \
  --exclude "orders.db" \
  --exclude "__pycache__/" \
  --exclude ".pytest_cache/" \
  "`$STAGE"/ "`$LIVE"/

chown -R malyarka-bot:malyarka-bot "`$LIVE"

echo "=== START SERVICE ==="
systemctl start malyarka-telegram-bot.service
sleep 3
systemctl --no-pager --full status malyarka-telegram-bot.service | sed -n '1,35p'
journalctl -u malyarka-telegram-bot.service --since "2 minutes ago" --no-pager -n 60 |
  sed -E 's@[0-9]{8,}:[A-Za-z0-9_-]{20,}@[TELEGRAM_TOKEN_REDACTED]@g'
"@

$remoteScript = $remoteScript -replace "`r`n", "`n"
$remoteScript | ssh -i $SshKey -o BatchMode=yes -o IdentitiesOnly=yes $Server "bash -s"

if (-not $Apply) {
    Write-Host "Dry run complete. Re-run with -Apply only after Telegram token/env is fixed and you approve deploy."
}
