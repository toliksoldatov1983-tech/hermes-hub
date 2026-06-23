import pytest

from malyarka_core.security.permissions import (
    ACTIONS,
    action_requires_confirmation,
    assert_can_perform_action,
    can_agent_perform_without_confirmation,
    can_perform_action,
    get_allowed_actions,
    get_role_policy,
)


def test_owner_can_perform_regular_actions():
    assert can_perform_action("owner", "create_order") is True
    assert can_perform_action("owner", "export_corel") is True
    assert can_perform_action("owner", "add_material") is True


def test_unknown_role_cannot_perform_actions():
    assert can_perform_action("unknown", "create_order") is False
    assert get_allowed_actions("unknown") == []
    assert get_role_policy("unknown") is None


def test_unknown_action_is_not_allowed():
    assert can_perform_action("owner", "unknown_action") is False
    assert can_perform_action("manager", "unknown_action") is False


def test_viewer_can_only_view():
    assert get_allowed_actions("viewer") == ["view_archive", "view_order"]
    assert can_perform_action("viewer", "view_order") is True
    assert can_perform_action("viewer", "view_archive") is True
    assert can_perform_action("viewer", "create_order") is False


def test_operator_cannot_change_prices_or_settings():
    assert can_perform_action("operator", "create_order") is True
    assert can_perform_action("operator", "add_order_item") is True
    assert can_perform_action("operator", "add_price") is False
    assert can_perform_action("operator", "set_setting") is False
    assert can_perform_action("operator", "add_material") is False


def test_manager_can_manage_orders_and_references():
    assert can_perform_action("manager", "create_order") is True
    assert can_perform_action("manager", "update_order") is True
    assert can_perform_action("manager", "finalize_order") is True
    assert can_perform_action("manager", "archive_order") is True
    assert can_perform_action("manager", "add_material") is True
    assert can_perform_action("manager", "add_color") is True
    assert can_perform_action("manager", "add_coating") is True
    assert can_perform_action("manager", "add_milling_type") is True
    assert can_perform_action("manager", "add_price") is True
    assert can_perform_action("manager", "set_setting") is True
    assert can_perform_action("manager", "commit_code") is False
    assert can_perform_action("manager", "push_code") is False
    assert can_perform_action("manager", "access_env") is False
    assert can_perform_action("manager", "access_orders_db") is False


def test_painter_can_view_malyarka_but_not_change_order():
    assert can_perform_action("painter", "export_malyarka") is True
    assert can_perform_action("painter", "view_archive") is True
    assert can_perform_action("painter", "update_order") is False
    assert can_perform_action("painter", "add_order_item") is False
    assert can_perform_action("painter", "add_price") is False


def test_agent_can_run_tests():
    assert can_perform_action("agent", "run_tests") is True


def test_agent_cannot_finalize_order():
    assert can_perform_action("agent", "finalize_order") is False


def test_agent_cannot_resolve_disputed_item():
    assert can_perform_action("agent", "resolve_disputed_item") is False


def test_agent_cannot_access_env_or_orders_db():
    assert can_perform_action("agent", "access_env") is False
    assert can_perform_action("agent", "access_orders_db") is False
    assert can_perform_action("agent", "access_customer_private_data") is False


def test_sensitive_actions_require_confirmation():
    assert action_requires_confirmation("resolve_disputed_item") is True
    assert action_requires_confirmation("finalize_order") is True
    assert action_requires_confirmation("archive_order") is True
    assert action_requires_confirmation("add_price") is True
    assert action_requires_confirmation("set_setting") is True
    assert action_requires_confirmation("access_customer_private_data") is True
    assert action_requires_confirmation("create_order") is False


def test_commit_and_push_require_confirmation():
    assert action_requires_confirmation("commit_code") is True
    assert action_requires_confirmation("push_code") is True


def test_assert_can_perform_action_raises_permission_error():
    assert_can_perform_action("manager", "create_order")

    with pytest.raises(PermissionError):
        assert_can_perform_action("viewer", "create_order")


def test_get_allowed_actions_returns_only_allowed_actions():
    manager_actions = get_allowed_actions("manager")

    assert manager_actions == sorted(manager_actions)
    assert set(manager_actions).issubset(set(ACTIONS))
    assert "create_order" in manager_actions
    assert "commit_code" not in manager_actions
    assert "access_env" not in manager_actions


def test_can_agent_perform_without_confirmation_only_safe_actions():
    assert can_agent_perform_without_confirmation("run_tests") is True
    assert can_agent_perform_without_confirmation("view_order") is True
    assert can_agent_perform_without_confirmation("finalize_order") is False
    assert can_agent_perform_without_confirmation("resolve_disputed_item") is False
    assert can_agent_perform_without_confirmation("access_env") is False
    assert can_agent_perform_without_confirmation("unknown_action") is False
