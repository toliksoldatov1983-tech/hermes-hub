"""
Server Adapter Skeleton — local sandbox implementation.

BUNDLE_271_300: Local implementation of the Hermes server adapter skeleton.
This is a local test-double that models the future server adapter contract.

RULES:
- off by default (HERMES_ADAPTER_ENABLED=false)
- dry-run only (dry_run=true required)
- safe mode required (safe_mode=true)
- side_effects=[] (always)
- no direct Telegram send
- no server/live/secrets/real orders
- fallback to current flow when disabled/blocked/unsafe
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SAFE_DEFAULT_FEATURE_FLAGS: Dict[str, bool] = {
    "HERMES_ADAPTER_ENABLED": False,
    "HERMES_SERVER_ADAPTER_ENABLED": False,
    "HERMES_TELEGRAM_INSERTION_ENABLED": False,
    "HERMES_SAFE_MODE": True,
    "HERMES_DRY_RUN_ONLY": True,
    "HERMES_EXPORT_CALLBACKS_ENABLED": False,
    "HERMES_ADMIN_CHANGES_ENABLED": False,
    "HERMES_ENGINEER_MODE_ENABLED": False,
    "HERMES_ASSISTANT_MODE_ENABLED": False,
}

ALLOWED_ACTIONS: List[str] = [
    "answer_text",
    "explain_status",
    "suggest_next_safe_step",
    "diagnostics",
    "fallback",
]

BLOCKED_ACTIONS: List[str] = [
    "send_telegram_message",
    "create_file",
    "edit_file",
    "delete_file",
    "change_database",
    "change_price",
    "change_rules",
    "run_polling",
    "restart_bot",
    "read_token",
    "read_env",
    "read_config",
    "call_api",
    "process_real_order_files",
]

REQUIRED_REQUEST_FIELDS: List[str] = [
    "action",
    "payload",
    "dry_run",
    "feature_flags",
    "safe_mode",
    "diagnostics",
]

RESPONSE_FIELDS: List[str] = [
    "ok",
    "status",
    "action",
    "dry_run",
    "blocked",
    "fallback_required",
    "reason",
    "output_type",
    "side_effects",
    "diagnostics_safe",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_feature_flags(raw_flags: Optional[Dict[str, Any]]) -> Dict[str, bool]:
    """Merge user flags with safe defaults. Unknown flags are ignored."""
    if not isinstance(raw_flags, dict):
        return dict(SAFE_DEFAULT_FEATURE_FLAGS)

    merged: Dict[str, bool] = dict(SAFE_DEFAULT_FEATURE_FLAGS)
    for key, value in raw_flags.items():
        if key in SAFE_DEFAULT_FEATURE_FLAGS:
            merged[key] = bool(value)
        # unknown flags are silently ignored (do not enable behaviour)
    return merged


def _make_response(
    *,
    ok: bool,
    status: str,
    action: str,
    dry_run: bool,
    blocked: bool,
    fallback_required: bool,
    reason: str,
    output_type: str,
    diagnostics_safe: bool = True,
) -> Dict[str, Any]:
    """Build a standard structured response. side_effects is always []."""
    return {
        "ok": ok,
        "status": status,
        "action": action,
        "dry_run": dry_run,
        "blocked": blocked,
        "fallback_required": fallback_required,
        "reason": reason,
        "output_type": output_type,
        "side_effects": [],  # invariant
        "diagnostics_safe": diagnostics_safe,
    }


def _validate_request_fields(request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return a blocked response if required fields are missing or wrong type."""
    if not isinstance(request, dict):
        return _make_response(
            ok=False,
            status="malformed",
            action="malformed",
            dry_run=True,
            blocked=True,
            fallback_required=True,
            reason="request is not a dict",
            output_type="malformed",
        )

    for field in REQUIRED_REQUEST_FIELDS:
        if field not in request:
            return _make_response(
                ok=False,
                status="malformed",
                action="malformed",
                dry_run=request.get("dry_run", True),
                blocked=True,
                fallback_required=True,
                reason=f"required field missing: {field}",
                output_type="malformed",
            )

    if not isinstance(request.get("action"), str):
        return _make_response(
            ok=False,
            status="malformed",
            action="malformed",
            dry_run=request.get("dry_run", True),
            blocked=True,
            fallback_required=True,
            reason="action must be a string",
            output_type="malformed",
        )

    if not isinstance(request.get("payload"), dict):
        return _make_response(
            ok=False,
            status="malformed",
            action="malformed",
            dry_run=request.get("dry_run", True),
            blocked=True,
            fallback_required=True,
            reason="payload must be a dict",
            output_type="malformed",
        )

    return None  # valid


# ---------------------------------------------------------------------------
# Main adapter function
# ---------------------------------------------------------------------------


def process_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Process a request through the server adapter skeleton.

    This is the main entry point. It validates the request, checks feature
    flags, and returns a structured response.

    NEVER sends Telegram messages, writes files, reads secrets, or produces
    side effects. Always returns side_effects=[].
    """
    # 0. Validate request structure
    validation_error = _validate_request_fields(request)
    if validation_error is not None:
        return validation_error

    action: str = request["action"]  # type: ignore[assignment]
    dry_run: bool = bool(request.get("dry_run", True))
    safe_mode: bool = bool(request.get("safe_mode", True))
    diagnostics: bool = bool(request.get("diagnostics", False))

    # 1. Normalize feature flags to safe defaults
    flags = _normalize_feature_flags(request.get("feature_flags"))

    # 2. Check adapter enabled
    if not flags.get("HERMES_ADAPTER_ENABLED", False):
        return _make_response(
            ok=False,
            status="disabled",
            action="fallback",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="adapter disabled by feature flag",
            output_type="fallback",
        )

    # 3. Check safe_mode
    if not safe_mode:
        return _make_response(
            ok=False,
            status="blocked",
            action="blocked",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="safe mode must be true",
            output_type="blocked",
        )

    # 4. Check dry_run
    if not dry_run:
        return _make_response(
            ok=False,
            status="blocked",
            action="blocked",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="dry-run must be true",
            output_type="blocked",
        )

    # 5. Check action-specific feature flag blocks (before generic BLOCKED_ACTIONS)
    # write actions
    if action in ("edit_file", "write_file", "delete_file", "create_file"):
        return _make_response(
            ok=False,
            status="blocked",
            action="blocked",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="write action forbidden",
            output_type="blocked",
        )

    # export callbacks
    if action == "create_export" and not flags.get(
        "HERMES_EXPORT_CALLBACKS_ENABLED", False
    ):
        return _make_response(
            ok=False,
            status="blocked",
            action="blocked",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="export action blocked by feature flags",
            output_type="blocked",
        )

    # admin changes
    if action == "admin_change" and not flags.get(
        "HERMES_ADMIN_CHANGES_ENABLED", False
    ):
        return _make_response(
            ok=False,
            status="blocked",
            action="blocked",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="admin changes disabled",
            output_type="blocked",
        )

    # 6. Check for explicitly blocked actions
    if action in BLOCKED_ACTIONS:
        return _make_response(
            ok=False,
            status="blocked",
            action="blocked",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason=f"action blocked: {action}",
            output_type="blocked",
        )

    # 7. Check if action is explicitly allowed
    if action not in ALLOWED_ACTIONS:
        return _make_response(
            ok=False,
            status="blocked",
            action="blocked",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="unknown action blocked",
            output_type="blocked",
        )

    # 8. Explicit fallback request
    if action == "fallback":
        return _make_response(
            ok=False,
            status="fallback",
            action="fallback",
            dry_run=dry_run,
            blocked=True,
            fallback_required=True,
            reason="fallback requested",
            output_type="fallback",
        )

    # 9. Safe diagnostics
    if action == "diagnostics":
        if diagnostics:
            return _make_response(
                ok=True,
                status="dry_run",
                action="diagnostics",
                dry_run=dry_run,
                blocked=False,
                fallback_required=False,
                reason="safe diagnostics only",
                output_type="diagnostics",
            )
        else:
            return _make_response(
                ok=True,
                status="dry_run",
                action="diagnostics",
                dry_run=dry_run,
                blocked=False,
                fallback_required=False,
                reason="safe diagnostics only",
                output_type="diagnostics",
            )

    # 10. Allowed safe dry-run action
    return _make_response(
        ok=True,
        status="dry_run",
        action=action,
        dry_run=dry_run,
        blocked=False,
        fallback_required=False,
        reason="safe dry-run action allowed",
        output_type="draft",
    )
