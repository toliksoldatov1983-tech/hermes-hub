import ast
import importlib
from pathlib import Path

from malyarka_ai import (
    DEFAULT_AI_PROVIDER,
    DEFAULT_DEEPSEEK_API_KEY_ENV_VAR,
    DEFAULT_DEEPSEEK_BASE_URL,
    DEFAULT_DEEPSEEK_MODEL,
    DeepSeekConfig,
    analyze_order_text_with_deepseek,
    build_deepseek_order_prompt,
    check_deepseek_ready,
    parse_deepseek_json_response,
    prepare_deepseek_order_analysis,
    validate_deepseek_order_response,
)
from malyarka_telegram.handlers import handle_photo_message
from malyarka_telegram.messages import format_photo_not_supported_message


def test_import_malyarka_ai_works_without_key(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    module = importlib.import_module("malyarka_ai")

    assert module.DEFAULT_AI_PROVIDER == "deepseek"


def test_default_deepseek_config_is_safe():
    config = DeepSeekConfig()

    assert config.provider == DEFAULT_AI_PROVIDER
    assert config.api_key is None
    assert config.api_key_env_var == DEFAULT_DEEPSEEK_API_KEY_ENV_VAR
    assert config.base_url == DEFAULT_DEEPSEEK_BASE_URL
    assert config.model == DEFAULT_DEEPSEEK_MODEL
    assert config.real_ai_enabled is False


def test_check_deepseek_ready_does_not_expose_key():
    secret = "deepseek-secret-value-that-must-not-leak"

    diagnostics = check_deepseek_ready(
        DeepSeekConfig(api_key=secret, real_ai_enabled=True)
    )

    assert diagnostics["provider"] == "deepseek"
    assert diagnostics["has_api_key"] is True
    assert diagnostics["real_ai_enabled"] is True
    assert diagnostics["base_url"] == "https://api.deepseek.com"
    assert diagnostics["model"] == "deepseek-v4-pro"
    assert secret not in str(diagnostics)


def test_missing_deepseek_key_does_not_raise():
    diagnostics = check_deepseek_ready(DeepSeekConfig(api_key=None))
    result = analyze_order_text_with_deepseek(
        "100 200 3 fasad",
        config=DeepSeekConfig(api_key=None, real_ai_enabled=True),
    )

    assert diagnostics["has_api_key"] is False
    assert result["status"] == "missing_api_key"
    assert result["external_api_called"] is False


def test_deepseek_layer_does_not_read_environment_key(monkeypatch):
    secret = "environment-deepseek-secret-that-must-not-be-read"
    monkeypatch.setenv("DEEPSEEK_API_KEY", secret)

    diagnostics = check_deepseek_ready()
    result = analyze_order_text_with_deepseek("100 200")

    assert diagnostics["has_api_key"] is False
    assert secret not in str(diagnostics)
    assert secret not in str(result)


def test_analyze_order_text_with_deepseek_disabled_does_not_call_api():
    secret = "deepseek-secret-value-that-must-not-leak"

    result = analyze_order_text_with_deepseek(
        "100 200 3 fasad",
        config=DeepSeekConfig(api_key=secret, real_ai_enabled=False),
    )

    assert result["status"] == "disabled"
    assert result["external_api_called"] is False
    assert result["real_ai_enabled"] is False
    assert result["confirmed_items"] == []
    assert result["disputed_items"] == []
    assert result["raw_response"] is None
    assert secret not in str(result)


def test_build_deepseek_order_prompt_contains_strict_rules():
    prompt = build_deepseek_order_prompt("1000*400")

    assert "ничего не додумывать" in prompt
    assert "первое число = height" in prompt
    assert "второе число = width" in prompt
    assert "третье число = quantity" in prompt
    assert "type=\"disputed\"" in prompt
    assert "reason обязателен" in prompt
    assert "вернуть только JSON" in prompt
    assert "не писать пояснения вне JSON" in prompt


def test_prepare_deepseek_order_analysis_does_not_call_external_api():
    secret = "deepseek-secret-value-that-must-not-leak"

    prepared = prepare_deepseek_order_analysis(
        "1000*400",
        config=DeepSeekConfig(api_key=secret, real_ai_enabled=False),
    )

    assert prepared["status"] == "prepared"
    assert prepared["provider"] == "deepseek"
    assert prepared["model"] == "deepseek-v4-pro"
    assert prepared["real_ai_enabled"] is False
    assert prepared["external_api_called"] is False
    assert "prompt" in prepared
    assert secret not in str(prepared)


def test_validate_deepseek_order_response_accepts_valid_row():
    result = validate_deepseek_order_response(
        {
            "items": [
                {
                    "type": "row",
                    "source": "text",
                    "raw": "1000*400",
                    "size": {"height": 1000, "width": 400, "quantity": 1},
                    "note": "",
                    "reason": "",
                }
            ]
        }
    )

    assert result["valid"] is True
    assert result["errors"] == []


def test_validate_deepseek_order_response_accepts_disputed_with_reason():
    result = validate_deepseek_order_response(
        {
            "items": [
                {
                    "type": "disputed",
                    "source": "text",
                    "raw": "непонятная строка",
                    "size": {},
                    "note": "",
                    "reason": "Недостаточно чисел для размера",
                }
            ]
        }
    )

    assert result["valid"] is True
    assert result["errors"] == []


def test_validate_deepseek_order_response_rejects_disputed_without_reason():
    result = validate_deepseek_order_response(
        {
            "items": [
                {
                    "type": "disputed",
                    "source": "text",
                    "raw": "непонятная строка",
                    "size": {},
                    "note": "",
                    "reason": "",
                }
            ]
        }
    )

    assert result["valid"] is False
    assert "reason is required" in result["errors"][0]


def test_validate_deepseek_order_response_rejects_row_without_size_fields():
    result = validate_deepseek_order_response(
        {
            "items": [
                {
                    "type": "row",
                    "source": "text",
                    "raw": "1000",
                    "size": {"height": 1000},
                    "note": "",
                    "reason": "",
                }
            ]
        }
    )

    assert result["valid"] is False
    assert any("width is required" in error for error in result["errors"])
    assert any("quantity is required" in error for error in result["errors"])


def test_parse_deepseek_json_response_does_not_raise_on_broken_json():
    result = parse_deepseek_json_response('{"items": [')

    assert result["valid"] is False
    assert result["data"] is None
    assert result["errors"]


def test_parse_deepseek_json_response_rejects_text_outside_json():
    result = parse_deepseek_json_response('{"items": []}\nextra text')

    assert result["valid"] is False
    assert result["data"] is None
    assert result["errors"]


def test_deepseek_api_is_not_called_even_when_enabled_with_key():
    secret = "deepseek-secret-value-that-must-not-leak"

    result = analyze_order_text_with_deepseek(
        "100 200 3 fasad",
        config=DeepSeekConfig(api_key=secret, real_ai_enabled=True),
    )

    assert result["status"] == "provider_not_connected"
    assert result["external_api_called"] is False
    assert secret not in str(result)


def test_telegram_photo_handler_stays_disconnected_from_ai():
    message = handle_photo_message()

    assert message == format_photo_not_supported_message()


def test_telegram_photo_handler_does_not_import_or_call_ai_layers():
    source = Path("malyarka_telegram/handlers.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = set()
    called_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called_names.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called_names.add(node.func.attr)

    assert "malyarka_ai" not in imported_modules
    assert "malyarka_ai.deepseek" not in imported_modules
    assert "analyze_order_text_with_deepseek" not in called_names


def test_requirements_do_not_include_google_genai():
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()

    assert "google-genai" not in {line.strip() for line in requirements}


def test_deepseek_layer_has_no_google_genai_imports():
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in Path("malyarka_ai").glob("*.py")
    )

    assert "google-genai" not in source
    assert "from google import genai" not in source
