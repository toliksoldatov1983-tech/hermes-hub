import ast
from pathlib import Path

from malyarka_ai import DeepSeekConfig, prepare_order_analysis_with_fallback
from malyarka_telegram.handlers import handle_photo_message
from malyarka_telegram.messages import format_photo_not_supported_message


def test_fallback_bridge_does_not_call_external_api_when_ai_disabled():
    result = prepare_order_analysis_with_fallback(
        "1000*400",
        config=DeepSeekConfig(real_ai_enabled=False),
    )

    assert result["provider"] == "deepseek"
    assert result["model"] == "deepseek-v4-pro"
    assert result["real_ai_enabled"] is False
    assert result["external_api_called"] is False
    assert result["fallback_used"] is True
    assert result["fallback_reason"]


def test_fallback_bridge_uses_local_parser_for_star_separated_rows():
    result = prepare_order_analysis_with_fallback(
        "1000*400\n1000*600",
        config=DeepSeekConfig(real_ai_enabled=False),
    )

    assert result["local_result"]["corel_lines"] == [
        "1000 400 1",
        "1000 600 1",
    ]
    assert result["local_preview"]["confirmed_count"] == 2
    assert result["local_preview"]["disputed_count"] == 0
    assert result["export_allowed"] is True


def test_fallback_bridge_keeps_disputed_rows_blocking_export():
    result = prepare_order_analysis_with_fallback(
        "1000*400\nunclear row\n1000*600",
        config=DeepSeekConfig(real_ai_enabled=False),
    )

    assert result["local_result"]["corel_lines"] == [
        "1000 400 1",
        "1000 600 1",
    ]
    assert result["local_preview"]["confirmed_count"] == 2
    assert result["local_preview"]["disputed_count"] == 1
    assert result["disputed_rows"]["has_disputed"] is True
    assert result["disputed_rows"]["blocks_export"] is True
    assert result["export_allowed"] is False


def test_fallback_bridge_prepares_deepseek_prompt_without_using_secret():
    secret = "deepseek-secret-value-that-must-not-leak"

    result = prepare_order_analysis_with_fallback(
        "1000*400",
        config=DeepSeekConfig(api_key=secret, real_ai_enabled=True),
    )

    assert result["fallback_used"] is True
    assert result["external_api_called"] is False
    assert result["configured_real_ai_enabled"] is True
    assert result["prepared_ai_analysis"]["status"] == "prepared"
    assert result["prepared_ai_analysis"]["external_api_called"] is False
    assert "1000*400" in result["prepared_ai_prompt"]
    assert secret not in str(result)


def test_fallback_bridge_uses_local_parser_when_key_is_missing():
    result = prepare_order_analysis_with_fallback(
        "1000*400",
        config=DeepSeekConfig(api_key=None, real_ai_enabled=True),
    )

    assert result["fallback_used"] is True
    assert result["external_api_called"] is False
    assert "key is not configured" in result["fallback_reason"]
    assert result["local_result"]["corel_lines"] == ["1000 400 1"]


def test_telegram_handlers_do_not_import_or_call_deepseek_bridge():
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

    assert "malyarka_ai.bridge" not in imported_modules
    assert "prepare_order_analysis_with_fallback" not in called_names


def test_photo_handler_remains_stub():
    assert handle_photo_message() == format_photo_not_supported_message()


def test_requirements_do_not_include_google_genai():
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()

    assert "google-genai" not in {line.strip() for line in requirements}
