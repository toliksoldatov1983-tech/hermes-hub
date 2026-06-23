import ast
from pathlib import Path

from malyarka_telegram.handlers import handle_photo_message
from malyarka_telegram.messages import format_photo_not_supported_message


def test_photo_handler_keeps_not_connected_message():
    message = handle_photo_message()

    assert message == format_photo_not_supported_message()


def test_photo_handler_does_not_import_or_call_vision_layer():
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

    assert "malyarka_vision" not in imported_modules
    assert "malyarka_vision.gemini" not in imported_modules
    assert "recognize_order_photo_stub" not in called_names
