import importlib
from pathlib import Path

from malyarka_vision import (
    DEFAULT_VISION_PROVIDER,
    VisionConfig,
    check_vision_ready,
    recognize_order_photo,
    recognize_order_photo_stub,
)


def test_import_malyarka_vision_does_not_require_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    module = importlib.import_module("malyarka_vision")

    assert module.DEFAULT_VISION_PROVIDER == "none"


def test_import_malyarka_vision_does_not_require_provider_sdk(monkeypatch):
    import builtins
    import malyarka_vision as vision_package

    original_import = builtins.__import__

    def blocked_provider_import(name, *args, **kwargs):
        if name == "google" or name.startswith("google."):
            raise ImportError("provider imports are blocked in this test")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_provider_import)

    reloaded = importlib.reload(vision_package)

    assert reloaded.DEFAULT_VISION_PROVIDER == DEFAULT_VISION_PROVIDER


def test_missing_key_does_not_raise():
    diagnostics = check_vision_ready(VisionConfig(api_key=None))

    assert diagnostics["vision_available"] is False
    assert diagnostics["has_api_key"] is False
    assert diagnostics["real_recognition_enabled"] is False
    assert diagnostics["provider"] == DEFAULT_VISION_PROVIDER
    assert diagnostics["model"] is None


def test_key_value_is_not_exposed_in_diagnostics():
    secret = "test-secret-value-that-must-not-leak"

    diagnostics = check_vision_ready(
        VisionConfig(api_key=secret, real_recognition_enabled=True)
    )

    assert diagnostics["has_api_key"] is True
    assert diagnostics["provider"] == DEFAULT_VISION_PROVIDER
    assert secret not in str(diagnostics)


def test_real_recognition_is_disabled_by_default():
    result = recognize_order_photo_stub(b"fake-photo-bytes")

    assert result["status"] == "not_connected"
    assert result["real_recognition_enabled"] is False
    assert result["external_api_called"] is False
    assert result["confirmed_items"] == []
    assert result["disputed_items"] == []


def test_recognize_order_photo_does_not_call_api_when_disabled():
    result = recognize_order_photo(
        b"fake-photo-bytes",
        config=VisionConfig(
            api_key="fake-key-that-must-not-leak",
            real_recognition_enabled=False,
        ),
    )

    assert result["status"] == "disabled"
    assert result["external_api_called"] is False
    assert "fake-key-that-must-not-leak" not in str(result)


def test_recognize_order_photo_without_key_does_not_raise_or_call_api():
    result = recognize_order_photo(
        "telegram-photo-placeholder",
        config=VisionConfig(api_key=None, real_recognition_enabled=True),
    )

    assert result["status"] == "missing_api_key"
    assert result["external_api_called"] is False


def test_recognize_order_photo_does_not_call_external_provider_even_when_enabled():
    result = recognize_order_photo(
        b"fake-photo-bytes",
        config=VisionConfig(
            api_key="fake-key-that-must-not-leak",
            real_recognition_enabled=True,
        ),
    )

    assert result["status"] == "provider_not_configured"
    assert result["external_api_called"] is False
    assert "fake-key-that-must-not-leak" not in str(result)


def test_vision_layer_does_not_read_environment_key(monkeypatch):
    secret = "environment-secret-that-must-not-be-read"
    monkeypatch.setenv("GEMINI_API_KEY", secret)
    monkeypatch.setenv("DEEPSEEK_API_KEY", secret)

    diagnostics = check_vision_ready()
    result = recognize_order_photo_stub("telegram-photo-placeholder")

    assert diagnostics["has_api_key"] is False
    assert secret not in str(diagnostics)
    assert secret not in str(result)


def test_requirements_do_not_include_google_genai():
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()

    assert "google-genai" not in {line.strip() for line in requirements}


def test_vision_layer_has_no_google_genai_imports():
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in Path("malyarka_vision").glob("*.py")
    )

    assert "google-genai" not in source
    assert "from google import genai" not in source
    assert "gemini-2.5-flash" not in source
