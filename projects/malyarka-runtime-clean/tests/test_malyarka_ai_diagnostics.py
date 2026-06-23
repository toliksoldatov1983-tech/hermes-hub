import ast
import json
import subprocess
import sys
from pathlib import Path

from malyarka_ai import DeepSeekConfig
from malyarka_ai.diagnostics import build_deepseek_fallback_diagnostic_preview


def test_diagnostic_preview_for_clean_order_is_safe():
    secret = "deepseek-secret-value-that-must-not-leak"

    result = build_deepseek_fallback_diagnostic_preview(
        "1000*400\n1000*600",
        config=DeepSeekConfig(api_key=secret, real_ai_enabled=True),
    )

    assert result["provider"] == "deepseek"
    assert result["model"] == "deepseek-v4-pro"
    assert result["real_ai_enabled"] is False
    assert result["external_api_called"] is False
    assert result["fallback_used"] is True
    assert result["export_allowed"] is True
    assert result["local_corel_lines"] == ["1000 400 1", "1000 600 1"]
    assert result["prepared_ai_prompt"]
    assert result["prepared_ai_analysis"]["external_api_called"] is False
    assert secret not in str(result)


def test_diagnostic_preview_for_disputed_order_blocks_export():
    result = build_deepseek_fallback_diagnostic_preview(
        "1000*400\nнепонятная строка\n1000*600",
        config=DeepSeekConfig(real_ai_enabled=False),
    )

    assert result["fallback_used"] is True
    assert result["external_api_called"] is False
    assert result["export_allowed"] is False
    assert result["local_corel_lines"] == ["1000 400 1", "1000 600 1"]
    assert result["disputed_rows"]["has_disputed"] is True
    assert result["disputed_rows"]["blocks_export"] is True
    assert result["disputed_rows"]["count"] == 1
    assert result["disputed_rows"]["items"][0]["raw"] == "непонятная строка"


def test_diagnostic_cli_sample_returns_json_without_api_or_polling():
    completed = subprocess.run(
        [sys.executable, "-m", "malyarka_ai.diagnostics", "--sample"],
        check=True,
        capture_output=True,
        text=True,
    )

    result = json.loads(completed.stdout)

    assert result["external_api_called"] is False
    assert result["fallback_used"] is True
    assert result["export_allowed"] is True
    assert result["local_corel_lines"] == ["1000 400 1", "1000 600 1"]
    assert "polling" not in completed.stderr.lower()
    assert "RuntimeWarning" not in completed.stderr


def test_diagnostic_cli_text_returns_json_without_keys(monkeypatch):
    secret = "environment-deepseek-secret-that-must-not-be-read"
    monkeypatch.setenv("DEEPSEEK_API_KEY", secret)

    completed = subprocess.run(
        [sys.executable, "-m", "malyarka_ai.diagnostics", "--text", "1000*400"],
        check=True,
        capture_output=True,
        text=True,
    )

    result = json.loads(completed.stdout)

    assert result["external_api_called"] is False
    assert result["fallback_used"] is True
    assert result["local_corel_lines"] == ["1000 400 1"]
    assert secret not in completed.stdout


def test_diagnostic_cli_stdin_accepts_multiline_order():
    completed = subprocess.run(
        [sys.executable, "-m", "malyarka_ai.diagnostics", "--stdin"],
        input="1000*400\nunclear row\n1000*600",
        check=True,
        capture_output=True,
        text=True,
    )

    result = json.loads(completed.stdout)

    assert result["external_api_called"] is False
    assert result["fallback_used"] is True
    assert result["export_allowed"] is False
    assert result["local_corel_lines"] == ["1000 400 1", "1000 600 1"]
    assert result["disputed_rows"]["count"] == 1
    assert result["prepared_ai_prompt"]


def test_diagnostic_cli_text_file_accepts_multiline_order(tmp_path):
    order_path = tmp_path / "order.txt"
    order_path.write_text("1000*400\nunclear row\n1000*600", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "malyarka_ai.diagnostics",
            "--text-file",
            str(order_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    result = json.loads(completed.stdout)

    assert result["external_api_called"] is False
    assert result["fallback_used"] is True
    assert result["export_allowed"] is False
    assert result["local_corel_lines"] == ["1000 400 1", "1000 600 1"]
    assert result["disputed_rows"]["count"] == 1
    assert result["prepared_ai_prompt"]


def test_diagnostic_cli_summary_format_is_human_readable():
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "malyarka_ai.diagnostics",
            "--text",
            "1000*400",
            "--format",
            "summary",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "export_allowed: true" in completed.stdout
    assert "fallback_used: true" in completed.stdout
    assert "external_api_called: false" in completed.stdout
    assert "1000 400 1" in completed.stdout


def test_telegram_handlers_do_not_import_or_call_deepseek_diagnostics():
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

    assert "malyarka_ai.diagnostics" not in imported_modules
    assert "build_deepseek_fallback_diagnostic_preview" not in called_names


def test_requirements_do_not_include_google_genai():
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()

    assert "google-genai" not in {line.strip() for line in requirements}
