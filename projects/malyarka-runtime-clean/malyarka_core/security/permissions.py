"""Role-based permission rules for the Malyarka core.

This module is intentionally independent from Telegram, OpenAI, Vision, and
SQLite. It describes default permissions only; actions that require explicit
confirmation remain marked even when the role is allowed to perform them.
"""

from copy import deepcopy

ROLE_OWNER = "owner"
ROLE_MANAGER = "manager"
ROLE_OPERATOR = "operator"
ROLE_PAINTER = "painter"
ROLE_VIEWER = "viewer"
ROLE_AGENT = "agent"

ROLES = (
    ROLE_OWNER,
    ROLE_MANAGER,
    ROLE_OPERATOR,
    ROLE_PAINTER,
    ROLE_VIEWER,
    ROLE_AGENT,
)

ACTION_CREATE_ORDER = "create_order"
ACTION_UPDATE_ORDER = "update_order"
ACTION_ADD_ORDER_ITEM = "add_order_item"
ACTION_SOFT_DELETE_ORDER_ITEM = "soft_delete_order_item"
ACTION_RESOLVE_DISPUTED_ITEM = "resolve_disputed_item"
ACTION_FINALIZE_ORDER = "finalize_order"
ACTION_EXPORT_COREL = "export_corel"
ACTION_EXPORT_MALYARKA = "export_malyarka"
ACTION_ARCHIVE_ORDER = "archive_order"
ACTION_REGISTER_ORDER_FILE = "register_order_file"
ACTION_MARK_ORDER_FILE_OBSOLETE = "mark_order_file_obsolete"
ACTION_ADD_MATERIAL = "add_material"
ACTION_ADD_COLOR = "add_color"
ACTION_ADD_COATING = "add_coating"
ACTION_ADD_MILLING_TYPE = "add_milling_type"
ACTION_ADD_PRICE = "add_price"
ACTION_SET_SETTING = "set_setting"
ACTION_ADD_COMMAND_ALIAS = "add_command_alias"
ACTION_RUN_TESTS = "run_tests"
ACTION_VIEW_ORDER = "view_order"
ACTION_VIEW_ARCHIVE = "view_archive"
ACTION_COMMIT_CODE = "commit_code"
ACTION_PUSH_CODE = "push_code"
ACTION_ACCESS_ENV = "access_env"
ACTION_ACCESS_ORDERS_DB = "access_orders_db"
ACTION_ACCESS_CUSTOMER_PRIVATE_DATA = "access_customer_private_data"

ACTIONS = (
    ACTION_CREATE_ORDER,
    ACTION_UPDATE_ORDER,
    ACTION_ADD_ORDER_ITEM,
    ACTION_SOFT_DELETE_ORDER_ITEM,
    ACTION_RESOLVE_DISPUTED_ITEM,
    ACTION_FINALIZE_ORDER,
    ACTION_EXPORT_COREL,
    ACTION_EXPORT_MALYARKA,
    ACTION_ARCHIVE_ORDER,
    ACTION_REGISTER_ORDER_FILE,
    ACTION_MARK_ORDER_FILE_OBSOLETE,
    ACTION_ADD_MATERIAL,
    ACTION_ADD_COLOR,
    ACTION_ADD_COATING,
    ACTION_ADD_MILLING_TYPE,
    ACTION_ADD_PRICE,
    ACTION_SET_SETTING,
    ACTION_ADD_COMMAND_ALIAS,
    ACTION_RUN_TESTS,
    ACTION_VIEW_ORDER,
    ACTION_VIEW_ARCHIVE,
    ACTION_COMMIT_CODE,
    ACTION_PUSH_CODE,
    ACTION_ACCESS_ENV,
    ACTION_ACCESS_ORDERS_DB,
    ACTION_ACCESS_CUSTOMER_PRIVATE_DATA,
)

ALWAYS_CONFIRM_ACTIONS = frozenset(
    {
        ACTION_RESOLVE_DISPUTED_ITEM,
        ACTION_FINALIZE_ORDER,
        ACTION_ARCHIVE_ORDER,
        ACTION_ADD_PRICE,
        ACTION_SET_SETTING,
        ACTION_COMMIT_CODE,
        ACTION_PUSH_CODE,
        ACTION_ACCESS_ENV,
        ACTION_ACCESS_ORDERS_DB,
        ACTION_ACCESS_CUSTOMER_PRIVATE_DATA,
    }
)

SENSITIVE_ACTIONS = frozenset(
    {
        ACTION_RESOLVE_DISPUTED_ITEM,
        ACTION_FINALIZE_ORDER,
        ACTION_ARCHIVE_ORDER,
        ACTION_ADD_PRICE,
        ACTION_SET_SETTING,
        ACTION_COMMIT_CODE,
        ACTION_PUSH_CODE,
        ACTION_ACCESS_ENV,
        ACTION_ACCESS_ORDERS_DB,
        ACTION_ACCESS_CUSTOMER_PRIVATE_DATA,
        ACTION_SOFT_DELETE_ORDER_ITEM,
        ACTION_MARK_ORDER_FILE_OBSOLETE,
    }
)

_ORDER_MANAGEMENT_ACTIONS = frozenset(
    {
        ACTION_CREATE_ORDER,
        ACTION_UPDATE_ORDER,
        ACTION_ADD_ORDER_ITEM,
        ACTION_SOFT_DELETE_ORDER_ITEM,
        ACTION_RESOLVE_DISPUTED_ITEM,
        ACTION_FINALIZE_ORDER,
        ACTION_EXPORT_COREL,
        ACTION_EXPORT_MALYARKA,
        ACTION_ARCHIVE_ORDER,
        ACTION_REGISTER_ORDER_FILE,
        ACTION_MARK_ORDER_FILE_OBSOLETE,
        ACTION_VIEW_ORDER,
        ACTION_VIEW_ARCHIVE,
    }
)

_REFERENCE_ACTIONS = frozenset(
    {
        ACTION_ADD_MATERIAL,
        ACTION_ADD_COLOR,
        ACTION_ADD_COATING,
        ACTION_ADD_MILLING_TYPE,
        ACTION_ADD_PRICE,
        ACTION_SET_SETTING,
        ACTION_ADD_COMMAND_ALIAS,
    }
)

_CODE_AND_SECRET_ACTIONS = frozenset(
    {
        ACTION_COMMIT_CODE,
        ACTION_PUSH_CODE,
        ACTION_ACCESS_ENV,
        ACTION_ACCESS_ORDERS_DB,
        ACTION_ACCESS_CUSTOMER_PRIVATE_DATA,
    }
)

ROLE_POLICIES = {
    ROLE_OWNER: {
        "role": ROLE_OWNER,
        "allowed_actions": frozenset(ACTIONS),
        "description": "Full access; sensitive actions still require confirmation.",
    },
    ROLE_MANAGER: {
        "role": ROLE_MANAGER,
        "allowed_actions": (
            _ORDER_MANAGEMENT_ACTIONS
            | _REFERENCE_ACTIONS
            | {ACTION_RUN_TESTS}
            - _CODE_AND_SECRET_ACTIONS
        ),
        "description": "Manages orders, exports, archive, references, and prices.",
    },
    ROLE_OPERATOR: {
        "role": ROLE_OPERATOR,
        "allowed_actions": frozenset(
            {
                ACTION_CREATE_ORDER,
                ACTION_ADD_ORDER_ITEM,
                ACTION_EXPORT_COREL,
                ACTION_EXPORT_MALYARKA,
                ACTION_VIEW_ORDER,
            }
        ),
        "description": "Creates orders, adds items, views orders, and exports valid orders.",
    },
    ROLE_PAINTER: {
        "role": ROLE_PAINTER,
        "allowed_actions": frozenset({ACTION_EXPORT_MALYARKA, ACTION_VIEW_ARCHIVE}),
        "description": "Views the malyarka file and archive without changing orders.",
    },
    ROLE_VIEWER: {
        "role": ROLE_VIEWER,
        "allowed_actions": frozenset({ACTION_VIEW_ORDER, ACTION_VIEW_ARCHIVE}),
        "description": "Read-only access.",
    },
    ROLE_AGENT: {
        "role": ROLE_AGENT,
        "allowed_actions": frozenset(
            {
                ACTION_RUN_TESTS,
                ACTION_VIEW_ORDER,
                ACTION_VIEW_ARCHIVE,
            }
        ),
        "description": "Automation agent with safe non-finalizing actions only.",
    },
}


def can_perform_action(role, action):
    """Return True when a known role is allowed to perform a known action."""
    if action not in ACTIONS:
        return False

    policy = ROLE_POLICIES.get(role)
    if policy is None:
        return False

    return action in policy["allowed_actions"]


def action_requires_confirmation(action):
    """Return True when an action always requires explicit confirmation."""
    return action in ALWAYS_CONFIRM_ACTIONS


def assert_can_perform_action(role, action):
    """Raise PermissionError when role cannot perform action."""
    if not can_perform_action(role, action):
        raise PermissionError(f"Role {role!r} cannot perform action {action!r}")


def get_allowed_actions(role):
    """Return a sorted list of actions allowed for role."""
    policy = ROLE_POLICIES.get(role)
    if policy is None:
        return []

    return sorted(policy["allowed_actions"])


def get_role_policy(role):
    """Return a copy of the role policy structure, or None for unknown roles."""
    policy = ROLE_POLICIES.get(role)
    if policy is None:
        return None

    copied_policy = deepcopy(policy)
    copied_policy["allowed_actions"] = sorted(policy["allowed_actions"])
    return copied_policy


def is_sensitive_action(action):
    """Return True for higher-risk actions."""
    return action in SENSITIVE_ACTIONS


def can_agent_perform_without_confirmation(action):
    """Return True for agent actions that are both allowed and non-sensitive."""
    return (
        can_perform_action(ROLE_AGENT, action)
        and not action_requires_confirmation(action)
        and not is_sensitive_action(action)
    )
