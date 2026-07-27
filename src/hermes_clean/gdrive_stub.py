"""Google Drive Stub — жёсткая блокировка облачной интеграции.

Гарантирует:
- Любая попытка чтения/записи → 403 appNotAuthorizedToFile
- Запрет на повторные попытки (Freeze) после первого обращения
- Альтернативные ручные варианты (manual instructions)
- Автоматическая регистрация в pending approvals (MemorySync)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .memory_sync import MemorySync


# ── Исключение ────────────────────────────────────────────────

class GDriveForbiddenError(Exception):
    """Возбуждается при любой попытке доступа к Google Drive.

    Симулирует HTTP 403 appNotAuthorizedToFile.
    """

    FORBIDDEN_CODE = "appNotAuthorizedToFile"
    FORBIDDEN_HTTP = 403

    def __init__(self, operation: str, path: str = ""):
        message = (
            f"[{self.FORBIDDEN_HTTP} {self.FORBIDDEN_CODE}] "
            f"Операция '{operation}' запрещена для файла '{path or '?'}'. "
            f"Google Drive интеграция заблокирована в изолированном контуре."
        )
        super().__init__(message)
        self.operation = operation
        self.path = path


# ── Состояние блокировки сессии ───────────────────────────────

@dataclass
class FreezeState:
    """Состояние блокировки Google Drive для текущей сессии."""

    frozen: bool = False
    first_attempt_at: datetime | None = None
    first_operation: str = ""
    attempts_count: int = 0
    last_error: str = ""


# ── Manual alternative instructions ────────────────────────────

MANUAL_INSTRUCTIONS = """### Ручное размещение файлов вместо Google Drive

Google Drive интеграция ЗАБЛОКИРОВАНА в изолированном контуре Hermes-Clean.

Для передачи файлов используйте локальную папку:

  1. Поместите файлы в папку:
     C:\\Users\\user\\Desktop\\Hermes-Clean\\gdrive_manual\\

  2. Убедитесь, что файлы имеют расширения:
     - .xlsx — таблицы экспорта
     - .pdf — заказы/документы
     - .json — структурированные данные
     - .txt — текстовые заметки

  3. После размещения файлов запустите:
     from hermes_clean.gdrive_stub import GDriveStub
     stub = GDriveStub()
     stub.check_manual_files()  # проверит наличие файлов

  4. Для разблокировки Google Drive (НЕ РЕКОМЕНДУЕТСЯ):
     - Требуется approval администратора
     - Изменение статуса в MemorySync
     - Отключение защит: SecretGuard, SafetyViolation
"""


# ── GDrive Stub ───────────────────────────────────────────────

class GDriveStub:
    """Заглушка Google Drive — все операции блокируются.

    Использование:
        stub = GDriveStub()
        try:
            stub.read_file("/some/file.txt")
        except GDriveForbiddenError as e:
            print(e)  # 403 appNotAuthorizedToFile

        stub.freeze()  # заморозка сессии
        stub.read_file("/another/file.txt")  # FreezeError
    """

    def __init__(self):
        self._freeze = FreezeState()
        self._manual_path = None

    # ── Свойства ──

    @property
    def is_frozen(self) -> bool:
        """True после первой же попытки обращения к GDrive."""
        return self._freeze.frozen

    @property
    def freeze_state(self) -> FreezeState:
        return self._freeze

    @property
    def manual_path(self) -> str | None:
        return str(self._manual_path) if self._manual_path else None

    # ── Внутренняя проверка freeze ──

    def _check_freeze(self, operation: str, path: str = "") -> None:
        """Проверить freeze перед операцией. Если заморожено — исключение."""
        if self._freeze.frozen:
            raise RuntimeError(
                f"❄️ Google Drive сессия ЗАМОРОЖЕНА после "
                f"первой попытки '{self._freeze.first_operation}' "
                f"в {self._freeze.first_attempt_at}. "
                f"Повторные запросы заблокированы до сброса сессии."
            )

    def _record_attempt(self, operation: str, path: str = "") -> None:
        """Записать попытку обращения и заморозить сессию."""
        now = datetime.now(timezone.utc)
        self._freeze.attempts_count += 1
        self._freeze.first_attempt_at = now
        self._freeze.first_operation = f"{operation}({path or '?'})"
        self._freeze.last_error = (
            f"[403 appNotAuthorizedToFile] {operation} на {path or '?'}"
        )
        self._freeze.frozen = True

    # ── Операции с Google Drive (все блокируются) ──

    def read_file(self, path: str) -> bytes:
        """Прочитать файл с Google Drive. Всегда → 403."""
        self._check_freeze("read_file", path)
        self._record_attempt("read_file", path)
        raise GDriveForbiddenError("read_file", path)

    def write_file(self, path: str, content: bytes | str) -> dict[str, Any]:
        """Записать файл на Google Drive. Всегда → 403."""
        self._check_freeze("write_file", path)
        self._record_attempt("write_file", path)
        raise GDriveForbiddenError("write_file", path)

    def list_files(self, folder: str = "/") -> list[dict[str, Any]]:
        """Список файлов на Google Drive. Всегда → 403."""
        self._check_freeze("list_files", folder)
        self._record_attempt("list_files", folder)
        raise GDriveForbiddenError("list_files", folder)

    def delete_file(self, path: str) -> dict[str, Any]:
        """Удалить файл на Google Drive. Всегда → 403."""
        self._check_freeze("delete_file", path)
        self._record_attempt("delete_file", path)
        raise GDriveForbiddenError("delete_file", path)

    def upload_file(self, path: str, content: bytes | str) -> dict[str, Any]:
        """Загрузить файл на Google Drive. Всегда → 403."""
        self._check_freeze("upload_file", path)
        self._record_attempt("upload_file", path)
        raise GDriveForbiddenError("upload_file", path)

    def sync_folder(self, local_path: str, remote_path: str) -> dict[str, Any]:
        """Синхронизировать папку с Google Drive. Всегда → 403."""
        self._check_freeze("sync_folder", remote_path)
        self._record_attempt("sync_folder", remote_path)
        raise GDriveForbiddenError("sync_folder", remote_path)

    # ── Заморозка вручную ──

    def freeze(self) -> str:
        """Вручную заморозить сессию без вызова операции."""
        if not self._freeze.frozen:
            now = datetime.now(timezone.utc)
            self._freeze.frozen = True
            self._freeze.first_attempt_at = now
            self._freeze.first_operation = "manual_freeze"
            self._freeze.last_error = "Сессия заморожена вручную."
        return "❄️ Google Drive сессия заморожена."

    def unfreeze(self) -> str:
        """Разморозить сессию (только для тестов/администратора)."""
        self._freeze = FreezeState()
        return "✅ Google Drive сессия разморожена."

    # ── Альтернативные ручные варианты ──

    @staticmethod
    def get_manual_instructions() -> str:
        """Вернуть инструкцию по ручному размещению файлов."""
        return MANUAL_INSTRUCTIONS

    def set_manual_path(self, path: str) -> None:
        """Установить локальную папку для ручного размещения."""
        self._manual_path = path

    def check_manual_files(self) -> dict[str, Any]:
        """Проверить наличие файлов в ручной папке.

        Returns:
            dict с found (bool), files (list), instructions (str).
        """
        from pathlib import Path

        if not self._manual_path:
            return {
                "found": False,
                "files": [],
                "error": "Ручная папка не задана. Используйте set_manual_path().",
                "instructions": MANUAL_INSTRUCTIONS,
            }

        base = Path(self._manual_path)
        if not base.exists():
            return {
                "found": False,
                "files": [],
                "error": f"Папка {self._manual_path} не существует.",
                "instructions": MANUAL_INSTRUCTIONS,
            }

        found_files = []
        for ext in ["*.xlsx", "*.pdf", "*.json", "*.txt"]:
            for f in base.glob(ext):
                found_files.append({
                    "name": f.name,
                    "path": str(f),
                    "size": f.stat().st_size,
                })

        return {
            "found": len(found_files) > 0,
            "files": found_files,
            "error": "",
            "instructions": MANUAL_INSTRUCTIONS,
        }

    # ── Регистрация в MemorySync pending approvals ──

    def register_pending_approval(self, memory_sync: MemorySync) -> str:
        """Зарегистрировать запрос на синхронизацию как отложенную задачу."""
        approval = memory_sync.request_approval(
            step_id="gdrive_unblock",
            description=(
                "Запрос на разблокировку Google Drive интеграции. "
                "Требуется ручное подтверждение администратора. "
                "Рекомендуется использовать ручное размещение файлов."
            ),
            subsystem="export",
        )
        return (
            f"📋 Запрос на разблокировку GDrive зарегистрирован: "
            f"'{approval.id}'. "
            f"Требуется approve() от администратора."
        )

    # ── Сброс ──

    def reset(self) -> None:
        """Полный сброс состояния заглушки."""
        self._freeze = FreezeState()
        self._manual_path = None
