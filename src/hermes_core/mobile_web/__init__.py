"""Mobile Web UI module — serves static files and preview.

This is a lightweight Python wrapper around the static web UI.
The actual UI lives in web/mobile/.
"""

from pathlib import Path

WEB_DIR = (Path(__file__).resolve().parents[3] / "web" / "mobile").resolve()


def get_web_files() -> dict[str, Path]:
    """Return all web UI files with their paths."""
    files = {}
    if WEB_DIR.exists():
        for f in WEB_DIR.glob("*"):
            if f.is_file():
                files[f.name] = f
    return files


def get_web_dir() -> Path:
    return WEB_DIR


def preview_url() -> str:
    """Return the local preview URL."""
    return f"file:///{WEB_DIR.as_posix()}/index.html"


def api_base_url() -> str:
    """Default API base URL."""
    return "http://127.0.0.1:8514"
