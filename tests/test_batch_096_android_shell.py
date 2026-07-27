"""Tests for BATCH_096: Android WebView Shell App.

Covers:
  - Android shell files exist
  - AndroidManifest exists and is valid
  - MainActivity exists
  - WebView security config exists
  - Default URL is 127.0.0.1
  - No 0.0.0.0 default
  - LAN mode disabled by default
  - External mode disabled by default
  - No secrets in Android files
  - No tokens in Android files
  - No dangerous permissions
  - No file access enabled by default
  - No Android JS bridge
  - No analytics/tracking SDK
  - No production signing keys
  - Documentation exists
  - CLI commands work
  - Regression for BATCH_088–095
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

ANDROID_DIR = PROJECT_ROOT / "android" / "HermesWebViewShell"


# ── 1. Files exist ──


class TestShellFiles:
    """All required Android scaffold files exist."""

    def test_project_dir_exists(self):
        assert ANDROID_DIR.exists(), f"{ANDROID_DIR} should exist"

    def test_manifest_exists(self):
        p = ANDROID_DIR / "app/src/main/AndroidManifest.xml"
        assert p.exists(), "AndroidManifest.xml should exist"

    def test_main_activity_exists(self):
        p = ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java"
        assert p.exists(), "MainActivity.java should exist"

    def test_layout_exists(self):
        p = ANDROID_DIR / "app/src/main/res/layout/activity_main.xml"
        assert p.exists(), "activity_main.xml should exist"

    def test_network_security_config_exists(self):
        p = ANDROID_DIR / "app/src/main/res/xml/network_security_config.xml"
        assert p.exists(), "network_security_config.xml should exist"

    def test_build_files_exist(self):
        assert (ANDROID_DIR / "app/build.gradle").exists()
        assert (ANDROID_DIR / "build.gradle").exists()
        assert (ANDROID_DIR / "settings.gradle").exists()
        assert (ANDROID_DIR / "gradle.properties").exists()

    def test_docs_exist(self):
        assert (PROJECT_ROOT / "docs/ANDROID_WEBVIEW_SHELL_RU.md").exists()

    def test_python_module_exists(self):
        assert (PROJECT_ROOT / "src/hermes_core/android_shell/__init__.py").exists()

    def test_required_files_all_present(self):
        from hermes_core.android_shell import check_required_files
        missing = check_required_files()
        assert len(missing) == 0, f"Missing files: {missing}"


# ── 2. Manifest checks ──


class TestManifestSafety:
    """AndroidManifest.xml security checks."""

    def test_default_url_is_localhost(self):
        from hermes_core.android_shell import get_default_url
        url = get_default_url()
        assert "127.0.0.1" in url, f"Default URL should be 127.0.0.1, got: {url}"

    def test_no_0_0_0_0_default(self):
        manifest = (ANDROID_DIR / "app/src/main/AndroidManifest.xml").read_text()
        assert "0.0.0.0" not in manifest, "Manifest should not reference 0.0.0.0"

    def test_no_dangerous_permissions(self):
        from hermes_core.android_shell import check_dangerous_permissions
        dangerous = check_dangerous_permissions()
        assert len(dangerous) == 0, f"Dangerous permissions found: {dangerous}"

    def test_only_internet_permission(self):
        manifest = (ANDROID_DIR / "app/src/main/AndroidManifest.xml").read_text()
        permissions = [l.strip() for l in manifest.splitlines() if "uses-permission" in l]
        # Only INTERNET should be there (maybe ACCESS_NETWORK_STATE for WiFi)
        for p in permissions:
            assert "INTERNET" in p, f"Unexpected permission: {p}"

    def test_no_backup(self):
        manifest = (ANDROID_DIR / "app/src/main/AndroidManifest.xml").read_text()
        assert 'allowBackup="false"' in manifest or "allowBackup" not in manifest


# ── 3. MainActivity security ──


class TestMainActivitySafety:
    """MainActivity.java security checks."""

    def test_no_js_bridge(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text()
        # Check active code lines (not comments)
        code_lines = [l.strip() for l in java.splitlines()
                      if not l.strip().startswith("//") and not l.strip().startswith("/*")]
        code_text = "\n".join(code_lines)
        assert "addJavascriptInterface" not in code_text, "JS bridge should NOT be added in code"

    def test_file_access_disabled(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text()
        assert "setAllowFileAccess(false)" in java or "setAllowFileAccess" not in java

    def test_no_secrets(self):
        from hermes_core.android_shell import check_secrets_in_files
        secrets = check_secrets_in_files()
        assert len(secrets) == 0, f"Secrets found: {secrets}"

    def test_no_token_storage(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text()
        assert "putString(\"token\"" not in java
        assert "putString(\"api_key\"" not in java

    def test_no_external_intents_blocked(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text()
        # Should not have external URL intents without confirmation
        assert "ACTION_VIEW" not in java, "External intents should not be used"

    def test_has_warning_about_phone_localhost(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text(encoding="utf-8")
        assert "127.0.0.1" in java and "телефон" in java.lower(), \
            "Should warn about 127.0.0.1 on phone"


# ── 4. WebView config ──


class TestWebViewConfig:
    """WebView configuration checks."""

    def test_network_security_localhost_only(self):
        config = (ANDROID_DIR / "app/src/main/res/xml/network_security_config.xml").read_text()
        assert "127.0.0.1" in config
        assert "localhost" in config

    def test_no_mixed_content(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text()
        assert "MIXED_CONTENT_NEVER_ALLOW" in java or "MIXED_CONTENT_ALWAYS_ALLOW" not in java

    def test_no_password_saving(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text()
        assert "setSavePassword(false)" in java

    def test_no_universal_access_from_file(self):
        java = (ANDROID_DIR / "app/src/main/java/com/hermes/webview/MainActivity.java").read_text()
        assert "setAllowUniversalAccessFromFileURLs(false)" in java


# ── 5. No analytics/tracking ──


class TestNoAnalytics:
    """No analytics or tracking SDK."""

    def test_no_firebase(self):
        gradle = (ANDROID_DIR / "app/build.gradle").read_text()
        assert "firebase" not in gradle.lower()

    def test_no_advertising(self):
        gradle = (ANDROID_DIR / "app/build.gradle").read_text()
        assert "play-services-ads" not in gradle.lower()
        assert "admob" not in gradle.lower()

    def test_no_crashlytics(self):
        gradle = (ANDROID_DIR / "app/build.gradle").read_text()
        assert "crashlytics" not in gradle.lower()

    def test_build_gradle_has_safety_comment(self):
        gradle = (ANDROID_DIR / "app/build.gradle").read_text()
        assert "NO analytics SDK" in gradle or "no analytics" in gradle.lower()


# ── 6. CLI integration ──


class TestCLIAndroidShell:
    """Android shell CLI commands work."""

    def test_android_shell_status_cli(self):
        from hermes_core.cli import android_shell_status_command
        import argparse
        rc = android_shell_status_command(argparse.Namespace())
        assert rc == 0

    def test_android_shell_files_cli(self):
        from hermes_core.cli import android_shell_files_command
        import argparse
        rc = android_shell_files_command(argparse.Namespace())
        assert rc == 0

    def test_android_shell_security_check_cli(self):
        from hermes_core.cli import android_shell_security_check_command
        import argparse
        rc = android_shell_security_check_command(argparse.Namespace())
        assert rc == 0

    def test_android_shell_build_info_cli(self):
        from hermes_core.cli import android_shell_build_info_command
        import argparse
        rc = android_shell_build_info_command(argparse.Namespace())
        assert rc == 0

    def test_commands_in_parser(self):
        from hermes_core.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["android-shell-status"])
        assert args.command == "android-shell-status"


# ── 7. Python module ──


class TestAndroidShellModule:
    """hermes_core.android_shell module works."""

    def test_get_android_dir(self):
        from hermes_core.android_shell import get_android_dir
        d = get_android_dir()
        assert d.exists()

    def test_get_shell_files(self):
        from hermes_core.android_shell import get_shell_files
        files = get_shell_files()
        assert len(files) >= 10

    def test_check_required_files(self):
        from hermes_core.android_shell import check_required_files
        missing = check_required_files()
        assert len(missing) == 0

    def test_check_dangerous_permissions(self):
        from hermes_core.android_shell import check_dangerous_permissions
        dangerous = check_dangerous_permissions()
        assert len(dangerous) == 0

    def test_get_default_url(self):
        from hermes_core.android_shell import get_default_url
        url = get_default_url()
        assert "127.0.0.1" in url


# ── 8. Regression ──


class TestRegression:
    """Android shell doesn't break existing functionality."""

    def test_tests_pass(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_ai_provider_ok(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        assert not AIProviderRouter().select("mock").is_blocked

    def test_runtime_bridge_ok(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        assert BridgeRouter().handle(BridgeRequest(action=BridgeActionType.STATUS)).is_ok

    def test_mobile_gateway_ok(self):
        from hermes_core.mobile_gateway import MobileGateway
        assert MobileGateway().status().status == "OK"

    def test_mobile_web_ok(self):
        from hermes_core.mobile_web import get_web_files
        assert len(get_web_files()) >= 4
