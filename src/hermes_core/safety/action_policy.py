from __future__ import annotations

from dataclasses import dataclass

from hermes_core.types import ActionDecision


@dataclass(frozen=True)
class ActionPolicy:
    decision: ActionDecision
    reason: str


SAFE_ACTIONS = {
    "answer_text",
    "create_local_report",
    "update_local_state",
    "dry_run",
    "local_test",
}

CONFIRM_REQUIRED_ACTIONS = {
    "read_external_folder",
    "read_old_archive",
    "read_google_drive_document",
    "run_external_api",
    "work_with_tokens",
    "connect_telegram",
}

BLOCKED_ACTIONS = {
    "delete",
    "modify_old_project",
    "modify_real_order",
    "telegram_live",
    "drive_move_without_approval",
    "read_secret",
    "change_permissions",
    "send_external_file",
}


def classify_action(action_type: str, approved: bool = False) -> ActionPolicy:
    normalized = action_type.strip().lower()
    if normalized in SAFE_ACTIONS:
        return ActionPolicy(ActionDecision.SAFE, "Safe local or dry-run action.")
    if normalized in CONFIRM_REQUIRED_ACTIONS:
        if approved:
            return ActionPolicy(ActionDecision.SAFE, "User approval was provided.")
        return ActionPolicy(ActionDecision.CONFIRM_REQUIRED, "Explicit user approval required.")
    if normalized in BLOCKED_ACTIONS:
        if approved and normalized in {"drive_move_without_approval"}:
            return ActionPolicy(ActionDecision.SAFE, "Drive move approved for explicit target list.")
        return ActionPolicy(ActionDecision.BLOCKED, "Action is blocked by Hermes-Clean policy.")
    return ActionPolicy(ActionDecision.CONFIRM_REQUIRED, "Unknown action needs review.")
