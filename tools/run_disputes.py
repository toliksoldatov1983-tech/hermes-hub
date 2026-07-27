"""Run dispute resolver contract checks for Hermes-Clean.

This is a local dry-run helper. It does not use Telegram, APIs, secrets,
real orders, Google Drive or Excel export.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from hermes_clean import DisputeResolver, get_fixture


def main() -> int:
    print("Hermes-Clean - Dispute Resolver Contract Check")
    print("=" * 64)
    print("Local synthetic dry-run only. No Telegram, API, DB, secrets or real orders.")
    print()

    passed = 0
    failed = 0

    fixture = get_fixture("dispute_missing_width")
    disputed = fixture["disputed_rows"]

    print("[accept] Resolve disputed row through accept")
    resolver = DisputeResolver()
    outcome = resolver.resolve(disputed[0], {"action": "accept", "height": 1000, "width": 400, "quantity": 1})
    if outcome.resolved and outcome.confirmed_row:
        print(f"  OK: resolved=True, confirmed_row={outcome.confirmed_row}")
        passed += 1
    else:
        print(f"  FAIL: {outcome}")
        failed += 1

    print("[delete] Delete disputed row")
    resolver = DisputeResolver()
    outcome = resolver.resolve(disputed[0], {"action": "delete"})
    if outcome.resolved and outcome.action == "delete":
        print("  OK: resolved=True, action=delete")
        passed += 1
    else:
        print(f"  FAIL: {outcome}")
        failed += 1

    print("[clarify] Ask for clarification")
    resolver = DisputeResolver()
    outcome = resolver.resolve(disputed[0], {"action": "clarify"})
    if not outcome.resolved and outcome.action == "clarify":
        print(f"  OK: resolved=False, action=clarify, note='{outcome.note}'")
        passed += 1
    else:
        print(f"  FAIL: {outcome}")
        failed += 1

    print("[split] Split disputed row")
    resolver = DisputeResolver()
    outcome = resolver.resolve(
        disputed[0],
        {
            "action": "split",
            "rows": [
                {"height": 1000, "width": 400, "quantity": 1},
                {"height": 500, "width": 300, "quantity": 1},
            ],
        },
    )
    if outcome.action == "split" and outcome.confirmed_row:
        print(f"  OK: action=split, confirmed_row={outcome.confirmed_row}, new_disputes={len(outcome.new_disputes)}")
        passed += 1
    else:
        print(f"  FAIL: {outcome}")
        failed += 1

    print("[resolve_all] Batch resolution")
    fixture2 = get_fixture("dispute_mixed")
    disputed_all = fixture2["disputed_rows"]
    resolutions = {row["dispute_id"]: {"action": "delete"} for row in disputed_all}

    resolver = DisputeResolver()
    summary = resolver.resolve_all(disputed_all, resolutions)
    print(
        f"  total={summary.total_disputes}, resolved={summary.resolved}, "
        f"unresolved={summary.unresolved}, export_unblocked={summary.export_unblocked}"
    )
    if summary.resolved == 1 and summary.is_fully_resolved:
        print(f"  OK: all disputed rows resolved, unresolved={summary.unresolved}")
        passed += 1
    else:
        print("  FAIL: expected resolved=1 and is_fully_resolved=True")
        failed += 1

    print("[max_attempts] Stop after max attempts")
    resolver = DisputeResolver(max_resolution_attempts=2)
    for _ in range(2):
        resolver.resolve(disputed[0], {"action": "clarify"})
    outcome = resolver.resolve(disputed[0], {"action": "clarify"})
    if not outcome.resolved and outcome.action == "clarify" and outcome.confirmed_row is None:
        print(f"  OK: attempts exhausted, note='{outcome.note}'")
        passed += 1
    else:
        print(f"  FAIL: {outcome}")
        failed += 1

    print()
    print(f"Result: {passed}/{passed + failed} checks OK")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
