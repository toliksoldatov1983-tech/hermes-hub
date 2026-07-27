"""Hermes Clean — изолированный контур безопасных компонентов Малярки.

Без Telegram, без API, без БД, без секретов, без Google Drive.
Только изолированная логика.
"""

from .validation import validate_order_result, validate_single_row
from .fixtures import FIXTURES, get_fixture, list_fixtures
from .dispute_resolver import (
    DisputeResolution,
    DisputeResolver,
    ResolverSummary,
    SUGGESTED_QUESTIONS,
    DISPUTE_ACTIONS,
    get_suggested_question,
)
from .export_gate import ExportBlockedError, build_export_model
from .state_machine import (
    OrderState,
    OrderStateMachine,
    StateTransition,
    StateMachineResult,
    STATE_LABELS,
)
from .preview_generator import (
    PreviewReport,
    generate_preview,
    preview_to_markdown,
    PRICE_PER_M2,
    MATERIAL_COST_PER_M2,
)
from .telegram_flow import (
    TelegramDialogFlow,
    DialogMessage,
    DialogState,
)
from .task_queue import (
    Task,
    TaskQueue,
    TaskRecord,
    TaskStatus,
    AuditViolation,
    create_default_queue,
)
from .memory_sync import (
    MemorySync,
    SafetyViolation,
    Decision,
    Prohibition,
    SafetyRule,
    PendingApproval,
    IntegrityReport,
    Subsystem,
)
from .secret_guard import (
    SecretGuard,
    SecretAccessError,
    MockProvider,
    sanitize_text,
    is_safe_string,
)
from .gdrive_stub import (
    GDriveStub,
    GDriveForbiddenError,
    FreezeState,
    MANUAL_INSTRUCTIONS,
)

__all__ = [
    "validate_order_result", "validate_single_row",
    "FIXTURES", "get_fixture", "list_fixtures",
    "DisputeResolution", "DisputeResolver", "ResolverSummary",
    "SUGGESTED_QUESTIONS", "DISPUTE_ACTIONS", "get_suggested_question",
    "ExportBlockedError", "build_export_model",
    "OrderState", "OrderStateMachine", "StateTransition", "StateMachineResult", "STATE_LABELS",
    "PreviewReport", "generate_preview", "preview_to_markdown", "PRICE_PER_M2", "MATERIAL_COST_PER_M2",
    "TelegramDialogFlow", "DialogMessage", "DialogState",
    "Task", "TaskQueue", "TaskRecord", "TaskStatus", "AuditViolation", "create_default_queue",
    "MemorySync", "SafetyViolation", "Decision", "Prohibition", "SafetyRule", "PendingApproval", "IntegrityReport", "Subsystem",
    "SecretGuard", "SecretAccessError", "MockProvider", "sanitize_text", "is_safe_string",
    "GDriveStub", "GDriveForbiddenError", "FreezeState", "MANUAL_INSTRUCTIONS",
]
