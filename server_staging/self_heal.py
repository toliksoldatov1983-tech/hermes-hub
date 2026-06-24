"""Self-healing: bot can read/write own code and restart itself."""

import shutil
import os
import subprocess
from pathlib import Path
from datetime import datetime


BOT_DIR = Path("/opt/malyarka-telegram-bot")
BACKUP_DIR = BOT_DIR / "backups" / "auto_fix"


def read_file(path: str) -> str:
    """Read a file from the bot directory."""
    full = BOT_DIR / path
    if not full.exists():
        return f"Файл не найден: {path}"
    return full.read_text(encoding="utf-8")


def fix_file(path: str, old: str, new: str) -> str:
    """Replace text in a file with backup."""
    full = BOT_DIR / path
    if not full.exists():
        return f"Файл не найден: {path}"

    content = full.read_text(encoding="utf-8")
    if old not in content:
        return f"Текст для замены не найден в {path}"

    # Backup
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"{Path(path).name}_{ts}.bak"
    shutil.copy2(full, backup_path)

    # Apply fix
    new_content = content.replace(old, new)
    full.write_text(new_content, encoding="utf-8")

    # Compile check
    try:
        subprocess.run(
            [str(BOT_DIR / ".venv/bin/python"), "-m", "py_compile", str(full)],
            capture_output=True, timeout=10, check=True
        )
    except subprocess.CalledProcessError as e:
        # Rollback
        shutil.copy2(backup_path, full)
        return f"Ошибка компиляции, откат. {e.stderr.decode()[:200]}"

    return f"Исправлено: {path}. Бэкап: {backup_path.name}"


def restart_bot() -> str:
    """Restart the systemd service."""
    try:
        subprocess.run(["systemctl", "restart", "malyarka-telegram-bot"],
                       capture_output=True, timeout=10, check=True)
        return "Бот перезапущен."
    except subprocess.CalledProcessError as e:
        return f"Ошибка перезапуска: {e.stderr.decode()[:200]}"


def health_check() -> str:
    """Quick health check."""
    try:
        subprocess.run(["systemctl", "is-active", "malyarka-telegram-bot"],
                       capture_output=True, timeout=5, check=True)
        return "Бот: active"
    except subprocess.CalledProcessError:
        return "Бот: не active"
