"""Tests для Memory Sync Hermes-Clean.

Проверяет:
- Создание реестра (запреты и правила по умолчанию)
- Добавление решений (с violation check, без)
- SafetyViolation при нарушении запрета
- SafetyViolation при нарушении safety rule
- Immutable решения
- Subsystem решения (Malyarka, AI provider, Telegram)
- Pending approvals (request, approve, reject)
- Integrity check
- Добавление запретов и правил
- Экспорт в JSON (to_dict)
- Дашборд
"""

import pytest

from hermes_clean import (
    MemorySync,
    SafetyViolation,
    Decision,
    Prohibition,
    SafetyRule,
    PendingApproval,
    IntegrityReport,
    Subsystem,
)


# ── 1. Создание реестра ──

def test_create_memory_sync():
    ms = MemorySync()
    assert len(ms.decisions) == 0
    assert len(ms.prohibitions) == 5  # default
    assert len(ms.safety_rules) == 5  # default
    assert len(ms.pending_approvals) == 0
    assert ms.check_integrity().is_consistent is True


def test_default_prohibition_keys():
    ms = MemorySync()
    keys = set(ms.prohibitions.keys())
    assert "no_external_network" in keys
    assert "no_real_api_keys" in keys
    assert "no_real_tokens" in keys
    assert "no_database_write" in keys
    assert "no_live_telegram" in keys


def test_default_safety_rule_keys():
    ms = MemorySync()
    keys = set(ms.safety_rules.keys())
    assert "no_secrets_in_code" in keys
    assert "validate_before_export" in keys
    assert "approval_for_blocked" in keys
    assert "single_contour" in keys
    assert "no_production_touch" in keys


# ── 2. Добавление решений ──

def test_add_decision():
    ms = MemorySync()
    d = ms.add_decision("architecture", "clean", Subsystem.MALYARKA, reason="Изолированный контур")
    assert isinstance(d, Decision)
    assert d.key == "architecture"
    assert d.value == "clean"
    assert d.subsystem == Subsystem.MALYARKA
    assert d.reason == "Изолированный контур"


def test_add_decision_general():
    ms = MemorySync()
    ms.add_decision("use_fixtures_only", True)
    assert ms.get_decision("use_fixtures_only").value is True


def test_add_decision_overwrite():
    ms = MemorySync()
    ms.add_decision("test_key", "v1")
    ms.add_decision("test_key", "v2")
    assert ms.get_decision("test_key").value == "v2"


def test_add_decision_immutable_blocks_overwrite():
    ms = MemorySync()
    ms.add_decision("test_imm", "original", immutable=True)
    with pytest.raises(SafetyViolation, match="immutable"):
        ms.add_decision("test_imm", "new_value")


# ── 3. SafetyViolation при нарушении запретов ──

def test_violation_network_key():
    ms = MemorySync()
    with pytest.raises(SafetyViolation, match="no_external_network"):
        ms.add_decision("enable_network", True)


def test_violation_network_value():
    ms = MemorySync()
    with pytest.raises(SafetyViolation, match="no_external_network"):
        ms.add_decision("mode", "network_active")


def test_violation_api_key():
    ms = MemorySync()
    with pytest.raises(SafetyViolation, match="no_real_api_keys"):
        ms.add_decision("my_api_key", "sk-12345")


def test_violation_token():
    ms = MemorySync()
    with pytest.raises(SafetyViolation):
        ms.add_decision("auth_token", "ghp_xxx")


def test_violation_db_write():
    ms = MemorySync()
    with pytest.raises(SafetyViolation):
        ms.add_decision("allow_db_write", True)


def test_violation_telegram_send():
    ms = MemorySync()
    with pytest.raises(SafetyViolation):
        ms.add_decision("telegram_send_message", True)


def test_skip_violation_check():
    ms = MemorySync()
    # С флагом skip — violation не проверяется
    d = ms.add_decision("api_key_config", "discussed", Subsystem.AI_PROVIDER,
                        skip_violation_check=True)
    assert d.value == "discussed"


# ── 4. SafetyViolation при нарушении safety rules ──

def test_safety_rule_no_secrets_in_code():
    ms = MemorySync()
    with pytest.raises(SafetyViolation, match="no_secrets_in_code"):
        ms.add_decision("db_password", "secret123")


def test_safety_rule_allows_ai_provider():
    """AI provider subsystem может обсуждать ключи (skip_violation_check)."""
    ms = MemorySync()
    d = ms.add_decision("provider_api_key", "config_ref", Subsystem.AI_PROVIDER,
                        skip_violation_check=True)
    assert d.value == "config_ref"


# ── 5. Subsystem решения ──

def test_subsystem_decisions():
    ms = MemorySync()
    ms.add_decision("parser", "built_in", Subsystem.MALYARKA)
    ms.add_decision("provider", "openrouter", Subsystem.AI_PROVIDER)
    ms.add_decision("dialog_mode", "mock", Subsystem.TELEGRAM)

    mal = ms.get_subsystem_decisions(Subsystem.MALYARKA)
    assert "parser" in mal

    ai = ms.get_subsystem_decisions(Subsystem.AI_PROVIDER)
    assert "provider" in ai

    tel = ms.get_subsystem_decisions(Subsystem.TELEGRAM)
    assert "dialog_mode" in tel


def test_subsystem_empty():
    ms = MemorySync()
    assert ms.get_subsystem_decisions(Subsystem.EXPORT) == {}


# ── 6. Pending approvals ──

def test_request_approval():
    ms = MemorySync()
    a = ms.request_approval("export_approval_001", "Разблокировка экспорта", "export")
    assert isinstance(a, PendingApproval)
    assert a.id == "export_approval_001"
    assert a.approved is False
    assert len(ms.pending_approvals) == 1


def test_approve():
    ms = MemorySync()
    ms.request_approval("step_1", "Тестовый шаг")
    a = ms.approve("step_1", approved_by="operator")
    assert a.approved is True
    assert a.approved_by == "operator"
    assert a.approved_at is not None
    assert len(ms.pending_approvals) == 0  # approved not pending


def test_approve_not_found():
    ms = MemorySync()
    with pytest.raises(ValueError, match="not found"):
        ms.approve("nonexistent")


def test_reject_approval():
    ms = MemorySync()
    ms.request_approval("step_2", "Шаг на удаление")
    ms.reject_approval("step_2")
    assert len(ms.pending_approvals) == 0


def test_request_duplicate_raises():
    ms = MemorySync()
    ms.request_approval("step_3", "Первый")
    with pytest.raises(ValueError, match="already exists"):
        ms.request_approval("step_3", "Дубликат")


# ── 7. Добавление запретов ──

def test_add_prohibition():
    ms = MemorySync()
    p = ms.add_prohibition(
        "no_real_orders",
        "Запрещено использовать реальные заказы в тестах.",
        "real_order",
        severity="error",
        reason="Только синтетические фикстуры.",
    )
    assert p.key == "no_real_orders"
    assert "no_real_orders" in ms.prohibitions

    # Проверка что новый запрет работает
    with pytest.raises(SafetyViolation):
        ms.add_decision("process_real_order", True)


def test_add_prohibition_duplicate_raises():
    ms = MemorySync()
    with pytest.raises(SafetyViolation, match="уже существует"):
        ms.add_prohibition("no_external_network", "dup", "dup")


# ── 8. Добавление safety rules ──

def test_add_safety_rule():
    ms = MemorySync()
    r = ms.add_safety_rule("test_rule", "Тестовое правило", "check")
    assert r.key == "test_rule"
    assert "test_rule" in ms.safety_rules


def test_add_safety_rule_duplicate_raises():
    ms = MemorySync()
    with pytest.raises(SafetyViolation, match="уже существует"):
        ms.add_safety_rule("no_secrets_in_code", "dup", "dup")


# ── 9. Integrity check ──

def test_integrity_clean():
    ms = MemorySync()
    report = ms.check_integrity()
    assert isinstance(report, IntegrityReport)
    assert report.is_consistent is True
    assert report.violations_found == 0


def test_integrity_with_violations():
    ms = MemorySync()
    # Добавляем решение, которое нарушает запрет (через skip)
    ms.add_decision("access_token", "ghp_xxx", skip_violation_check=True)
    report = ms.check_integrity()
    assert report.is_consistent is False
    assert report.violations_found >= 1
    assert any("token" in v for v in report.violations)


def test_integrity_report_counts():
    ms = MemorySync()
    ms.add_decision("use_pytest", True, Subsystem.MALYARKA)
    ms.add_decision("provider", "deepseek", Subsystem.AI_PROVIDER)
    ms.request_approval("test_approval", "test")
    report = ms.check_integrity()
    assert report.total_decisions == 2
    assert report.total_prohibitions == 5
    assert report.total_safety_rules == 5
    assert report.pending_approvals == 1


# ── 10. Экспорт в JSON ──

def test_to_dict():
    ms = MemorySync()
    ms.add_decision("key1", "val1", Subsystem.MALYARKA)
    ms.add_decision("key2", 42)
    ms.request_approval("appr_1", "test approval")

    data = ms.to_dict()
    assert "decisions" in data
    assert "prohibitions" in data
    assert "safety_rules" in data
    assert "pending_approvals" in data
    assert "subsystem_decisions" in data
    assert len(data["decisions"]) == 2
    assert len(data["prohibitions"]) == 5
    assert len(data["pending_approvals"]) == 1
    assert "MALYARKA" in data["subsystem_decisions"]


# ── 11. Дашборд ──

def test_dashboard():
    ms = MemorySync()
    ms.add_decision("test", True)
    dash = ms.render_dashboard()
    assert "MEMORY SYNC DASHBOARD" in dash
    assert "Decisions:" in dash
    assert "Prohibitions:" in dash
    assert "Safety Rules:" in dash
    assert "Pending Approvals:" in dash
    assert "CONSISTENT" in dash


def test_dashboard_with_violations():
    ms = MemorySync()
    ms.add_decision("api_key_value", "sk-test", skip_violation_check=True)
    dash = ms.render_dashboard()
    assert "VIOLATION" in dash


# ── 12. Decision dataclass ──

def test_decision_frozen():
    d = Decision(key="k", value="v")
    with pytest.raises(AttributeError):
        d.key = "new"


def test_decision_defaults():
    d = Decision(key="k", value="v")
    assert d.subsystem == Subsystem.GENERAL
    assert d.immutable is False


# ── 13. Subsystem enum ──

def test_subsystem_values():
    assert Subsystem.GENERAL is not None
    assert Subsystem.MALYARKA is not None
    assert Subsystem.AI_PROVIDER is not None
    assert Subsystem.TELEGRAM is not None
    assert Subsystem.EXPORT is not None


# ── 14. SafetyViolation exception ──

def test_safety_violation():
    e = SafetyViolation("test error", rule_key="no_network")
    assert str(e) == "test error"
    assert e.rule_key == "no_network"


# ── 15. Полный сценарий ──

def test_full_scenario():
    """Полный цикл работы с MemorySync."""
    ms = MemorySync()

    # 1. Добавляем решения
    ms.add_decision("architecture", "clean_contour", Subsystem.MALYARKA,
                    reason="Изоляция от production")
    ms.add_decision("use_local_parser", True, Subsystem.MALYARKA)
    ms.add_decision("ai_model", "deepseek-v4", Subsystem.AI_PROVIDER)

    # 2. Попытка нарушения
    with pytest.raises(SafetyViolation):
        ms.add_decision("enable_network", True)

    # 3. Добавляем запрет
    ms.add_prohibition("no_mock_orders", "Без моков", "mock_order")

    # 4. Запрашиваем approval
    ms.request_approval("export_01", "Разблокировка экспорта", "export")

    # 5. Integrity check
    report = ms.check_integrity()
    assert report.total_decisions == 3
    assert report.total_prohibitions == 6
    assert report.pending_approvals == 1
    assert report.is_consistent is True

    # 6. Approve
    ms.approve("export_01")
    assert len(ms.pending_approvals) == 0

    # 7. Subsystem решения
    mal = ms.get_subsystem_decisions(Subsystem.MALYARKA)
    assert len(mal) == 2

    # 8. Дашборд
    dash = ms.render_dashboard()
    assert "CONSISTENT" in dash
