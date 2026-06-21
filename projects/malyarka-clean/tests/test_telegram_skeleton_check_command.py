import builtins
import importlib.util
import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "check_telegram_skeleton.py"
SRC_ROOT = PROJECT_ROOT / "src"


def test_check_command_runs_without_token(tmp_path):
    env = _safe_subprocess_env()

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        cwd=tmp_path,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Итог: OK" in result.stdout
    assert "token" in result.stdout


def test_check_command_does_not_read_env_file(monkeypatch, tmp_path):
    original_open = builtins.open
    original_path_open = Path.open

    def guarded_open(file, *args, **kwargs):
        if str(file).endswith(".env"):
            raise AssertionError(".env must not be read by Telegram skeleton check")
        return original_open(file, *args, **kwargs)

    def guarded_path_open(self, *args, **kwargs):
        if str(self).endswith(".env"):
            raise AssertionError(".env must not be read by Telegram skeleton check")
        return original_path_open(self, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", guarded_open)
    monkeypatch.setattr(Path, "open", guarded_path_open)
    monkeypatch.chdir(tmp_path)

    module = _load_check_module()

    assert module.main() == 0


def test_check_command_diagnostics_are_safe():
    module = _load_check_module()

    diagnostics = module.get_telegram_skeleton_diagnostics()

    assert diagnostics["live_telegram"] is False
    assert diagnostics["polling"] is False
    assert diagnostics["token_required"] is False
    assert diagnostics["reads_env_file"] is False
    assert diagnostics["uses_old_bot_py"] is False
    assert diagnostics["sends_files"] is False
    assert diagnostics["creates_excel"] is False


def test_check_command_does_not_create_corel_export_xlsx(tmp_path, monkeypatch):
    module = _load_check_module()
    monkeypatch.chdir(tmp_path)

    assert module.main() == 0

    assert not (tmp_path / "COREL_EXPORT.xlsx").exists()
    assert not (tmp_path / "outputs" / "COREL_EXPORT.xlsx").exists()


def test_check_command_does_not_import_old_bot_py(monkeypatch, tmp_path):
    for module_name in list(sys.modules):
        if module_name == "bot" or module_name.endswith(".bot"):
            monkeypatch.delitem(sys.modules, module_name, raising=False)

    monkeypatch.chdir(tmp_path)
    module = _load_check_module()

    assert module.main() == 0
    assert "bot" not in sys.modules
    assert all(not name.endswith(".bot") for name in sys.modules)


def test_check_command_does_not_start_telegram_or_polling():
    module = _load_check_module()

    assert module.main() == 0
    diagnostics = module.get_telegram_skeleton_diagnostics()

    assert diagnostics["live_telegram"] is False
    assert diagnostics["polling"] is False


def _safe_subprocess_env():
    env = os.environ.copy()
    for name in ("TELEGRAM_TOKEN", "BOT_TOKEN", "TELEGRAM_BOT_TOKEN"):
        env.pop(name, None)
    env["PYTHONPATH"] = str(SRC_ROOT)
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _load_check_module():
    spec = importlib.util.spec_from_file_location("check_telegram_skeleton_for_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
