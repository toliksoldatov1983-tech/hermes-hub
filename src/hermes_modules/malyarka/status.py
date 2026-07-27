from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MALYARKA_COMMANDS = [
    "scripts\\hermes.cmd malyarka-preview",
    "scripts\\hermes.cmd malyarka-fixtures",
    "scripts\\hermes.cmd malyarka-resolve",
    "scripts\\hermes.cmd malyarka-workflow",
    "scripts\\hermes.cmd malyarka-status",
]

READY_CONTRACTS = [
    "order_contract",
    "parser_contract",
    "validation_contract",
    "preview_contract",
    "dispute_contract",
    "dispute_questions",
    "resolution_contract",
    "export_source_policy",
    "workflow",
    "export_contract gated stub",
]

GATED_ITEMS = [
    "real order access requires APPROVE_REAL_ORDER_ACCESS",
    "archive import requires APPROVE_MALYARKA_ARCHIVE_IMPORT or APPROVE_ARCHIVE_UNPACK",
    "real export requires a future explicit approval",
    "Excel integration is not enabled",
]


@dataclass(frozen=True)
class MalyarkaStatusResult:
    path: Path
    commands_count: int
    contracts_count: int
    gated_count: int


class MalyarkaStatusReport:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()
        self.output_path = self.project_root / "05_REPORTS" / "MALYARKA_MODULE_STATUS.md"

    def write(self) -> MalyarkaStatusResult:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self._render(), encoding="utf-8")
        return MalyarkaStatusResult(
            path=self.output_path,
            commands_count=len(MALYARKA_COMMANDS),
            contracts_count=len(READY_CONTRACTS),
            gated_count=len(GATED_ITEMS),
        )

    def _render(self) -> str:
        commands = "\n".join(f"- `{command}`" for command in MALYARKA_COMMANDS)
        contracts = "\n".join(f"- `{contract}`" for contract in READY_CONTRACTS)
        gated = "\n".join(f"- {item}" for item in GATED_ITEMS)
        return (
            "# MALYARKA_MODULE_STATUS\n\n"
            f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
            "## Ready Local Commands\n\n"
            f"{commands}\n\n"
            "## Ready Contracts\n\n"
            f"{contracts}\n\n"
            "## Gated Items\n\n"
            f"{gated}\n\n"
            "## Safety\n\n"
            "Malyarka status is local and synthetic. It does not read real orders, Excel files, Google Drive, old archives, secrets or client documents.\n"
        )
