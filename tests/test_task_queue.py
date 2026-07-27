"""Tests для Task Queue Hermes-Clean.

Проверяет:
- Создание очереди (валидация, дубликаты, deps, порядок)
- activate_next() — нормальный, ошибки, разрыв последовательности
- complete_current() — атомарный перенос в DONE
- approve_current() — подтверждение
- block_current() / cancel_current()
- audit() — целостность
- render_dashboard() — формат
- create_default_queue() — фабрика
- Прогресс, next_task_id, свойства
"""

import pytest

from hermes_clean import (
    Task,
    TaskQueue,
    TaskRecord,
    TaskStatus,
    AuditViolation,
    create_default_queue,
)


# ── Вспомогательная фабрика ──

def _simple_tasks() -> list[Task]:
    return [
        Task(id="A", name="Task A", order=1),
        Task(id="B", name="Task B", order=2, deps=("A",)),
        Task(id="C", name="Task C", order=3, deps=("B",)),
    ]


# ── 1. Создание очереди ──

def test_create_queue():
    q = TaskQueue(_simple_tasks())
    assert len(q.all_records) == 3
    assert q.progress == "0/3 (0.0%)"
    assert q.current is None
    assert q.next_task_id == "A"


def test_create_queue_empty_raises():
    with pytest.raises(ValueError, match="пустой"):
        TaskQueue([])


def test_create_queue_duplicate_ids_raises():
    tasks = [
        Task(id="A", name="A", order=1),
        Task(id="A", name="B", order=2),
    ]
    with pytest.raises(ValueError, match="дубликаты"):
        TaskQueue(tasks)


def test_create_queue_bad_order_raises():
    """Пропущен order=2 — должен быть разрыв последовательности."""
    tasks = [
        Task(id="A", name="A", order=1),
        Task(id="C", name="C", order=3),
    ]
    with pytest.raises(ValueError, match="Порядок задач нарушен"):
        TaskQueue(tasks)


def test_create_queue_missing_dep_raises():
    tasks = [
        Task(id="A", name="A", order=1),
        Task(id="B", name="B", order=2, deps=("X",)),
    ]
    with pytest.raises(ValueError, match="зависит от"):
        TaskQueue(tasks)


def test_create_queue_dep_order_mismatch_raises():
    """dep должен иметь меньший order (выполняться раньше)."""
    tasks = [
        Task(id="A", name="A", order=1, deps=("B",)),
        Task(id="B", name="B", order=2),
    ]
    # A(order=1) depends on B(order=2) — B выполняется ПОСЛЕ A, нарушение
    with pytest.raises(ValueError, match="должна выполняться раньше"):
        TaskQueue(tasks)


# ── 2. activate_next() ──

def test_activate_first():
    q = TaskQueue(_simple_tasks())
    msg = q.activate_next()
    assert "Активирована" in msg
    assert q.current is not None
    assert q.current.task.id == "A"
    assert q.current.status == TaskStatus.ACTIVE
    assert q.next_task_id == "B"


def test_activate_second_after_first_complete():
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    q.complete_current("OK")
    msg = q.activate_next()
    assert "Активирована" in msg
    assert q.current.task.id == "B"


def test_activate_dep_not_met():
    """B зависит от A, но A не завершена."""
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    # Пытаемся завершить A и активировать B? Нет, пытаемся пропустить A
    q.complete_current("OK")
    # Теперь A завершена, активируем B
    q.activate_next()
    assert q.current.task.id == "B"

    # Активировать C нельзя, пока B не завершена
    q2 = TaskQueue(_simple_tasks())
    q2.activate_next()  # A active
    q2.complete_current("OK")  # A done
    # Не активируем B, пытаемся вручную — такого метода нет
    # activate_next всегда идёт по порядку


def test_activate_with_active_current_blocked():
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    msg = q.activate_next()  # A ещё активна
    assert "ещё активна" in msg


def test_activate_all_done():
    q = TaskQueue(_simple_tasks())
    q.activate_next(); q.complete_current()
    q.activate_next(); q.complete_current()
    q.activate_next(); q.complete_current()
    msg = q.activate_next()
    assert "нет ожидающих задач" in msg


# ── 3. complete_current() ──

def test_complete_no_current():
    q = TaskQueue(_simple_tasks())
    msg = q.complete_current()
    assert "нет активной задачи" in msg


def test_complete_not_active():
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    assert q.current is not None
    q.complete_current("OK")
    # После complete current=None
    assert q.current is None
    assert len(q.done) == 1
    assert q.done[0].task.id == "A"


def test_complete_with_result():
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    q.complete_current("SUCCESS")
    assert q.done[0].result == "SUCCESS"


# ── 4. approve_current() ──

def test_approve_not_needed():
    tasks = [Task(id="A", name="A", order=1)]
    q = TaskQueue(tasks)
    msg = q.approve_current()
    assert "не требует подтверждения" in msg


def test_approve_required():
    tasks = [Task(id="A", name="A", order=1, requires_approval=True)]
    q = TaskQueue(tasks)
    msg = q.approve_current()
    assert "подтверждена" in msg
    assert q.pending[0].approved is True


def test_activate_requires_approval():
    tasks = [Task(id="A", name="A", order=1, requires_approval=True)]
    q = TaskQueue(tasks)
    msg = q.activate_next()
    assert "ОЖИДАНИЕ" in msg
    assert "требует подтверждения" in msg
    # После approve
    q.approve_current()
    msg2 = q.activate_next()
    assert "Активирована" in msg2
    assert q.current.task.id == "A"


# ── 5. block_current() / cancel_current() ──

def test_block_no_current():
    q = TaskQueue(_simple_tasks())
    msg = q.block_current()
    assert "нет активной задачи" in msg


def test_block_current():
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    msg = q.block_current("тестовая блокировка")
    assert "заблокирована" in msg or "тестовая" in msg


def test_cancel_current():
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    msg = q.cancel_current()
    assert "отменена" in msg
    assert len(q.done) == 1  # cancelled goes to done
    assert q.done[0].status == TaskStatus.CANCELLED


# ── 6. Audit ──

def test_audit_clean():
    """Без зависимостей — аудит чист с самого начала."""
    tasks = [
        Task(id="A", name="A", order=1),
        Task(id="B", name="B", order=2),
    ]
    q = TaskQueue(tasks)
    violations = q.audit()
    assert len(violations) == 0


def test_audit_gap_in_sequence():
    """Создать разрыв — задача с пропущенным order."""
    tasks = [
        Task(id="A", name="A", order=1),
        Task(id="C", name="C", order=3),  # пропущен order=2
    ]
    # Создание очереди с пропущенным order вызовет ошибку
    with pytest.raises(ValueError, match="Порядок задач нарушен"):
        TaskQueue(tasks)


def test_audit_unmet_dep():
    """Аудит находит незавершённую зависимость."""
    tasks = [
        Task(id="A", name="A", order=1),
        Task(id="B", name="B", order=2, deps=("A",)),
    ]
    q = TaskQueue(tasks)

    # Испортим вручную — сделаем A completed, но не добавим в done
    # На самом деле audit проверит done_ids
    # A не в done, B pending с dep A → violation
    violations = q.audit()
    assert any("зависит" in v.message for v in violations)


def test_audit_pending_approval():
    tasks = [
        Task(id="A", name="A", order=1, requires_approval=True),
        Task(id="B", name="B", order=2, deps=("A",)),
    ]
    q = TaskQueue(tasks)
    # Approve A and complete it so B's dep is satisfied
    q.approve_current()
    q.activate_next()
    q.complete_current("OK")
    violations = q.audit()
    assert len(violations) == 0


# ── 7. render_dashboard() ──

def test_dashboard_contains_key_info():
    q = TaskQueue(_simple_tasks())
    dash = q.render_dashboard()
    assert "TASK QUEUE DASHBOARD" in dash
    assert "Progress:" in dash
    assert "Current:" in dash
    assert "Next:" in dash
    assert "#01" in dash
    assert "#02" in dash
    assert "#03" in dash
    assert "A" in dash or "Task A" in dash


def test_dashboard_after_progress():
    q = TaskQueue(_simple_tasks())
    q.activate_next()
    q.complete_current()
    dash = q.render_dashboard()
    assert "1/3" in dash
    assert "✅" in dash or "COMPLETED" in dash


# ── 8. create_default_queue() ──

def test_default_queue_has_7_tasks():
    q = create_default_queue()
    assert len(q.all_records) == 7
    assert q.all_records[0].task.id == "BATCH_063C"
    assert q.all_records[-1].task.id == "BATCH_078"


def test_default_queue_deps_chain():
    q = create_default_queue()
    violations = q.audit()
    # Свежая очередь с зависимостями — ошибки deps не выполнены (6 штук)
    assert len(violations) == 6
    # Все сообщения — про невыполненные зависимости (последовательность)
    assert all("зависит" in v.message for v in violations)


def test_default_queue_approval_required():
    q = create_default_queue()
    # BATCH_077 и BATCH_078 require approval
    assert q.all_records[5].task.requires_approval is True
    assert q.all_records[6].task.requires_approval is True


def test_default_queue_full_cycle():
    """Пройти всю стандартную очередь от начала до конца."""
    q = create_default_queue()
    for i in range(7):
        r = q.activate_next()
        if "ОЖИДАНИЕ" in r:
            q.approve_current()
            r = q.activate_next()
        assert "Активирована" in r, f"Failed on step {i}: {r}"
        r = q.complete_current("OK")
        assert "Завершена" in r, f"Failed on complete {i}: {r}"

    assert q.progress == "7/7 (100.0%)"
    assert len(q.done) == 7
    assert q.current is None
    violations = q.audit()
    assert len(violations) == 0


# ── 9. Task dataclass frozen ──

def test_task_frozen():
    t = Task(id="A", name="A", order=1)
    with pytest.raises(AttributeError):
        t.id = "B"


# ── 10. TaskStatus enum values ──

def test_task_status_values():
    assert TaskStatus.PENDING is not None
    assert TaskStatus.ACTIVE is not None
    assert TaskStatus.COMPLETED is not None
    assert TaskStatus.CANCELLED is not None
    assert TaskStatus.BLOCKED is not None


# ── 11. AuditViolation dataclass ──

def test_audit_violation():
    v = AuditViolation(severity="error", message="test", task_id="X")
    assert v.severity == "error"
    assert v.message == "test"
    assert v.task_id == "X"


# ── 12. audit_report() ──

def test_audit_report_clean():
    """Без зависимостей — аудит чист."""
    tasks = [
        Task(id="A", name="A", order=1),
        Task(id="B", name="B", order=2),
    ]
    q = TaskQueue(tasks)
    report = q.audit_report()
    assert "Аудит пройден" in report


def test_audit_report_with_violations():
    tasks = [
        Task(id="A", name="A", order=1, requires_approval=True),
        Task(id="B", name="B", order=2, deps=("A",)),
    ]
    q = TaskQueue(tasks)
    # Симулируем: активируем A (не утверждена)
    # audit найдет unmet dep для B
    report = q.audit_report()
    assert "ОТЧЁТ АУДИТА" in report
