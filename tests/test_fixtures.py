"""Tests для синтетических фикстур Hermes-Clean."""

from hermes_clean import FIXTURES, get_fixture, list_fixtures, validate_order_result


def test_all_fixtures_listed():
    names = list_fixtures()
    assert len(names) >= 10, f"Expected >= 10 fixtures, got {len(names)}"


def test_list_fixtures_by_tag():
    clean = list_fixtures(tag="clean")
    assert len(clean) >= 3
    assert "clean_single" in clean


def test_list_fixtures_by_tag_disputed():
    disp = list_fixtures(tag="disputed")
    assert len(disp) >= 4
    assert "dispute_missing_width" in disp


def test_get_fixture_returns_dict():
    f = get_fixture("clean_single")
    assert isinstance(f, dict)


def test_get_fixture_raises_for_missing():
    try:
        get_fixture("nonexistent")
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_fixture_ids_are_unique():
    ids = [f["id"] for f in FIXTURES.values()]
    assert len(ids) == len(set(ids))


def test_all_fixtures_have_tags():
    for name, f in FIXTURES.items():
        assert f.get("tags"), f"Fixture '{name}' has no tags"


def test_malyarka_reference_fixtures_are_available_and_keep_control_totals():
    uch_002 = get_fixture("malyarka_reference_uch_002")
    uch_003 = get_fixture("malyarka_reference_uch_003")

    assert uch_002["order_type"] == "Фрезеровка + покраска"
    assert uch_002["expected_area_m2"] == 5.68368
    assert uch_002["expected_calculation_area_m2"] == 5.90272
    assert uch_002["expected_group_count"] == 5

    assert uch_003["order_type"] == "Покраска"
    assert uch_003["expected_area_m2"] == 4.54410
    assert uch_003["expected_calculation_area_m2"] == 5.05494
    assert uch_003["expected_group_count"] == 5


def test_clean_fixtures_pass_validation():
    for name in list_fixtures(tag="clean"):
        f = get_fixture(name)
        order = {
            "status": f.get("expected_status", "clean"),
            "confirmed_rows": f["confirmed_rows"],
            "disputed_rows": f["disputed_rows"],
            "total_area_m2": f.get("expected_area_m2", 0),
        }
        v = validate_order_result(order)
        if name == "edge_zero_size":
            assert v["valid"] is False  # 0 height is out of range
        else:
            assert v["valid"] is True, f"Fixture '{name}' failed validation: {v['violations']}"


def test_disputed_fixtures_block_validation():
    for name in list_fixtures(tag="disputed"):
        f = get_fixture(name)
        order = {
            "status": f.get("expected_status", "has_disputes"),
            "confirmed_rows": f["confirmed_rows"],
            "disputed_rows": f["disputed_rows"],
            "total_area_m2": f.get("expected_area_m2", 0),
        }
        v = validate_order_result(order)
        # Validation flags only parser-failure reasons (unparsed_order_text, empty_or_garbage)
        # Structural disputes (missing_width, too_many_numbers) are handled by the resolver
        has_parser_failure = any(
            d.get("reason") in ("unparsed_order_text", "empty_or_garbage")
            for d in f["disputed_rows"]
        )
        if has_parser_failure:
            assert v["valid"] is False, f"Disputed fixture '{name}' should be invalid"
            assert v["blocked"] is True
