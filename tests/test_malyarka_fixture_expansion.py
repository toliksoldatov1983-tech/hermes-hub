from hermes_modules.malyarka.fixtures import fixture_names, run_all_fixtures


def test_fixture_expansion_contains_adapted_hardening_cases():
    names = set(fixture_names())

    assert "zero_quantity" in names
    assert "malformed_extra_field" in names
    assert "manual_ready_unknown_unit" in names


def test_expanded_fixtures_are_synthetic_and_local():
    results = run_all_fixtures()
    by_name = {result.name: result for result in results}

    assert len(results) >= 12
    assert by_name["zero_quantity"].final_ready is False
    assert by_name["malformed_extra_field"].final_ready is False
    assert by_name["manual_ready_unknown_unit"].final_ready is True
    assert all("READY:" in r.export_status or "BLOCKED:" in r.export_status for r in results)
