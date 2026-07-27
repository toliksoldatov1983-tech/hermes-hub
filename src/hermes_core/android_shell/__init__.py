"""Android WebView Shell module — scaffold management.

This module manages the Android shell project scaffold.
No Android SDK required for status/file listing.
SDK is only needed for actual APK build.
"""

from pathlib import Path

ANDROID_DIR = (Path(__file__).resolve().parents[3] / "android" / "HermesWebViewShell").resolve()

REQUIRED_FILES = [
    "app/src/main/AndroidManifest.xml",
    "app/src/main/java/com/hermes/webview/MainActivity.java",
    "app/src/main/res/layout/activity_main.xml",
    "app/src/main/res/values/strings.xml",
    "app/src/main/res/values/themes.xml",
    "app/src/main/res/xml/network_security_config.xml",
    "app/build.gradle",
    "build.gradle",
    "settings.gradle",
    "gradle.properties",
]

DANGEROUS_PERMISSIONS = [
    "ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION",
    "CAMERA", "RECORD_AUDIO",
    "READ_EXTERNAL_STORAGE", "WRITE_EXTERNAL_STORAGE",
    "READ_CONTACTS", "READ_SMS", "SEND_SMS",
    "READ_PHONE_STATE", "CALL_PHONE",
    "BLUETOOTH", "BLUETOOTH_ADMIN",
    "ACCESS_BACKGROUND_LOCATION",
]


def get_android_dir() -> Path:
    return ANDROID_DIR


def get_shell_files() -> dict[str, Path]:
    """Return all shell files with their paths."""
    files = {}
    if ANDROID_DIR.exists():
        for f in ANDROID_DIR.rglob("*"):
            if f.is_file() and not f.name.startswith("."):
                rel = f.relative_to(ANDROID_DIR).as_posix()
                files[rel] = f
    return files


def check_required_files() -> list[str]:
    """Return list of missing required files."""
    missing = []
    for rel in REQUIRED_FILES:
        if not (ANDROID_DIR / rel).exists():
            missing.append(rel)
    return missing


def check_dangerous_permissions() -> list[str]:
    """Check manifest for dangerous permissions (excluding comments)."""
    manifest = ANDROID_DIR / "app/src/main/AndroidManifest.xml"
    if not manifest.exists():
        return []
    content = manifest.read_text(encoding="utf-8")
    found = []
    for perm in DANGEROUS_PERMISSIONS:
        # Only flag if it appears in an actual <uses-permission> or <permission> tag
        # Not in XML comments <!-- -->
        for line in content.splitlines():
            stripped = line.strip()
            if perm in stripped and not stripped.startswith("<!--"):
                if "<uses-permission" in stripped or "<permission" in stripped:
                    found.append(perm)
                    break
    return found


def check_secrets_in_files() -> list[str]:
    """Check shell files for secrets/tokens."""
    suspicious = []
    for f in ANDROID_DIR.rglob("*"):
        if f.is_file() and f.suffix in (".java", ".xml", ".gradle", ".properties", ".kt"):
            try:
                content = f.read_text(encoding="utf-8").lower()
            except Exception:
                continue
            if "api_key" in content or "token" in content or "secret" in content:
                # Ignore comments/strings like "no secrets"
                lines = content.splitlines()
                secrets_lines = [
                    l for l in lines
                    if ("api_key" in l or "token" in l or "secret" in l)
                    and not l.strip().startswith("//")
                    and not l.strip().startswith("/*")
                    and not l.strip().startswith("*")
                    and "no secret" not in l.lower()
                    and "blocked" not in l.lower()
                ]
                if secrets_lines:
                    suspicious.append(f"{f.relative_to(ANDROID_DIR)}: {secrets_lines[0][:80]}")
    return suspicious


def get_default_url() -> str:
    """Read default API URL from MainActivity."""
    main = ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java"
    if main.exists():
        content = main.read_text(encoding="utf-8")
        for line in content.splitlines():
            if "DEFAULT_API_URL" in line and "http" in line:
                url = line.split('"')[1] if '"' in line else "unknown"
                return url
    return "unknown"


def has_android_sdk() -> bool:
    """Check if Android SDK is available."""
    import shutil
    return shutil.which("adb") is not None or shutil.which("gradle") is not None
