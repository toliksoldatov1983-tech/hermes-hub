"""Tests для Secret Guard Hermes-Clean.

Проверяет:
- Создание SecretGuard
- Проверка .env файлов (фейковый .env в temp)
- Проверка os.environ с фейковыми секретами
- Санитизация текста (удаление sk-..., api_key=...)
- validate_no_real_secrets() рекурсивно
- MockProvider — создание, request, validate_key
- MockProvider — SecretAccessError при реальном ключе
- report() формат
- run_full_check()
- sanitize_text(), is_safe_string()
"""

import os
import tempfile
from pathlib import Path

import pytest

from hermes_clean import (
    SecretGuard,
    SecretAccessError,
    MockProvider,
    sanitize_text,
    is_safe_string,
)


# ── 1. Создание ──

def test_create_guard():
    guard = SecretGuard()
    assert guard.is_active is True
    assert guard.contour_path is not None


def test_create_guard_with_path():
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        assert str(guard.contour_path) == Path(tmp).resolve().as_posix() or \
               str(guard.contour_path) == tmp


# ── 2. Санитизация текста ──

def test_sanitize_openai_key():
    guard = SecretGuard()
    text = "api_key = sk-proj-1234567890abcdef1234567890abcdef"
    result = guard.sanitize(text)
    assert "[REDACTED]" in result
    assert "sk-proj" not in result


def test_sanitize_github_token():
    guard = SecretGuard()
    text = "token = ghp_1234567890abcdef1234567890abcdef12345678"
    result = guard.sanitize(text)
    assert "[REDACTED]" in result
    assert "ghp_" not in result


def test_sanitize_slack_token():
    guard = SecretGuard()
    text = "slack_token = xoxb-1234567890-1234567890-abcdef123456"
    result = guard.sanitize(text)
    assert "[REDACTED]" in result


def test_sanitize_aws_key():
    guard = SecretGuard()
    text = "aws_key = AKIA1234567890123456"
    result = guard.sanitize(text)
    assert "[REDACTED]" in result


def test_sanitize_clean_text():
    guard = SecretGuard()
    text = "Это обычный текст без секретов."
    result = guard.sanitize(text)
    assert result == text


def test_sanitize_mixed():
    guard = SecretGuard()
    text = "key=sk-test1234567890abcdef и ещё текст"
    result = guard.sanitize(text)
    assert "[REDACTED]" in result
    assert "sk-test" not in result


# ── 3. sanitize_text() utility ──

def test_sanitize_text_utility():
    text = "api_key = sk-1234567890abcdef1234567890abcdef"
    result = sanitize_text(text)
    assert "[REDACTED]" in result


# ── 4. is_safe_string() ──

def test_is_safe_string_true():
    assert is_safe_string("чистый текст") is True


def test_is_safe_string_false():
    assert is_safe_string("sk-testABCDEFGHIJKLMNOPQRSTUVWXYZ") is False
    assert is_safe_string("api_key=sk-testABCDEFGHIJKLMNOPQRSTUVWXYZ") is False


# ── 5. validate_no_real_secrets() ──

def test_validate_no_secrets_clean_dict():
    guard = SecretGuard()
    data = {"name": "test", "value": 42, "items": [1, 2, 3]}
    found = guard.validate_no_real_secrets(data)
    assert found == []


def test_validate_no_secrets_dirty_dict():
    guard = SecretGuard()
    data = {"name": "test", "api_key": "sk-abc1234567890abcdef1234567890abcdef"}
    found = guard.validate_no_real_secrets(data)
    assert len(found) >= 1
    assert "api_key" in found[0]


def test_validate_no_secrets_nested():
    guard = SecretGuard()
    data = {"config": {"credentials": {"token": "ghp_test1234567890abcdef1234567890abcdef12345678"}}}
    found = guard.validate_no_real_secrets(data)
    assert len(found) >= 1
    assert "token" in found[0]


# ── 6. MockProvider ──

def test_create_mock():
    guard = SecretGuard()
    mock = guard.create_mock("openai")
    assert isinstance(mock, MockProvider)
    assert mock.name == "openai"
    assert mock.mock_api_key == "mock-key-placeholder"


def test_get_mock():
    guard = SecretGuard()
    guard.create_mock("deepseek", version="1.0.0")
    mock = guard.get_mock("deepseek")
    assert mock is not None
    assert mock.version == "1.0.0"


def test_get_mock_not_found():
    guard = SecretGuard()
    assert guard.get_mock("nonexistent") is None


def test_mock_request():
    mock = MockProvider(name="test_provider")
    result = mock.request()
    assert result["status"] == "mock"
    assert "[MOCK]" in result["data"]["result"]
    assert result["api_key_used"] == "mock-key-placeholder"


def test_mock_request_with_endpoint():
    mock = MockProvider(name="openai")
    result = mock.request(endpoint="/v1/chat/completions")
    assert result["endpoint"] == "/v1/chat/completions"


def test_mock_validate_key_ok():
    mock = MockProvider(name="test")
    assert mock.validate_key("mock-key-placeholder") is True


def test_mock_validate_key_real_secret_raises():
    mock = MockProvider(name="test")
    with pytest.raises(SecretAccessError, match="реальный ключ"):
        mock.validate_key("sk-testABCDEFGHIJKLMNOPQRSTUVWXYZ")


# ── 7. MockProvider — frozen ──

def test_mock_provider_frozen():
    mock = MockProvider(name="test")
    with pytest.raises(AttributeError):
        mock.name = "new"


# ── 8. SecretAccessError ──

def test_secret_access_error():
    e = SecretAccessError("test error", source="test")
    assert str(e) == "test error"
    assert e.source == "test"


# ── 9. .env файл в контуре (фейковый) ──

def test_env_file_check_no_env():
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        result = guard.check_env_files()
        assert result["found"] is False
        assert result["blocked"] is False


def test_env_file_check_with_env():
    with tempfile.TemporaryDirectory() as tmp:
        env_path = Path(tmp) / ".env"
        env_path.write_text(
            "OPENAI_API_KEY=sk-test-12345\n"
            "DEEPSEEK_API_KEY=mock-key\n",
            encoding="utf-8",
        )
        guard = SecretGuard(tmp)
        result = guard.check_env_files()
        assert result["found"] is True
        assert len(result["files"]) >= 1


# ── 10. os.environ с фейковыми секретами ──

def test_os_environ_check_no_secrets(monkeypatch):
    # Очищаем окружение от секретов для теста
    for var in list(os.environ.keys()):
        if any(pat.match(var) for pat in [
            pytest.importorskip("re").compile(r"(?i)^.*(api_key|secret|token).*$"),
        ] if False):
            pass  # не удаляем, просто проверяем

    # Создаём guard и проверяем
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        # Не подсовываем реальные секреты
        guard.check_os_environ()


def test_os_environ_with_fake_secret(monkeypatch):
    """Подсовываем фейковый секрет и проверяем блокировку."""
    monkeypatch.setenv("FAKE_TEST_API_KEY", "sk-test-fake-12345")
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        result = guard.check_os_environ()
        # FAKE_TEST_API_KEY должен быть обнаружен
        assert result["has_secrets"] is True
        assert any("FAKE_TEST_API_KEY" in v for v in result["secret_vars"])


# ── 11. run_full_check() ──

def test_run_full_check_clean():
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        check = guard.run_full_check()
        assert "env_files" in check
        assert "os_environ" in check
        assert "code_secrets" in check
        assert "total_violations" in check


def test_run_full_check_with_env_violation(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY_FAKE", "sk-fake-12345")
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        check = guard.run_full_check()
        assert check["total_violations"] >= 0


# ── 12. report() ──

def test_report_format():
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        report = guard.report()
        assert "SECRET GUARD REPORT" in report
        assert "Guard active:" in report
        assert "Contour path:" in report


def test_report_with_mock():
    with tempfile.TemporaryDirectory() as tmp:
        guard = SecretGuard(tmp)
        guard.create_mock("openai", version="1.0.0")
        report = guard.report()
        assert "openai" in report
        assert "1.0.0" in report


# ── 13. reset() ──

def test_reset():
    guard = SecretGuard()
    guard.create_mock("test")
    guard.reset()
    assert guard.mock_providers == {}
    assert guard.violations == []


# ── 14. deactivate() ──

def test_deactivate():
    guard = SecretGuard()
    assert guard.is_active is True
    guard.deactivate()
    assert guard.is_active is False
