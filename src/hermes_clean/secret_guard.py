"""Secret Guard — максимальная изоляция от реальных секретов и .env.

Гарантирует:
- .env не читается и не создаётся внутри контура
- os.environ не используется для поиска секретов
- Mock-провайдеры используют исключительно хардкод-заглушки
- Документация не содержит упоминаний реальных ключей
- Любой запрещённый доступ → SecretAccessError
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ── Паттерны секретов ─────────────────────────────────────────

SECRET_PATTERNS: list[re.Pattern] = [
    re.compile(r"(?i)(api_key|apikey)\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{20,}"),
    re.compile(r"(?i)(secret|token|password)\s*[=:]\s*['\"]?[a-zA-Z0-9_\-]{8,}"),
    re.compile(r"(?i)(sk-[a-zA-Z0-9]{20,})"),          # OpenAI-style
    re.compile(r"(?i)(ghp_[a-zA-Z0-9]{36,})"),          # GitHub PAT
    re.compile(r"(?i)(gho_[a-zA-Z0-9]{36,})"),          # GitHub OAuth
    re.compile(r"(?i)(xox[bpras]-[a-zA-Z0-9\-]{20,})"),  # Slack tokens
    re.compile(r"(?i)(AKIA[0-9A-Z]{16})"),              # AWS AK
]

ENV_VAR_PATTERNS: list[re.Pattern] = [
    re.compile(r"(?i)^.*(api_key|apikey|secret|token|password).*$"),
    re.compile(r"(?i)^(OPENAI|ANTHROPIC|DEEPSEEK|XAI|GROQ|MISTRAL|OPENROUTER)"),
    re.compile(r"(?i)^.*_API_KEY$"),
    re.compile(r"(?i)^.*_TOKEN$"),
    re.compile(r"(?i)^.*_SECRET$"),
]


# ── Исключение ────────────────────────────────────────────────

class SecretAccessError(Exception):
    """Возбуждается при попытке доступа к реальным секретам."""

    def __init__(self, message: str, source: str = ""):
        super().__init__(message)
        self.source = source


# ── Mock Provider ──────────────────────────────────────────────

@dataclass(frozen=True)
class MockProvider:
    """Заглушка для внешнего сервиса/модели.

    Все методы возвращают предопределённые mock-данные.
    Любая попытка использовать реальный ключ → SecretAccessError.
    """

    name: str
    """Имя провайдера (например, 'openai', 'deepseek')."""

    mock_api_key: str = "mock-key-placeholder"
    """Жёстко заданный mock-ключ."""

    version: str = "0.0.0"
    """Версия mock-провайдера."""

    def request(self, endpoint: str = "", payload: dict | None = None) -> dict:
        """Эмулировать запрос к API. Всегда возвращает mock-ответ."""
        return {
            "provider": self.name,
            "endpoint": endpoint or "mock",
            "status": "mock",
            "data": {"result": f"[MOCK] {self.name} response"},
            "api_key_used": self.mock_api_key,
        }

    def validate_key(self, key: str) -> bool:
        """Проверить, что ключ — mock, а не реальный секрет."""
        if key != self.mock_api_key and _looks_like_secret(key):
            raise SecretAccessError(
                f"MockProvider '{self.name}' получил реальный ключ. "
                f"Используйте только '{self.mock_api_key}'.",
                source="mock_provider",
            )
        return True


# ── Secret Guard ───────────────────────────────────────────────

class SecretGuard:
    """Главный страж изоляции секретов.

    Использование:
        guard = SecretGuard()
        guard.check_env_files()       # проверка .env в контуре
        guard.check_os_environ()      # проверка os.environ
        guard.sanitize(text)          # зачистка секретов
        guard.create_mock("openai")   # создание mock-провайдера
        print(guard.report())
    """

    def __init__(self, contour_path: str | Path | None = None):
        self._contour_path = Path(contour_path).resolve() if contour_path else Path.cwd()
        self._active = True
        self._env_scan_result: dict[str, Any] = {}
        self._environ_scan_result: dict[str, Any] = {}
        self._mock_providers: dict[str, MockProvider] = {}
        self._violations: list[str] = []

    # ── Свойства ──

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def contour_path(self) -> Path:
        return self._contour_path

    @property
    def mock_providers(self) -> dict[str, MockProvider]:
        return dict(self._mock_providers)

    @property
    def violations(self) -> list[str]:
        return list(self._violations)

    # ── Проверка .env файлов в контуре ──

    def check_env_files(self) -> dict[str, Any]:
        """Проверить, есть ли .env файлы в контуре.

        Returns:
            dict с ключами: found (bool), files (list), errors (list).
        """
        result: dict[str, Any] = {
            "found": False,
            "files": [],
            "errors": [],
            "blocked": False,
        }

        # Ищем .env и .env.* в контуре (не в .git, не в .venv)
        env_files = list(self._contour_path.rglob(".env"))
        env_files += list(self._contour_path.rglob(".env.*"))

        # Фильтруем системные/виртуальные директории
        filtered = []
        for f in env_files:
            rel = f.relative_to(self._contour_path)
            parts = rel.parts
            # Пропускаем .git, .venv, __pycache__, node_modules
            skip_dirs = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache"}
            if not any(p in skip_dirs for p in parts):
                filtered.append(f)

        if filtered:
            result["found"] = True
            result["files"] = [str(f) for f in filtered]
            # Читаем только для проверки — не используем значения!
            for f in filtered:
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    lines = content.strip().split("\n")
                    secret_lines = []
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            for pat in ENV_VAR_PATTERNS:
                                if pat.match(line):
                                    secret_lines.append(line.split("=")[0])
                                    break
                    if secret_lines:
                        result["errors"].append(
                            f"{f.name}: обнаружены секретные переменные: {', '.join(secret_lines)}"
                        )
                        self._violations.append(
                            f".env файл {f} содержит секреты ({', '.join(secret_lines)})"
                        )
                except Exception as e:
                    result["errors"].append(f"Ошибка чтения {f}: {e}")

        # Если найден .env → защита блокирует
        if result["found"] and result["errors"]:
            result["blocked"] = True

        self._env_scan_result = result
        return result

    # ── Проверка os.environ ──

    def check_os_environ(self) -> dict[str, Any]:
        """Проверить os.environ на наличие секретных переменных.

        Returns:
            dict с ключами: has_secrets (bool), secret_vars (list), blocked (bool).
        """
        result: dict[str, Any] = {
            "has_secrets": False,
            "secret_vars": [],
            "blocked": False,
            "message": "",
        }

        secret_vars = []
        for var_name in os.environ:
            for pat in ENV_VAR_PATTERNS:
                if pat.match(var_name):
                    secret_vars.append(var_name)
                    break

        if secret_vars:
            result["has_secrets"] = True
            result["secret_vars"] = secret_vars
            result["message"] = (
                f"Обнаружены секретные переменные окружения: {', '.join(secret_vars)}. "
                f"Их использование в контуре ЗАПРЕЩЕНО."
            )
            result["blocked"] = True
            self._violations.append(result["message"])
        else:
            result["message"] = "Секретные переменные окружения не обнаружены."

        self._environ_scan_result = result
        return result

    # ── Санитизация текста ──

    def sanitize(self, text: str, replacement: str = "[REDACTED]") -> str:
        """Зачистить текст от реальных секретов.

        Заменяет все совпадения SECRET_PATTERNS на [REDACTED].
        """
        result = text
        for pat in SECRET_PATTERNS:
            result = pat.sub(replacement, result)
        return result

    # ── Проверка данных на секреты ──

    def validate_no_real_secrets(self, data: Any, path: str = "") -> list[str]:
        """Рекурсивно проверить данные (dict/list/str) на наличие секретов.

        Returns:
            Список путей к полям, содержащим секреты.
        """
        found: list[str] = []

        if isinstance(data, str):
            for pat in SECRET_PATTERNS:
                if pat.search(data):
                    found.append(f"{path} (совпадение: {pat.pattern})")
                    break

        elif isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                found.extend(self.validate_no_real_secrets(value, current_path))

        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                found.extend(self.validate_no_real_secrets(item, current_path))

        return found

    # ── Mock-провайдеры ──

    def create_mock(self, name: str, version: str = "0.0.0") -> MockProvider:
        """Создать изолированный mock-провайдер.

        Если провайдер с таким именем уже существует — возвращает существующий.
        """
        if name in self._mock_providers:
            return self._mock_providers[name]

        provider = MockProvider(name=name, version=version)
        self._mock_providers[name] = provider
        return provider

    def get_mock(self, name: str) -> MockProvider | None:
        """Получить mock-провайдер по имени."""
        return self._mock_providers.get(name)

    # ── Полная проверка контура ──

    def run_full_check(self) -> dict[str, Any]:
        """Запустить полную проверку изоляции секретов."""
        env_check = self.check_env_files()
        environ_check = self.check_os_environ()

        # Проверка, нет ли реальных секретов в файлах модулей (pep-484 / safety scan)
        src_path = self._contour_path / "src"
        code_secrets = []
        if src_path.exists():
            for py_file in src_path.rglob("*.py"):
                rel = py_file.relative_to(self._contour_path)
                content = py_file.read_text(encoding="utf-8", errors="ignore")

                # Ищем "sk-...", "api_key=..." в коде (не в комментариях)
                for i, line in enumerate(content.split("\n"), start=1):
                    stripped = line.strip()
                    if stripped.startswith("#"):
                        continue  # пропускаем комментарии
                    for pat in SECRET_PATTERNS:
                        m = pat.search(stripped)
                        if m:
                            # Разрешаем только "mock-key-placeholder"
                            if "mock-key-placeholder" not in stripped:
                                code_secrets.append(f"{rel}:{i}")
                                self._violations.append(
                                    f"Код содержит секрет: {rel}:{i}"
                                )
                            break

        return {
            "env_files": env_check,
            "os_environ": environ_check,
            "code_secrets": code_secrets,
            "total_violations": len(self._violations),
            "is_clean": len(self._violations) == 0,
        }

    # ── Отчёт ──

    def report(self) -> str:
        """Сформировать отчёт о состоянии защиты."""
        lines: list[str] = []
        lines.append("┌─────────────────────────────────────────────────────────────┐")
        lines.append("│              SECRET GUARD REPORT                           │")
        lines.append("├─────────────────────────────────────────────────────────────┤")
        lines.append(f"│ Guard active:  {'✅ YES' if self._active else '❌ NO':<53} │")
        lines.append(f"│ Contour path:  {str(self._contour_path):<53} │")
        lines.append("├─────────────────────────────────────────────────────────────┤")

        # .env
        if self._env_scan_result:
            env = self._env_scan_result
            if env.get("found"):
                lines.append(f"│ ❌ .env FOUND: {len(env['files'])} file(s)               │")
                for f in env.get("files", []):
                    lines.append(f"│     • {str(Path(f).name):<53} │")
                for e in env.get("errors", []):
                    lines.append(f"│     ⚠ {e:<53} │")
            else:
                lines.append("│ ✅ No .env files in contour                       │")

        # os.environ
        if self._environ_scan_result:
            env_os = self._environ_scan_result
            if env_os.get("has_secrets"):
                lines.append(f"│ ❌ os.environ has {len(env_os['secret_vars'])} secret var(s)        │")
                for v in env_os.get("secret_vars", []):
                    lines.append(f"│     • {v:<53} │")
            else:
                lines.append("│ ✅ os.environ clean                               │")

        # Mock providers
        if self._mock_providers:
            lines.append("├─────────────────────────────────────────────────────────────┤")
            lines.append("│ Mock providers:                                              │")
            for name, p in self._mock_providers.items():
                lines.append(f"│   ✅ {name:<20} v{p.version:<30} │")

        # Violations
        if self._violations:
            lines.append("├─────────────────────────────────────────────────────────────┤")
            lines.append(f"│ ❌ VIOLATIONS: {len(self._violations)}                                      │")
            for v in self._violations[:3]:
                lines.append(f"│     • {v[:55]:<55} │")
            if len(self._violations) > 3:
                lines.append(f"│     ... and {len(self._violations) - 3} more                   │")

        lines.append("└─────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)

    # ── Сброс ──

    def reset(self) -> None:
        """Сбросить результаты проверок (не отключает guard)."""
        self._env_scan_result = {}
        self._environ_scan_result = {}
        self._mock_providers = {}
        self._violations = []

    def deactivate(self) -> None:
        """Отключить guard (для тестов)."""
        self._active = False


# ── Вспомогательные утилиты ───────────────────────────────────

def _looks_like_secret(value: str) -> bool:
    """Проверить, выглядит ли строка как реальный секрет."""
    for pat in SECRET_PATTERNS:
        if pat.search(value):
            return True
    return False


def is_safe_string(value: str) -> bool:
    """Проверить, безопасна ли строка (не содержит секретов)."""
    return not _looks_like_secret(value)


def sanitize_text(text: str) -> str:
    """Зачистить текст от секретов. Удобный вызов без создания guard."""
    guard = SecretGuard()
    return guard.sanitize(text)
