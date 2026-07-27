from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hermes_core.tasks.task_status_store import LocalTaskStatusStore


@dataclass(frozen=True)
class RuntimeSubsystem:
    name: str
    status: str
    mode: str
    approval_gate: str


@dataclass(frozen=True)
class LocalRuntimeStatus:
    project_root: Path
    app_mode: str
    source_of_truth: str
    next_task: str
    enabled_subsystems: list[RuntimeSubsystem]
    disabled_subsystems: list[RuntimeSubsystem]
    can_start_live_services: bool = False
    can_read_secrets: bool = False
    can_touch_real_orders: bool = False
    can_change_google_drive: bool = False


@dataclass(frozen=True)
class RuntimeStatusReportResult:
    path: Path
    app_mode: str
    enabled_count: int
    disabled_count: int


class LocalRuntimeStatusBuilder:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def build(self) -> LocalRuntimeStatus:
        tasks = LocalTaskStatusStore(self.project_root).snapshot()
        enabled = [
            RuntimeSubsystem("local_cli", "ENABLED", "local", "none"),
            RuntimeSubsystem("dashboard", "ENABLED", "local markdown", "none"),
            RuntimeSubsystem("smoke_tests", "ENABLED", "local", "none"),
            RuntimeSubsystem("telegram_dry_run", "ENABLED", "dry-run", "none"),
            RuntimeSubsystem("malyarka_synthetic", "ENABLED", "synthetic/manual test", "none"),
            RuntimeSubsystem("mock_ai_provider", "ENABLED", "mock", "none"),
        ]
        disabled = [
            RuntimeSubsystem("live_telegram", "DISABLED", "live external", "APPROVE_TELEGRAM_LIVE"),
            RuntimeSubsystem("real_ai_providers", "DISABLED", "external API", "APPROVE_SECRET_SETUP"),
            RuntimeSubsystem("google_drive_write", "DISABLED", "external write", "APPROVE_GOOGLE_DRIVE_MOVE"),
            RuntimeSubsystem("real_order_access", "DISABLED", "customer data", "APPROVE_REAL_ORDER_ACCESS"),
            RuntimeSubsystem("archive_import", "DISABLED", "old archive import", "APPROVE_ARCHIVE_UNPACK"),
            RuntimeSubsystem("delete_files", "DISABLED", "destructive", "APPROVE_DELETE"),
        ]
        return LocalRuntimeStatus(
            project_root=self.project_root,
            app_mode="local-safe",
            source_of_truth="Hermes-Clean",
            next_task=tasks.next_task,
            enabled_subsystems=enabled,
            disabled_subsystems=disabled,
        )


class LocalRuntimeStatusReport:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.output_path = self.project_root / "05_REPORTS" / "LOCAL_RUNTIME_STATUS.md"

    def write(self) -> RuntimeStatusReportResult:
        status = LocalRuntimeStatusBuilder(self.project_root).build()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self._render(status), encoding="utf-8")
        return RuntimeStatusReportResult(
            path=self.output_path,
            app_mode=status.app_mode,
            enabled_count=len(status.enabled_subsystems),
            disabled_count=len(status.disabled_subsystems),
        )

    def _render(self, status: LocalRuntimeStatus) -> str:
        enabled = "\n".join(
            f"- `{item.name}`: {item.status}; mode={item.mode}; approval={item.approval_gate}"
            for item in status.enabled_subsystems
        )
        disabled = "\n".join(
            f"- `{item.name}`: {item.status}; mode={item.mode}; approval={item.approval_gate}"
            for item in status.disabled_subsystems
        )
        return (
            "# LOCAL_RUNTIME_STATUS\n\n"
            f"- project_root: `{status.project_root}`\n"
            f"- app_mode: `{status.app_mode}`\n"
            f"- source_of_truth: `{status.source_of_truth}`\n"
            f"- next_task: `{status.next_task}`\n\n"
            "## Enabled Subsystems\n\n"
            f"{enabled}\n\n"
            "## Disabled Subsystems\n\n"
            f"{disabled}\n\n"
            "## Hard Runtime Gates\n\n"
            f"- can_start_live_services: `{status.can_start_live_services}`\n"
            f"- can_read_secrets: `{status.can_read_secrets}`\n"
            f"- can_touch_real_orders: `{status.can_touch_real_orders}`\n"
            f"- can_change_google_drive: `{status.can_change_google_drive}`\n\n"
            "This report is local. It does not read `.env`, tokens, keys, real orders, Google Drive files or old archives.\n"
        )
