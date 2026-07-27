"""Run synthetic fixtures and validation for Hermes-Clean.

This is a local dry-run helper. It does not use Telegram, APIs, secrets,
real orders, Google Drive or Excel export.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from hermes_clean import get_fixture, list_fixtures, validate_order_result


def main() -> int:
    print("Hermes-Clean - Synthetic Fixtures + Validation")
    print("=" * 64)
    print("Local synthetic dry-run only. No Telegram, API, DB, secrets or real orders.")
    print()

    all_names = list_fixtures()
    passed = 0
    failed = 0
    violations_total = 0

    for name in all_names:
        fixture = get_fixture(name)
        label = fixture["label"]
        print(f"[{name}] {label}")

        order = {
            "status": fixture.get("expected_status", "clean"),
            "confirmed_rows": fixture["confirmed_rows"],
            "disputed_rows": fixture["disputed_rows"],
            "total_area_m2": fixture.get("expected_area_m2", 0),
        }
        validation = validate_order_result(order)

        confirmed = len(order["confirmed_rows"])
        disputed = len(order["disputed_rows"])
        area = order["total_area_m2"]
        valid = validation["valid"]
        violations = len(validation["violations"])

        ok = True
        checks = []

        if "expected_status" in fixture and order["status"] != fixture["expected_status"]:
            ok = False
            checks.append(f"  FAIL: status={order['status']}, expected={fixture['expected_status']}")

        if ok:
            passed += 1
            print(
                "  OK: "
                f"status={order['status']}, confirmed={confirmed}, disputed={disputed}, "
                f"area_m2={area:.6g}, validation={valid}, violations={violations}"
            )
        else:
            failed += 1
            for check in checks:
                print(check)

        if violations > 0:
            violations_total += violations
            for violation in validation["violations"]:
                print(f"  ! {violation.get('message', violation)}")

        print()

    print(f"Result: {passed}/{len(all_names)} fixtures OK", end="")
    if failed:
        print(f", {failed} FAIL")
        return 1
    print()
    if violations_total:
        print(f"Validation violations total: {violations_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
