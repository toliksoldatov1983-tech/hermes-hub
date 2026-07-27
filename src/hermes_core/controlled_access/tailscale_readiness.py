"""Tailscale Readiness — safe detection layer.

Detects Tailscale presence without installation, login, or network changes.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from subprocess import run, PIPE
from typing import Any


@dataclass
class TailscaleStatus:
    """Tailscale detection result — safe, read-only."""

    installed: bool = False
    running: bool = False
    version: str = ""
    tailscale_ip: str = ""
    tailnet_name: str = ""
    is_ready: bool = False
    warnings: list[str] = field(default_factory=list)
    audit: dict[str, Any] = field(default_factory=lambda: {
        "safe_local": True,
        "no_install": True,
        "no_login": True,
        "no_network_change": True,
        "no_secret_read": True,
        "env_read": False,
    })


def detect_tailscale() -> TailscaleStatus:
    """Safely detect Tailscale presence.

    Does NOT install, login, or change network.
    Only checks if the CLI is available and running.
    """
    status = TailscaleStatus()

    # Check if tailscale CLI exists
    cli = shutil.which("tailscale") or shutil.which("tailscale.exe")
    if not cli:
        status.warnings.append("Tailscale не установлен на этом ПК.")
        return status

    status.installed = True

    # Check version (safe, no auth)
    try:
        r = run([cli, "version"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            status.version = r.stdout.strip().split("\n")[0] if r.stdout else "unknown"
    except Exception:
        status.warnings.append("Не удалось проверить версию Tailscale.")

    # Check status (safe, no auth)
    try:
        r = run([cli, "status", "--json"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            import json as _json
            try:
                data = _json.loads(r.stdout)
                status.running = data.get("BackendState", "") == "Running"
                status.tailscale_ip = data.get("Self", {}).get("TailscaleIPs", [""])[0] if data.get("Self") else ""
                status.tailnet_name = data.get("CurrentTailnet", {}).get("Name", "") if data.get("CurrentTailnet") else ""
            except Exception:
                status.warnings.append("Не удалось разобрать статус Tailscale.")
    except Exception:
        status.warnings.append("Tailscale не запущен.")

    status.is_ready = status.installed and status.running and bool(status.tailscale_ip)
    return status


def get_tailscale_access_plan() -> str:
    """Return the Tailscale access plan instructions."""
    return """
Шаги для включения Tailscale доступа к Hermes-Clean с телефона:

1. Установить Tailscale на ПК:
   https://tailscale.com/download

2. Установить Tailscale на телефон:
   Google Play / App Store → Tailscale

3. Войти в один аккаунт на обоих устройствах.

4. Узнать Tailscale IP ПК:
   tailscale status
   → IP будет вида 100.x.x.x

5. В Hermes-Clean:
   - дать APPROVE_TAILSCALE_MODE
   - дать APPROVE_PHONE_PAIRING
   - изменить bind address на Tailscale IP ПК

6. В Android Shell на телефоне:
   - изменить API URL на http://<tailscale-ip>:8514

Hermes НЕ делает эти шаги автоматически.
"""
