"""Local fake Hermes adapter for dry-run contract tests only.

This module is intentionally isolated from the live Telegram bot. It accepts
plain dictionaries and returns plain dictionaries. It performs no I/O.
"""

from typing import Any


ALLOWED_ACTIONS = {
    "answer_text",
    "suggest_mode",
    "explain_status",
    "prepare_engineer_task_draft",
    "summarize_project_state",
    "explain_order_result",
    "suggest_next_safe_step",
}

FORBIDDEN_ACTIONS = {
    "send_telegram_message",
    "create_file",
    "edit_file",
    "delete_file",
    "change_price",
    "change_rules",
    "change_database",
    "run_polling",
    "restart_bot",
    "read_token",
    "read_env",
    "call_api",
    "process_real_order_files",
}

REQUIRED_REQUEST_FIELDS = ("action", "payload", "dry_run", "feature_flags")

RESPONSE_FIELDS = (
    "ok",
    "status",
    "action",
    "dry_run",
    "blocked",
    "fallback_required",
    "reason",
    "diagnostics_safe",
    "side_effects",
    "output_type",
)

SENSITIVE_DIAGNOSTIC_MARKERS = (
    "token",
    ".env",
    "environment",
    "api_key",
    "password",
    "private_key",
    "secret",
    "orders.db",
    "database",
    "real_order",
    "polling",
    "restart",
    "config.py",
    "/opt/malyarka-telegram-bot",
    "/var/log",
    "live.log",
)


def build_fake_adapter_response(request: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic dry-run response for contract tests."""
    if not isinstance(request, dict):
        return _fallback_response(
            action="invalid_request",
            dry_run=True,
            reason="malformed_request",
            diagnostics_safe=True,
        )

    dry_run = request.get("dry_run") if isinstance(request.get("dry_run"), bool) else True

    missing_fields = [field for field in REQUIRED_REQUEST_FIELDS if field not in request]
    if missing_fields:
        return _fallback_response(
            action=_safe_action_name(request.get("action")),
            dry_run=dry_run,
            reason="missing_required_fields: " + ", ".join(missing_fields),
            diagnostics_safe=True,
        )

    action = request["action"]
    payload = request["payload"]
    feature_flags = request["feature_flags"]
    diagnostics = request.get("diagnostics", False)

    type_errors = []
    if not isinstance(action, str):
        type_errors.append("action")
    if not isinstance(payload, dict):
        type_errors.append("payload")
    if not isinstance(request["dry_run"], bool):
        type_errors.append("dry_run")
    if not isinstance(feature_flags, dict):
        type_errors.append("feature_flags")
    if "diagnostics" in request and not isinstance(diagnostics, bool):
        type_errors.append("diagnostics")
    if type_errors:
        return _fallback_response(
            action=_safe_action_name(action),
            dry_run=dry_run,
            reason="wrong_field_types: " + ", ".join(type_errors),
            diagnostics_safe=True,
        )

    if payload.get("fallback_required") is True:
        return _fallback_response(
            action=action,
            dry_run=dry_run,
            reason="fallback_required_by_request",
            diagnostics_safe=True,
        )

    if diagnostics and _contains_sensitive_diagnostics(payload):
        return _unsafe_response(
            action=action,
            dry_run=dry_run,
            reason="unsafe_diagnostics_blocked",
        )

    if feature_flags.get("HERMES_ADAPTER_ENABLED") is not True:
        return _fallback_response(
            action=action,
            dry_run=dry_run,
            reason="adapter_disabled_by_default",
            diagnostics_safe=True,
        )

    if action in FORBIDDEN_ACTIONS:
        return _blocked_response(
            action=action,
            dry_run=dry_run,
            reason="forbidden_action: " + action,
            diagnostics_safe=True,
        )

    if action not in ALLOWED_ACTIONS:
        return _blocked_response(
            action=action,
            dry_run=dry_run,
            reason="unknown_action: " + action,
            diagnostics_safe=True,
        )

    return {
        "ok": True,
        "status": "ok",
        "action": action,
        "dry_run": dry_run,
        "blocked": False,
        "fallback_required": False,
        "reason": "allowed_dry_run_action",
        "diagnostics_safe": True,
        "side_effects": [],
        "output_type": "valid_output",
    }


def validate_fake_adapter_response(
    response: Any,
    *,
    fallback_action: str = "invalid_output",
    dry_run: bool = True,
) -> dict[str, Any]:
    """Convert malformed or unsafe fake outputs to a safe fallback response."""
    if not isinstance(response, dict):
        return _fallback_response(
            action=fallback_action,
            dry_run=dry_run,
            reason="malformed_output_not_dict",
            diagnostics_safe=True,
        )

    missing_fields = [field for field in RESPONSE_FIELDS if field not in response]
    if missing_fields:
        return _fallback_response(
            action=_safe_action_name(response.get("action", fallback_action)),
            dry_run=response.get("dry_run") if isinstance(response.get("dry_run"), bool) else dry_run,
            reason="malformed_output_missing_fields: " + ", ".join(missing_fields),
            diagnostics_safe=True,
        )

    if response.get("side_effects") != []:
        return _fallback_response(
            action=_safe_action_name(response.get("action", fallback_action)),
            dry_run=response.get("dry_run") if isinstance(response.get("dry_run"), bool) else dry_run,
            reason="unsafe_output_side_effects_blocked",
            diagnostics_safe=True,
        )

    if _contains_sensitive_diagnostics(response.get("diagnostics")):
        return _unsafe_response(
            action=_safe_action_name(response.get("action", fallback_action)),
            dry_run=response.get("dry_run") if isinstance(response.get("dry_run"), bool) else dry_run,
            reason="unsafe_output_diagnostics_blocked",
        )

    return response


def _fallback_response(
    *,
    action: str,
    dry_run: bool,
    reason: str,
    diagnostics_safe: bool,
) -> dict[str, Any]:
    return {
        "ok": False,
        "status": "fallback_required",
        "action": action,
        "dry_run": dry_run,
        "blocked": True,
        "fallback_required": True,
        "reason": reason,
        "diagnostics_safe": diagnostics_safe,
        "side_effects": [],
        "output_type": "fallback_output",
    }


def _blocked_response(
    *,
    action: str,
    dry_run: bool,
    reason: str,
    diagnostics_safe: bool,
) -> dict[str, Any]:
    return {
        "ok": False,
        "status": "blocked",
        "action": action,
        "dry_run": dry_run,
        "blocked": True,
        "fallback_required": True,
        "reason": reason,
        "diagnostics_safe": diagnostics_safe,
        "side_effects": [],
        "output_type": "blocked_output",
    }


def _unsafe_response(*, action: str, dry_run: bool, reason: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": "blocked",
        "action": action,
        "dry_run": dry_run,
        "blocked": True,
        "fallback_required": True,
        "reason": reason,
        "diagnostics_safe": False,
        "side_effects": [],
        "output_type": "unsafe_output",
    }


def _safe_action_name(value: Any) -> str:
    return value if isinstance(value, str) and value else "invalid_request"


def _contains_sensitive_diagnostics(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in SENSITIVE_DIAGNOSTIC_MARKERS)
    if isinstance(value, dict):
        return any(
            _contains_sensitive_diagnostics(key) or _contains_sensitive_diagnostics(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple, set)):
        return any(_contains_sensitive_diagnostics(item) for item in value)
    return False
