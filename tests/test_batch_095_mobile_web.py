"""Tests for BATCH_095: Mobile Web UI.

Covers:
  - Mobile web files exist (index.html, app.css, app.js, api_client.js)
  - HTML contains all required screens
  - CSS is mobile-first
  - JS has no external URLs
  - api_client uses localhost default
  - No secrets in UI code
  - No token storage
  - No external API calls in JS
  - No 0.0.0.0 in defaults
  - Malyarka screen exists
  - Assistant screen exists
  - Status/Checks/AI Provider/Safety screens exist
  - CLI commands work
  - Regression for BATCH_088–094
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

WEB_DIR = PROJECT_ROOT / "web" / "mobile"


# ── 1. Files exist ──


class TestWebFilesExist:
    """All required web files are present."""

    REQUIRED = ["index.html", "app.css", "app.js", "api_client.js"]

    @pytest.mark.parametrize("filename", REQUIRED)
    def test_file_exists(self, filename):
        path = WEB_DIR / filename
        assert path.exists(), f"{filename} should exist in {WEB_DIR}"

    @pytest.mark.parametrize("filename", REQUIRED)
    def test_file_not_empty(self, filename):
        path = WEB_DIR / filename
        assert path.stat().st_size > 0, f"{filename} should not be empty"

    def test_all_four_files(self):
        from hermes_core.mobile_web import get_web_files
        files = get_web_files()
        for f in self.REQUIRED:
            assert f in files, f"{f} should be in web files"


# ── 2. HTML structure ──


class TestHTMLStructure:
    """index.html contains all required screens."""

    def test_html_has_home_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-home"' in html

    def test_html_has_assistant_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-assistant"' in html

    def test_html_has_malyarka_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-malyarka"' in html

    def test_html_has_status_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-status"' in html

    def test_html_has_checks_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-checks"' in html

    def test_html_has_ai_provider_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-ai-provider"' in html

    def test_html_has_safety_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-safety"' in html

    def test_html_has_settings_screen(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="screen-settings"' in html

    def test_html_has_bottom_nav(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'id="bottom-nav"' in html

    def test_html_has_viewport_meta(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'viewport' in html.lower()

    def test_html_references_css(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'app.css' in html

    def test_html_references_js(self):
        html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
        assert 'app.js' in html
        assert 'api_client.js' in html


# ── 3. CSS mobile-first ──


class TestCSSMobileFirst:
    """CSS has mobile-first layout."""

    def test_css_has_max_width(self):
        css = (WEB_DIR / "app.css").read_text(encoding="utf-8")
        assert "max-width" in css, "CSS should have max-width for mobile"

    def test_css_has_dark_theme(self):
        css = (WEB_DIR / "app.css").read_text(encoding="utf-8")
        assert "--bg" in css, "CSS should have dark theme variables"
        assert "--green" in css

    def test_css_has_bottom_nav(self):
        css = (WEB_DIR / "app.css").read_text(encoding="utf-8")
        assert "#bottom-nav" in css, "CSS should style bottom navigation"

    def test_css_has_sticky_header(self):
        css = (WEB_DIR / "app.css").read_text(encoding="utf-8")
        assert "sticky" in css, "CSS should have sticky header"

    def test_css_no_external_urls(self):
        css = (WEB_DIR / "app.css").read_text(encoding="utf-8")
        assert "https://" not in css, "CSS should not reference external URLs"

    def test_css_has_grid(self):
        css = (WEB_DIR / "app.css").read_text(encoding="utf-8")
        assert "grid-template-columns" in css


# ── 4. JS safety ──


class TestJSSafety:
    """JavaScript has no secrets or external API calls."""

    def test_app_js_no_external_urls(self):
        js = (WEB_DIR / "app.js").read_text(encoding="utf-8")
        # Check for actual https:// URLs (not in comments)
        lines_with_https = [l for l in js.splitlines() if "https://" in l and not l.strip().startswith("//")]
        assert len(lines_with_https) == 0, f"app.js should not have https:// URLs in code: {lines_with_https}"
        # Check 0.0.0.0 (not in comments, not as display text — only as config/default)
        lines_with_0000 = [l for l in js.splitlines()
                          if "0.0.0.0" in l
                          and not l.strip().startswith("//")
                          and "заблокирован" not in l
                          and "blocked" not in l.lower()]
        assert len(lines_with_0000) == 0, f"app.js should not reference 0.0.0.0: {lines_with_0000}"

    def test_app_js_no_secrets(self):
        js = (WEB_DIR / "app.js").read_text(encoding="utf-8")
        lowered = js.lower()
        assert "api_key" not in lowered, "app.js should not contain api_key"
        assert "token" not in lowered, "app.js should not contain token"
        # "secret" is common in api_client but check app.js specifically
        assert ".env" not in lowered, "app.js should not reference .env"

    def test_api_client_uses_localhost(self):
        js = (WEB_DIR / "api_client.js").read_text(encoding="utf-8")
        assert "127.0.0.1" in js, "api_client.js must default to 127.0.0.1"
        assert "DEFAULT_BASE" in js

    def test_api_client_no_external_api(self):
        js = (WEB_DIR / "api_client.js").read_text(encoding="utf-8")
        assert "gemini" not in js.lower(), "api_client should not call Gemini"
        assert "deepseek" not in js.lower(), "api_client should not call DeepSeek"
        assert "googleapis" not in js.lower()

    def test_api_client_no_token_storage(self):
        js = (WEB_DIR / "api_client.js").read_text(encoding="utf-8")
        lowered = js.lower()
        assert "localstorage.setitem('token'" not in lowered.replace(" ", "")
        assert "sessionstorage.setitem('token'" not in lowered.replace(" ", "")

    def test_api_client_warns_non_localhost(self):
        js = (WEB_DIR / "api_client.js").read_text(encoding="utf-8")
        assert "non-localhost" in js or "not localhost" in js.lower()

    def test_app_js_has_screen_navigation(self):
        js = (WEB_DIR / "app.js").read_text(encoding="utf-8")
        assert "showScreen" in js or "screen-home" in js

    def test_app_js_has_malyarka_handler(self):
        js = (WEB_DIR / "app.js").read_text(encoding="utf-8")
        assert "malyarka" in js.lower()

    def test_app_js_has_assistant_handler(self):
        js = (WEB_DIR / "app.js").read_text(encoding="utf-8")
        assert "assistant" in js.lower() or "dailyAssistant" in js


# ── 5. CLI integration ──


class TestCLIMobileWeb:
    """Mobile web CLI commands work."""

    def test_mobile_web_status_cli(self):
        from hermes_core.cli import mobile_web_status_command
        import argparse
        rc = mobile_web_status_command(argparse.Namespace())
        assert rc == 0

    def test_mobile_web_preview_cli(self):
        from hermes_core.cli import mobile_web_preview_command
        import argparse
        rc = mobile_web_preview_command(argparse.Namespace())
        assert rc == 0

    def test_mobile_web_files_cli(self):
        from hermes_core.cli import mobile_web_files_command
        import argparse
        rc = mobile_web_files_command(argparse.Namespace())
        assert rc == 0

    def test_mobile_web_self_check_cli(self):
        from hermes_core.cli import mobile_web_self_check_command
        import argparse
        rc = mobile_web_self_check_command(argparse.Namespace())
        assert rc == 0

    def test_commands_in_parser(self):
        from hermes_core.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["mobile-web-self-check"])
        assert args.command == "mobile-web-self-check"


# ── 6. Python module ──


class TestMobileWebModule:
    """hermes_core.mobile_web module works."""

    def test_get_web_files(self):
        from hermes_core.mobile_web import get_web_files
        files = get_web_files()
        assert len(files) >= 4

    def test_get_web_dir(self):
        from hermes_core.mobile_web import get_web_dir
        d = get_web_dir()
        assert d.exists()

    def test_preview_url(self):
        from hermes_core.mobile_web import preview_url
        url = preview_url()
        assert "index.html" in url

    def test_api_base_url(self):
        from hermes_core.mobile_web import api_base_url
        url = api_base_url()
        assert "127.0.0.1" in url


# ── 7. Regression ──


class TestRegression:
    """Mobile web doesn't break existing functionality."""

    def test_malyarka_fixtures(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_ai_provider_router(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        assert not AIProviderRouter().select("mock").is_blocked

    def test_runtime_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        assert BridgeRouter().handle(BridgeRequest(action=BridgeActionType.STATUS)).is_ok

    def test_mobile_gateway(self):
        from hermes_core.mobile_gateway import MobileGateway
        assert MobileGateway().status().status == "OK"
