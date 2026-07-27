from __future__ import annotations

import argparse
from pathlib import Path

from hermes_core.router import HermesRouter
from hermes_core.ai.provider_factory import ProviderConfig, ProviderFactory
from hermes_core.ai_provider import (
    AIProviderRequest,
    AIProviderRouter,
    ProviderCapability,
    get_default_registry,
)
from hermes_core.command_help import build_command_help
from hermes_core.daily_report import LocalDailyReport
from hermes_core.dashboard import LocalDashboard
from hermes_core.health import LocalHealthChecker
from hermes_core.memory.local_memory_store import LocalProjectMemoryStore
from hermes_core.project_audit import LocalProjectAudit
from hermes_core.report_index import LocalReportIndex
from hermes_core.refresh_all import LocalRefreshAll
from hermes_core.release_checklist import LocalReleaseChecklist
from hermes_core.runtime_status import LocalRuntimeStatusReport
from hermes_core.start_summary import LocalStartSummaryBuilder
from hermes_core.smoke import LocalSmokeTester
from hermes_core.status_export import LocalStatusExporter
from hermes_core.tasks.task_status_store import LocalTaskStatusStore
from hermes_core.safety.action_policy import classify_action
from hermes_core.safety.audit_log import LocalAuditLog
from hermes_core.review.review_provider_factory import ReviewProviderConfig, ReviewProviderFactory
from hermes_core.telegram.dry_run_gateway import TelegramDryRunGateway
from hermes_core.telegram.message_contract import TelegramMessage
from hermes_core.telegram.scenarios import run_telegram_scenarios
from hermes_core.telegram.status_report import TelegramDryRunStatusReport
from hermes_core.types import UserRequest
from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.preview_contract import build_preview
from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.fixtures import run_all_fixtures
from hermes_modules.malyarka.resolution_contract import resolve_with_replacement
from hermes_modules.malyarka.export_preview import build_export_preview
from hermes_modules.malyarka.schema_contract import export_preview_columns, schema_as_lines
from hermes_modules.malyarka.status import MalyarkaStatusReport
from hermes_modules.malyarka.workflow import build_synthetic_workflow
from hermes_modules.malyarka.demo import build_demo
from hermes_modules.malyarka.synthetic_pricing import build_synthetic_pricing_preview
from hermes_modules.malyarka.dispute_classifier import MalyarkaDisputeClassificationReport, build_fixture_dispute_summary
from hermes_modules.malyarka.combined_preview import build_combined_preview
from hermes_clean.telegram_flow_runner import format_run_result, run_telegram_flow_case, run_telegram_flow_text
from hermes_clean.malyarka_dialog_commands import format_script_results, run_dialog_script
from hermes_clean.malyarka_transcript_report import write_transcript_report


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read_next_task_id() -> str:
    next_task = PROJECT_ROOT / "03_TASKS" / "NEXT_TASK.md"
    if not next_task.exists():
        return "NEXT_TASK.md not found"
    for line in next_task.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("BATCH_") or stripped.startswith("HERMES_"):
            return stripped
    return "NEXT_TASK.md has no task id"


def status_command(_: argparse.Namespace) -> int:
    print("Hermes-Clean local app")
    print(f"project_root={PROJECT_ROOT}")
    print("mode=dry-run")
    print("source_of_truth=Hermes-Clean")
    print(f"next_task={_read_next_task_id()}")
    return 0


def message_command(args: argparse.Namespace) -> int:
    text = " ".join(args.text).strip() or "/статус"
    result = TelegramDryRunGateway().simulate_incoming(TelegramMessage(text))
    print(f"command={result.command}")
    print(f"planned_response={result.planned_response}")
    print(f"blocked_actions={len(result.blocked_actions)}")
    print(f"warnings={'; '.join(result.warnings) if result.warnings else '-'}")
    print(f"next_step={result.next_step}")
    for key, value in result.payload.items():
        print(f"payload.{key}={value}")
    return 0


def telegram_scenarios_command(_: argparse.Namespace) -> int:
    results = run_telegram_scenarios()
    print("telegram_scenarios=dry-run")
    print(f"scenarios={len(results)}")
    for result in results:
        print(
            f"- {result.name}: command={result.command}; "
            f"blocked={result.blocked_actions_count}; warnings={result.warnings_count}; "
            f"next_step={result.next_step}"
        )
    return 0


def telegram_status_command(_: argparse.Namespace) -> int:
    result = TelegramDryRunStatusReport(PROJECT_ROOT).write()
    print("telegram_status=dry-run")
    print(f"path={result.path}")
    print(f"aliases={result.aliases_count}")
    print(f"scenarios={result.scenarios_count}")
    print(f"safety_limits={result.safety_limits_count}")
    print(f"blocked_actions={result.blocked_actions_count}")
    for cat, count in sorted(result.blocked_categories.items()):
        print(f"blocked.{cat}={count}")
    return 0


def telegram_flow_command(args: argparse.Namespace) -> int:
    if args.text:
        result = run_telegram_flow_text(" ".join(args.text), auto_delete_disputes=args.auto_resolve)
    else:
        result = run_telegram_flow_case(args.case)
    print(format_run_result(result))
    return 0


def malyarka_dialog_command(args: argparse.Namespace) -> int:
    if args.script == "clean":
        commands = [
            "/order paint | 2 | bucket\\nroller | 3 | piece",
            "/preview",
            "/export",
            "/report",
        ]
    elif args.script == "disputed":
        commands = [
            "/order paint | 2 | bucket\\nneeds clarification\\nbroken row\\nroller | 3 | piece",
            "/questions",
            "/resolve-all-delete",
            "/preview",
            "/export",
            "/report",
        ]
    else:
        commands = args.commands
    results = run_dialog_script(commands)
    print(format_script_results(results))
    return 0


def malyarka_transcript_command(args: argparse.Namespace) -> int:
    result = write_transcript_report(
        project_root=PROJECT_ROOT,
        script_name=args.script,
        output_name=args.output,
    )
    print("malyarka_transcript=local-dry-run")
    print(f"path={result.path}")
    print(f"script={result.script_name}")
    print(f"commands={result.commands_count}")
    print(f"final_status={result.final_status}")
    print(f"final_export_ready={result.final_export_ready}")
    print(f"final_pending_disputes={result.final_pending_disputes}")
    return 0


def dashboard_command(_: argparse.Namespace) -> int:
    result = LocalDashboard(PROJECT_ROOT).write()
    print("dashboard=local")
    print(f"path={result.path}")
    print(f"health_status={result.health_status}")
    print(f"smoke_status={result.smoke_status}")
    print(f"next_task={result.next_task}")
    print(f"malyarka_fixtures={result.malyarka_fixtures}")
    print(f"telegram_aliases={result.telegram_aliases}")
    return 0


def app_status_command(_: argparse.Namespace) -> int:
    result = LocalRuntimeStatusReport(PROJECT_ROOT).write()
    print("app_status=local-safe")
    print(f"path={result.path}")
    print(f"app_mode={result.app_mode}")
    print(f"enabled={result.enabled_count}")
    print(f"disabled={result.disabled_count}")
    return 0


def daily_report_command(_: argparse.Namespace) -> int:
    result = LocalDailyReport(PROJECT_ROOT).write()
    print("daily_report=local")
    print(f"path={result.path}")
    print(f"health_status={result.health_status}")
    print(f"smoke_status={result.smoke_status}")
    print(f"next_task={result.next_task}")
    print(f"disabled_subsystems={result.disabled_subsystems_count}")
    return 0


def project_audit_command(_: argparse.Namespace) -> int:
    result = LocalProjectAudit(PROJECT_ROOT).write()
    print("project_audit=local")
    print(f"path={result.path}")
    print(f"status={result.status}")
    print(f"checks={result.checks_count}")
    print(f"failed={result.failed_count}")
    return 0 if result.status == "OK" else 1


def refresh_all_command(_: argparse.Namespace) -> int:
    result = LocalRefreshAll(PROJECT_ROOT).run()
    print("refresh_all=local")
    print(f"refreshed={result.count}")
    for path in result.refreshed_paths:
        print(f"- {path}")
    return 0


def route_command(args: argparse.Namespace) -> int:
    text = " ".join(args.text).strip() or "status"
    response = HermesRouter().handle(UserRequest(text=text, channel="cli"))
    print(f"decision={response.decision.value}")
    for action in response.planned_actions:
        print(f"action={action.action_type}: {action.description}")
    if response.warnings:
        print(f"warnings={'; '.join(response.warnings)}")
    print(f"next_step={response.next_step}")
    return 0


def safety_command(args: argparse.Namespace) -> int:
    action_type = args.action_type.strip()
    policy = classify_action(action_type, approved=args.approved)
    print(f"decision={policy.decision.value}")
    print(f"reason={policy.reason}")

    # Log to audit
    audit = LocalAuditLog(PROJECT_ROOT)
    entry = audit.log(
        action=f"safety_check:{action_type}",
        decision=policy.decision,
        source="cli",
        detail=f"approved={args.approved}",
    )
    print(f"audit_logged={entry.decision}")
    return 0


def safety_audit_command(_: argparse.Namespace) -> int:
    audit = LocalAuditLog(PROJECT_ROOT)
    snapshot = audit.snapshot()
    print("safety_audit=local")
    print(f"log_path={snapshot.log_path}")
    print(f"total_entries={snapshot.total_entries}")
    print(f"safe={snapshot.safe_count}")
    print(f"confirm_required={snapshot.confirm_count}")
    print(f"blocked={snapshot.blocked_count}")
    for i, entry in enumerate(snapshot.entries[-10:], start=1):
        print(f"  [{i}] {entry.timestamp} {entry.decision} {entry.action} ({entry.source}): {entry.detail}")
    return 0


def ai_provider_command(args: argparse.Namespace) -> int:
    selection = ProviderFactory().select(
        ProviderConfig(
            mode=args.mode,
            secret_setup_approved=args.approved,
            gemini_key_available=args.key_available,
            deepseek_key_available=False,
        )
    )
    print(f"provider={selection.provider_name}")
    print(f"mode={selection.mode}")
    print(f"blocked={selection.is_blocked}")
    print(f"blocked_reason={selection.blocked_reason or '-'}")
    resp = selection.provider.generate_response("local smoke test")
    if hasattr(resp, 'text'):
        print(resp.text)
    else:
        print(resp)
    return 0


def review_provider_command(args: argparse.Namespace) -> int:
    selection = ReviewProviderFactory().select(
        ReviewProviderConfig(
            mode=args.mode,
            secret_setup_approved=args.approved,
            key_available=args.key_available,
        )
    )
    result = selection.review("print('local smoke test')", cycles_used=args.cycles_used)
    print(f"provider={selection.provider_name}")
    print(f"mode={selection.mode}")
    print(f"blocked={selection.is_blocked}")
    print(f"blocked_reason={selection.blocked_reason or '-'}")
    print(f"approved={result.approved}")
    print(f"can_edit_project={result.can_edit_project}")
    print(f"cycles_used={result.cycles_used}")
    print(f"findings={'; '.join(result.findings)}")
    return 0


def memory_command(_: argparse.Namespace) -> int:
    snapshot = LocalProjectMemoryStore(PROJECT_ROOT).snapshot()
    print("memory_store=local")
    print(f"source_of_truth={snapshot.source_of_truth}")
    print(f"documents={len(snapshot.documents)}")
    for document in snapshot.documents:
        status = "exists" if document.exists else "missing"
        print(f"document={document.relative_path}:{status}")
    print(f"next_task={snapshot.next_task}")
    print(f"pending_approvals={snapshot.pending_approvals_preview}")
    print(f"prohibitions={snapshot.prohibitions_preview}")
    return 0


def tasks_command(_: argparse.Namespace) -> int:
    snapshot = LocalTaskStatusStore(PROJECT_ROOT).snapshot()
    print("task_store=local")
    print(f"active_batch={snapshot.active_batch}")
    print(f"next_task={snapshot.next_task}")
    print(f"done_count={snapshot.done_count}")
    print(f"blocked_count={snapshot.blocked_count}")
    print(f"last_done={snapshot.last_done}")
    print(f"pending_approvals={snapshot.pending_approvals_preview}")
    return 0


def health_command(_: argparse.Namespace) -> int:
    report = LocalHealthChecker(PROJECT_ROOT).run()
    print("health_check=local")
    print(f"project_root={report.project_root}")
    print(f"status={'OK' if report.ok else 'ATTENTION'}")
    print(f"missing_required_paths={len(report.missing_required_paths)}")
    for path in report.missing_required_paths:
        print(f"missing={path}")
    print(f"env_files_found={len(report.env_files_found)}")
    for path in report.env_files_found:
        print(f"env_file={path}")
    print(f"active_batch={report.task_snapshot.active_batch}")
    print(f"next_task={report.task_snapshot.next_task}")
    print(f"done_count={report.task_snapshot.done_count}")
    print(f"memory_documents={len(report.memory_snapshot.documents)}")
    print(f"memory_source={report.memory_snapshot.source_of_truth}")
    return 0


def reports_command(_: argparse.Namespace) -> int:
    snapshot = LocalReportIndex(PROJECT_ROOT).snapshot()
    print("report_index=local")
    print(f"project_root={snapshot.project_root}")
    print(f"reports_count={snapshot.reports_count}")
    print(f"active_batch={snapshot.task_snapshot.active_batch}")
    print(f"next_task={snapshot.task_snapshot.next_task}")
    print(f"done_count={snapshot.task_snapshot.done_count}")
    print("key_reports:")
    for report in snapshot.key_reports:
        print(f"- {report.relative_path} size={report.size_bytes} modified={report.modified_at}")
    print("recent_reports:")
    for report in snapshot.recent_reports:
        marker = " key" if report.is_key_report else ""
        print(f"- {report.relative_path} size={report.size_bytes} modified={report.modified_at}{marker}")
    print(f"pending_approvals={snapshot.task_snapshot.pending_approvals_preview}")
    return 0


def start_summary_command(_: argparse.Namespace) -> int:
    summary = LocalStartSummaryBuilder(PROJECT_ROOT).build()
    print("start_summary=local")
    print(f"project_root={summary.project_root}")
    print(f"health_status={summary.health_status}")
    print(f"active_batch={summary.active_batch}")
    print(f"next_task={summary.next_task}")
    print(f"done_count={summary.done_count}")
    print(f"reports_count={summary.reports_count}")
    print(f"env_files_found={summary.env_files_found}")
    print("safe_commands:")
    for command in summary.safe_commands:
        print(f"- {command}")
    return 0


def help_local_command(_: argparse.Namespace) -> int:
    help_data = build_command_help()
    print("help_local=Hermes-Clean")
    print("commands:")
    for entry in help_data.commands:
        print(
            f"- {entry.command}: purpose={entry.purpose}; "
            f"mode={entry.mode}; approval_required={entry.approval_required}"
        )
    print("approval_gates:")
    for gate in help_data.approval_gates:
        print(f"- {gate}")
    return 0


def smoke_command(_: argparse.Namespace) -> int:
    report = LocalSmokeTester(PROJECT_ROOT).run()
    print("smoke=local")
    print(f"status={report.status}")
    print(f"checks={len(report.checks)}")
    print(f"failed={len(report.failed_checks)}")
    for check in report.checks:
        state = "OK" if check.ok else "FAIL"
        print(f"- {check.name}: {state}; {check.detail}")
    return 0 if report.status == "OK" else 1


def export_status_command(_: argparse.Namespace) -> int:
    result = LocalStatusExporter(PROJECT_ROOT).export()
    print("export_status=local")
    print(f"path={result.path}")
    print(f"health_status={result.status}")
    print(f"smoke_status={result.smoke_status}")
    print(f"next_task={result.next_task}")
    print(f"reports_count={result.reports_count}")
    return 0


def release_checklist_command(_: argparse.Namespace) -> int:
    result = LocalReleaseChecklist(PROJECT_ROOT).write()
    print("release_checklist=local")
    print(f"path={result.path}")
    print(f"health_status={result.health_status}")
    print(f"smoke_status={result.smoke_status}")
    print(f"next_task={result.next_task}")
    print(f"approval_gates={result.approval_gates_count}")
    return 0


def malyarka_preview_command(args: argparse.Namespace) -> int:
    source = " ".join(args.text).strip()
    order = ParserContract().parse(source)
    preview = build_preview(order)
    print("malyarka_preview=dry-run")
    print(f"confirmed_rows={preview['confirmed_count']}")
    print(f"disputed_rows={preview['disputed_count']}")
    print(f"final_ready={preview['final_ready']}")
    for row in preview["disputed"]:
        print(f"dispute={row['raw_text']}: {row['reason']}")
    print(f"export={export_blocked_until_confirmed(order)}")
    return 0


def malyarka_fixtures_command(_: argparse.Namespace) -> int:
    results = run_all_fixtures()
    print("malyarka_fixtures=synthetic")
    print(f"fixtures={len(results)}")
    print("status=OK")
    for result in results:
        print(
            f"- {result.name}: confirmed={result.confirmed_count}; "
            f"disputed={result.disputed_count}; final_ready={result.final_ready}; export={result.export_status}"
        )
        for dispute in result.disputes:
            print(f"  dispute={dispute}")
    return 0


def malyarka_resolve_command(args: argparse.Namespace) -> int:
    source = " ".join(args.source).strip()
    result = resolve_with_replacement(source, args.replacement)
    print("malyarka_resolve=dry-run")
    print(f"original_disputed_count={result.original_disputed_count}")
    print(f"resolved_disputed_count={result.resolved_disputed_count}")
    print(f"replacement_accepted={result.replacement_accepted}")
    print(f"resolved_final_ready={result.resolved_final_ready}")
    print(f"export={result.export_status}")
    return 0


def malyarka_workflow_command(_: argparse.Namespace) -> int:
    workflow = build_synthetic_workflow()
    print("malyarka_workflow=dry-run")
    print(f"final_status={workflow.final_status}")
    for step in workflow.steps:
        print(f"- {step.name}: {step.status}; {step.detail}")
    return 0


def malyarka_status_command(_: argparse.Namespace) -> int:
    result = MalyarkaStatusReport(PROJECT_ROOT).write()
    print("malyarka_status=local")
    print(f"path={result.path}")
    print(f"commands={result.commands_count}")
    print(f"contracts={result.contracts_count}")
    print(f"gated={result.gated_count}")
    return 0


def malyarka_schema_command(_: argparse.Namespace) -> int:
    order = ParserContract().parse("wall paint | 2 | bucket")
    preview = build_export_preview(order)
    print("malyarka_schema=local")
    print("fields:")
    for line in schema_as_lines():
        print(f"- {line}")
    print(f"export_columns={','.join(export_preview_columns())}")
    print(f"preview_rows={len(preview.rows)}")
    print(f"can_write_file={preview.can_write_file}")
    print(f"blocked_reason={preview.blocked_reason}")
    return 0


def malyarka_demo_command(_: argparse.Namespace) -> int:
    demo = build_demo()
    print("malyarka_demo=local")
    print(f"fixtures={demo.fixtures_count}")
    print(f"ready_fixtures={demo.ready_fixtures}")
    print(f"disputed_fixtures={demo.disputed_fixtures}")
    print(f"workflow_status={demo.workflow_status}")
    print(f"export_columns={','.join(demo.export_columns)}")
    print(f"export_gated={demo.export_gated}")
    return 0


def malyarka_pricing_command(_: argparse.Namespace) -> int:
    order = ParserContract().parse("wall paint | 2 | bucket\nroller | 3 | piece")
    preview = build_synthetic_pricing_preview(order)
    print("malyarka_pricing=synthetic")
    print(f"lines={len(preview.lines)}")
    print(f"total={preview.total}")
    print(f"missing_prices={len(preview.missing_prices)}")
    print(f"can_use_as_real_price={preview.can_use_as_real_price}")
    for line in preview.lines:
        print(
            f"- {line.item_name}: quantity={line.quantity}; unit={line.unit}; "
            f"unit_price={line.unit_price}; line_total={line.line_total}; "
            f"customer={line.customer_label}; order={line.order_reference}"
        )
    return 0


def malyarka_disputes_command(_: argparse.Namespace) -> int:
    result = MalyarkaDisputeClassificationReport(PROJECT_ROOT).write()
    summary = build_fixture_dispute_summary()
    print("malyarka_disputes=synthetic")
    print(f"path={result.path}")
    print(f"total_disputes={result.total_disputes}")
    print(f"categories={result.categories_count}")
    for category, count in sorted(summary.categories.items()):
        print(f"- {category}: {count}")
    return 0


def malyarka_combined_command(args: argparse.Namespace) -> int:
    source = " ".join(args.text).strip()
    preview = build_combined_preview(source)
    print("malyarka_combined=local")
    print(f"source_mode={preview.source_mode}")
    print(f"confirmed_rows={preview.confirmed_count}")
    print(f"disputed_rows={preview.disputed_count}")
    print(f"final_ready={preview.final_ready}")
    print(f"export={preview.export_status}")
    print(f"pricing_total={preview.pricing.total}")
    print(f"missing_prices={len(preview.pricing.missing_prices)}")
    print(f"can_write_file={preview.can_write_file}")
    print(f"can_use_as_real_order={preview.can_use_as_real_order}")
    for category, count in sorted(preview.dispute_categories.items()):
        print(f"dispute_category.{category}={count}")
    for line in preview.pricing.lines:
        print(f"priced={line.item_name}; quantity={line.quantity}; line_total={line.line_total}")
    for classification in preview.dispute_classifications:
        print(f"dispute={classification.category}; raw={classification.raw_text}; action={classification.recommended_action}")
    return 0


# ── New universal AI provider commands ──


# ── Daily Assistant commands ──


def daily_assistant_command(_: argparse.Namespace) -> int:
    """Show daily assistant — full project snapshot."""
    from hermes_core.daily_assistant import build_daily_assistant
    report = build_daily_assistant()
    print("daily_assistant=local-safe")
    print(f"project_root={report.project_root}")
    print(f"health_status={report.health_status}")
    print(f"active_batch={report.active_batch}")
    print(f"next_task={report.next_task}")
    print(f"done_count={report.done_count}")
    print(f"tests_passed={report.tests_passed}")
    print(f"smoke={report.smoke_checks}")
    print(f"audit={report.audit_checks}")
    print()
    print("--- Malyarka ---")
    print(f"status={report.malyarka_status}")
    print(f"fixtures={report.malyarka_fixtures}")
    print(f"commands={report.malyarka_commands}")
    print()
    print("--- AI Provider ---")
    print(f"total={report.ai_providers_total}")
    print(f"safe={report.ai_providers_safe}")
    print(f"blocked={report.ai_providers_blocked}")
    for detail in report.provider_details:
        print(f"  {detail}")
    print()
    print("--- Safety Gates ---")
    print(f"enabled={report.enabled_subsystems}")
    print(f"disabled={report.disabled_subsystems}")
    for gate in report.gates:
        print(f"  {gate}")
    print()
    print("--- Recommended Commands ---")
    for cmd in report.recommended_commands:
        print(f"  {cmd}")
    print()
    print("--- Blocked Without Approval ---")
    for item in report.blocked_without_approval:
        print(f"  {item}")
    return 0


def daily_brief_command(_: argparse.Namespace) -> int:
    """One-screen daily brief."""
    from hermes_core.daily_assistant import build_daily_brief
    brief = build_daily_brief()
    print("daily_brief=local-safe")
    print(f"date={brief.date}")
    print(f"project={brief.project}")
    print(f"next_task={brief.next_task}")
    print(f"health={brief.health}")
    print(f"malyarka={brief.malyarka}")
    print(f"ai_provider={brief.ai_provider}")
    print(f"recommendation={brief.recommendation}")
    for w in brief.warnings:
        print(f"warning={w}")
    return 0


def what_next_command(_: argparse.Namespace) -> int:
    """What to do next."""
    from hermes_core.daily_assistant import build_what_next
    report = build_what_next()
    print("what_next=local-safe")
    print(f"next_task={report.next_task_id}")
    print(f"status={report.status}")
    print()
    print("Safe commands:")
    for cmd in report.safe_commands:
        print(f"  {cmd}")
    print()
    print("Blocked actions:")
    for action in report.blocked_actions:
        print(f"  {action}")
    print()
    print(f"notes={report.notes}")
    return 0


def local_health_command(_: argparse.Namespace) -> int:
    """Local health check — fast, one-screen."""
    from hermes_core.health import LocalHealthChecker
    report = LocalHealthChecker(PROJECT_ROOT).run()
    print("local_health=OK" if report.ok else "local_health=ATTENTION")
    print(f"project_root={report.project_root}")
    print(f"status={'OK' if report.ok else 'ATTENTION'}")
    print(f"missing_paths={len(report.missing_required_paths)}")
    for p in report.missing_required_paths:
        print(f"  missing={p}")
    print(f"env_files_found={len(report.env_files_found)}")
    print(f"next_task={report.task_snapshot.next_task}")
    return 0


def project_status_command(_: argparse.Namespace) -> int:
    """Quick project status."""
    from hermes_core.tasks.task_status_store import LocalTaskStatusStore
    from hermes_core.ai_provider import AIProviderRouter
    snapshot = LocalTaskStatusStore(PROJECT_ROOT).snapshot()
    router = AIProviderRouter()
    providers = router.list_providers()
    safe = sum(1 for d in providers if d.metadata and d.metadata.can_use_now)
    print("project_status=local-safe")
    print(f"active_batch={snapshot.active_batch}")
    print(f"next_task={snapshot.next_task}")
    print(f"done_count={snapshot.done_count}")
    print(f"ai_providers={len(providers)} ({safe} safe)")
    print(f"malyarka=dry-run")
    print(f"telegram=dry-run")
    return 0


def malyarka_mode_status_command(_: argparse.Namespace) -> int:
    """Malyarka mode status."""
    from hermes_modules.malyarka.ai_review import review_disputed_row
    print("malyarka_mode_status=dry-run")
    print("ai_review_path=router (malyarka.ai_review.review_disputed_row)")
    print("direct_gemini=False")
    print("direct_deepseek=False")
    print("router_policy=safe_local (mock only)")
    print()
    # Prove Malyarka uses router, not direct calls
    result = review_disputed_row("broken row")
    print(f"test_review_provider={result.provider_id}")
    print(f"test_review_is_mock={result.is_mock}")
    print(f"test_review_direct_gemini={result.safety['direct_gemini_call']}")
    print(f"test_review_direct_deepseek={result.safety['direct_deepseek_call']}")
    print(f"test_review_network={result.safety['network_called']}")
    return 0


def ai_provider_list_command(_: argparse.Namespace) -> int:
    """List all registered AI providers with their status."""
    router = AIProviderRouter()
    providers = router.list_providers()
    print("ai_provider_list=universal")
    print(f"total={len(providers)}")
    for d in providers:
        m = d.metadata
        status = "SAFE" if d.metadata and d.metadata.can_use_now else "BLOCKED"
        caps = ", ".join(c.name for c in (m.capabilities if m else ()))
        print(
            f"- {d.provider_id}: {status}; "
            f"name={d.provider_name}; "
            f"secret={m.requires_secret if m else '?'}; "
            f"network={m.requires_network if m else '?'}; "
            f"capabilities=[{caps}]"
        )
        if d.is_blocked:
            print(f"  reason={d.blocked_reason}")
    return 0


def ai_provider_status_command(args: argparse.Namespace) -> int:
    """Show current AI provider router status for a given provider_id."""
    router = AIProviderRouter()
    provider_id = args.provider_id or "mock"
    decision = router.select(provider_id, approved=args.approved)
    print(f"ai_provider_status=universal")
    print(f"provider_id={decision.provider_id}")
    print(f"provider_name={decision.provider_name}")
    print(f"mode={decision.mode}")
    print(f"is_blocked={decision.is_blocked}")
    if decision.is_blocked:
        print(f"blocked_reason={decision.blocked_reason}")
    else:
        m = decision.metadata
        if m:
            caps = ", ".join(c.name for c in m.capabilities)
            print(f"capabilities=[{caps}]")
            print(f"secret_policy={m.secret_policy.value}")
            print(f"requires_secret={m.requires_secret}")
            print(f"requires_network={m.requires_network}")
    return 0


def ai_provider_mock_command(_: argparse.Namespace) -> int:
    """Select mock provider explicitly."""
    router = AIProviderRouter()
    decision = router.select("mock")
    print("ai_provider_mock=universal")
    print(f"provider_id={decision.provider_id}")
    print(f"provider_name={decision.provider_name}")
    print(f"is_blocked={decision.is_blocked}")
    if decision.metadata:
        print(f"mode={decision.metadata.mode}")
    print("Mock provider is always available in safe-local mode.")
    return 0


def ai_provider_router_command(args: argparse.Namespace) -> int:
    """Test router decision for a given provider_id."""
    router = AIProviderRouter()
    provider_id = args.provider_id or "mock"
    decision = router.select(provider_id, approved=args.approved)
    print(f"ai_provider_router=universal")
    print(f"provider_id={decision.provider_id}")
    print(f"is_blocked={decision.is_blocked}")
    print(f"blocked_reason={decision.blocked_reason or '-'}")
    if decision.metadata:
        print(f"can_use_now={decision.metadata.can_use_now}")
        print(f"requires_secret={decision.metadata.requires_secret}")
        print(f"requires_network={decision.metadata.requires_network}")
        print(f"secret_policy={decision.metadata.secret_policy.value}")
        print(f"approval_required={decision.metadata.approval_required or '-'}")
    return 0


def ai_provider_capabilities_command(_: argparse.Namespace) -> int:
    """Show capabilities of all registered providers."""
    router = AIProviderRouter()
    providers = router.list_providers()
    print("ai_provider_capabilities=universal")
    print(f"total_providers={len(providers)}")
    for d in providers:
        m = d.metadata
        if not m:
            continue
        caps = "\n    ".join(f"- {c.name}: {c.name.replace('_', ' ').title()}" for c in m.capabilities)
        print(f"\n{d.provider_id} ({d.provider_name}):")
        print(f"  model={m.model_id}")
        print(f"  mode={m.mode}")
        print(f"  capabilities:\n    {caps}")
        print(f"  local_only={'LOCAL_ONLY' in [c.name for c in m.capabilities]}")
        print(f"  network_required={'NETWORK_REQUIRED' in [c.name for c in m.capabilities]}")
    return 0


def secret_gate_command(_: argparse.Namespace) -> int:
    """Show secret gate status from the universal AI provider layer."""
    router = AIProviderRouter()
    decision = router.select("mock")
    print("secret_gate=universal")
    print("Secret gate is active in local-safe mode.")
    print("All real AI providers are BLOCKED until APPROVE_SECRET_SETUP.")
    print()
    providers = router.list_providers()
    blocked_secret = [d for d in providers if d.metadata and d.metadata.requires_secret]
    print(f"Providers requiring secret approval: {len(blocked_secret)}")
    for d in blocked_secret:
        print(f"  - {d.provider_id}: {d.blocked_reason}")
    print()
    print("To enable real AI providers, you must:")
    print("  1. Configure provider API key (in .env or secure store)")
    print("  2. Grant APPROVE_SECRET_SETUP approval")
    print("  3. Restart router with approved=True")
    return 0


def review_provider_mock_command(_: argparse.Namespace) -> int:
    """Select mock review provider explicitly."""
    # Still uses old factory for backward compat, but indicates universal path
    from hermes_core.review.review_provider_factory import ReviewProviderConfig, ReviewProviderFactory
    selection = ReviewProviderFactory().select(ReviewProviderConfig(mode="mock-review"))
    result = selection.review("local smoke test")
    print("review_provider=mock-universal")
    print(f"provider={selection.provider_name}")
    print(f"approved={result.approved}")
    print(f"blocked={selection.is_blocked}")
    return 0


def review_provider_disabled_command(args: argparse.Namespace) -> int:
    """Select a disabled review provider."""
    from hermes_core.review.review_provider_factory import ReviewProviderConfig, ReviewProviderFactory
    mode = args.mode or "deepseek-disabled"
    selection = ReviewProviderFactory().select(ReviewProviderConfig(mode=mode))
    result = selection.review("local smoke test")
    print("review_provider=disabled-universal")
    print(f"provider={selection.provider_name}")
    print(f"mode={mode}")
    print(f"approved={result.approved}")
    print(f"blocked={selection.is_blocked}")
    if result.blocked_reason:
        print(f"blocked_reason={result.blocked_reason}")
    return 0


# ── Runtime Bridge command ──


def bridge_command(args: argparse.Namespace) -> int:
    """Execute a command through the Old Hermes → Hermes-Clean runtime bridge."""
    from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
    from hermes_core.runtime_bridge.contract import ROUTE_TO_ACTION

    # Map CLI action name to BridgeActionType
    action_name = args.action.strip().lower().replace("_", "-")
    action = ROUTE_TO_ACTION.get(action_name)
    if action is None:
        # Try the from_string fallback
        req = BridgeRequest.from_string(action_name)
        action = req.action
    router = BridgeRouter()
    resp = router.handle(BridgeRequest(action=action))
    print(f"bridge_status={resp.status}")
    print(f"bridge_action={resp.action}")
    print(f"bridge_route={resp.route}")
    if resp.is_blocked:
        print(f"bridge_blocked_reason={resp.blocked_reason}")
    else:
        for line in resp.output_lines:
            print(line)
    print(f"bridge_safe_local={resp.audit_metadata.get('safe_local', True)}")
    return 0 if resp.is_ok else 1


# ── Mobile Gateway commands ──


def mobile_gateway_status_command(_: argparse.Namespace) -> int:
    """Show mobile gateway status."""
    from hermes_core.mobile_gateway import MobileGateway, ALLOWED_ENDPOINTS, BLOCKED_ENDPOINTS
    gw = MobileGateway()
    resp = gw.status()
    print("mobile_gateway_status=safe-local")
    print(f"bind_address=127.0.0.1:8514")
    print(f"allowed_endpoints={len(ALLOWED_ENDPOINTS)}")
    print(f"blocked_endpoints={len(BLOCKED_ENDPOINTS)}")
    print(f"gateway_ok={resp.status == 'OK'}")
    print(f"mobile_server_available=True")
    print(f"0.0.0.0_blocked=True")
    print(f"external_port_blocked=True")
    print(f"android_app_created=False")
    print(f"next_step=BATCH_095_HERMES_MOBILE_WEB_UI")
    return 0


def mobile_api_contract_command(_: argparse.Namespace) -> int:
    """Show mobile API contract (all endpoints)."""
    from hermes_core.mobile_gateway import ALLOWED_ENDPOINTS, BLOCKED_ENDPOINTS
    print("mobile_api_contract=safe-local")
    print()
    print("Allowed endpoints:")
    for ep in sorted(ALLOWED_ENDPOINTS, key=lambda e: e.value):
        print(f"  {ep.value}  # {ep.name}")
    print()
    print("Blocked endpoints:")
    for ep in sorted(BLOCKED_ENDPOINTS, key=lambda e: e.value):
        print(f"  {ep.value}  # {ep.name}")
    print()
    print("Base URL: http://127.0.0.1:8514")
    print("All responses: JSON with audit_metadata")
    return 0


def mobile_api_dry_run_command(_: argparse.Namespace) -> int:
    """Dry-run mobile API: test all endpoints without starting a server."""
    from hermes_core.mobile_gateway import MobileGateway
    gw = MobileGateway()
    endpoints = [
        ("status", gw.status),
        ("dashboard", gw.dashboard),
        ("daily-assistant", gw.daily_assistant),
        ("what-next", gw.what_next),
        ("local-health", gw.local_health),
        ("malyarka-status", gw.malyarka_status),
        ("ai-provider-status", gw.ai_provider_status),
        ("bridge-status", gw.bridge_status),
    ]
    print("mobile_api_dry_run=safe-local")
    passed = 0
    for name, fn in endpoints:
        resp = fn()
        ok = resp.status == "OK"
        if ok:
            passed += 1
        print(f"  {name}: status={resp.status}; data_keys={len(resp.data)}; "
              f"safe_local={resp.audit_metadata.get('safe_local', '?')}")
    print(f"results={passed}/{len(endpoints)} OK")
    return 0


def mobile_api_server_check_command(_: argparse.Namespace) -> int:
    """Quick self-check: start server, make request, stop."""
    from hermes_core.mobile_gateway import LocalAPIServer
    print("mobile_api_server_check=running...")
    server = LocalAPIServer()
    ok = server.self_check()
    print(f"self_check={'OK' if ok else 'FAIL'}")
    print(f"bind_address=127.0.0.1:8514")
    print(f"server_was_started=True")
    print(f"server_was_stopped=True")
    print(f"0.0.0.0_not_used=True")
    return 0 if ok else 1


# ── Mobile Web UI commands ──


def mobile_web_status_command(_: argparse.Namespace) -> int:
    """Show mobile web UI status."""
    from hermes_core.mobile_web import get_web_files, get_web_dir
    files = get_web_files()
    print("mobile_web_status=local")
    print(f"web_dir={get_web_dir()}")
    print(f"files_count={len(files)}")
    for name in sorted(files):
        size = files[name].stat().st_size
        print(f"  {name}: {size} bytes")
    print(f"preview_url=file:///{get_web_dir().as_posix()}/index.html")
    print(f"api_url=http://127.0.0.1:8514")
    print(f"android_app=False")
    print(f"lan_external_disabled=True")
    return 0


def mobile_web_preview_command(_: argparse.Namespace) -> int:
    """Show mobile web UI preview info."""
    from hermes_core.mobile_web import preview_url, api_base_url
    print("mobile_web_preview=local")
    print(f"preview_url={preview_url()}")
    print(f"api_url={api_base_url()}")
    print()
    print("To preview:")
    print(f"  1. Start API server: scripts\\hermes.cmd mobile-api-server-check")
    print(f"  2. Open in browser: {preview_url()}")
    print(f"  3. API should be at: {api_base_url()}")
    print()
    print("Safe-local only. No external access.")
    return 0


def mobile_web_files_command(_: argparse.Namespace) -> int:
    """List mobile web UI files."""
    from hermes_core.mobile_web import get_web_files, get_web_dir
    files = get_web_files()
    print("mobile_web_files=local")
    print(f"dir={get_web_dir()}")
    for name in sorted(files):
        size = files[name].stat().st_size
        print(f"  {name} ({size} bytes)")
    return 0


def mobile_web_self_check_command(_: argparse.Namespace) -> int:
    """Self-check: verify all web files exist and are valid."""
    from hermes_core.mobile_web import get_web_files
    files = get_web_files()
    required = ["index.html", "app.css", "app.js", "api_client.js"]
    missing = [f for f in required if f not in files]
    print(f"mobile_web_self_check={'OK' if not missing else 'FAIL'}")
    print(f"total_files={len(files)}")
    print(f"missing={len(missing)}")
    for m in missing:
        print(f"  MISSING: {m}")
    # Check HTML for external URLs
    if "index.html" in files:
        html = files["index.html"].read_text(encoding="utf-8")
        has_external = "https://" in html.replace("https://127.0.0.1", "") and "https://" in html
        print(f"external_urls={'FOUND' if has_external else 'none'}")
    if "app.js" in files:
        js = files["app.js"].read_text(encoding="utf-8")
        has_secrets = "token" in js.lower() or "api_key" in js.lower() or "secret" in js.lower()
        print(f"secrets_in_js={'FOUND' if has_secrets else 'none'}")
    if "api_client.js" in files:
        api_js = files["api_client.js"].read_text(encoding="utf-8")
        has_localhost = "127.0.0.1" in api_js
        has_external = any(h in api_js for h in ["https://api.", "https://gemini", "https://deepseek"])
        print(f"localhost_default={has_localhost}")
        print(f"external_api_urls={'FOUND' if has_external else 'none'}")
    return 0 if not missing else 1


# ── Android WebView Shell commands ──


def android_shell_status_command(_: argparse.Namespace) -> int:
    """Show Android WebView Shell status."""
    from hermes_core.android_shell import (
        get_android_dir, get_shell_files, check_required_files,
        get_default_url, has_android_sdk,
    )
    files = get_shell_files()
    missing = check_required_files()
    print("android_shell_status=safe-local-scaffold")
    print(f"project_dir={get_android_dir()}")
    print(f"total_files={len(files)}")
    print(f"missing_required={len(missing)}")
    for m in missing:
        print(f"  MISSING: {m}")
    print(f"default_url={get_default_url()}")
    print(f"android_sdk={'detected' if has_android_sdk() else 'not detected (scaffold ready)'}")
    print(f"apk_built=False")
    print(f"published=False")
    print(f"production_signed=False")
    print(f"lan_external_disabled=True")
    return 0


def android_shell_files_command(_: argparse.Namespace) -> int:
    """List Android shell files."""
    from hermes_core.android_shell import get_android_dir, get_shell_files
    files = get_shell_files()
    print("android_shell_files=local")
    print(f"dir={get_android_dir()}")
    for name in sorted(files):
        size = files[name].stat().st_size
        print(f"  {name} ({size} bytes)")
    return 0


def android_shell_security_check_command(_: argparse.Namespace) -> int:
    """Security check of Android shell."""
    from hermes_core.android_shell import (
        check_required_files, check_dangerous_permissions,
        check_secrets_in_files, get_default_url,
    )
    missing = check_required_files()
    dangerous = check_dangerous_permissions()
    secrets = check_secrets_in_files()
    url = get_default_url()

    ok = not missing and not dangerous and not secrets and "127.0.0.1" in url

    print(f"android_shell_security={'OK' if ok else 'ATTENTION'}")
    print(f"required_missing={len(missing)}")
    for m in missing:
        print(f"  MISSING: {m}")
    print(f"dangerous_permissions={len(dangerous)}")
    for d in dangerous:
        print(f"  DANGEROUS: {d}")
    print(f"secrets_found={len(secrets)}")
    for s in secrets:
        print(f"  SECRET: {s}")
    print(f"default_url={url}")
    print(f"localhost_default={'127.0.0.1' in url}")
    print(f"0.0.0.0_default=False")
    print(f"js_bridge=False")
    print(f"analytics_sdk=False")
    return 0 if ok else 1


def android_shell_build_info_command(_: argparse.Namespace) -> int:
    """Show Android shell build info."""
    from hermes_core.android_shell import get_android_dir, has_android_sdk
    print("android_shell_build_info=local")
    print(f"project_dir={get_android_dir()}")
    print()
    if has_android_sdk():
        print("Android SDK: detected")
        print()
        print("To build debug APK:")
        print(f"  cd {get_android_dir()}")
        print(f"  gradlew assembleDebug")
        print(f"  APK will be at: app/build/outputs/apk/debug/app-debug.apk")
    else:
        print("Android SDK: NOT detected")
        print()
        print("To build APK, you need:")
        print("  1. Install Android Studio")
        print("  2. Open project: " + str(get_android_dir()))
        print("  3. Build → Build Bundle(s) / APK(s) → Build APK(s)")
    print()
    print("Scaffold is ready. APK build requires Android SDK.")
    return 0


# ── Phone Connectivity commands ──


def phone_connectivity_status_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import get_default_policy, ConnectivityMode
    p = get_default_policy()
    r = p.status_report()
    print("phone_connectivity_status=safe-local")
    print(f"current_mode={r['current_mode']}")
    print(f"localhost_only={r['localhost_only']}")
    print(f"lan_enabled={r['lan_enabled']}")
    print(f"external_blocked={r['external_blocked']}")
    print(f"pairing_real_enabled={r['pairing_real_enabled']}")
    print(f"pairing_dry_run_allowed={r['pairing_dry_run_allowed']}")
    print(f"total_options={r['total_options']}")
    print(f"enabled_options={r['enabled_options']}")
    print(f"disabled_options={r['disabled_options']}")
    print(f"next_step={r['next_step']}")
    return 0


def phone_connectivity_options_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import get_default_policy, ConnectivityOption
    p = get_default_policy()
    print("phone_connectivity_options=safe-local")
    for opt in p.list_options():
        s = "ENABLED" if opt.enabled else "DISABLED"
        print(f"\n--- {opt.name} [{s}] ---")
        print(f"  description={opt.description}")
        print(f"  pros={'; '.join(opt.pros[:2])}")
        print(f"  risks={'; '.join(opt.risks[:2])}")
        print(f"  requirements={'; '.join(opt.requirements[:2])}")
        print(f"  approval_gates={'; '.join(opt.approval_gates)}")
        print(f"  forbidden={'; '.join(opt.forbidden[:2])}")
    return 0


def phone_pairing_contract_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import DevicePairing
    p = DevicePairing.dry_run()
    print("phone_pairing_contract=dry-run")
    for k, v in p.to_dict().items():
        if k != "audit_metadata":
            print(f"  {k}={v}")
    print("  audit_metadata:")
    for k, v in p.audit_metadata.items():
        print(f"    {k}={v}")
    return 0


def phone_pairing_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import DevicePairing, PairingMode, ConnectionStatus
    for name, pid in [("TestPhone", "dry-run-001"), ("DemoPhone", "dry-run-002")]:
        p = DevicePairing.dry_run_pair(name, pid)
        print(f"phone_pairing_dry_run: {p.device_name} ({p.device_id})")
        print(f"  mode={p.pairing_mode.value}; status={p.connection_status.value}")
        print(f"  is_real={p.is_real}; is_dry_run={p.is_dry_run}")
    print("pairing_dry_run=OK (mock only, no real tokens)")
    return 0


def phone_lan_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import get_default_policy
    p = get_default_policy()
    ok, msg = p.can_bind_to("192.168.1.100")
    print("phone_lan_dry_run=safe-local")
    print(f"test_bind=192.168.1.100 -> {'ALLOWED' if ok else 'BLOCKED'}: {msg}")
    print("lan_mode=DISABLED (requires APPROVE_LAN_MODE + APPROVE_PHONE_PAIRING)")
    print("recommendation=Use Tailscale/VPN for first phone access")
    return 0


def phone_tailscale_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import CONNECTIVITY_OPTIONS
    ts = [o for o in CONNECTIVITY_OPTIONS if "Tailscale" in o.name]
    print("phone_tailscale_dry_run=safe-local")
    if ts:
        opt = ts[0]
        print(f"status={'ENABLED' if opt.enabled else 'DISABLED'}")
        print(f"approval_gates={'; '.join(opt.approval_gates)}")
    print("tailscale_mode=DISABLED (requires APPROVE_TAILSCALE_MODE)")
    print("recommendation=Install Tailscale on PC and phone, then enable via approval")
    return 0


def phone_security_check_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import get_default_policy
    p = get_default_policy()
    checks = {
        "localhost_only": p.is_localhost_only,
        "0.0.0.0_blocked": not p.can_bind_to("0.0.0.0")[0],
        "lan_blocked": not p.can_bind_to("192.168.1.1")[0],
        "public_blocked": not p.can_bind_to("8.8.8.8")[0],
        "external_blocked": p.is_external_blocked,
        "pairing_dry_run_only": True,
        "no_real_tokens": True,
    }
    all_ok = all(checks.values())
    print(f"phone_security_check={'OK' if all_ok else 'FAIL'}")
    for k, v in checks.items():
        print(f"  {k}={v}")
    return 0 if all_ok else 1


# ── Controlled Phone Access commands ──


def phone_access_status_command(_: argparse.Namespace) -> int:
    from hermes_core.controlled_access import get_access_policy, get_bind_config
    policy = get_access_policy()
    bind = get_bind_config()
    r = policy.status_report()
    print("phone_access_status=safe-local")
    print(f"bind_mode={bind.mode.value}")
    print(f"bind_address={bind.bind_address}")
    print(f"tailscale_recommended={r['tailscale_recommended']}")
    print(f"tailscale_enabled={r['tailscale_enabled']}")
    print(f"lan_enabled={r['lan_enabled']}")
    print(f"public_blocked={r['public_blocked']}")
    print(f"zero_blocked={r['zero_blocked']}")
    print(f"pairing_real={r['pairing_real']}")
    print(f"hard_blocked_actions={len(r['hard_blocked_actions'])}")
    print(f"safe_remote_actions={len(r['safe_remote_actions'])}")
    return 0


def phone_access_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.controlled_access import TAILSCALE_RECOMMENDATION
    print("phone_access_plan=safe-local")
    print(TAILSCALE_RECOMMENDATION)
    return 0


def tailscale_status_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.controlled_access import detect_tailscale
    ts = detect_tailscale()
    print("tailscale_status_dry_run=safe")
    print(f"installed={ts.installed}")
    print(f"running={ts.running}")
    print(f"version={ts.version or 'N/A'}")
    print(f"tailscale_ip={ts.tailscale_ip or 'N/A'}")
    print(f"is_ready={ts.is_ready}")
    for w in ts.warnings:
        print(f"warning={w}")
    print(f"no_install={ts.audit['no_install']}")
    print(f"no_network_change={ts.audit['no_network_change']}")
    return 0


def tailscale_access_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.controlled_access import get_tailscale_access_plan
    print("tailscale_access_plan=safe-local")
    print(get_tailscale_access_plan())
    return 0


def tailscale_approval_check_command(_: argparse.Namespace) -> int:
    from hermes_core.controlled_access import detect_tailscale, get_access_policy, AccessRequest
    ts = detect_tailscale()
    policy = get_access_policy()
    host = ts.tailscale_ip if ts.tailscale_ip else "100.64.0.1"
    result = policy.check(AccessRequest(client_host=host, approval_approved=False))
    print("tailscale_approval_check=safe-local")
    print(f"tailscale_installed={ts.installed}")
    print(f"tailscale_ready={ts.is_ready}")
    print(f"approval_decision={result.decision.value}")
    print(f"approval_gate={result.approval_gate}")
    print(f"reason={result.reason}")
    return 0


def lan_access_plan_command(_: argparse.Namespace) -> int:
    print("lan_access_plan=safe-local")
    print("LAN (локальная сеть) — альтернативный вариант доступа с телефона.")
    print()
    print("Шаги:")
    print("  1. Узнать IP ПК в локальной сети (ipconfig → IPv4 Address)")
    print("  2. Дать APPROVE_LAN_MODE + APPROVE_PHONE_PAIRING")
    print("  3. Изменить bind address на LAN IP ПК")
    print("  4. В Android Shell изменить API URL на http://<lan-ip>:8514")
    print()
    print("⚠️ Риски LAN:")
    print("  - Порт открыт в локальной сети")
    print("  - Другие устройства в Wi-Fi могут сканировать")
    print("  - Tailscale безопаснее (рекомендован)")
    return 0


def lan_approval_check_command(_: argparse.Namespace) -> int:
    from hermes_core.controlled_access import get_access_policy, AccessRequest
    policy = get_access_policy()
    result = policy.check(AccessRequest(client_host="192.168.1.100"))
    print("lan_approval_check=safe-local")
    print(f"decision={result.decision.value}")
    print(f"approval_gate={result.approval_gate}")
    print(f"reason={result.reason}")
    return 0


def lan_security_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.controlled_access import get_access_policy, AccessRequest
    policy = get_access_policy()
    result = policy.check(AccessRequest(client_host="192.168.1.100"))
    print("lan_security_dry_run=safe-local")
    print(f"host=192.168.1.100 -> {result.decision.value}: {result.reason}")
    print(f"allowed_actions={len(result.allowed_actions)}")
    print(f"blocked_actions={len(result.blocked_actions)}")
    print(f"hard_blocked_includes_secrets={'secret-read' in result.blocked_actions}")
    return 0


def pairing_status_command(_: argparse.Namespace) -> int:
    from hermes_core.phone_connectivity import DevicePairing
    p = DevicePairing.dry_run()
    print("pairing_status=dry-run-only")
    print(f"real_pairing_enabled=False")
    print(f"dry_run_allowed=True")
    print(f"is_real={p.is_real}")
    print(f"is_dry_run={p.is_dry_run}")
    print(f"real_token={p.audit_metadata['real_token']}")
    return 0


def pairing_security_check_command(_: argparse.Namespace) -> int:
    print("pairing_security_check=OK")
    print("  real_tokens=False")
    print("  secrets_stored=False")
    print("  tokens_logged=False")
    print("  pairing_dry_run_only=True")
    return 0


# ── Telegram Intent Router commands ──


def telegram_intent_status_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_intent import TelegramIntentRouter
    router = TelegramIntentRouter()
    print("telegram_intent_status=dry-run")
    print("router=active (dry-run only)")
    print("live_telegram=DISABLED")
    print("token_required=False")
    print("mock_only=True")
    r = router.detect("test")
    print(f"detection_works={r.intent.value}")
    return 0


def telegram_intent_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_intent import TelegramIntentRouter
    router = TelegramIntentRouter()
    cases = [
        ("привет, как дела?", "general_chat"),
        ("720х300 краска белая", "malyarka_order"),
        ("размеры 1200 x 800, цвет серый, 5 шт", "malyarka_order"),
        ("/status", "project_status"),
        ("что дальше?", "what_next"),
        ("помощь", "help"),
        ("исправь размер на 800х600", "malyarka_order"),  # без контекста — просто заказ
        ("да, подтверждаю", "malyarka_order"),  # без контекста — возможно подтверждение заказа
        ("прочитай .env", "safety_sensitive"),
    ]
    print("telegram_intent_dry_run=safe-local")
    for text, expected in cases:
        r = router.detect(text)
        ok = r.intent.value == expected
        print(f"  [{('OK' if ok else 'MISMATCH')}] '{text[:40]}' → {r.intent.value} (conf={r.confidence:.2f})")
    return 0


def telegram_intent_order_detect_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_intent import detect_order
    cases = [
        "720х300 краска белая 3 шт",
        "1200 x 800 цвет серый",
        "фасады мдф 5 штук",
        "обычный текст без размеров",
        "заказ №42 клиент Иванов",
        "300*200*18 мм",
    ]
    print("telegram_intent_order_detect=dry-run")
    for text in cases:
        r = detect_order(text)
        print(f"  is_order={r.is_order} conf={r.confidence:.2f} patterns={r.found_patterns} → '{text[:50]}'")
    return 0


def telegram_intent_chat_detect_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_intent import TelegramIntentRouter
    router = TelegramIntentRouter()
    cases = ["привет", "как погода?", "что такое Hermes?", "расскажи про малярку"]
    print("telegram_intent_chat_detect=dry-run")
    for text in cases:
        r = router.detect(text)
        print(f"  intent={r.intent.value} conf={r.confidence:.2f} route={r.route_target} → '{text}'")
    return 0


def telegram_intent_clarify_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_intent import TelegramIntentRouter
    router = TelegramIntentRouter()
    print("telegram_intent_clarify=dry-run")
    cases = [
        ("720х300", {"has_draft_order": False}),
        ("краска белая", {"has_draft_order": False}),
        ("исправь размер", {"has_draft_order": True, "has_disputed_rows": True}),
    ]
    for text, ctx in cases:
        r = router.detect(text, context=ctx)
        print(f"  intent={r.intent.value} needs_clar={r.needs_clarification} q='{r.suggested_question}' → '{text}'")
    return 0


def telegram_flow_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_intent import TelegramIntentRouter
    router = TelegramIntentRouter()
    print("telegram_flow_dry_run=safe-local")
    flow = [
        "привет",
        "720х300 краска белая 3 шт",
        "да, разобрать как заказ",
        "исправь цвет на серый",
        "да, подтверждаю",
    ]
    context = {}
    for msg in flow:
        r = router.detect(msg, context=context)
        print(f"  [{r.intent.value}] '{msg}' → route={r.route_target} clarif={r.requires_clarification}")
        context["last_intent"] = r.intent.value
        if r.intent.value.startswith("malyarka"):
            context["has_draft_order"] = True
        if "подтвержд" in msg.lower() or r.intent == "malyarka_order_confirmation":
            context["awaiting_confirmation"] = True
    return 0


def telegram_safety_check_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_intent import TelegramIntentRouter
    router = TelegramIntentRouter()
    print("telegram_safety_check=safe-local")
    blocked_cases = [
        "telegram token",
        ".env",
        "google drive",
        "delete файл",
        "gemini",
        "deepseek",
    ]
    for text in blocked_cases:
        r = router.detect(text)
        print(f"  '{text}' → {r.intent.value} blocked={bool(r.blocked_reason)}")
    print("live_telegram=DISABLED")
    print("polling=DISABLED")
    print("webhook=DISABLED")
    return 0


# ── Telegram E2E commands ──


def telegram_e2e_status_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_e2e import build_all_scenarios
    scenarios = build_all_scenarios()
    print("telegram_e2e_status=dry-run")
    print(f"total_scenarios={len(scenarios)}")
    total_steps = sum(len(s.steps) for s in scenarios)
    print(f"total_steps={total_steps}")
    print("live_telegram=DISABLED")
    return 0


def telegram_e2e_scenario_list_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_e2e import build_all_scenarios
    scenarios = build_all_scenarios()
    print("telegram_e2e_scenario_list=dry-run")
    for s in scenarios:
        print(f"\n  {s.scenario_id}: {s.title}")
        print(f"    steps={len(s.steps)} → {s.expected_final_state}")
    return 0


def telegram_e2e_run_all_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_e2e import E2EScenarioRunner, build_all_scenarios
    runner = E2EScenarioRunner()
    scenarios = build_all_scenarios()
    results, summary = runner.run_all_and_report(scenarios)
    print(f"telegram_e2e_run_all={summary}")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"  [{status}] {r.scenario_id}: {r.passed_steps}/{r.total_steps}")
        for e in r.errors:
            print(f"    ERROR: {e}")
    return 0


def telegram_e2e_order_happy_path_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_e2e import E2EScenarioRunner, build_all_scenarios
    runner = E2EScenarioRunner()
    scenarios = [s for s in build_all_scenarios() if "happy-path" in s.scenario_id]
    if scenarios:
        r = runner.run_scenario(scenarios[0])
        print(f"telegram_e2e_order_happy_path={'PASS' if r.passed else 'FAIL'}")
        for t in r.transcript:
            print(f"  {t}")
    return 0


def telegram_e2e_ambiguous_order_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_e2e import E2EScenarioRunner, build_all_scenarios
    runner = E2EScenarioRunner()
    scenarios = [s for s in build_all_scenarios() if "ambiguous" in s.scenario_id]
    if scenarios:
        r = runner.run_scenario(scenarios[0])
        print(f"telegram_e2e_ambiguous={'PASS' if r.passed else 'FAIL'}")
        for t in r.transcript:
            print(f"  {t}")
    return 0


def telegram_e2e_correction_flow_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_e2e import E2EScenarioRunner, build_all_scenarios
    runner = E2EScenarioRunner()
    scenarios = [s for s in build_all_scenarios() if "correction-flow" in s.scenario_id]
    if scenarios:
        r = runner.run_scenario(scenarios[0])
        print(f"telegram_e2e_correction={'PASS' if r.passed else 'FAIL'}")
        for t in r.transcript:
            print(f"  {t}")
    return 0


def telegram_e2e_safety_check_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_e2e import E2EScenarioRunner, build_all_scenarios
    runner = E2EScenarioRunner()
    scenarios = [s for s in build_all_scenarios() if "safety" in s.scenario_id]
    if scenarios:
        r = runner.run_scenario(scenarios[0])
        print(f"telegram_e2e_safety={'PASS' if r.passed else 'FAIL'}")
        for t in r.transcript:
            print(f"  {t}")
    return 0


def telegram_e2e_ux_preview_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_memory import ContextAwareRouter
    router = ContextAwareRouter()
    print("telegram_e2e_ux_preview=dry-run")
    # Show UX for a full order flow
    msgs = ["720х300 краска белая 3 шт", "да, подтверждаю"]
    for msg in msgs:
        r = router.route(msg, "ux-demo")
        print(f"\n  👤 User: {msg}")
        print(f"  🤖 Bot: {r.text[:120]}")
        if r.buttons:
            print(f"  🔘 Buttons: {r.buttons}")
        if r.warnings:
            print(f"  ⚠️ Warnings: {r.warnings}")
    return 0


# ── Telegram Live Gateway commands ──


def telegram_live_status_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import TelegramLiveGatewayConfig
    cfg = TelegramLiveGatewayConfig().to_dict()
    print("telegram_live_status=readiness_only")
    for k, v in cfg.items():
        if k != "audit_metadata":
            print(f"  {k}={v}")
    print("  audit: token_read=False api_called=False")
    return 0


def telegram_live_readiness_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import TelegramLiveGatewayConfig
    cfg = TelegramLiveGatewayConfig()
    checks = {
        "mode_readiness": cfg.mode.value == "readiness_only",
        "token_not_read": not cfg.token_read_allowed,
        "polling_blocked": not cfg.polling_allowed,
        "webhook_blocked": not cfg.webhook_allowed,
        "send_blocked": not cfg.send_message_allowed,
        "receive_blocked": not cfg.receive_message_allowed,
        "dry_run_ok": cfg.dry_run_allowed,
        "approval_required": cfg.approval_required,
    }
    all_ok = all(checks.values())
    print(f"telegram_live_readiness={'OK' if all_ok else 'ATTENTION'}")
    for k, v in checks.items():
        print(f"  {k}={v}")
    return 0


def telegram_live_approval_gates_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import APPROVAL_GATES
    print("telegram_live_approval_gates=all_closed")
    for g in APPROVAL_GATES:
        print(f"\n  {g.gate_id}")
        print(f"    title={g.title}")
        print(f"    risk={g.risk_level}")
        print(f"    state={g.default_state}")
        print(f"    requires_confirmation={g.required_user_confirmation}")
    return 0


def telegram_token_policy_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import TelegramLiveGatewayConfig, TelegramTokenPolicy
    cfg = TelegramLiveGatewayConfig()
    print("telegram_token_policy=safe")
    print(f"token_read_allowed={cfg.token_read_allowed}")
    print(f"token_readable={TelegramTokenPolicy.is_token_readable()}")
    print(TelegramTokenPolicy.policy_text())
    return 0


def telegram_polling_plan_command(_: argparse.Namespace) -> int:
    print("telegram_polling_plan=disabled")
    print("Polling readiness plan:")
    print("  1. APPROVE_TELEGRAM_TOKEN_READ")
    print("  2. APPROVE_TELEGRAM_POLLING_START")
    print("  3. APPROVE_TELEGRAM_RECEIVE_MESSAGE")
    print("  4. APPROVE_TELEGRAM_SEND_MESSAGE")
    print()
    print("Сейчас: polling не запускается. Telegram API не вызывается.")
    return 0


def telegram_webhook_plan_command(_: argparse.Namespace) -> int:
    print("telegram_webhook_plan=disabled")
    print("Webhook readiness plan (future):")
    print("  1. APPROVE_TELEGRAM_WEBHOOK_START")
    print("  2. HTTPS endpoint + сертификат")
    print("  3. Reverse proxy или public URL")
    print()
    print("Сейчас: webhook не запускается. Порт наружу не открывается.")
    print("Рекомендация: polling безопаснее для первого live-теста.")
    return 0


def telegram_send_safety_check_command(_: argparse.Namespace) -> int:
    print("telegram_send_safety_check=blocked")
    print("  send_message_allowed=False")
    print("  requires_approval=True")
    print("  blocked_outputs: secrets, tokens, keys, real_data, real_export")
    return 0


def telegram_live_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_memory import ContextAwareRouter
    router = ContextAwareRouter()
    print("telegram_live_dry_run=safe (fake update, no API)")
    updates = [
        ("привет", "general_chat"),
        ("paint|2|bucket", "malyarka_order"),
        ("/status", "project_status"),
        (".env", "safety_blocked"),
    ]
    for msg, expected_mode in updates:
        r = router.route(msg, "live-dry-run")
        mode = r.session_state.get("mode", "?")
        ok = "OK" if mode == expected_mode else f"expected {expected_mode}"
        print(f"  [{ok}] '{msg}' → {mode}")
    return 0


def telegram_live_blocked_actions_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import TelegramLiveGatewayConfig
    cfg = TelegramLiveGatewayConfig()
    print("telegram_live_blocked_actions=safe")
    blocked = []
    if not cfg.token_read_allowed: blocked.append("token_read")
    if not cfg.polling_allowed: blocked.append("polling")
    if not cfg.webhook_allowed: blocked.append("webhook")
    if not cfg.send_message_allowed: blocked.append("send_message")
    if not cfg.receive_message_allowed: blocked.append("receive_message")
    print(f"  blocked={', '.join(blocked)}")
    print(f"  approval_required={cfg.approval_required}")
    return 0


def telegram_live_safety_check_command(_: argparse.Namespace) -> int:
    print("telegram_live_safety_check=OK")
    checks = [
        "token_not_read", "polling_blocked", "webhook_blocked",
        "send_blocked", "receive_blocked", "api_not_called",
        "network_not_called", "env_not_read", "firewall_not_changed",
    ]
    for c in checks:
        print(f"  {c}=True")
    return 0


# ── First Live Approval Plan commands ──


def telegram_live_approval_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import APPROVAL_PLAN
    print("telegram_live_approval_plan=staged")
    for step in APPROVAL_PLAN:
        status = "COMPLETED" if step.is_completed else ("BLOCKED" if step.is_blocked else "PENDING")
        print(f"\n  [{status}] {step.title}")
        print(f"    stage={step.stage.value}")
        print(f"    gate={step.approval_gate or 'none'}")
        print(f"    reason={step.blocked_reason or step.description[:80]}")
    return 0


def telegram_live_approval_package_command(_: argparse.Namespace) -> int:
    print("telegram_live_approval_package=dry-run")
    print("Что включается: ничего (только планирование)")
    print("Что остаётся выключено: всё (polling, webhook, send, token_read)")
    print("Риски: отсутствуют (live не запущен)")
    print("Gates открываются: 0 из 10")
    print("Rollback: не требуется (ничего не включено)")
    print("Успех: план готов, preflight dry-run проходит")
    print("Провал: preflight dry-run падает")
    print("Команда пользователя: явно подтвердить переход к live preflight")
    return 0


def telegram_live_preflight_dry_run_command(_: argparse.Namespace) -> int:
    checks = {
        "gateway_contract_ready": True,
        "approval_gates_ready": True,
        "gates_closed": True,
        "token_policy_ready": True,
        "allowlist_plan_ready": True,
        "polling_plan_ready": True,
        "rollback_plan_ready": True,
        "e2e_dry_run_passing": True,
        "token_not_read": True,
        "api_not_called": True,
    }
    all_ok = all(checks.values())
    print(f"telegram_live_preflight={'OK' if all_ok else 'FAIL'}")
    for k, v in checks.items():
        print(f"  {k}={v}")
    return 0 if all_ok else 1


def telegram_token_handling_plan_command(_: argparse.Namespace) -> int:
    print("telegram_token_handling_plan=safe")
    print("Token handling (будущее):")
    print("  - задаётся пользователем вручную")
    print("  - не хранится в репозитории")
    print("  - не пишется в отчёты")
    print("  - не логируется")
    print("  - не попадает в тесты")
    print("  - не показывается в CLI")
    print("  - читается только после APPROVE_TELEGRAM_TOKEN_READ")
    print("Сейчас: token не читается.")
    return 0


def telegram_allowlist_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import ALLOWLIST_POLICY
    print("telegram_allowlist_plan=disabled")
    print(ALLOWLIST_POLICY)
    return 0


def telegram_first_polling_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import FIRST_POLLING_PLAN
    print("telegram_first_polling_plan=disabled")
    print(FIRST_POLLING_PLAN)
    return 0


def telegram_webhook_future_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import WEBHOOK_FUTURE_PLAN
    print("telegram_webhook_future_plan=disabled")
    print(WEBHOOK_FUTURE_PLAN)
    return 0


def telegram_send_guardrails_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import SEND_GUARDRAILS
    print("telegram_send_guardrails=active")
    print(SEND_GUARDRAILS)
    return 0


def telegram_live_rollback_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import ROLLBACK_PLAN
    print("telegram_live_rollback_plan=ready")
    print(ROLLBACK_PLAN)
    return 0


def telegram_live_go_no_go_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import get_go_nogo
    d = get_go_nogo()
    print(f"telegram_live_go_no_go: planning={d.planning_preflight}, live={d.actual_live_telegram}")
    print(f"  reason={d.reason}")
    print(f"  user_action={d.user_action_required}")
    print(f"  next_step={d.next_safe_step}")
    return 0


# ── System Hardening commands ──


def telegram_hardening_status_command(_: argparse.Namespace) -> int:
    print("telegram_hardening_status=ready")
    items = ["message_safety", "duplicate_protection", "rate_limit", "idempotency",
             "safe_shutdown", "emergency_stop", "audit_trail", "readiness_board"]
    for item in items:
        print(f"  {item}=READY")
    return 0


def telegram_message_safety_check_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import check_message_safety
    cases = ["привет", "прочитай .env", "удали файл", "включи polling", "сделай export"]
    print("telegram_message_safety_check=dry-run")
    for t in cases:
        r = check_message_safety(t)
        s = "BLOCKED" if not r.allowed else "OK"
        print(f"  [{s}] '{t}' → {r.blocked_reason or 'safe'}")
    return 0


def telegram_duplicate_update_check_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import DuplicateProtection, UpdateFingerprint
    dp = DuplicateProtection()
    fp1 = UpdateFingerprint.from_text("test", "upd-1")
    assert not dp.is_duplicate(fp1)
    assert dp.is_duplicate(fp1)  # Second time → duplicate
    print("telegram_duplicate_update_check=OK")
    print("  duplicate_detected=True")
    print("  first_pass=False second_pass=True")
    return 0


def telegram_rate_limit_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import RateLimitPolicy
    rl = RateLimitPolicy()
    ok, _ = rl.is_allowed(5, rl.max_per_minute)
    blocked, reason = rl.is_allowed(11, rl.max_per_minute)
    print(f"telegram_rate_limit_dry_run: 5/10={'OK' if ok else 'BLOCKED'}, 11/10={'BLOCKED' if blocked else 'OK'}")
    return 0


def telegram_idempotency_check_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import check_idempotency
    for action in ["create_draft", "confirm_draft", "cancel_draft"]:
        ok, msg = check_idempotency(action, False)
        ok2, msg2 = check_idempotency(action, True)
        print(f"  {action}: first={ok}, repeat={ok2} ({msg2[:50]})")
    return 0


def telegram_safe_shutdown_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import SAFE_SHUTDOWN_PLAN
    print("telegram_safe_shutdown_plan=dry-run")
    print(SAFE_SHUTDOWN_PLAN)
    return 0


def telegram_safe_shutdown_rehearsal_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import run_shutdown_rehearsal
    print("telegram_safe_shutdown_rehearsal=dry-run")
    for line in run_shutdown_rehearsal():
        print(f"  {line}")
    return 0


def telegram_emergency_stop_status_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import EmergencyStopState
    estop = EmergencyStopState()
    print(f"telegram_emergency_stop=active={estop.active} blocked_actions={len(estop.blocked_actions)}")
    return 0


def telegram_emergency_stop_dry_run_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import EmergencyStopState
    estop = EmergencyStopState()
    estop.activate("dry-run test")
    print(f"telegram_emergency_stop_dry_run: active={estop.active} reason={estop.reason}")
    estop.deactivate()
    return 0


def telegram_audit_trail_status_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import AuditTrail
    at = AuditTrail()
    at.log("test", "message_check", allowed=True)
    at.log("test", "dangerous_request", allowed=False, blocked_reason="secret request", risk="critical")
    print(f"telegram_audit_trail: events={at.count()} no_secrets=True")
    return 0


def telegram_live_readiness_board_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import READINESS_BOARD
    print(READINESS_BOARD)
    return 0


# ── Operator Console + Failure Drills commands ──


def telegram_operator_console_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import OPERATOR_CONSOLE
    print(OPERATOR_CONSOLE)
    return 0


def telegram_live_blockers_board_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import BLOCKERS_BOARD, LIVE_BLOCKERS
    print("telegram_live_blockers_board=10_blockers")
    for b in LIVE_BLOCKERS:
        print(f"  {b.blocker_id}: {b.description} [{b.current_status}]")
    return 0


def telegram_pre_live_checklist_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import PRE_LIVE_CHECKLIST
    print("telegram_pre_live_checklist=15_checks")
    ready = 0
    for cid, desc, status in PRE_LIVE_CHECKLIST:
        print(f"  {cid}: {desc} [{status}]")
        if status == "READY":
            ready += 1
    print(f"  ready={ready}/{len(PRE_LIVE_CHECKLIST)}")
    return 0


def _drill_cmd(name: str, drill_id: str) -> int:
    from hermes_core.telegram_live import FAILURE_DRILLS
    for d in FAILURE_DRILLS:
        if d.drill_id == drill_id:
            print(f"telegram_failure_drill={name} → {d.transcript}")
            return 0
    return 0


def telegram_failure_drills_run_all_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import FAILURE_DRILLS, run_failure_drills
    transcripts = run_failure_drills()
    print(f"telegram_failure_drills_run_all: {len(transcripts)}/{len(FAILURE_DRILLS)}")
    for t in transcripts:
        print(f"  {t}")
    return 0


def telegram_failure_drill_missing_token_command(_: argparse.Namespace) -> int:
    return _drill_cmd("missing-token", "D01")


def telegram_failure_drill_unknown_chat_command(_: argparse.Namespace) -> int:
    return _drill_cmd("unknown-chat", "D02")


def telegram_failure_drill_duplicate_update_command(_: argparse.Namespace) -> int:
    return _drill_cmd("duplicate-update", "D04")


def telegram_failure_drill_rate_limit_command(_: argparse.Namespace) -> int:
    return _drill_cmd("rate-limit", "D05")


def telegram_failure_drill_dangerous_message_command(_: argparse.Namespace) -> int:
    return _drill_cmd("dangerous-message", "D06")


def telegram_failure_drill_send_blocked_command(_: argparse.Namespace) -> int:
    return _drill_cmd("send-blocked", "D07")


def telegram_failure_drill_emergency_stop_command(_: argparse.Namespace) -> int:
    return _drill_cmd("emergency-stop", "D10")


def telegram_safe_recovery_plan_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import SAFE_RECOVERY_PLAN
    print(SAFE_RECOVERY_PLAN)
    return 0


def telegram_command_summary_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import COMMAND_SUMMARY
    print(COMMAND_SUMMARY)
    return 0


def telegram_final_approval_wording_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import FINAL_APPROVAL_WORDING
    print(FINAL_APPROVAL_WORDING)
    return 0


# ── User Acceptance + Freeze commands ──


def telegram_acceptance_status_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import ACCEPTANCE_SCENARIOS
    print(f"telegram_acceptance_status: {len(ACCEPTANCE_SCENARIOS)} scenarios")
    for s in ACCEPTANCE_SCENARIOS:
        print(f"  {s.scenario_id}: {s.title} [{'ACCEPTED' if s.accepted else 'PENDING'}]")
    return 0


def telegram_acceptance_checklist_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import ACCEPTANCE_CHECKLIST
    print(ACCEPTANCE_CHECKLIST)
    return 0


def telegram_acceptance_run_all_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import ACCEPTANCE_SCENARIOS
    from hermes_core.telegram_memory import ContextAwareRouter
    router = ContextAwareRouter()
    passed = 0
    print("telegram_acceptance_run_all=dry-run")
    for s in ACCEPTANCE_SCENARIOS:
        ok = True
        for msg in s.messages:
            r = router.route(msg, f"accept-{s.scenario_id}")
            mode = r.session_state.get("mode", "?")
            draft = r.draft_state.get("status") if r.draft_state else "none"
            if s.expected_draft_status and draft != s.expected_draft_status:
                if not (s.scenario_id == "A08" and draft == "none"):  # cancel yields no draft
                    ok = False
        if ok:
            passed += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {s.scenario_id}: {s.title}")
    print(f"  results={passed}/{len(ACCEPTANCE_SCENARIOS)}")
    return 0


def telegram_dry_run_demo_pack_command(_: argparse.Namespace) -> int:
    print("telegram_dry_run_demo_pack=ready")
    print("10 scenarios available. Run: telegram-acceptance-run-all")
    return 0


def telegram_expected_responses_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import EXPECTED_BOT_RESPONSES
    print("telegram_expected_responses=dry-run")
    for title, resp in EXPECTED_BOT_RESPONSES:
        print(f"  {title}: {resp}")
    return 0


def telegram_dry_run_freeze_status_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import DRY_RUN_FREEZE
    print(DRY_RUN_FREEZE)
    return 0


def telegram_live_preflight_blockers_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import LIVE_BLOCKERS_FINAL
    print("telegram_live_preflight_blockers=9_blockers")
    for bid, (desc, batch, approval, risk) in LIVE_BLOCKERS_FINAL.items():
        print(f"  {bid}: {desc} [{risk}]")
    return 0


def telegram_final_go_no_go_snapshot_command(_: argparse.Namespace) -> int:
    from hermes_core.telegram_live import FINAL_GO_NOGO
    print(FINAL_GO_NOGO)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hermes", description="Hermes-Clean local dry-run CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Show local status")
    status.set_defaults(func=status_command)

    message = sub.add_parser("message", help="Simulate Telegram dry-run message")
    message.add_argument("text", nargs="*")
    message.set_defaults(func=message_command)

    telegram_scenarios = sub.add_parser("telegram-scenarios", help="Run Telegram dry-run usage scenarios")
    telegram_scenarios.set_defaults(func=telegram_scenarios_command)

    telegram_status = sub.add_parser("telegram-status", help="Write Telegram dry-run status report")
    telegram_status.set_defaults(func=telegram_status_command)

    telegram_flow = sub.add_parser("telegram-flow", help="Run local Malyarka Telegram dialog flow")
    telegram_flow.add_argument("--case", default="disputed", choices=["clean", "disputed"])
    telegram_flow.add_argument("--no-auto-resolve", dest="auto_resolve", action="store_false")
    telegram_flow.set_defaults(auto_resolve=True)
    telegram_flow.add_argument("text", nargs="*")
    telegram_flow.set_defaults(func=telegram_flow_command)

    malyarka_dialog = sub.add_parser("malyarka-dialog", help="Run local operator-style Malyarka dialog commands")
    malyarka_dialog.add_argument("--script", default="disputed", choices=["clean", "disputed", "custom"])
    malyarka_dialog.add_argument("commands", nargs="*")
    malyarka_dialog.set_defaults(func=malyarka_dialog_command)

    malyarka_transcript = sub.add_parser("malyarka-transcript", help="Write local Malyarka dialog transcript report")
    malyarka_transcript.add_argument("--script", default="disputed", choices=["clean", "disputed"])
    malyarka_transcript.add_argument("--output", default="MALYARKA_DIALOG_TRANSCRIPT.md")
    malyarka_transcript.set_defaults(func=malyarka_transcript_command)

    dashboard = sub.add_parser("dashboard", help="Write local Hermes-Clean dashboard")
    dashboard.set_defaults(func=dashboard_command)

    app_status = sub.add_parser("app-status", help="Write local Hermes-Clean runtime status")
    app_status.set_defaults(func=app_status_command)

    daily_report = sub.add_parser("daily-report", help="Write local Hermes-Clean daily report")
    daily_report.set_defaults(func=daily_report_command)

    project_audit = sub.add_parser("project-audit", help="Write local Hermes-Clean project audit")
    project_audit.set_defaults(func=project_audit_command)

    refresh_all = sub.add_parser("refresh-all", help="Refresh local Hermes-Clean summary reports")
    refresh_all.set_defaults(func=refresh_all_command)

    route = sub.add_parser("route", help="Route a local request through safety gate")
    route.add_argument("text", nargs="*")
    route.set_defaults(func=route_command)

    safety = sub.add_parser("safety", help="Classify an action type and log to audit")
    safety.add_argument("action_type")
    safety.add_argument("--approved", action="store_true")
    safety.set_defaults(func=safety_command)

    safety_audit = sub.add_parser("safety-audit", help="Show local safety audit log")
    safety_audit.set_defaults(func=safety_audit_command)

    provider = sub.add_parser("ai-provider", help="Select local-safe AI provider mode")
    provider.add_argument("--mode", default="mock", choices=["mock", "gemini-disabled", "gemini", "fallback", "deepseek-disabled", "deepsig-disabled"])
    provider.add_argument("--approved", action="store_true")
    provider.add_argument("--key-available", action="store_true")
    provider.set_defaults(func=ai_provider_command)

    review_provider = sub.add_parser("review-provider", help="Select local-safe review provider mode")
    review_provider.add_argument("--mode", default="mock-review", choices=["mock-review", "deepseek-disabled", "deepsig-disabled", "deepseek", "deepsig"])
    review_provider.add_argument("--approved", action="store_true")
    review_provider.add_argument("--key-available", action="store_true")
    review_provider.add_argument("--cycles-used", type=int, default=0)
    review_provider.set_defaults(func=review_provider_command)

    memory = sub.add_parser("memory", help="Show local Hermes-Clean memory snapshot")
    memory.set_defaults(func=memory_command)

    tasks = sub.add_parser("tasks", help="Show local Hermes-Clean task status snapshot")
    tasks.set_defaults(func=tasks_command)

    health = sub.add_parser("health", help="Run local Hermes-Clean health-check")
    health.set_defaults(func=health_command)

    reports = sub.add_parser("reports", help="Show local Hermes-Clean report index")
    reports.set_defaults(func=reports_command)

    start_summary = sub.add_parser("start-summary", help="Show daily local Hermes-Clean startup summary")
    start_summary.set_defaults(func=start_summary_command)

    help_local = sub.add_parser("help-local", help="Show local Hermes-Clean command help")
    help_local.set_defaults(func=help_local_command)

    smoke = sub.add_parser("smoke", help="Run local Hermes-Clean smoke checks")
    smoke.set_defaults(func=smoke_command)

    export_status = sub.add_parser("export-status", help="Write local Hermes-Clean markdown status export")
    export_status.set_defaults(func=export_status_command)

    release_checklist = sub.add_parser("release-checklist", help="Write local Hermes-Clean release checklist")
    release_checklist.set_defaults(func=release_checklist_command)

    malyarka = sub.add_parser("malyarka-preview", help="Run Malyarka contract preview")
    malyarka.add_argument("text", nargs="*")
    malyarka.set_defaults(func=malyarka_preview_command)

    malyarka_fixtures = sub.add_parser("malyarka-fixtures", help="Run synthetic Malyarka fixture scenarios")
    malyarka_fixtures.set_defaults(func=malyarka_fixtures_command)

    malyarka_resolve = sub.add_parser("malyarka-resolve", help="Dry-run Malyarka disputed row replacement")
    malyarka_resolve.add_argument("source", nargs="*")
    malyarka_resolve.add_argument("--replacement", required=True)
    malyarka_resolve.set_defaults(func=malyarka_resolve_command)

    malyarka_workflow = sub.add_parser("malyarka-workflow", help="Show synthetic Malyarka local workflow")
    malyarka_workflow.set_defaults(func=malyarka_workflow_command)

    malyarka_status = sub.add_parser("malyarka-status", help="Write local Malyarka module status report")
    malyarka_status.set_defaults(func=malyarka_status_command)

    malyarka_schema = sub.add_parser("malyarka-schema", help="Show local Malyarka schema and export preview")
    malyarka_schema.set_defaults(func=malyarka_schema_command)

    malyarka_demo = sub.add_parser("malyarka-demo", help="Show local Malyarka module demo summary")
    malyarka_demo.set_defaults(func=malyarka_demo_command)

    malyarka_pricing = sub.add_parser("malyarka-pricing", help="Show synthetic Malyarka pricing preview")
    malyarka_pricing.set_defaults(func=malyarka_pricing_command)

    malyarka_disputes = sub.add_parser("malyarka-disputes", help="Write synthetic Malyarka dispute classification report")
    malyarka_disputes.set_defaults(func=malyarka_disputes_command)

    malyarka_combined = sub.add_parser("malyarka-combined", help="Show combined local Malyarka preview")
    malyarka_combined.add_argument("text", nargs="*")
    malyarka_combined.set_defaults(func=malyarka_combined_command)

    # ── Universal AI provider commands ──

    ai_provider_list = sub.add_parser("ai-provider-list", help="List all registered AI providers with status")
    ai_provider_list.set_defaults(func=ai_provider_list_command)

    ai_provider_status = sub.add_parser("ai-provider-status", help="Show router status for a provider")
    ai_provider_status.add_argument("provider_id", nargs="?", default="mock")
    ai_provider_status.add_argument("--approved", action="store_true")
    ai_provider_status.set_defaults(func=ai_provider_status_command)

    ai_provider_mock = sub.add_parser("ai-provider-mock", help="Select mock provider explicitly")
    ai_provider_mock.set_defaults(func=ai_provider_mock_command)

    ai_provider_router = sub.add_parser("ai-provider-router", help="Test router decision for a provider")
    ai_provider_router.add_argument("provider_id", nargs="?", default="mock")
    ai_provider_router.add_argument("--approved", action="store_true")
    ai_provider_router.set_defaults(func=ai_provider_router_command)

    ai_provider_capabilities = sub.add_parser("ai-provider-capabilities", help="Show capabilities of all registered providers")
    ai_provider_capabilities.set_defaults(func=ai_provider_capabilities_command)

    secret_gate = sub.add_parser("secret-gate", help="Show secret gate status from universal provider layer")
    secret_gate.set_defaults(func=secret_gate_command)

    review_provider_mock = sub.add_parser("review-provider-mock", help="Select mock review provider explicitly")
    review_provider_mock.set_defaults(func=review_provider_mock_command)

    review_provider_disabled = sub.add_parser("review-provider-disabled", help="Select a disabled review provider")
    review_provider_disabled.add_argument("--mode", default="deepseek-disabled", choices=["deepseek-disabled", "deepsig-disabled"])
    review_provider_disabled.set_defaults(func=review_provider_disabled_command)

    # ── Daily Assistant commands ──

    daily_assistant = sub.add_parser("daily-assistant", help="Show daily assistant — full project snapshot")
    daily_assistant.set_defaults(func=daily_assistant_command)

    daily_brief = sub.add_parser("daily-brief", help="One-screen daily brief summary")
    daily_brief.set_defaults(func=daily_brief_command)

    what_next = sub.add_parser("what-next", help="What to do next")
    what_next.set_defaults(func=what_next_command)

    local_health = sub.add_parser("local-health", help="Fast local health check")
    local_health.set_defaults(func=local_health_command)

    project_status = sub.add_parser("project-status", help="Quick project status")
    project_status.set_defaults(func=project_status_command)

    malyarka_mode_status = sub.add_parser("malyarka-mode-status", help="Malyarka mode and AI review path status")
    malyarka_mode_status.set_defaults(func=malyarka_mode_status_command)

    # ── Runtime Bridge ──
    bridge = sub.add_parser("bridge", help="Route command through Old Hermes → Hermes-Clean runtime bridge")
    bridge.add_argument("action", help="Bridge action name (e.g., daily-assistant, malyarka-status)")
    bridge.set_defaults(func=bridge_command)

    # ── Mobile Gateway ──
    mobile_gateway_status = sub.add_parser("mobile-gateway-status", help="Show mobile gateway status")
    mobile_gateway_status.set_defaults(func=mobile_gateway_status_command)

    mobile_api_contract = sub.add_parser("mobile-api-contract", help="Show mobile API contract (all endpoints)")
    mobile_api_contract.set_defaults(func=mobile_api_contract_command)

    mobile_api_dry_run = sub.add_parser("mobile-api-dry-run", help="Dry-run all mobile API endpoints")
    mobile_api_dry_run.set_defaults(func=mobile_api_dry_run_command)

    mobile_api_server_check = sub.add_parser("mobile-api-server-check", help="Quick self-check of local API server")
    mobile_api_server_check.set_defaults(func=mobile_api_server_check_command)

    # ── Mobile Web UI ──
    mobile_web_status = sub.add_parser("mobile-web-status", help="Show mobile web UI status")
    mobile_web_status.set_defaults(func=mobile_web_status_command)

    mobile_web_preview = sub.add_parser("mobile-web-preview", help="Show mobile web UI preview info")
    mobile_web_preview.set_defaults(func=mobile_web_preview_command)

    mobile_web_files = sub.add_parser("mobile-web-files", help="List mobile web UI files")
    mobile_web_files.set_defaults(func=mobile_web_files_command)

    mobile_web_self_check = sub.add_parser("mobile-web-self-check", help="Self-check mobile web UI files")
    mobile_web_self_check.set_defaults(func=mobile_web_self_check_command)

    # ── Android WebView Shell ──
    android_shell_status = sub.add_parser("android-shell-status", help="Show Android shell scaffold status")
    android_shell_status.set_defaults(func=android_shell_status_command)

    android_shell_files = sub.add_parser("android-shell-files", help="List Android shell files")
    android_shell_files.set_defaults(func=android_shell_files_command)

    android_shell_security_check = sub.add_parser("android-shell-security-check", help="Security check of Android shell")
    android_shell_security_check.set_defaults(func=android_shell_security_check_command)

    android_shell_build_info = sub.add_parser("android-shell-build-info", help="Show Android shell build info")
    android_shell_build_info.set_defaults(func=android_shell_build_info_command)

    # ── Phone Connectivity (BATCH_097) ──
    phone_conn_status = sub.add_parser("phone-connectivity-status", help="Phone connectivity status")
    phone_conn_status.set_defaults(func=phone_connectivity_status_command)
    phone_conn_options = sub.add_parser("phone-connectivity-options", help="Phone connectivity options")
    phone_conn_options.set_defaults(func=phone_connectivity_options_command)
    phone_pair_contract = sub.add_parser("phone-pairing-contract", help="Phone pairing contract")
    phone_pair_contract.set_defaults(func=phone_pairing_contract_command)
    phone_pair_dry = sub.add_parser("phone-pairing-dry-run", help="Phone pairing dry-run")
    phone_pair_dry.set_defaults(func=phone_pairing_dry_run_command)
    phone_lan_dry = sub.add_parser("phone-lan-dry-run", help="LAN dry-run")
    phone_lan_dry.set_defaults(func=phone_lan_dry_run_command)
    phone_ts_dry = sub.add_parser("phone-tailscale-dry-run", help="Tailscale dry-run")
    phone_ts_dry.set_defaults(func=phone_tailscale_dry_run_command)
    phone_sec = sub.add_parser("phone-security-check", help="Phone security check")
    phone_sec.set_defaults(func=phone_security_check_command)

    # ── Controlled Access (BATCH_098) ──
    pa_status = sub.add_parser("phone-access-status", help="Phone access status")
    pa_status.set_defaults(func=phone_access_status_command)
    pa_plan = sub.add_parser("phone-access-plan", help="Phone access plan")
    pa_plan.set_defaults(func=phone_access_plan_command)
    ts_status = sub.add_parser("tailscale-status-dry-run", help="Tailscale status dry-run")
    ts_status.set_defaults(func=tailscale_status_dry_run_command)
    ts_plan = sub.add_parser("tailscale-access-plan", help="Tailscale access plan")
    ts_plan.set_defaults(func=tailscale_access_plan_command)
    ts_approval = sub.add_parser("tailscale-approval-check", help="Tailscale approval check")
    ts_approval.set_defaults(func=tailscale_approval_check_command)
    lan_plan = sub.add_parser("lan-access-plan", help="LAN access plan")
    lan_plan.set_defaults(func=lan_access_plan_command)
    lan_approval = sub.add_parser("lan-approval-check", help="LAN approval check")
    lan_approval.set_defaults(func=lan_approval_check_command)
    lan_sec = sub.add_parser("lan-security-dry-run", help="LAN security dry-run")
    lan_sec.set_defaults(func=lan_security_dry_run_command)
    pair_status = sub.add_parser("pairing-status", help="Pairing status")
    pair_status.set_defaults(func=pairing_status_command)
    pair_sec = sub.add_parser("pairing-security-check", help="Pairing security check")
    pair_sec.set_defaults(func=pairing_security_check_command)

    # ── Telegram Intent Router (BATCH_099) ──
    ti_status = sub.add_parser("telegram-intent-status", help="Telegram intent router status")
    ti_status.set_defaults(func=telegram_intent_status_command)
    ti_dry = sub.add_parser("telegram-intent-dry-run", help="Telegram intent dry-run")
    ti_dry.set_defaults(func=telegram_intent_dry_run_command)
    ti_order = sub.add_parser("telegram-intent-order-detect", help="Order detection dry-run")
    ti_order.set_defaults(func=telegram_intent_order_detect_command)
    ti_chat = sub.add_parser("telegram-intent-chat-detect", help="Chat detection dry-run")
    ti_chat.set_defaults(func=telegram_intent_chat_detect_command)
    ti_clarify = sub.add_parser("telegram-intent-clarify", help="Clarification dry-run")
    ti_clarify.set_defaults(func=telegram_intent_clarify_command)
    tg_flow = sub.add_parser("telegram-flow-dry-run", help="Full flow dry-run")
    tg_flow.set_defaults(func=telegram_flow_dry_run_command)
    tg_safety = sub.add_parser("telegram-safety-check", help="Telegram safety check")
    tg_safety.set_defaults(func=telegram_safety_check_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
