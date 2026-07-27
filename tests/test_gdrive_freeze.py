"""Tests для GDrive Stub — заморозка Google Drive и 403.

Проверяет:
- GDriveForbiddenError с кодом 403 appNotAuthorizedToFile
- read_file / write_file / list_files / delete_file / upload_file / sync_folder
- Freeze — после первого обращения все операции блокируются
- Ручная freeze / unfreeze
- get_manual_instructions() — текст инструкции
- set_manual_path / check_manual_files
- register_pending_approval() — интеграция с MemorySync
- reset()
"""

import os
import tempfile
from pathlib import Path

import pytest

from hermes_clean import (
    GDriveStub,
    GDriveForbiddenError,
    FreezeState,
    MANUAL_INSTRUCTIONS,
    MemorySync,
)


# ── 1. GDriveForbiddenError ──

def test_forbidden_error_code():
    e = GDriveForbiddenError("read_file", "/test.txt")
    assert "403" in str(e)
    assert "appNotAuthorizedToFile" in str(e)
    assert "read_file" in str(e)
    assert e.operation == "read_file"
    assert e.path == "/test.txt"


def test_forbidden_error_constants():
    assert GDriveForbiddenError.FORBIDDEN_CODE == "appNotAuthorizedToFile"
    assert GDriveForbiddenError.FORBIDDEN_HTTP == 403


# ── 2. Все операции → 403 ──

def test_read_file_raises_403():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError, match="403"):
        stub.read_file("/test.txt")


def test_write_file_raises_403():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError, match="403"):
        stub.write_file("/test.txt", b"data")


def test_list_files_raises_403():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError, match="403"):
        stub.list_files("/")


def test_delete_file_raises_403():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError, match="403"):
        stub.delete_file("/test.txt")


def test_upload_file_raises_403():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError, match="403"):
        stub.upload_file("/test.txt", b"data")


def test_sync_folder_raises_403():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError, match="403"):
        stub.sync_folder("/local", "/remote")


# ── 3. Freeze — запрет повторных попыток ──

def test_freeze_after_first_attempt():
    stub = GDriveStub()
    assert stub.is_frozen is False

    with pytest.raises(GDriveForbiddenError):
        stub.read_file("/test.txt")

    assert stub.is_frozen is True


def test_frozen_block_second_attempt():
    stub = GDriveStub()

    with pytest.raises(GDriveForbiddenError):
        stub.read_file("/test.txt")

    # Вторая попытка — freeze вместо 403
    with pytest.raises(RuntimeError, match="ЗАМОРОЖЕНА"):
        stub.read_file("/another.txt")


def test_frozen_block_any_operation():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError):
        stub.read_file("/a.txt")  # первая — 403, freeze сработал

    assert stub.is_frozen is True

    with pytest.raises(RuntimeError, match="ЗАМОРОЖЕНА"):
        stub.write_file("/b.txt", b"test")

    with pytest.raises(RuntimeError, match="ЗАМОРОЖЕНА"):
        stub.list_files("/")

    with pytest.raises(RuntimeError, match="ЗАМОРОЖЕНА"):
        stub.delete_file("/c.txt")

    with pytest.raises(RuntimeError, match="ЗАМОРОЖЕНА"):
        stub.upload_file("/d.txt", b"test")

    with pytest.raises(RuntimeError, match="ЗАМОРОЖЕНА"):
        stub.sync_folder("/local", "/remote")


def test_freeze_state_tracks_attempt():
    stub = GDriveStub()
    try:
        stub.read_file("/test.txt")
    except GDriveForbiddenError:
        pass

    assert stub.freeze_state.attempts_count == 1
    assert stub.freeze_state.first_operation == "read_file(/test.txt)"
    assert stub.freeze_state.first_attempt_at is not None
    assert stub.freeze_state.last_error != ""


# ── 4. Ручная freeze / unfreeze ──

def test_manual_freeze():
    stub = GDriveStub()
    msg = stub.freeze()
    assert "заморожена" in msg
    assert stub.is_frozen is True


def test_frozen_then_unfreeze():
    stub = GDriveStub()
    stub.freeze()
    assert stub.is_frozen is True

    stub.unfreeze()
    assert stub.is_frozen is False

    # После unfreeze можно снова получить 403
    with pytest.raises(GDriveForbiddenError):
        stub.read_file("/test.txt")


# ── 5. MANUAL_INSTRUCTIONS ──

def test_manual_instructions_content():
    instructions = GDriveStub.get_manual_instructions()
    assert "Google Drive" in instructions
    assert "ЗАБЛОКИРОВАНА" in instructions
    assert "Hermes-Clean" in instructions
    assert "gdrive_manual" in instructions
    assert ".xlsx" in instructions
    assert ".pdf" in instructions


def test_manual_instructions_constant():
    assert isinstance(MANUAL_INSTRUCTIONS, str)
    assert len(MANUAL_INSTRUCTIONS) > 200


# ── 6. set_manual_path / check_manual_files ──

def test_check_manual_files_no_path():
    stub = GDriveStub()
    result = stub.check_manual_files()
    assert result["found"] is False
    assert "не задана" in result["error"]


def test_check_manual_files_nonexistent():
    stub = GDriveStub()
    stub.set_manual_path("/nonexistent/path")
    result = stub.check_manual_files()
    assert result["found"] is False
    assert "не существует" in result["error"]


def test_check_manual_files_with_files():
    with tempfile.TemporaryDirectory() as tmp:
        # Создаём фейковый файл
        (Path(tmp) / "export.xlsx").write_text("test")
        (Path(tmp) / "order.json").write_text('{"key": "value"}')

        stub = GDriveStub()
        stub.set_manual_path(tmp)
        result = stub.check_manual_files()
        assert result["found"] is True
        assert len(result["files"]) == 2


# ── 7. register_pending_approval ──

def test_register_pending_approval():
    ms = MemorySync()
    stub = GDriveStub()

    msg = stub.register_pending_approval(ms)
    assert "зарегистрирован" in msg
    assert "gdrive_unblock" in msg

    # Проверяем что approval появился в MemorySync
    assert len(ms.pending_approvals) == 1
    assert ms.pending_approvals[0].id == "gdrive_unblock"

    # Approve
    ms.approve("gdrive_unblock")
    assert len(ms.pending_approvals) == 0


def test_register_pending_approval_description():
    ms = MemorySync()
    stub = GDriveStub()
    stub.register_pending_approval(ms)
    a = ms.all_approvals[0]
    assert "Google Drive" in a.description
    assert "ручное подтверждение" in a.description


# ── 8. reset() ──

def test_reset():
    stub = GDriveStub()
    with pytest.raises(GDriveForbiddenError):
        stub.read_file("/test.txt")  # freeze

    assert stub.is_frozen is True
    stub.set_manual_path("/some/path")
    assert stub.manual_path is not None

    stub.reset()
    assert stub.is_frozen is False
    assert stub.manual_path is None

    # После reset можно снова получить 403
    with pytest.raises(GDriveForbiddenError):
        stub.read_file("/test.txt")


# ── 9. FreezeState dataclass ──

def test_freeze_state_defaults():
    fs = FreezeState()
    assert fs.frozen is False
    assert fs.first_attempt_at is None
    assert fs.first_operation == ""
    assert fs.attempts_count == 0
    assert fs.last_error == ""
